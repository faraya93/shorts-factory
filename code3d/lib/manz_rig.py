"""Rig of production 025 (why you do not get poisoned if you swallow an apple seed): the sealed apple asset, the apple cut in two (the sealed mesh bisected, cut faces filled with flesh,
a core and seeds on each cut face), the enlarged seed (two shell halves around an emissive kernel), a half tube, two pressing pads, juice drops, a cloud of accent beads and a heap
of seeds. The apple is the sealed library asset placed through avion_rig.place; everything else is a build. Runs inside Blender.
Scene units: 0.6 per asset millimetre (the apple is about 47 wide and 43 high, standing on z = 0); the camera looks along +y, x right, z up. Composite things are driven as rigid groups:
every member is a swarm-style item of the Shot, placed per frame from the group's transform."""
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import avion_rig as av  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

KS = 0.6
K = 1000.0
ZC = 21.5                                  # height of the apple's centre (the cut pivot)
SEED_L, SEED_W = 5.4, 3.0                  # a real seed in scene units
BIG = 4.6                                  # the enlarged seed's scale factor
LIGHT_K = 2.0
ease = av.ease
look = av.look
lights = av.lights


class Mats:
    """Hero colours come from scenes.json hero_colours; the plate and board take the production's support colours."""

    def __init__(self, S):
        hc = (S.p or {}).get("hero") or {}
        self.skin = S.hero("housing", hc.get("skin", "#8E2A32"), rough=0.5, coat=0.08)
        self.flesh = S.hero("small", hc.get("flesh", "#F4E7C6"), rough=0.55)
        self.core = S.hero("blade", hc.get("core", "#D9CFA3"), rough=0.6)
        self.seed = S.hero("rubber", hc.get("seed", "#4B2C1E"), rough=0.6, coat=0.0)
        self.pad = S.hero("big", hc.get("pad", "#51555A"), rough=0.5)
        self.tube = S.hero("g_board", hc.get("tube", "#F0E6D8"), rough=0.6)
        self.juice = tr.plain("juice", "#D7D27A", rough=0.3)
        self.stem = tr.plain("stem", "#4A3220", rough=0.6)
        self.plate = S.plate_mat(rough=0.7)
        self.board = S.board_mat()
        self.ink = S.ink
        self.accent = S.accent
        self.red = S.error


class Rigid:
    """A group of items that move as one body. add(obj, offset, rot, k); set(loc, rot, k) places every member (None hides the group)."""

    def __init__(self, S):
        self.S, self.members = S, []

    def add(self, o, off=(0, 0, 0), rot=(0, 0, 0), k=1.0):
        self.members.append((o, Vector(off), Euler(rot), k))
        return o

    def _d(self, o):
        return next(d for ob, d in self.S.items if ob is o)

    def set(self, loc, rot=(0, 0, 0), k=1.0):
        if loc is None or k < 1e-3:
            for o, *_ in self.members:
                self._d(o)["sw"] = None
            return
        R = Euler(rot).to_matrix()
        for o, off, mrot, mk in self.members:
            w = Vector(loc) + R @ (off * k)
            self._d(o)["sw"] = (tuple(w), k * mk, (R @ mrot.to_matrix()).to_euler())


def seed_surface(name, mat, L, W, half=None, thick=0.0, nx=22, na=28, parent=None):
    """A teardrop seed, long axis +x (tip at +x), centred; half = 'top' / 'bottom' for a shell half (open at z = 0), thick = shell thickness."""
    a0, a1 = {None: (0.0, 2 * math.pi), "top": (0.0, math.pi), "bottom": (math.pi, 2 * math.pi)}[half]

    def prof(u):
        if u < 0.38:
            return math.sqrt(max(0.0, 1 - ((0.38 - u) / 0.38) ** 2))
        t = (u - 0.38) / 0.62
        return max(0.0, 1 - t ** 1.7) ** 0.62

    def pos(i, j):
        u = i / (nx - 1)
        a = a0 + (a1 - a0) * j / na
        f = prof(u)
        return (L * (u - 0.4), W / 2 * f * math.cos(a), 0.75 * W / 2 * f * math.sin(a))
    return av.grid_surface(name, nx, na, pos, mat, thick=thick, flip=(half == "top"), parent=parent)


