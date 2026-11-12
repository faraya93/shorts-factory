"""Rig of production 022 (why a fork sparks in the microwave): a cutaway microwave oven (steel shell, open cavity, turning plate, hinged door with window and a metal-wire screen, control panel),
a fork and a spoon lying on the plate, the glowing "charge" beads that slosh through the metal, the wave fronts that bounce between the walls, the glow of the walls and the screen, and the
sparks between the tine tips. Rigid, geometric parts are code primitives (the library oven candidates are unsealed search results; the build is the audit's route). Runs inside Blender.
Scene units are centimetres of a toy scale (the oven is 64 wide, 38 deep, 36 tall); the opening faces -y (the camera side), x right, z up. Driven per frame by the scene script."""
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import avion_rig as av  # noqa: E402
import common as c  # noqa: E402
import machine_kit as mk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

LIGHT_K = 2.0
OW, OD, OH = 64.0, 38.0, 44.0               # oven width, depth, height
WALL = 2.0
CX0, CX1 = -30.0, 8.0                       # cavity interior x range
CY0, CY1 = -19.0, 17.0                      # cavity interior y range (front opening at -19)
CZ0, CZ1 = 2.0, 42.0
PLATE_C = (-11.0, 0.0)                      # turning plate centre (x, y)
PLATE_R, PLATE_T = 16.0, 0.8
PLATE_Z = CZ0 + 1.0                         # plate top = PLATE_Z + PLATE_T / 2
CS = 1.1                                  # cutlery scale
HINGE = (-32.0, -19.0)
DOOR_W, DOOR_H = 41.0, 40.0
STEEL = "#B8C0C9"
SHELL = "#D8DBDF"
INNER = "#E6E8EB"
PLATE = "#2B3441"
INK = "#1D1B2E"
ease = av.ease
look = av.look
lights = av.lights


def glow_mat(name, hex_color, strength=2.0):
    """Translucent accent emission whose opacity is animated (set(k), k 0..1)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = c.linear(hex_color)
    em.inputs["Strength"].default_value = strength
    tp = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tp.outputs["BSDF"], mix.inputs[1])
    nt.links.new(em.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    mix.inputs[0].default_value = 0.0

    def set_k(k):
        mix.inputs[0].default_value = max(0.0, min(1.0, k))
    return m, set_k


class Mats:
    """Hero colours come from scenes.json hero_colours; the plate and board take the production's support colours."""

    def __init__(self, S):
        hc = (S.p or {}).get("hero") or {}
        self.shell = S.hero("housing", hc.get("shell", SHELL), rough=0.38, metal=0.2, coat=0.15)
        self.inner = S.hero("big", hc.get("inner", INNER), rough=0.45, metal=0.1)
        self.steel = S.hero("small", hc.get("steel", STEEL), rough=0.28, metal=0.7)
        self.panel = S.hero("blade", hc.get("panel", "#C9CED4"), rough=0.4)
        self.plate = tr.plain("plate", S.p.get("support_plate", PLATE), rough=0.55)
        self.board = S.board_mat()
        self.glass = tr.plain("door_glass", "#2A2F3E", rough=0.05)
        g = self.glass.node_tree.nodes["Principled BSDF"]
        g.inputs["Alpha"].default_value = 0.35
        self.glass.surface_render_method = "BLENDED"
        self.ink = S.ink
        self.accent = S.accent
        self.red = S.error
        self.wave, self.wave_k = glow_mat("wave_glow", "#0A5C6B", 3.0)
        self.wall, self.wall_k = glow_mat("wall_glow", "#0A5C6B", 3.0)
        self.screen_mat, self.screen_k = glow_mat("screen_glow", "#0A5C6B", 4.0)
        self.core = tr.gold_emit("spark_core", "#EAFBFF", 9.0)                       # the hot centre of a spark (rung 1 of the sparks element: bluish-white)
        self.halo, self.halo_k = glow_mat("spark_halo", "#7FD8EA", 1.0)
        self.screen_steel = tr.plain("screen_steel", "#7F8892", rough=0.3, metallic=0.8)


