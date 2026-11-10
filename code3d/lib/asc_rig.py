"""Rig of production 017 (what if an elevator cable is cut): the shaft with rails, landings and a governor wheel in the pit, the car (closed or cut away), its steel ropes
(each one cut on its own cue), the safety wedges on the rails, the pit buffer and a phone. Rigid, genuinely geometric parts: code primitives. Runs inside Blender.
Scene units are centimetres of a toy scale (the car is 26 wide); x right, y away from the camera, z up. Moving things are driven per frame by the scene script."""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

CAB_W, CAB_D, CAB_H = 26.0, 22.0, 34.0
RAIL_X = 15.6
LANDING = 42.0
SHAFT_HALF = 36.0
GOV_R = 8.5
ROPE_R = 0.7
CUT_LEN = 9.0                                  # length of rope left hanging on the car roof when a rope is cut
ROOF_ABOVE = CAB_H + 4.0                        # roof frame top above the car base
LIGHT_K = 3.0

CABIN, DOORS, RAILS, ROPE, PHONE = "#E3E0DC", "#B9BEC4", "#C9CED4", "#D5D8DC", "#2D2A2B"
SLATE = "#3B4553"
INK = "#1D1B2E"


def ease(k):
    k = min(1.0, max(0.0, k))
    return k * k * (3 - 2 * k)


def fall_z(t, t0, z0, g, floor=0.0):
    """Base height of a car released at t0 from z0, falling under g, stopping at `floor`."""
    if t <= t0:
        return z0
    return max(floor, z0 - 0.5 * g * (t - t0) ** 2)


def fall_v(t, t0, g, z0=None, floor=0.0):
    if t <= t0:
        return 0.0
    v = g * (t - t0)
    if z0 is not None and z0 - 0.5 * g * (t - t0) ** 2 <= floor:
        return 0.0
    return v


class Mats:
    """Materials by gate role. Hero colours come from scenes.json hero_colours (the module constants are only the fallbacks); the shaft wall and the landings take the production's support colours."""

    def __init__(self, S):
        hc = (S.p or {}).get("hero") or {}
        self.cabin = S.hero("housing", hc.get("cabin", CABIN), rough=0.4, coat=0.2)
        self.doors = S.hero("big", hc.get("doors", DOORS), rough=0.35, metal=0.15)
        self.rails = S.hero("small", hc.get("rails", RAILS), rough=0.4, metal=0.0)
        self.rope = S.hero("blade", hc.get("rope", ROPE), rough=0.4, metal=0.0)
        self.plate = S.plate_mat(rough=0.7)
        self.ink = S.ink
        self.dark = S.ink                                      # dark parts (phone screen, weights, coils) are ink: same class as the plinth, never a second dark hero colour
        self.board = S.board_mat()
        self.accent = S.accent


def lights(S):
    """The stage lights ride with the subject: the shaft is tall and the lights are fixed. Returns f(dz) to raise them."""
    ls = [S.stage.key, S.stage.rim, S.stage.fill]
    for x in ls:                                                       # the stage lights are placed for a hero a few cm across; the shaft is 70 wide and 15 deep, so back them off
        if x.data.type != "SUN":                                       # (same direction, energy by the square of the distance, size with it) or the car blows out and the wall goes black
            x.location = tuple(LIGHT_K * v for v in x.location)
            x.data.energy *= LIGHT_K ** 2
            if hasattr(x.data, "size"):
                x.data.size *= LIGHT_K
    base = [tuple(x.location) for x in ls]

    def f(dz):
        for x, b in zip(ls, base):
            x.location = (b[0], b[1], b[2] + dz)
    return f


def look(S, target, radius, el, az):
    tr.look(S.stage, target, radius, el, az)


