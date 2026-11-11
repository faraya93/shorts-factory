"""Rig of production 020 (what if lightning hits you inside a car): the wet road, the ink storm cloud, the sealed cartoon car (with its roof splittable and slidable away), the seated driver
(sealed human-figure), branching bolts and short arcs as accent tubes, and the cage of accent lines around the cabin. Rigid, geometric parts are code primitives; the car and the driver are sealed
library assets placed through avion_rig.place. Runs inside Blender.
Scene units are centimetres of a toy scale (the car is 42 long, 9 wide, 16 tall); the car drives toward -x, the camera sits on the -y side; z up. Driven per frame by the scene script."""
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import avion_rig as av  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

K = 10.0                                  # the car, metres to scene units
CAR_L, CAR_W, CAR_H = 4.21 * K, 0.93 * K, 1.62 * K
ROOF_Z = 0.03                             # mesh-local height of the window sill: faces above it are the roof group (pillars, glass, roof)
LIGHT_K = 2.5
INK = "#1D1B2E"
DRIVER = ("#D99E7A", "#2973CC", "#2E3347", "#59331A")
ease = av.ease
look = av.look
lights = av.lights


class Mats:
    """Hero colours come from scenes.json hero_colours; the plate and board take the production's support colours."""

    def __init__(self, S):
        self.road = tr.plain("road_wet", S.p.get("support_plate", "#2B3441"), rough=0.22, coat=0.4)
        self.dash = tr.plain("road_dash", "#F6F2EE", rough=0.5)
        self.cloud = tr.plain("storm_cloud", INK, rough=0.9)
        self.plate = S.plate_mat(rough=0.7)
        self.board = S.board_mat()
        self.ink = S.ink
        self.accent = S.accent
        self.red = S.error


def road(S, m, length=420.0, width=160.0, dash_n=22, name="road"):
    """A wet dark road with a row of cream dashes down its middle; returns the dashes so a scene can scroll them."""
    tr.rbox(name, (length, width, 0.6), (0, 0, -0.3), m.road, bevel=0.2)
    dashes = []
    for i in range(dash_n):
        dashes.append(tr.rbox(f"dash_{i}", (10.0, 1.2, 0.15), (0, 16.0, 0.05), m.dash, bevel=0.05))
    return dashes


def scroll_dashes(dashes, t, speed, length=420.0):
    n = len(dashes)
    step = length / n
    for i, d in enumerate(dashes):
        x = ((-length / 2 + i * step - speed * t) % length) - length / 2
        d.location = (x, 16.0, 0.05)


def storm_cloud(S, m, centre=(0.0, 20.0, 110.0), seed=4, name="cloud"):
    """A dark slab of overlapping ink puffs, flat underneath. Returns the root empty."""
    rnd = random.Random(seed)
    root = tr.empty(f"{name}_root", centre)
    for i in range(14):
        r = rnd.uniform(13.0, 20.0)
        S.ball(f"{name}_{i}", m.cloud, r, (rnd.uniform(-52, 52), rnd.uniform(-14, 14), rnd.uniform(-3, 6)), shape=(1.3, 1.0, 0.55), parent=root)
    return root


def split_roof(obj, zb=ROOF_Z):
    """Cut `obj` (a car mesh) at mesh-local height zb: the faces above it become a new object (same materials, same parent and transform) and are removed from the original. Returns the new object or None."""
    me = obj.data.copy()
    obj.data = me
    bm = bmesh.new()
    bm.from_mesh(me)
    up = [f for f in bm.faces if f.calc_center_median().z > zb]
    if not up:
        bm.free()
        return None
    top = bm.copy()
    bmesh.ops.delete(top, geom=[f for f in top.faces if f.calc_center_median().z <= zb], context="FACES")
    bmesh.ops.delete(bm, geom=up, context="FACES")
    bm.to_mesh(me)
    bm.free()
    me2 = bpy.data.meshes.new(me.name + "_roof")
    top.to_mesh(me2)
    top.free()
    for mat in me.materials:
        me2.materials.append(mat)
    for p in me2.polygons:
        p.use_smooth = True
    o2 = bpy.data.objects.new(obj.name + "_roof", me2)
    bpy.context.scene.collection.objects.link(o2)
    o2.parent = obj.parent
    o2.matrix_parent_inverse = obj.matrix_parent_inverse.copy()
    o2.location, o2.rotation_euler, o2.scale = obj.location.copy(), obj.rotation_euler.copy(), obj.scale.copy()
    for src in obj.modifiers:                              # the asset is modelled as one half plus a Mirror: the roof half needs the same modifiers
        dst = o2.modifiers.new(src.name, src.type)
        for prop in src.bl_rna.properties:
            if not prop.is_readonly:
                setattr(dst, prop.identifier, getattr(src, prop.identifier))
    return o2