# ------------------------------------------------------------------ the oven
def _box(name, size, loc, mat, bevel=0.2, parent=None):
    return tr.rbox(name, size, loc, mat, bevel=bevel, parent=parent)


def screen_mesh(name, w, h, mat, parent, pitch=1.3, bar=0.22, thick=0.4):
    """A wire grid (vertical and horizontal bars) merged into one mesh, centred on the origin, standing in the xz plane."""
    bm = bmesh.new()
    nx, nz = int(w / pitch), int(h / pitch)
    for i in range(nx + 1):
        x = -w / 2 + i * w / nx
        r = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(bar, thick, h), verts=r["verts"])
        bmesh.ops.translate(bm, vec=(x, 0, 0), verts=r["verts"])
    for j in range(nz + 1):
        z = -h / 2 + j * h / nz
        r = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=(w, thick, bar), verts=r["verts"])
        bmesh.ops.translate(bm, vec=(0, 0, z), verts=r["verts"])
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat)
    o.parent = parent
    return o


def oven(S, m, name="oven", door_angle=105.0):
    """The cutaway oven standing on z = 0 with its opening toward -y. Returns a namespace: root, door (pivot empty), plate (turning root), top, glow plates, screen, wave slabs source."""
    ns = type("Oven", (), {})()
    root = tr.empty(f"{name}_root")
    ns.root = root
    ns.top = _box(f"{name}_top", (OW, OD, WALL), (0, 0, OH - WALL / 2), m.shell, parent=root)
    _box(f"{name}_base", (OW, OD, WALL), (0, 0, WALL / 2), m.shell, parent=root)
    _box(f"{name}_back", (OW, WALL, OH), (0, OD / 2 - WALL / 2, OH / 2), m.shell, parent=root)
    _box(f"{name}_left", (WALL, OD, OH), (-OW / 2 + WALL / 2, 0, OH / 2), m.shell, parent=root)
    _box(f"{name}_div", (WALL, OD, OH), (9.0, 0, OH / 2), m.shell, parent=root)
    _box(f"{name}_panel_block", (OW / 2 - 10.0, OD, OH), ((OW / 2 + 10.0) / 2, 0, OH / 2), m.panel, parent=root)
    # cavity lining: lighter inner faces so the cutlery reads (separate thin plates just inside the walls)
    _box(f"{name}_in_back", (CX1 - CX0, 0.3, CZ1 - CZ0), ((CX0 + CX1) / 2, CY1 - 0.15, (CZ0 + CZ1) / 2), m.inner, bevel=0.05, parent=root)
    _box(f"{name}_in_left", (0.3, CY1 - CY0, CZ1 - CZ0), (CX0 + 0.15, (CY0 + CY1) / 2, (CZ0 + CZ1) / 2), m.inner, bevel=0.05, parent=root)
    _box(f"{name}_in_right", (0.3, CY1 - CY0, CZ1 - CZ0), (CX1 - 0.15, (CY0 + CY1) / 2, (CZ0 + CZ1) / 2), m.inner, bevel=0.05, parent=root)
    _box(f"{name}_in_floor", (CX1 - CX0, CY1 - CY0, 0.3), ((CX0 + CX1) / 2, (CY0 + CY1) / 2, CZ0 + 0.15), m.inner, bevel=0.05, parent=root)
    # control panel: display, buttons, a dial
    px = (OW / 2 + 10.0) / 2
    _box(f"{name}_display", (11.0, 0.5, 4.5), (px, -OD / 2 - 0.1, OH - 8.0), m.ink, bevel=0.15, parent=root)
    for r in range(4):
        for k in range(3):
            _box(f"{name}_btn_{r}_{k}", (3.3, 0.7, 2.2), (px - 4.0 + 4.0 * k, -OD / 2 - 0.2, OH - 16.0 - 4.4 * r), m.steel, bevel=0.35, parent=root)
    tr.cyl(f"{name}_dial", 3.6, 1.2, (px, -OD / 2 - 0.4, 6.0), m.steel, axis="Y", parent=root, verts=40, bevel=0.2)
    # turning plate (rotates), roller ring under it
    ns.plate = tr.empty(f"{name}_plate_root", (PLATE_C[0], PLATE_C[1], PLATE_Z), parent=root)
    tr.cyl(f"{name}_plate", PLATE_R, PLATE_T, (0, 0, 0), m.plate, axis="Z", parent=ns.plate, verts=64, bevel=0.15)
    tr.cyl(f"{name}_hub", 3.0, 1.2, (PLATE_C[0], PLATE_C[1], CZ0 + 0.6), m.steel, axis="Z", parent=root, verts=32)
    # door on its hinge
    ns.door = tr.empty(f"{name}_door", (HINGE[0], HINGE[1], CZ0), parent=root)
    ns.door_angle = door_angle
    dz = DOOR_H / 2
    _box(f"{name}_door_top", (DOOR_W, 3.0, 4.0), (DOOR_W / 2, -1.5, DOOR_H - 2.0), m.shell, parent=ns.door)
    _box(f"{name}_door_bot", (DOOR_W, 3.0, 4.0), (DOOR_W / 2, -1.5, 2.0), m.shell, parent=ns.door)
    _box(f"{name}_door_l", (4.0, 3.0, DOOR_H), (2.0, -1.5, dz), m.shell, parent=ns.door)
    _box(f"{name}_door_r", (4.0, 3.0, DOOR_H), (DOOR_W - 2.0, -1.5, dz), m.shell, parent=ns.door)
    wx0, wx1, wz0, wz1 = 4.0, DOOR_W - 4.0, 4.0, DOOR_H - 4.0
    ns.screen = screen_mesh(f"{name}_screen", wx1 - wx0, wz1 - wz0, m.screen_steel, ns.door)
    ns.screen.location = ((wx0 + wx1) / 2, -1.5, (wz0 + wz1) / 2)
    ns.screen_glow = screen_mesh(f"{name}_screen_glow", wx1 - wx0, wz1 - wz0, m.screen_mat, ns.door, bar=0.34, thick=0.55)
    ns.screen_glow.location = ((wx0 + wx1) / 2, -1.5, (wz0 + wz1) / 2)
    ns.screen_glow.scale = (1.0, 1.0, 1.0)
    pane = _box(f"{name}_door_glass", (wx1 - wx0, 0.3, wz1 - wz0), ((wx0 + wx1) / 2, -2.5, (wz0 + wz1) / 2), m.glass, bevel=0.05, parent=ns.door)
    pane.visible_shadow = False
    tr.cyl(f"{name}_handle", 0.9, 22.0, (DOOR_W + 1.2, -4.0, dz), m.steel, axis="Z", parent=ns.door, verts=24, bevel=0.1)
    # wall glow plates (opacity animated): lining of the cavity, drawn just inside the lighter plates
    ns.walls = []
    for nm, size, loc in (("back", (CX1 - CX0, 0.1, CZ1 - CZ0), ((CX0 + CX1) / 2, CY1 - 0.4, (CZ0 + CZ1) / 2)),
                          ("left", (0.1, CY1 - CY0, CZ1 - CZ0), (CX0 + 0.4, (CY0 + CY1) / 2, (CZ0 + CZ1) / 2)),
                          ("right", (0.1, CY1 - CY0, CZ1 - CZ0), (CX1 - 0.4, (CY0 + CY1) / 2, (CZ0 + CZ1) / 2)),
                          ("floor", (CX1 - CX0, CY1 - CY0, 0.1), ((CX0 + CX1) / 2, (CY0 + CY1) / 2, CZ0 + 0.4)),
                          ("ceil", (CX1 - CX0, CY1 - CY0, 0.1), ((CX0 + CX1) / 2, (CY0 + CY1) / 2, CZ1 - 0.4))):
        o = _box(f"wallglow_{nm}", size, loc, m.wall, bevel=0.02, parent=root)
        o.visible_shadow = False
        ns.walls.append(o)
    return ns