def half_pipe(name, x0, x1, r, zc, mat, thick=0.8, nx=24, na=36):
    """The back half (y >= 0) of a tube along x, axis at height zc, open toward the camera."""
    def pos(i, j):
        x = x0 + (x1 - x0) * i / (nx - 1)
        a = math.pi * j / na
        return (x, r * math.sin(a), zc + r * math.cos(a))
    return av.grid_surface(name, nx, na, pos, mat, thick=thick, flip=True)


class Seed:
    """The enlarged seed: shell halves (top and bottom) around an emissive kernel, one rigid group. Pose with set(loc, rot, gap, k, kernel): gap = separation of the halves,
    kernel = scale of the glowing kernel (0 hides it). Names start with `seed_`."""

    def __init__(self, S, m, prefix="seed", L=SEED_L * BIG, W=SEED_W * BIG):
        self.g = Rigid(S)
        self.top = S.reg(seed_surface(f"{prefix}_top", m.seed, L, W, "top", thick=0.9))
        self.bot = S.reg(seed_surface(f"{prefix}_bot", m.seed, L, W, "top", thick=0.9))               # the top half turned over: the one orientation that renders from the inside
        self.ker = S.reg(seed_surface(f"{prefix}_kernel", m.accent, L * 0.8, W * 0.74))
        self.g.add(self.top)
        self.g.add(self.bot, rot=(math.pi, 0, 0))
        self.g.add(self.ker)
        self.L, self.W = L, W

    def set(self, loc, rot=(0, 0, 0), gap=0.0, k=1.0, kernel=1.0):
        g = self.g
        g.members[0] = (self.top, Vector((0, 0, gap / 2)), g.members[0][2], 1.0)
        g.members[1] = (self.bot, Vector((0, 0, -gap / 2)), g.members[1][2], 1.0)
        g.members[2] = (self.ker, Vector((0, 0, 0)), g.members[2][2], max(kernel, 1e-3))
        g.set(loc, rot, k)
        if loc is not None and kernel < 1e-3:
            g._d(self.ker)["sw"] = None