# ------------------------------------------------------------------ shaft
def shaft(S, H, m=None):
    """Back wall, landings with doors, two guide rails, the pit slab, the top beam and the sheave."""
    m = m or Mats(S)
    ns = type("Shaft", (), {})()
    ns.H, ns.m = H, m
    tr.rbox("shaft_back", (2 * SHAFT_HALF, 1.2, H + 20), (0, 16.0, H / 2 + 5), m.plate, bevel=0.2)
    for k in range(1, int(H / LANDING) + 1):
        z = k * LANDING
        tr.rbox(f"landing_{k}", (2 * SHAFT_HALF, 3.0, 1.6), (0, 14.6, z), m.ink, bevel=0.3)
        for s in (-1, 1):
            tr.rbox(f"landdoor_{k}_{s}", (10.0, 0.8, 30.0), (s * 5.6, 14.9, z + 16.5), m.board, bevel=0.3)
    for s in (-1, 1):
        tr.rbox(f"rail_{s}", (2.4, 3.0, H + 10), (s * RAIL_X, 0.0, H / 2 + 5 - 5), m.rails, bevel=0.3)
    tr.rbox("pit", (2 * SHAFT_HALF + 8, 40.0, 4.0), (0, 4.0, -2.0), m.ink, bevel=0.4)
    tr.rbox("top_beam", (2 * SHAFT_HALF, 9.0, 6.0), (0, 4.0, H + 3.0), m.ink, bevel=0.5)
    tr.cyl("sheave", 8.0, 4.0, (0, 0.0, H - 5.0), m.rails, axis="Y", verts=40)
    return ns


def governor_wheel(m, cab, name="gov"):
    """The car-mounted overspeed governor: a spoked wheel that rolls on the outer face of the right rail, on a bracket from the car side, with two fly-weights on arms.
    gov_set(g, angle, open_k) turns it and swings the weights out as the car speeds up."""
    cx = RAIL_X + 1.2 + GOV_R
    root = tr.empty(f"{name}_root", (cx, -4.0, 12.0), parent=cab.root)
    spin = tr.empty(f"{name}_spin", (0, 0, 0), parent=root)
    tr.cyl(f"{name}_rim", GOV_R, 2.2, (0, 0, 0), m.doors, axis="Y", parent=spin, verts=40, bevel=0.3)
    tr.cyl(f"{name}_hub", 2.6, 3.0, (0, -1.2, 0), m.rails, axis="Y", parent=spin, verts=24)
    for k in range(2):
        tr.rbox(f"{name}_arm{k}", (2 * GOV_R - 2.0, 1.0, 1.2), (0, -1.6, 0), m.ink, bevel=0.3, parent=spin, rot=(0, k * math.pi / 2 + math.pi / 4, 0))
    weights = []
    for k in range(2):
        w = tr.empty(f"{name}_w{k}", (0, 0, 0), parent=spin)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.9, location=(0, 0, 0), segments=24, ring_count=14)
        o = bpy.context.object
        o.name = f"{name}_weight{k}"
        tr._finish(o, m.dark)
        o.parent = w
        weights.append(w)
    tr.rbox(f"{name}_bracket", (cx - CAB_W / 2 + 0.5, 1.2, 1.6), ((cx + CAB_W / 2 - 0.5) / 2, -4.0, 12.0), m.ink, bevel=0.3, parent=cab.root)
    return type("Gov", (), {"spin": spin, "weights": weights})()


def gov_set(g, angle, open_k):
    if g is None:                                                      # the governor wheel failed blind naming (safe / valve wheel): off screen
        return
    g.spin.rotation_euler = (0.0, angle, 0.0)
    for k, w in enumerate(g.weights):
        r = 3.0 + 3.8 * open_k
        a = k * math.pi + math.pi / 4
        w.location = (r * math.cos(a), -2.6, r * math.sin(a))


