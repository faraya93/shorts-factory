"""Rig of production 026 (why the Titanic sank if they said it was unsinkable): a stylised ocean liner built from primitives (no livery, no name), with a closed exterior state (hull, deck,
white deckhouse tiers, windows, lifeboats, four funnels, two masts) and a lengthwise cutaway state (the near half of the hull swings away, the deck and deckhouse lift off), fifteen bulkheads that
divide the hull into sixteen open-topped compartments, per-compartment water that keeps a level surface in the world when the ship pitches, the spill sheets over the bulkhead tops, an iceberg,
the sea and a row of slits on the bow plates. Runs inside Blender.
Scene units are centimetres of a toy scale (the liner is 120 long); x is the ship's length (the bow at +x), y away from the camera (the camera sits on the -y side), z up, the deck at z = 0.
Driven per frame by the scene script through Liner.update()."""
import math
import sys
from pathlib import Path

import bmesh
import bpy
import mathutils
from mathutils import noise

sys.path.insert(0, str(Path(__file__).resolve().parent))
import avion_rig as av  # noqa: E402
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

L, W, D = 120.0, 11.0, 10.0                  # hull length, half-beam, depth below the deck
NB = 15                                      # bulkheads (sixteen compartments)
NC = NB + 1
ZB = -1.8                                    # bulkhead tops: below the deck line
SEA_Z = -4.0                                 # waterline
EPS = 1e-4
WALL = 0.5
LIGHT_K = 3.0
BULK_X = [-L / 2 + L * (i + 1) / NC for i in range(NB)]
EDGE_X = [-L / 2] + BULK_X + [L / 2]         # compartment k spans EDGE_X[k]..EDGE_X[k+1]; k = 0 is the stern, NC - 1 the bow

HULL, DECK, WHITE, BUFF = "#23252B", "#B58A55", "#F1EEE8", "#E4A83C"
SEA, ICE, WATER, BULK, FLOOR = "#2A6F8F", "#B9D3E3", "#4FB3D9", "#EFE6D2", "#8B8F96"

ease = av.ease
lights = av.lights
look = av.look
smooth = c.smooth


def lerp(a, b, k):
    return a + (b - a) * k


def hw(x):
    """Outer half-beam at x: a pointed bow, a blunt stern."""
    s = x / (L / 2)
    if s > 0.55:
        u = (s - 0.55) / 0.45
        return W * max(0.0, 1.0 - u ** 2.2) ** 0.6
    if s < -0.8:
        u = (-s - 0.8) / 0.2
        return W * (1.0 - 0.55 * u * u)
    return W


def hd(x):
    """Outer depth below the deck at x."""
    s = x / (L / 2)
    if s > 0.55:
        u = (s - 0.55) / 0.45
        return D * (1.0 - 0.55 * u * u)
    if s < -0.8:
        u = (-s - 0.8) / 0.2
        return D * (1.0 - 0.3 * u * u)
    return D


def sec(x, a, inset=0.0):
    """A point of the hull section at x, angle a (0 = the near deck edge, pi/2 = the keel line, pi = the far deck edge)."""
    w, d = max(0.05, hw(x) - inset), max(0.3, hd(x) - inset)
    return (x, -w * math.cos(a), -d * math.sin(a) ** 0.45)


def profile(x, level, n=10, inset=WALL):
    """The far half of the section at x, from the keel line up the far wall to `level`, closed back along the surface: [(y, z)], n + 2 points."""
    w, d = max(0.05, hw(x) - inset), max(0.3, hd(x) - inset)
    r = min(1.0, max(0.02, -level / d))
    a_top = math.pi - math.asin(min(1.0, r ** (1.0 / 0.45)))
    pts = []
    for k in range(n + 1):
        a = math.pi / 2 + (a_top - math.pi / 2) * k / n
        pts.append((-w * math.cos(a), -d * math.sin(a) ** 0.45))
    pts.append((0.0, pts[-1][1]))
    return pts


def mesh_obj(name, mat, parent=None):
    me = bpy.data.meshes.new(name)
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat)
    if parent:
        o.parent = parent
    return o