def set_door(ns, k):
    """k 1 = open, 0 = closed (the door swings about its left hinge toward the camera)."""
    ns.door.rotation_euler = (0.0, 0.0, -math.radians(ns.door_angle) * k)


def hide(o, off=True):
    o.hide_render = off
    o.hide_viewport = off


# ------------------------------------------------------------------ cutlery on the plate
FORK_X, SPOON_X = -6.0, 6.0                 # plate-local x of the fork and spoon axes; both point toward the camera (-y)
FZ = PLATE_T / 2 + 0.3                      # cutlery centre height above the plate centre


def fork(S, m, parent, name="fork", mat=None, grow=0.0):
    """Fork along plate-local x, tines toward +x (handle at -x). Returns (root, tine tip points in fork space)."""
    mat = mat or m.steel
    g = grow
    root = tr.empty(f"{name}_root", (FORK_X, 0.0, FZ), parent=parent)
    root.rotation_euler = (0.0, 0.0, -math.pi / 2)
    root.scale = (CS, CS, CS)
    _box(f"{name}_handle", (8.0 + g, 1.8 + g, 0.5 + g), (-7.0, 0, 0), mat, bevel=0.2, parent=root)
    _box(f"{name}_neck", (4.4 + g, 2.8 + g, 0.5 + g), (-2.0, 0, 0), mat, bevel=0.2, parent=root)
    _box(f"{name}_head", (4.4 + g, 8.4 + g, 0.5 + g), (2.2, 0, 0), mat, bevel=0.2, parent=root)
    tips = []
    for j, y in enumerate((-3.3, -1.1, 1.1, 3.3)):
        _box(f"{name}_tine{j}", (8.0 + g, 0.95 + g, 0.5 + g), (8.2, y, 0), mat, bevel=0.22, parent=root)
        tips.append((11.7, y, 0.3))
    return root, tips