# ------------------------------------------------------------------ the car
class Cab:
    """The car. `root` carries it (set `root.location.z` each frame); parts are children. open_front cuts the front away to show the inside (scene 4)."""

    def __init__(self, S, m, z0, open_front=False, name="cab", governor=False):
        self.m, self.z0 = m, z0
        self.root = tr.empty(f"{name}_root", (0, 0, z0))
        r = self.root
        if open_front:
            tr.rbox(f"{name}_floor", (CAB_W, CAB_D, 1.8), (0, 0, 0.9), m.cabin, bevel=0.3, parent=r)
            tr.rbox(f"{name}_back", (CAB_W, 1.2, CAB_H), (0, CAB_D / 2 - 0.6, CAB_H / 2), m.cabin, bevel=0.3, parent=r)
            for s in (-1, 1):
                tr.rbox(f"{name}_side{s}", (1.2, CAB_D, CAB_H), (s * (CAB_W / 2 - 0.6), 0, CAB_H / 2), m.doors, bevel=0.3, parent=r)
            tr.rbox(f"{name}_ceiling", (CAB_W, CAB_D, 1.4), (0, 0, CAB_H - 0.7), m.cabin, bevel=0.3, parent=r)
            tr.rbox(f"{name}_handrail", (CAB_W - 4, 1.0, 1.0), (0, CAB_D / 2 - 2.6, 14.0), m.rails, bevel=0.3, parent=r)
            for s in (-1, 1):
                tr.rbox(f"{name}_post{s}", (2.6, 1.6, CAB_H), (s * (CAB_W / 2 - 1.3), -CAB_D / 2 + 0.8, CAB_H / 2), m.doors, bevel=0.3, parent=r)
            tr.rbox(f"{name}_header", (CAB_W, 1.6, 4.0), (0, -CAB_D / 2 + 0.8, CAB_H - 2.0), m.doors, bevel=0.3, parent=r)
            ld = bpy.data.lights.new(f"{name}_lamp", "POINT")             # the cut-away's inside sits in the car's own shadow: a lamp in the ceiling lights the car from within
            ld.energy, ld.shadow_soft_size = 4000.0, 6.0
            lamp = bpy.data.objects.new(f"{name}_lamp", ld)
            bpy.context.scene.collection.objects.link(lamp)
            lamp.parent = r
            lamp.location = (0.0, -6.0, CAB_H - 5.0)
        else:
            tr.rbox(f"{name}_body", (CAB_W, CAB_D, CAB_H), (0, 0, CAB_H / 2), m.cabin, bevel=0.5, parent=r)
            for s in (-1, 1):
                tr.rbox(f"{name}_door{s}", (CAB_W / 2 - 3.2, 0.8, CAB_H - 8.5), (s * (CAB_W / 4 - 1.0), -CAB_D / 2 - 0.2, (CAB_H - 8.5) / 2 + 1.5), m.doors, bevel=0.3, parent=r)
            tr.rbox(f"{name}_display", (8.0, 0.6, 3.0), (0, -CAB_D / 2 - 0.1, CAB_H - 3.6), m.ink, bevel=0.3, parent=r)
            tr.rbox(f"{name}_panel", (2.6, 0.6, 11.0), (CAB_W / 2 - 1.6, -CAB_D / 2 - 0.1, 17.0), m.ink, bevel=0.3, parent=r)
            for k in range(3):
                tr.cyl(f"{name}_btn{k}", 0.55, 0.4, (CAB_W / 2 - 1.6, -CAB_D / 2 - 0.5, 20.0 - k * 3.2), m.doors, axis="Y", parent=r, verts=16)
        tr.rbox(f"{name}_crosshead", (CAB_W + 3, 6.0, 3.0), (0, 0, CAB_H + 1.5), m.ink, bevel=0.4, parent=r)
        for s in (-1, 1):
            for zz in (4.0, CAB_H - 4.0):
                tr.rbox(f"{name}_shoe{s}_{int(zz)}", (3.6, 5.4, 5.0), (s * (RAIL_X - 0.4), 0, zz), m.ink, bevel=0.4, parent=r)
        self.gear = safety_gear(self, m, name)
        self.m = m
        self.gov = governor_wheel(m, self, f"{name}_gov") if governor else None

    def set_z(self, z):
        self.root.location = (0, 0, z)


def safety_gear(cab, m, name):
    """The grip on the rails (rung 2 of the 017 reshape: the clamp hardware failed blind naming in seven readings, so it stays off screen). Per rail one accent sleeve that
    hugs the guide rail under the car when the car is gripped: the rail itself lights up in the accent (the active quantity). gear_set(k): 0 = nothing, 1 = gripped."""
    glows = []
    for s in (-1, 1):
        g = tr.rbox(f"grip_{s}", (3.6, 4.2, 18.0), (s * RAIL_X, 0.0, -2.0), m.accent, bevel=0.5, parent=cab.root)
        g.scale = (1.0, 1.0, 1e-3)
        glows.append(g)
    cab.gear_parts = glows
    return []


def gear_set(cab, k):
    """k 0 -> 1: the accent sleeves grow along the rails around the car's base (the car is held by its rails)."""
    k = ease(k)
    for g in cab.gear_parts:
        g.scale = (1.0, 1.0, max(1e-3, k))