def loft(o, rows, close=False, thick=0.0):
    """rows: list of rings of (x, y, z); a surface between consecutive rings."""
    n = len(rows[0])
    verts = [p for r in rows for p in r]
    faces = []
    for i in range(len(rows) - 1):
        for j in range(n - 1 + (1 if close else 0)):
            j1 = (j + 1) % n
            faces.append((i * n + j, i * n + j1, (i + 1) * n + j1, (i + 1) * n + j))
    me = o.data
    me.clear_geometry()
    me.from_pydata(verts, [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    if thick and not o.modifiers:
        m = o.modifiers.new("solid", "SOLIDIFY")
        m.thickness, m.offset, m.use_even_offset = thick, -1.0, True


class Mats:
    """Hero colours come from scenes.json hero_colours (module constants are the fallbacks); the plate and board take the production's support colours."""

    def __init__(self, S):
        hc = (S.p or {}).get("hero") or {}
        self.hull = S.hero("housing", hc.get("hull", HULL), rough=0.5, coat=0.15)
        self.deck = S.hero("big", hc.get("deck", DECK), rough=0.6)
        self.white = S.hero("blade", hc.get("white", WHITE), rough=0.5)
        self.buff = S.hero("small", hc.get("buff", BUFF), rough=0.5)
        self.bulk = tr.plain("bulkhead", hc.get("bulk", BULK), rough=0.55)
        self.floor = tr.plain("floor", hc.get("floor", FLOOR), rough=0.6)
        self.ink = S.ink
        self.sea_hex = hc.get("sea", SEA)
        self.sea = S.glass(self.sea_hex, alpha=0.82, rough=0.55, name="sea_water")
        self.sea_solid = tr.plain("sea_solid", self.sea_hex, rough=0.3)
        self.water = S.glass(hc.get("water", WATER), alpha=0.62, rough=0.1, name="hull_water")
        self.spill = S.glass("#BFE6F5", alpha=0.85, rough=0.1, name="spill_water")
        self.ice = tr.plain("ice_berg", hc.get("ice", ICE), rough=0.45)
        self.accent = S.accent
        self.red = S.error
        self.plate = S.plate_mat(rough=0.7)
        self.board = S.board_mat()


# ------------------------------------------------------------------ the liner
class Liner:
    """One liner. root carries the pitch and the sink; lid (deck, deckhouse, boats) and near (the near half of the hull) lift away for the cutaway."""

    def __init__(self, S, m, name="liner", loc=(0, 0, 0)):
        self.S, self.m, self.name = S, m, name
        self.root = tr.empty(f"{name}_root", loc)
        r = self.root
        nx = 90
        xs = [-L / 2 + L * i / (nx - 1) for i in range(nx)]
        # far half of the hull shell (stays) and the near half (swings away on a hinge along the keel line)
        far = mesh_obj(f"{name}_hull_far", m.hull, r)
        loft(far, [[sec(x, math.pi / 2 + (math.pi / 2) * j / 24) for j in range(25)] for x in xs], thick=WALL)
        self.near_hinge = tr.empty(f"{name}_near_hinge", (0.0, 0.0, -D), r)
        nr = mesh_obj(f"{name}_hull_near", m.hull, self.near_hinge)
        loft(nr, [[tuple(p - q for p, q in zip(sec(x, (math.pi / 2) * j / 24), (0.0, 0.0, -D))) for j in range(25)] for x in xs], thick=WALL)
        # the lid
        self.lid = tr.empty(f"{name}_lid", (0.0, 0.0, 0.0), r)
        lid = self.lid
        deck = mesh_obj(f"{name}_deck", m.deck, lid)
        loft(deck, [[(x, -hw(x) * (1.0 - 2.0 * j / 12), 0.02) for j in range(13)] for x in xs], thick=0.3)
        self._deckhouse(lid)
        # funnels and masts stay with the ship (they stand on the centre line)
        self.funnels = []
        for k, x in enumerate((-26.0, -9.0, 8.0, 25.0)):
            f = tr.cyl(f"{name}_funnel{k}", 3.3, 18.0, (x, 0.0, 7.0), m.buff, axis="Z", verts=40, parent=r)
            f.scale = (0.8, 1.0, 1.0)
            cap = tr.cyl(f"{name}_funnelcap{k}", 3.4, 2.2, (x, 0.0, 15.3), m.ink, axis="Z", verts=40, parent=r)
            cap.scale = (0.8, 1.0, 1.0)
            self.funnels += [f, cap]
        for k, x in enumerate((44.0, -50.0)):
            self.funnels.append(tr.cyl(f"{name}_mast{k}", 0.45, 17.0, (x, 0.0, 8.0), m.white, axis="Z", verts=12, parent=r))
        self.funnel_base = [tuple(o.scale) for o in self.funnels]
        # interior: bulkheads (rise from the floor), floor tiles, water, spill sheets
        self.bulks, self.floors, self.waters, self.spills = [], [], [], []
        for i, x in enumerate(BULK_X):
            b = mesh_obj(f"{name}_bulk{i}", m.bulk, r)
            pts = profile(x, ZB)
            verts = [(x, y, z) for (y, z) in pts]
            n = len(pts)
            b.data.from_pydata(verts, [], [tuple(range(n))])
            b.data.update()
            mod = b.modifiers.new("solid", "SOLIDIFY")
            mod.thickness, mod.offset = 0.55, 0.0
            b.data.use_auto_texspace = True
            for p in b.data.polygons:
                p.use_smooth = False
            self.bulks.append(b)
        for k in range(NC):
            x0, x1 = EDGE_X[k], EDGE_X[k + 1]
            xm = 0.5 * (x0 + x1)
            fl = tr.rbox(f"{name}_floor{k}", (x1 - x0 - 0.7, max(0.5, hw(xm) - WALL - 0.2), 0.4), (xm, max(0.5, hw(xm) - WALL - 0.2) / 2, -hd(xm) + WALL + 0.3), m.floor, bevel=0.1, parent=r)
            self.floors.append(fl)
            w = mesh_obj(f"{name}_water{k}", m.water, r)
            self.waters.append(w)
            sp = tr.rbox(f"{name}_spill{k}", (0.5, 1.0, 1.0), (x0, 3.0, ZB - 1.0), m.spill, bevel=0.05, parent=r)
            self.spills.append(sp)
        self.tops = []
        for i, x in enumerate(BULK_X):
            wi = max(1.0, hw(x) - WALL)
            tp = tr.rbox(f"{name}_top{i}", (1.0, wi, 0.5), (x, wi / 2, ZB + 0.3), m.accent, bevel=0.1, parent=r)
            tp.scale = (EPS, EPS, EPS)
            self.tops.append(tp)
        self.slits = []

    # ------------------------------------------------------------------ parts
    def _deckhouse(self, lid):
        m, name = self.m, self.name
        tr.rbox(f"{name}_tier1", (66.0, 17.0, 3.6), (-2.0, 0.0, 1.8), m.white, bevel=0.5, parent=lid)
        tr.rbox(f"{name}_tier2", (50.0, 13.0, 3.2), (-6.0, 0.0, 5.2), m.white, bevel=0.5, parent=lid)
        tr.rbox(f"{name}_bridge", (9.0, 14.0, 3.0), (33.0, 0.0, 2.6), m.white, bevel=0.5, parent=lid)
        tr.rbox(f"{name}_bow_cabin", (14.0, 11.0, 2.4), (-44.0, 0.0, 1.4), m.white, bevel=0.4, parent=lid)
        for sgn in (-1, 1):
            for k in range(22):
                x = -33.0 + 3.0 * k
                tr.rbox(f"{name}_win{sgn}_{k}", (1.3, 0.3, 1.0), (x, sgn * 8.55, 1.9), m.ink, bevel=0.1, parent=lid)
            for k in range(15):
                x = -29.0 + 3.0 * k
                tr.rbox(f"{name}_win2{sgn}_{k}", (1.3, 0.3, 1.0), (x, sgn * 6.55, 5.3), m.ink, bevel=0.1, parent=lid)
            for k in range(8):
                x = -22.0 + 6.0 * k
                tr.rbox(f"{name}_boat{sgn}_{k}", (4.2, 1.2, 1.1), (x, sgn * 7.6, 4.3 + 0.0), m.white, bevel=0.3, parent=lid)

    def add_slits(self, n=6, x_from=None, x_to=None):
        """Narrow openings along the near bow plates, hidden until Liner.update(slit=...) pops them."""
        x_from = EDGE_X[NC - 6] if x_from is None else x_from
        x_to = EDGE_X[NC - 1] - 3.0 if x_to is None else x_to
        for k in range(n):
            x = lerp(x_to, x_from, k / (n - 1))                  # k = 0 is the one nearest the bow
            z = -2.6 - 0.9 * (k % 3)
            o = tr.rbox(f"{self.name}_slit{k}", (3.4, 0.5, 0.45), (x, -hw(x) - 0.15, z), self.m.red, bevel=0.1, parent=self.root)
            o.scale = (EPS, EPS, EPS)
            self.slits.append((o, x))
        return self.slits

    # ------------------------------------------------------------------ per frame
    def _water(self, k, f, theta):
        """Water of compartment k: fraction f of the way from the floor to the level that touches the aft bulkhead top, in the world plane for pitch theta."""
        x0, x1 = EDGE_X[k], EDGE_X[k + 1]
        o = self.waters[k]
        if f <= 0.01:
            o.scale = (EPS, EPS, EPS)
            return
        o.scale = (1.0, 1.0, 1.0)
        tn = math.tan(theta)
        xm = 0.5 * (x0 + x1)
        floor = -hd(xm) + WALL + 0.5
        full = ZB - 0.15
        base = lerp(floor, full, min(1.0, f))
        lv = lambda x: min(-0.1, base + (x - x0) * tn * min(1.0, f * 1.5))
        rows = [[(x, y, z) for (y, z) in profile(x, lv(x))] for x in (x0 + 0.5, x1 - 0.5)]
        loft(o, rows, close=True)

    def _spill(self, k, amount, fnext):
        """Spill sheet over bulkhead k (between compartments k and k + 1, the water pouring from the bow side to the aft side): amount 0..1 is how much is pouring, fnext the receiving compartment's fill."""
        o = self.spills[k]
        if amount <= 0.02:
            o.scale = (EPS, EPS, EPS)
            return
        x = BULK_X[k]
        w = max(1.0, hw(x) - WALL - 0.5) * min(1.0, amount)
        drop = max(0.5, 5.0 * (1.0 - fnext) + 0.5)
        o.scale = (0.55, w, drop)
        o.location = (x - 0.9, w / 2, ZB - drop / 2 + 0.2)

    def glow(self, tops):
        """tops: per-bulkhead 0..1, the accent bar that lights the open top of each wall."""
        for i, tp in enumerate(self.tops):
            k = tops[i] if tops else 0.0
            tp.scale = (EPS, EPS, EPS) if k <= 0.01 else (1.0, 1.0, min(1.0, k))

    def update(self, open=0.0, near_open=None, bulk=None, fill=None, pitch=0.0, drop=0.0, lid_k=None, spill=None, tints=None, funnel=None):
        """open 0..1: the lid lifts and the near shell swings away; near_open overrides the shell if given. bulk: per-bulkhead rise 0..1 (None = all up). fill: per-compartment water 0..1.
        pitch (rad, bow down), drop (units the ship sinks). spill: {bulkhead k: (amount, receiving_fill)}. tints: {k: 'accent' | 'red'} for the floor tiles."""
        no = open if near_open is None else near_open
        lk = open if lid_k is None else lid_k
        self.root.location = (0.0, 0.0, -drop)
        self.root.rotation_euler = (0.0, pitch, 0.0)
        self.lid.location = (0.0, 0.0, 70.0 * ease(lk))
        self.lid.scale = tuple(max(EPS, 1.0 - smooth(0.55, 1.0, lk)) for _ in range(3))
        fk = max(EPS, 1.0 - smooth(0.55, 1.0, lk)) if funnel is None else funnel          # the funnels and masts leave with the lid unless a scene keeps them
        for o, b in zip(self.funnels, self.funnel_base):
            o.scale = tuple(fk * v for v in b)
        self.near_hinge.rotation_euler = (math.radians(115.0) * ease(no), 0.0, 0.0)
        self.near_hinge.scale = tuple(max(EPS, 1.0 - smooth(0.6, 1.0, no)) for _ in range(3))
        for i, b in enumerate(self.bulks):
            kk = 1.0 if bulk is None else bulk[i]
            xb = BULK_X[i]
            b.location = (0.0, 0.0, 0.0)
            b.scale = (1.0, 1.0, max(EPS, ease(kk)))
            b.location.z = (-hd(xb) + WALL) * (1.0 - max(EPS, ease(kk)))
        for k in range(NB, NC):
            self.spills[k].scale = (EPS, EPS, EPS)
        for k in range(NC):
            f = 0.0 if fill is None else fill[k]
            self._water(k, f, pitch)
            sp = (0.0, 0.0)
            if spill and k in spill:
                sp = spill[k]
            if k < NB:
                self._spill(k, sp[0], sp[1])
            t = (tints or {}).get(k)
            fl = self.floors[k]
            fl.data.materials.clear()
            fl.data.materials.append(self.m.accent if t == "accent" else self.m.red if t == "red" else self.m.floor)

    def slit_state(self, k_on):
        for i, (o, x) in enumerate(self.slits):
            on = ease(k_on * len(self.slits) - i)
            o.scale = (max(EPS, on),) * 3 if on > 0.01 else (EPS, EPS, EPS)


# ------------------------------------------------------------------ the sea
class Sea:
    """The open sea: a wide translucent slab whose top is the waterline (exterior scenes), or the front panels that stand for the sea beside a cutaway hull."""

    def __init__(self, S, m, name="sea", size=(2000.0, 1600.0), z=SEA_Z, thick=26.0):
        self.slab = tr.rbox(f"{name}_slab", (size[0], size[1], thick), (0.0, 0.0, z - thick / 2), m.sea, bevel=0.3)
        self.top = z

    def hide(self):
        self.slab.scale = (EPS, EPS, EPS)


class Panels:
    """Thin sea panels in front of the cut plane, with a hole where the hull is, so the hull interior stays dry and the waterline reads across the picture; `fill` closes the hole."""

    def __init__(self, S, m, name="panel", half=150.0, depth=34.0, z=SEA_Z):
        t = 1.0
        y = -t / 2 - 0.05
        right = L / 2 + 0.2
        hole = D + 1.0 + z                                   # the hole runs from the waterline down to just below the keel (z = -(D + 1))
        self.parts = [
            tr.rbox(f"{name}_aft", (half - right, t, depth), (-(half + right) / 2, y, z - depth / 2), m.sea, bevel=0.1),
            tr.rbox(f"{name}_bow", (half - right, t, depth), ((half + right) / 2, y, z - depth / 2), m.sea, bevel=0.1),
            tr.rbox(f"{name}_keel", (2 * right, t, depth - hole), (0.0, y, -(D + 1.0) - (depth - hole) / 2), m.sea, bevel=0.1),
        ]
        self.fillp = tr.rbox(f"{name}_fill", (2 * right, t, hole), (0.0, y, z - hole / 2), m.sea, bevel=0.1)
        self.fillp.scale = (EPS, EPS, EPS)
        self.parts.append(tr.rbox(f"{name}_back", (2 * half, 1.0, depth), (0.0, W + 6.0, z - depth / 2), m.sea_solid, bevel=0.1))
        self.line = tr.rbox(f"{name}_line", (2 * half, t + 0.1, 0.18), (0.0, y, z), m.accent, bevel=0.05)

    def fill(self, k):
        self.fillp.scale = (1.0, 1.0, 1.0) if k > 0.5 else (EPS, EPS, EPS)

    def show(self, on):
        s = (1.0, 1.0, 1.0) if on else (EPS, EPS, EPS)
        for o in self.parts + [self.line]:
            o.scale = s


# ------------------------------------------------------------------ the iceberg
class Iceberg:
    """A faceted, lumpy iceberg: a big mass below the waterline, a ragged peak above. root is placed by the scene (z = the waterline)."""

    def __init__(self, S, m, name="berg", loc=(0, 0, SEA_Z), size=(16.0, 11.0, 15.0), seed=3):
        self.root = tr.empty(f"{name}_root", loc)
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
        for v in bm.verts:
            p = v.co
            n = noise.noise((p.x * 1.6 + seed, p.y * 1.6, p.z * 1.6)) * 0.34 + noise.noise((p.x * 3.7, p.y * 3.7 + seed, p.z * 3.7)) * 0.14
            r = 1.0 + n
            v.co = mathutils.Vector((p.x * r * size[0], p.y * r * size[1], p.z * r * size[2] * (1.35 if p.z > 0 else 0.75)))
        me = bpy.data.meshes.new(name)
        bm.to_mesh(me)
        bm.free()
        o = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(o)
        me.materials.append(m.ice)
        for p in me.polygons:
            p.use_smooth = False
        o.parent = self.root
        self.obj = o