def spoon(S, m, parent, name="spoon", mat=None, grow=0.0):
    mat = mat or m.steel
    g = grow
    root = tr.empty(f"{name}_root", (SPOON_X, 0.0, FZ), parent=parent)
    root.rotation_euler = (0.0, 0.0, -math.pi / 2)
    root.scale = (CS, CS, CS)
    _box(f"{name}_handle", (8.0 + g, 1.8 + g, 0.5 + g), (-7.0, 0, 0), mat, bevel=0.2, parent=root)
    _box(f"{name}_neck", (5.4 + g, 2.2 + g, 0.5 + g), (-1.5, 0, 0), mat, bevel=0.2, parent=root)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.0, location=(5.4, 0, 0.0))
    bowl = bpy.context.object
    bowl.name = f"{name}_bowl"
    bowl.scale = (5.6 + g, 3.8 + g, 0.4 + g * 0.5)
    tr._finish(bowl, mat)
    bowl.parent = root
    return root


def plate_angle(t, rate=0.28, a0=0.0):
    return a0 + rate * t


def to_world(ns, lx, ly, lz, ang):
    """A plate-local point (x, y, z above the plate centre) to world, for a plate turned by `ang`."""
    ca, sa = math.cos(ang), math.sin(ang)
    return (PLATE_C[0] + lx * ca - ly * sa, PLATE_C[1] + lx * sa + ly * ca, PLATE_Z + lz)


def fork_pt(p, ang):
    """A point in fork space (the fork root sits at plate-local (FORK_X, 0), turned -90 degrees about z, scale CS) to world."""
    return to_world(None, FORK_X + p[1] * CS, -p[0] * CS, FZ + p[2] * CS, ang)


def spoon_pt(p, ang):
    return to_world(None, SPOON_X + p[1] * CS, -p[0] * CS, FZ + p[2] * CS, ang)


def build(S, door=1.0):
    """Mats, the oven with its door at `door` (1 open .. 0 closed), the fork and the spoon on the plate. Returns a namespace."""
    n = type("Set", (), {})()
    n.m = Mats(S)
    n.o = oven(S, n.m)
    set_door(n.o, door)
    n.fork, n.tips = fork(S, n.m, n.o.plate)
    n.spoon = spoon(S, n.m, n.o.plate)
    n.lift = lights(S, LIGHT_K)
    return n