class Fruit:
    """The sealed apple (whole) plus the same apple cut in two. The whole apple is `root` (hide() to swap it for the halves); halves are two rigid groups pivoting at (0, 0, ZC)
    on the cut plane x = 0: half R (stem on it) keeps x > 0, half L keeps x < 0. split(k) places both: k = 0 joined as the whole apple, k = 1 opened like a book with the
    cut faces toward the camera, one on each side."""

    def __init__(self, S, m, seeds=True, skip=()):
        self.S, self.m, self.skip = S, m, skip
        root, objs = av.place("apple", None, K * KS)
        self.root, self.objs = root, objs
        body = next(o for o in objs if o.name == "apple_body")
        for o in objs:
            if o.type != "MESH":
                continue
            o.name = "apple_" + o.name.replace("apple_", "")
            for i in range(len(o.material_slots)):
                o.material_slots[i].material = m.stem if "stem" in o.name else m.skin
        bpy.context.view_layer.update()
        self.groups = {}
        for side in ("L", "R"):
            self.groups[side] = self._half(side, body, seeds)

    def _half(self, side, body, seeds):
        S, m = self.S, self.m
        bm = bmesh.new()
        bm.from_mesh(body.data)
        bm.transform(body.matrix_world)
        res = bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(0, 0, 0), plane_no=(1, 0, 0),
                                     clear_inner=(side == "R"), clear_outer=(side == "L"))
        cut = [e for e in res["geom_cut"] if isinstance(e, bmesh.types.BMEdge)]
        new = bmesh.ops.holes_fill(bm, edges=cut, sides=len(cut) + 2)["faces"]
        for f in bm.faces:
            f.material_index = 2 if f in new else 0
            f.smooth = f.material_index == 0
        bm.transform(Matrix.Translation((0, 0, -ZC)))
        me = bpy.data.meshes.new(f"half_{side}")
        bm.to_mesh(me)
        bm.free()
        for mt in (m.skin, m.skin, m.flesh):
            me.materials.append(mt)
        o = bpy.data.objects.new(f"half_{side}", me)
        bpy.context.scene.collection.objects.link(o)
        S.reg(o)
        g = Rigid(S)
        g.add(o)
        n = -1.0 if side == "R" else 1.0                                       # the cut face looks along n (x) before the half is turned to the camera
        core = S.ball(f"half_core_{side}", m.core, 1.0, (0, 0, 0), shape=(0.04, 6.8, 11.5), seg=32)
        g.add(core, off=(n * 0.06, 0, 1.0))
        for i, (yy, zz) in enumerate(((-2.4, 3.0), (2.4, 3.0))):
            cav = S.ball(f"half_cav_{side}{i}", m.stem, 1.0, (0, 0, 0), shape=(0.04, 2.4, 4.4), seg=24)
            g.add(cav, off=(n * 0.12, yy, zz))
            if seeds and (side, i) not in self.skip:
                sd = S.reg(seed_surface(f"half_seed_{side}{i}", m.seed, SEED_L * 1.25, SEED_W * 1.25))
                g.add(sd, off=(n * 0.4, yy, zz), rot=(0, -math.pi / 2, 0.12 * (1 if i else -1)))
        if side == "R":
            stem = S.cyl("half_stem", 0.8, 17.0, (0, 0, 0), m.stem, axis="Z", verts=14)
            g.add(stem, off=(1.6, 0, 36.0 - ZC + 7.5), rot=(0, math.radians(12), 0))
        return g

    def hide_whole(self, hidden=True):
        self.root.scale = (1e-4,) * 3 if hidden else (1.0, 1.0, 1.0)

    def whole_at(self, loc=(0, 0, 0), rot=(0, 0, 0)):
        self.root.location, self.root.rotation_euler = loc, rot

    def split(self, k, base=(0.0, 0.0, 0.0), lift=0.0):
        """Open the two halves by k (0..1) about the pivot at base + (0, 0, ZC); lift raises them (a hop while they fall open)."""
        if k <= 0.0:
            self.hide_whole(False)
            for g in self.groups.values():
                g.set(None)
            return
        self.hide_whole(True)
        kk = ease(k)
        spread = 25.5 * kk
        for side, sgn in (("R", 1.0), ("L", -1.0)):
            loc = (base[0] + sgn * spread, base[1], base[2] + ZC + lift)
            self.groups[side].set(loc, (0, 0, sgn * math.pi / 2 * kk))

    def whole_only(self, loc=(0, 0, 0), rot=(0, 0, 0)):
        """Show the whole apple at loc (halves hidden)."""
        self.hide_whole(False)
        self.whole_at(loc, rot)
        for g in self.groups.values():
            g.set(None)


def tube_bands(S, m, name, n, x0, x1, r, zc):
    """Slim rings around a half tube (static ribs, a cue that it is a pipe): returns the objects."""
    out = []
    for i in range(n):
        x = x0 + (x1 - x0) * i / max(1, n - 1)
        o = S.torus(f"{name}_{i}", r + 0.5, 0.5, (x, 0, zc), m.tube, rot=(0, math.pi / 2, 0))
        out.append(o)
    return out


def drops(S, m, n, name="juice", r=0.9):
    """n small juice beads (swarm items placed by the scene script)."""
    src = S.ball(f"{name}_src", m.juice, r, (0, 0, 0))
    return S.swarm(n, src, lambda i, t: None)


def cloud(S, m, n, name="cloud", r=1.5, seed=11):
    """n accent beads released from a point; returns (objects, dirs). Place with cloud_at."""
    src = S.ball(f"{name}_src", m.accent, r, (0, 0, 0))
    objs = S.swarm(n, src, lambda i, t: None)
    rnd = random.Random(seed)
    dirs = []
    for _ in range(n):
        v = Vector((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-0.3, 1.2)))
        dirs.append(v.normalized() * rnd.uniform(0.5, 1.0))
    return objs, dirs


def pile_seeds(S, m, n, name="pile", scale=1.9):
    """n clones of one seed (a heap grows from them). Returns the objects; the scene script places them."""
    src = S.reg(seed_surface(f"{name}_src", m.seed, SEED_L * scale, SEED_W * scale, nx=12, na=14))
    return S.swarm(n, src, lambda i, t: None)