def car(S, m, name="car", loc=(0.0, 0.0, 0.0), roof=True, driver=True, rot_z=-math.pi / 2):
    """The sealed cartoon car standing on z = 0, nose toward -x. ns.root, ns.objs, ns.roof (object list, split from the body when roof is needed), ns.wheels, ns.driver (root or None)."""
    ns = type("Car", (), {})()
    root, objs = av.place("cartoon-car", None, K, loc=(loc[0], loc[1], loc[2] + 0.034 * K), rot=(0, 0, rot_z))        # wheels' lowest point is 0.034 m below the root
    ns.root, ns.objs = root, objs
    ns.wheels = [o for o in objs if "wheel" in o.name and o.type == "MESH"]
    ns.roof = []
    if roof:
        for o in list(objs):
            if o.type == "MESH" and any(k in o.name for k in ("chasis", "front_door", "back_door", "door.001")):
                r = split_roof(o)
                if r is not None:
                    ns.roof.append(r)
                    objs.append(r)
    for j, o in enumerate(objs):
        o.name = f"car_{name}_{j}"
    ns.driver = None
    if driver:
        droot, dobjs = av.place("human-figure", None, 0.85 * K, loc=(loc[0] + 1.0, loc[1] - 2.6, loc[2] + 5.4), rot=(0, 0, -math.pi / 2))
        av.pose_armature(next(o for o in dobjs if o.type == "ARMATURE"), "pose_seated")
        av.tint_figure(dobjs, DRIVER)
        for j, o in enumerate(dobjs):
            o.name = f"car_{name}_driver_{j}"
        ns.driver = droot
    return ns


def set_roof(ns, k, lift=22.0, back=18.0):
    """k 0 -> 1: the roof group rises and slides back; fully gone at k = 1 (hidden)."""
    for o in ns.roof:                                     # children of the car root (root space = scene units; the car's tail is +y there, up is +z)
        o.hide_render = k >= 0.999
        o.hide_viewport = k >= 0.999
        o.delta_location = (0.0, back * ease(k), lift * ease(k))


# ------------------------------------------------------------------ bolts and arcs
def zig(p0, p1, n, amp, seed):
    rnd = random.Random(seed)
    pts = []
    for i in range(n + 1):
        k = i / n
        p = [a + (b - a) * k for a, b in zip(p0, p1)]
        if 0 < i < n:
            p[0] += rnd.uniform(-amp, amp)
            p[1] += rnd.uniform(-amp, amp) * 0.4
        pts.append(tuple(p))
    return pts


def bolt(S, name, p0, p1, mat, t0, t1, r=0.8, n=9, amp=6.0, seed=1, branches=3, t_off=None):
    """A branching bolt from p0 down to p1 drawn between t0 and t1 (tube radius r). Object names start with `name` (use "bolt_" or "arc_" so the visibility check finds them);
    t_off hides it again at that time. Returns the list of line objects."""
    main = zig(p0, p1, n, amp, seed)
    objs = [S.line(f"{name}_main", main, r, mat, grow=(t0, t1), smooth=False)]
    rnd = random.Random(seed + 50)
    for b in range(branches):
        i = rnd.randint(2, max(2, n - 3))
        sx, sy, sz = main[i]
        span = abs(p1[2] - p0[2]) or 1.0
        end = (sx + rnd.choice((-1, 1)) * rnd.uniform(0.15, 0.3) * span, sy + rnd.uniform(-0.06, 0.06) * span, sz - rnd.uniform(0.12, 0.25) * span)
        ts = t0 + (t1 - t0) * i / n
        objs.append(S.line(f"{name}_br{b}", zig((sx, sy, sz), end, 4, amp * 0.5, seed + b + 7), r * 0.6, mat, grow=(ts, ts + 0.25), smooth=False))
    if t_off is not None:
        def hide(t, objs=objs):
            off = t >= t_off
            for o in objs:
                o.hide_render = off
                o.hide_viewport = off
        S.every_frame(hide)
    return objs


# ------------------------------------------------------------------ the cage
ROOF_TOP, BELT, SILL = 19.3, 10.9, 2.7           # roof, window sill and body bottom heights in scene units (car on z = 0)
CW = 9.0                                           # half the cage width (measured: the body box spans y -9.8..9.3, the wheels sit at y +-8)
CAGE_EDGES = []
for _y in (-CW, CW):
    # lower body rectangle and cabin rectangle (x along the car), both sides; the greenhouse measured x -9.2..15, roof top 18.9
    CAGE_EDGES += [((-21.0, _y, SILL), (22.0, _y, SILL)), ((-21.0, _y, BELT), (22.0, _y, BELT)), ((-21.0, _y, SILL), (-21.0, _y, BELT)), ((22.0, _y, SILL), (22.0, _y, BELT)),
                   ((-9.2, _y, BELT), (-5.5, _y, ROOF_TOP)), ((15.0, _y, BELT), (11.5, _y, ROOF_TOP)), ((-5.5, _y, ROOF_TOP), (11.5, _y, ROOF_TOP)), ((3.0, _y, BELT), (3.0, _y, ROOF_TOP))]
CAGE_EDGES += [((-5.5, -CW, ROOF_TOP), (-5.5, CW, ROOF_TOP)), ((11.5, -CW, ROOF_TOP), (11.5, CW, ROOF_TOP)),
               ((-21.0, -CW, SILL), (-21.0, CW, SILL)), ((22.0, -CW, SILL), (22.0, CW, SILL))]


def cage(S, mat, t0, dt=0.9, r=0.28, name="cage"):
    """Accent bars along the shell's edges, drawn in one after the other starting at t0 over dt seconds."""
    objs = []
    n = len(CAGE_EDGES)
    for i, (a, b) in enumerate(CAGE_EDGES):
        ts = t0 + dt * i / n
        objs.append(S.line(f"{name}_{i}", [a, b], r, mat, grow=(ts, ts + 0.25), smooth=False))
    return objs