def spin_plate(n, ang):
    n.o.plate.rotation_euler = (0.0, 0.0, ang)


# ------------------------------------------------------------------ the arcs
def zig(p0, p1, n, amp, seed):
    rnd = random.Random(seed)
    pts = []
    for i in range(n + 1):
        k = i / n
        p = [a + (b - a) * k for a, b in zip(p0, p1)]
        if 0 < i < n:
            for ax in range(3):
                p[ax] += rnd.uniform(-amp, amp)
        pts.append(tuple(p))
    return pts


def burst_arcs(S, mat, name, pairs, windows, parent=None, r=0.22, amp=0.7, seed=1, arch=1.6, core=None):
    """Short branching arcs between point pairs (in `parent` space), visible inside each (t0, dur) window, flickering between three shapes. Object names start with `name`."""
    groups = []
    rnd = random.Random(seed)
    for f in range(3):                                    # three flicker shapes per pair, shown in turn
        objs = []
        for i, (a, b) in enumerate(pairs):
            pts = [(p[0], p[1], p[2] + arch * math.sin(math.pi * k / 6)) for k, p in enumerate(zig(a, b, 6, amp, seed + f * 31 + i * 7))]
            mat = core if core is not None else mat
            objs.append(S.line(f"{name}_{f}_{i}", pts, r, mat, smooth=False))
            sx, sy, sz = pts[3]
            end = (sx + rnd.uniform(-1.6, 1.6), sy + rnd.uniform(-1.6, 1.6), sz + rnd.uniform(0.4, 2.0))
            objs.append(S.line(f"{name}_{f}_{i}b", zig((sx, sy, sz), end, 3, amp * 0.5, seed + f + i), r * 0.65, mat, smooth=False))
        groups.append(objs)
    if parent is not None:
        for g in groups:
            for o in g:
                o.parent = parent

    def upd(t):
        for f, objs in enumerate(groups):
            on = any(t0 <= t < t0 + dur for t0, dur in windows) and int(t * 24) % 3 == f
            for o in objs:
                hide(o, not on)
    S.every_frame(upd)
    return [o for g in groups for o in g]


# ------------------------------------------------------------------ charge beads (glow sloshing in the metal)
def beads(S, m, parent, name, n, fn, r=0.7):
    """n accent beads parented to `parent`; fn(i, t) -> ((x, y, z), scale) in the parent's space, or None (hidden)."""
    objs = [mk.sphere(f"{name}_{i}", m.accent, r, (0, 0, 0), shape=(1.0, 1.0, 0.8), parent=parent, seg=16) for i in range(n)]

    def upd(t):
        for i, o in enumerate(objs):
            v = fn(i, t)
            if v is None:
                o.scale = (sp.EPS,) * 3
            else:
                o.location = v[0]
                o.scale = (v[1], v[1], v[1] * 0.8)
    S.every_frame(upd)
    return objs


def waves(S, m, n=6, name="wave"):
    """Thin accent slabs spanning the cavity cross-section that bounce between the left and right walls; wave_k (the shared material) fades them in. Returns the objects; place with set_waves."""
    objs = [_box(f"{name}_{i}", (0.7, CY1 - CY0 - 2.0, CZ1 - CZ0 - 2.0), ((CX0 + CX1) / 2, (CY0 + CY1) / 2, (CZ0 + CZ1) / 2), m.wave, bevel=0.1) for i in range(n)]
    for o in objs:
        o.visible_shadow = False
    return objs


def set_waves(objs, t, speed=22.0, x0=CX0 + 1.5, x1=CX1 - 1.5):
    """Triangle-wave position of each slab (phase spread), so the fronts reverse at the walls."""
    span = x1 - x0
    n = len(objs)
    for i, o in enumerate(objs):
        u = (speed * t / span + i / n) % 2.0
        u = u if u <= 1.0 else 2.0 - u
        o.location = (x0 + span * u, (CY0 + CY1) / 2, (CZ0 + CZ1) / 2)