# ------------------------------------------------------------------ ropes
class Ropes:
    """n parallel steel ropes from the car roof to the top beam, each in two parts: the upper one (world) and the stub on the roof (child of the car), so a cut leaves
    the car carrying its stub while the upper part recoils. xs: x positions; roof0: roof height while hanging; ztop: where the ropes end."""

    def __init__(self, S, cab, m, xs, roof0, ztop):
        self.cab, self.n, self.roof0, self.ztop = cab, len(xs), roof0, ztop
        self.upper, self.stub = [], []
        zc = roof0 + CUT_LEN
        for i, x in enumerate(xs):
            top = tr.empty(f"rope_top{i}", (x, 0.0, ztop))
            L = ztop - zc
            u = tr.cyl(f"rope_up{i}", ROPE_R, L, (0, 0, -L / 2), m.rope, axis="Z", parent=top, verts=10)
            st = tr.cyl(f"rope_stub{i}", ROPE_R, CUT_LEN + 1.0, (x, 0.0, ROOF_ABOVE - 1.0 + (CUT_LEN + 1.0) / 2), m.rope, axis="Z", parent=cab.root, verts=10)
            self.upper.append(top)
            self.stub.append(st)

    def set(self, t, appear=None, cut=None, show_from=0):
        """appear[i]: time rope i starts to grow in (None = present); cut[i]: time rope i is cut (None = never)."""
        for i in range(self.n):
            a = 1.0 if (appear is None or appear[i] is None) else ease((t - appear[i]) / 0.35)
            a = max(a, 1e-3)
            tc = None if cut is None else cut[i]
            up, st = self.upper[i], self.stub[i]
            rec = 0.0 if tc is None or t < tc else ease((t - tc) / 0.22)
            up.scale = (a, a, max(1e-3, 1.0 - 0.6 * rec))
            st.scale = (a, a, 1.0)
            sway = 0.0 if tc is None or t < tc else 0.25 * math.exp(-4.0 * (t - tc)) * math.sin(18.0 * (t - tc)) * (1 if i % 2 else -1)
            st.rotation_euler = (0.0, sway, 0.0)


# ------------------------------------------------------------------ buffer
class Buffer:
    """The pit buffer: sleeve, rod and cap plate. set(s): s = how far the rod has sunk into the sleeve (0..STROKE)."""
    STROKE = 24.0
    SLEEVE_H = 30.0
    ROD_H = 30.0

    def __init__(self, S, m, x=0.0, y=0.0):
        self.x, self.y = x, y
        tr.cyl("buf_base", 9.0, 2.0, (x, y, 1.0), m.ink, axis="Z", verts=32, bevel=0.3)
        tr.cyl("buf_sleeve", 6.0, self.SLEEVE_H, (x, y, 2.0 + self.SLEEVE_H / 2), m.doors, axis="Z", verts=32, bevel=0.3)
        self.rod = tr.cyl("buf_rod", 3.6, self.ROD_H, (x, y, 0), m.rails, axis="Z", verts=24)
        self.cap = tr.cyl("buf_cap", 9.5, 2.0, (x, y, 0), m.accent, axis="Z", verts=32, bevel=0.3)
        self.coils = []
        for k in range(8):                                                   # a coil spring around the rod: eight rings squeezed together as the rod sinks
            bpy.ops.mesh.primitive_torus_add(major_radius=7.4, minor_radius=1.0, major_segments=40, minor_segments=12, location=(x, y, 0))
            o = bpy.context.object
            o.name = f"buf_coil{k}"
            tr._finish(o, m.dark)
            self.coils.append(o)
        self.set(0.0)

    @property
    def top0(self):
        return 2.0 + self.SLEEVE_H + self.ROD_H + 2.0          # cap top height at rest

    def set(self, s):
        zt = 2.0 + self.SLEEVE_H + self.ROD_H - s
        self.rod.location = (self.x, self.y, zt - self.ROD_H / 2)
        self.cap.location = (self.x, self.y, zt + 1.0)
        lo, hi = 2.0 + self.SLEEVE_H + 1.5, zt - 0.5
        for k, o in enumerate(self.coils):
            o.location = (self.x, self.y, lo + (hi - lo) * k / (len(self.coils) - 1))


# ------------------------------------------------------------------ phone
def phone(S, m, parent=None, name="phone"):
    """A chunky phone slab (exaggerated: the car is 26 wide, the phone 7.5): bezel, dark screen, camera dot. Returns the root empty."""
    r = tr.empty(f"{name}_root", (0, 0, 0))
    tr.rbox(f"{name}_body", (7.6, 1.2, 14.0), (0, 0, 0), m.doors, bevel=0.7, parent=r)
    tr.rbox(f"{name}_screen", (6.4, 0.3, 12.0), (0, -0.62, -0.2), m.dark, bevel=0.4, parent=r)
    tr.cyl(f"{name}_cam", 0.5, 0.3, (0, -0.7, 5.8), m.cabin, axis="Y", verts=16, parent=r)
    return r
