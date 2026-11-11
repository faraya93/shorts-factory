"""Rig of production 019 (why nobody can open an airplane door in flight): a curved fuselage section with oval windows, a plug door and its handle, the top-down plug cutaway,
the cabin cut-away with seat rows and seated figures, the accent air, a door laid flat for the cars, and a whole airliner with a door-plug panel. Rigid, geometric parts: code
primitives; the hand, the figures and the cars are sealed library assets placed through asset_rig. Runs inside Blender.
Scene units are centimetres of a toy scale (the fuselage section is 80 across); x right (the fuselage axis), y away from the camera, z up. Driven per frame by the scene script."""
import math
import random
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_rig as ar  # noqa: E402
import common as c  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

R = 40.0                                   # fuselage section radius
SEC_L = 60.0                               # section length along x
FLOOR_Z = -14.0                            # cabin floor height (axis at z = 0)
DOOR_W, DOOR_H, DOOR_T = 20.0, 34.0, 3.2
DOOR_Z0, DOOR_Z1 = FLOOR_Z, FLOOR_Z + DOOR_H
WIN_Z, WIN_W, WIN_H = 14.0, 5.0, 11.0
LIGHT_K = 2.5

SKIN, DOOR, PANE_G, PANE_S, SEAT, PANEL = "#ECEAE6", "#C9CED4", "#F4E6BE", "#28477F", "#51555A", "#D8DBDF"
INK = "#1D1B2E"
CLOUD = "#F6F2EE"
FIG = {  # per passenger: skin, shirt, pants, boots (wardrobe of the notes)
    0: ("#D99E7A", "#2973CC", "#2E3347", "#59331A"), 1: ("#8D5A3B", "#C8553D", "#3B4A3A", "#2A2A2A"),
    2: ("#F0C8A8", "#E8B931", "#5A5F6B", "#6B4A2B"), 3: ("#B07A55", "#3E8E6E", "#22252E", "#4A2E1C")}


def ease(k):
    k = min(1.0, max(0.0, k))
    return k * k * (3 - 2 * k)


class Mats:
    """Hero colours come from scenes.json hero_colours (module constants are the fallbacks); the plate and board take the production's support colours."""

    def __init__(self, S):
        hc = (S.p or {}).get("hero") or {}
        self.skin = S.hero("housing", hc.get("skin", SKIN), rough=0.45, coat=0.15)
        self.door = S.hero("big", hc.get("door", DOOR), rough=0.35, metal=0.15)
        self.seat = S.hero("small", hc.get("seat", SEAT), rough=0.55)
        self.panel = S.hero("blade", hc.get("panel", PANEL), rough=0.4)
        self.pane_g = tr.plain("pane_ground", hc.get("pane_ground", PANE_G), rough=0.3)
        self.pane_s = tr.plain("pane_sky", hc.get("pane_sky", PANE_S), rough=0.3)
        self.cloud = tr.plain("cloud_white", CLOUD, rough=0.9)
        self.plate = S.plate_mat(rough=0.7)
        self.board = S.board_mat()
        self.ink = S.ink
        self.accent = S.accent
        self.red = S.error


def lights(S, k=LIGHT_K):
    """Back the stage lights off for a set 100+ cm across (same direction, energy by the square of the distance, size with it). Returns f(dx, dz) that moves them with the subject."""
    ls = [S.stage.key, S.stage.rim, S.stage.fill]
    for x in ls:
        if x.data.type != "SUN":
            x.location = tuple(k * v for v in x.location)
            x.data.energy *= k ** 2
            if hasattr(x.data, "size"):
                x.data.size *= k
    base = [tuple(x.location) for x in ls]

    def f(dx=0.0, dz=0.0):
        for x, b in zip(ls, base):
            x.location = (b[0] + dx, b[1], b[2] + dz)
    return f


def look(S, target, radius, el, az):
    tr.look(S.stage, target, radius, el, az)


# ------------------------------------------------------------------ geometry helpers
def grid_surface(name, nx, na, pos, mat, thick=1.2, flip=False, parent=None):
    """A smooth open surface from pos(i, j) (i along the axis, j around), solidified inward by `thick`."""
    verts = [pos(i, j) for i in range(nx) for j in range(na + 1)]
    faces = [(i * (na + 1) + j, i * (na + 1) + j + 1, (i + 1) * (na + 1) + j + 1, (i + 1) * (na + 1) + j) for i in range(nx - 1) for j in range(na)]
    if flip:
        faces = [f[::-1] for f in faces]
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts, [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat)
    if thick:
        m = o.modifiers.new("solid", "SOLIDIFY")
        m.thickness, m.offset, m.use_even_offset = thick, -1.0, True
    if parent:
        o.parent = parent
    return o


def tube(name, x0, x1, radius, a0, a1, mat, parent=None, thick=1.2, nx=2, na=96, flip=False):
    """Fuselage skin: axis along x, angle a (0 = the camera side, -y; pi/2 = top). radius is a number or f(x)."""
    rf = radius if callable(radius) else (lambda x: radius)

    def pos(i, j):
        x = x0 + (x1 - x0) * i / (nx - 1)
        a = a0 + (a1 - a0) * j / na
        r = rf(x)
        return (x, -r * math.cos(a), r * math.sin(a))
    return grid_surface(name, nx, na, pos, mat, thick=thick, flip=flip, parent=parent)


def oval(name, x, a, r, w, h, mat, parent, lift=1.6):
    """An oval window pane on the skin at axial position x, angle a (a flat ellipse standing proud of the skin, facing the axis)."""
    o = tr.cyl(name, 0.5, 0.5, (x, -(r + lift) * math.cos(a), (r + lift) * math.sin(a)), mat, axis="Y", parent=parent, verts=32)
    o.scale = (w, h, 1.0)                                  # tr.cyl(axis="Y") turns the disc to face y; local y becomes the height
    o.rotation_euler = (math.pi / 2 - a, 0, 0)
    return o


# ------------------------------------------------------------------ the fuselage section with its door (scenes 1 and 6)
class Section:
    """A full fuselage ring segment with four oval windows per side beside a plug door on the camera side, a handle on the door.
    root carries it; hinge is the door pivot (rotation z swings it outward); window panes are `pane` ("ground" or "sky")."""

    def __init__(self, S, m, pane="sky", name="sec", loc=(0, 0, 0)):
        self.m, self.name = m, name
        self.root = tr.empty(f"{name}_root", loc)
        r = self.root
        pm = m.pane_s if pane == "sky" else m.pane_g
        tube(f"{name}_skin", -SEC_L / 2, SEC_L / 2, R, math.pi, 3 * math.pi, m.skin, parent=r, nx=2, na=120)          # the seam sits at the back
        for k, x in enumerate((-24.0, -16.0, 16.0, 24.0)):
            oval(f"{name}_win{k}", x, 0.0 + math.asin(WIN_Z / R), R, WIN_W, WIN_H, pm, r)
        tr.rbox(f"{name}_opening", (DOOR_W + 2.4, 1.6, DOOR_H + 2.4), (0, -R - 0.1, (DOOR_Z0 + DOOR_Z1) / 2), m.ink, bevel=0.4, parent=r)
        self.hinge = tr.empty(f"{name}_hinge", (-DOOR_W / 2, -R - 0.7, 0.0), parent=r)
        zc = (DOOR_Z0 + DOOR_Z1) / 2
        tr.rbox(f"door_{name}_slab", (DOOR_W, DOOR_T, DOOR_H), (DOOR_W / 2, 0, zc), m.door, bevel=0.7, parent=self.hinge)
        tr.rbox(f"door_{name}_porthole", (4.6, 0.6, 5.6), (DOOR_W / 2, -DOOR_T / 2 - 0.1, zc + 11.0), m.pane_s if pane == "sky" else m.pane_g, bevel=0.6, parent=self.hinge)
        self.handle_loc = (DOOR_W / 2 + 4.0, -DOOR_T / 2 - 1.6, zc + 1.0)             # in hinge space
        tr.rbox(f"door_{name}_plate", (7.0, 0.8, 9.0), (self.handle_loc[0], -DOOR_T / 2 - 0.2, self.handle_loc[2]), m.ink, bevel=0.4, parent=self.hinge)
        tr.cyl(f"door_{name}_bar", 0.9, 8.0, (self.handle_loc[0], self.handle_loc[1] - 0.3, self.handle_loc[2]), m.ink, axis="X", parent=self.hinge, verts=20)     # the grip bar runs along x (the sealed hand's lever pose wraps an x-axis bar)
        for dx in (-3.6, 3.6):
            tr.cyl(f"door_{name}_post{dx}", 0.6, 1.8, (self.handle_loc[0] + dx, -DOOR_T / 2 - 0.9, self.handle_loc[2]), m.ink, axis="Y", parent=self.hinge, verts=12)


def door_swing(sec, k):
    """k 0 -> 1: the door swings outward about its hinge."""
    sec.hinge.rotation_euler = (0.0, 0.0, -ease(k) * math.radians(78))


# ------------------------------------------------------------------ the hand on the handle (sealed hand-articulated, pose lever)
def pose_armature(arm, action):
    arm.animation_data_create()
    arm.animation_data.action = bpy.data.actions[action]
    bpy.context.view_layer.update()


def place(slug, parent, k, loc=(0, 0, 0), rot=(0, 0, 0)):
    """Load a sealed asset into a root empty (armature scaled by k, its meshes stay its children)."""
    col = ar.al.load_hero(slug)
    root = tr.empty(f"{slug}_root", loc, parent=parent)
    root.rotation_euler = rot
    objs = list(col.objects)
    for o in objs:
        if o.parent is None:
            o.parent = root
            o.scale = tuple(x * k for x in o.scale)
            o.location = tuple(x * k for x in o.location)
    return root, objs


def hand(S, sec, loc_off=(0.0, -3.6, 0.74), rot=(0, 0, math.pi), k=62.0):
    """The sealed hand in its lever pose, wrapped over the grip bar from the camera side (fingers point down, palm toward the door); child of the hinge, so it rides the door."""
    root, objs = place("hand-articulated", sec.hinge, k, loc=tuple(a + b for a, b in zip(sec.handle_loc, loc_off)), rot=rot)
    arm = next(o for o in objs if o.type == "ARMATURE")
    pose_armature(arm, "pose_lever")
    return root, objs


# ------------------------------------------------------------------ top-down plug cutaway (scene 2)
class Plug:
    """A horizontal cut through the door: straight wall with a 20 wide opening, the frame stops inboard of it, the door slab (28 wide, pressed outward against the stops)
    and the cabin context (two seats, oval window gaps). y > 0 is inboard, y < 0 outside."""
    GAP = 20.0
    DW = 28.0

    def __init__(self, S, m):
        self.m = m
        g = self.GAP / 2
        tr.rbox("pc_plate", (170, 130, 1.0), (0, 8, -3.0), m.plate, bevel=0.3)
        tr.rbox("pc_floor", (150, 40, 1.2), (0, 20, -1.0), m.panel, bevel=0.3)                         # the cabin floor inboard of the wall
        for s in (-1, 1):
            tr.rbox(f"pc_wall{s}_a", (22, 3.0, 26), (s * (g + 11), 0, 10.0), m.skin, bevel=0.3)
            tr.rbox(f"pc_wall{s}_b", (20, 3.0, 26), (s * (g + 22 + 6 + 10), 0, 10.0), m.skin, bevel=0.3)
            tr.rbox(f"pc_win{s}", (6.0, 3.2, 10), (s * (g + 25), 0, 14.0), m.pane_s, bevel=1.2)
            window_view(m, s * (g + 25), 1.4, 14.0, 3 if s < 0 else 1)
            tr.rbox(f"pc_bin{s}", (38, 9.0, 6.0), (s * (g + 36), 5.5, 24.0), m.panel, bevel=2.0)         # overhead luggage bins beside the door
            tr.rbox(f"pc_stop{s}", (4.5, 1.6, 26), (s * (g - 2.2), 2.3, 10.0), m.accent, bevel=0.3)       # frame stops, inboard of the wall
            tr.rbox(f"pc_seat{s}_base", (14, 8, 4), (s * 40, 16, 1.0), m.seat, bevel=0.6)
            tr.rbox(f"pc_seat{s}_back", (14, 2.4, 14), (s * 40, 20.5, 7.0), m.seat, bevel=0.8)
        self.root = tr.empty("pc_door_root", (0, 5.0, 10.0))
        tr.rbox("pc_door_slab", (self.DW, 2.8, 26), (0, 0, 0), m.door, bevel=0.5, parent=self.root)
        tr.rbox("pc_door_porthole", (3.6, 0.6, 7.0), (7.0, 1.5, 6.0), m.pane_s, bevel=1.4, parent=self.root)
        tr.rbox("pc_door_handle", (1.6, 1.2, 9.0), (-8.0, 2.0, -1.0), m.ink, bevel=0.5, parent=self.root)

    def set(self, t, t_in, t_turn, t_out, t_end):
        """Slides inboard, turns 90 degrees, then goes out through the opening."""
        k_in, k_turn, k_out = ease((t - t_in) / 1.0), ease((t - t_turn) / 0.7), ease((t - t_out) / (t_end - t_out))
        y = 5.0 + 11.0 * k_in - 41.0 * k_out
        self.root.location = (0.0, y, 10.0)
        self.root.rotation_euler = (0.0, 0.0, k_turn * math.radians(90))


def window_view(m, x, y, z, k):
    """What the oval windows show: sky with a cloud, and a grey wing in every third window (the airplane cue). Drawn just inboard of the pane, facing the camera (inboard)."""
    tr.rbox(f"cab_cloud{k}_{int(x)}", (3.6, 0.4, 2.2), (x + 0.6, y - 0.4, z - 1.2), m.cloud, bevel=0.9)
    if k % 3 == 0:
        tr.rbox(f"cab_wing{k}_{int(x)}", (3.8, 0.4, 1.0), (x - 0.4, y - 0.4, z + 2.4), m.door, bevel=0.3, rot=(0, 0.25, 0))


# ------------------------------------------------------------------ the cabin cut-away (scene 3)
def cabin(S, m, length=96.0, passengers=True):
    """Back half of the fuselage ring (a cut-away facing the camera): curved ceiling, back wall with oval windows (sky), floor, four seat rows facing +x with a figure each."""
    ns = type("Cabin", (), {})()
    a_floor = math.pi + math.asin(-FLOOR_Z / R)
    tube("cab_skin", -length / 2, length / 2, R, math.pi / 2, a_floor, m.skin, nx=2, na=60)
    for k in range(6):
        x = -40.0 + k * 16.0
        oval(f"cab_win{k}", x, math.pi - math.asin(WIN_Z / R), R, WIN_W, WIN_H, m.pane_s, None, lift=-0.9)
        window_view(m, x, 36.0, WIN_Z, k)
    tr.rbox("cab_bins", (length - 4.0, 9.0, 6.0), (0, 27.0, 25.0), m.panel, bevel=2.0)                     # overhead luggage bins
    for k in range(7):
        tr.rbox(f"cab_bin_door{k}", (length / 7 - 1.0, 0.6, 4.4), (-length / 2 + 2 + k * length / 7 + length / 14, 22.4, 25.0), m.skin, bevel=0.5)
    tr.rbox("cab_floor", (length, 2 * R * 0.0 + 70.0, 1.6), (0, 0, FLOOR_Z - 0.8), m.panel, bevel=0.3)
    tr.rbox("cab_aisle", (length - 4, 6.0, 0.4), (0, -6.0, FLOOR_Z + 0.1), m.ink, bevel=0.1)
    ns.figs = []
    for i in range(4):
        x = -36.0 + i * 24.0
        tr.rbox(f"seat_{i}_base", (12.0, 10.0, 3.0), (x, 12.0, FLOOR_Z + 4.5), m.seat, bevel=0.8)
        tr.rbox(f"seat_{i}_back", (2.6, 10.0, 15.0), (x - 6.0, 12.0, FLOOR_Z + 12.0), m.seat, bevel=0.9)
        tr.rbox(f"seat_{i}_head", (3.6, 7.0, 4.0), (x - 6.0, 12.0, FLOOR_Z + 21.0), m.seat, bevel=1.0)
        tr.rbox(f"seat_{i}_leg", (3.0, 3.0, 4.0), (x, 12.0, FLOOR_Z + 1.5), m.ink, bevel=0.4)
        if passengers:
            root, objs = place("human-figure", None, 14.0, loc=(x - 1.0, 12.0, FLOOR_Z + 6.0), rot=(0, 0, math.radians(90)))
            arm = next(o for o in objs if o.type == "ARMATURE")
            pose_armature(arm, "pose_seated")
            tint_figure(objs, FIG[i])
            ns.figs.append(root)
    return ns


def tint_figure(objs, cols):
    names = ("fig_skin", "fig_shirt", "fig_pants", "fig_boots")
    for o in objs:
        if o.type != "MESH":
            continue
        for idx, slot in enumerate(o.material_slots):
            mat = slot.material
            if mat is None:
                continue
            for n, hexc in zip(names, cols):
                if mat.name.startswith(n):
                    mc = mat.copy()
                    mc.name = f"{n}_{id(o) % 9999}"
                    ar.retint(mc, hexc)
                    slot.material = mc


def cabin_door(S, m, pane, loc, length=64.0, name="cd"):
    """A cut-away cabin seen from inside with a door in its back wall (the hook, rung 4 of the 019 ladder: the door in its setting): curved wall, floor, oval windows either side,
    a seated passenger beside the door, the door with its porthole and grip bar. pane "ground" shows warm apron light through the opening and windows, "sky" the dark blue."""
    ns = type("CabinDoor", (), {})()
    ns.root = tr.empty(f"{name}_root", loc)
    r = ns.root
    a_floor = math.pi + math.asin(-FLOOR_Z / R)
    tube(f"{name}_skin", -length / 2, length / 2, R, math.pi / 2, a_floor, m.skin, parent=r, nx=2, na=60)
    pm = m.pane_s if pane == "sky" else m.pane_g
    for k, x in enumerate((-24.0, -15.0, 15.0, 24.0)):
        o = oval(f"{name}_win{k}", x, math.pi - math.asin(WIN_Z / R), R, WIN_W, WIN_H, pm, r, lift=-0.9)
    tr.rbox(f"{name}_floor", (length, 70.0, 1.6), (0, 0, FLOOR_Z - 0.8), m.panel, bevel=0.3, parent=r)
    ys = R * math.cos(math.asin(3.0 / R)) - 2.8
    jet_door(m, ns, name, pane, s=1.0, x=0.0, ys=ys, zc=3.0, open_dy=2.0, open_mat=pm)
    for i, x in enumerate((-28.0, 28.0)):
        tr.rbox(f"{name}_seat{i}_base", (12.0, 10.0, 3.0), (x, 22.0, FLOOR_Z + 4.5), m.seat, bevel=0.8, parent=r)
        tr.rbox(f"{name}_seat{i}_back", (2.6, 10.0, 15.0), (x - 6.0, 22.0, FLOOR_Z + 12.0), m.seat, bevel=0.9, parent=r)
        tr.rbox(f"{name}_seat{i}_head", (3.6, 7.0, 4.0), (x - 6.0, 22.0, FLOOR_Z + 21.0), m.seat, bevel=1.0, parent=r)
    root, objs = place("human-figure", r, 14.0, loc=(-29.0, 22.0, FLOOR_Z + 6.0), rot=(0, 0, math.radians(90)))
    pose_armature(next(o for o in objs if o.type == "ARMATURE"), "pose_seated")
    tint_figure(objs, FIG[1])
    return ns


AISLE_L = 120.0


def aisle(S, m, door=True, passengers=((-8, -14, 1), (8, 24, 2), (24, -24, 3), (-24, 14, 0)), name="ai"):
    """The cabin seen down its aisle (the canonical airplane-cabin picture): the full ring of skin (x from -60 to 60), floor and aisle strip, five rows of two seats on each side, oval windows
    along both walls, overhead bins, and at the far end (x = 60) a front wall with a door-shaped hole, the frame stops and the plug door (28 wide, the hole is 20) pressed against them.
    passengers: (x, y, wardrobe) seated figures. The door is driven by door_plug(ns, ...)."""
    ns = type("Aisle", (), {})()
    L = AISLE_L
    tube(f"{name}_skin", -L / 2, L / 2, R, 0.0, 2 * math.pi, m.skin, nx=2, na=96)
    tr.rbox(f"{name}_floor", (L, 60.0, 1.6), (0, 0, FLOOR_Z - 0.8), m.panel, bevel=0.3)
    tr.rbox(f"{name}_carpet", (L - 4, 8.0, 0.3), (0, 0, FLOOR_Z + 0.1), m.plate, bevel=0.1)      # the aisle strip takes the plate colour (the dark slate), never the ink: ink is the plinth class of the colour gate
    a = math.asin(WIN_Z / R)
    for k in range(9):
        x = -48.0 + k * 12.0
        oval(f"{name}_winL{k}", x, a, R, WIN_W, WIN_H, m.pane_s, None, lift=-1.0)
        oval(f"{name}_winR{k}", x, math.pi - a, R, WIN_W, WIN_H, m.pane_s, None, lift=-1.0)
    for s in (-1, 1):
        tr.rbox(f"{name}_bins{s}", (L - 14, 10.0, 6.0), (-2.0, s * 27.5, 26.0), m.panel, bevel=2.0)
        for r_ in range(5):
            x = -40.0 + r_ * 16.0
            for y in (s * 14.0, s * 24.0):
                tr.rbox(f"seat_{name}_{r_}_{y}_base", (9.0, 8.0, 3.0), (x, y, FLOOR_Z + 4.5), m.seat, bevel=0.8)
                tr.rbox(f"seat_{name}_{r_}_{y}_back", (2.6, 8.0, 15.0), (x - 4.5, y, FLOOR_Z + 12.0), m.seat, bevel=0.9)
                tr.rbox(f"seat_{name}_{r_}_{y}_head", (3.4, 6.0, 4.0), (x - 4.5, y, FLOOR_Z + 21.0), m.seat, bevel=1.0)
    for k, x in enumerate((-40.0, 0.0, 40.0)):                                                      # ceiling lamps: the closed tube shuts the stage lights out
        ld = bpy.data.lights.new(f"{name}_lamp{k}", "POINT")
        ld.energy, ld.shadow_soft_size = 8000.0, 8.0
        lamp = bpy.data.objects.new(f"{name}_lamp{k}", ld)
        bpy.context.scene.collection.objects.link(lamp)
        lamp.location = (x, 0.0, 30.0)
    ns.figs = []
    for x, y, w in passengers:
        root, objs = place("human-figure", None, 14.0, loc=(x - 1.0, y, FLOOR_Z + 6.0), rot=(0, 0, math.radians(90)))
        pose_armature(next(o for o in objs if o.type == "ARMATURE"), "pose_seated")
        tint_figure(objs, FIG[w])
        ns.figs.append(root)
    if door:
        xw = L / 2
        for nm, size, loc in (("l", (2.0, 30.0, 90.0), (xw, -25.0, 0.0)), ("r", (2.0, 30.0, 90.0), (xw, 25.0, 0.0)), ("t", (2.0, 20.0, 30.0), (xw, 0.0, 35.0)), ("b", (2.0, 20.0, 16.0), (xw, 0.0, -22.0))):
            tr.rbox(f"{name}_wall{nm}", size, loc, m.skin, bevel=0.3)
        for s in (-1, 1):
            tr.rbox(f"{name}_stop{s}", (1.6, 4.5, 34.0), (xw - 1.4, s * 12.0, 3.0), m.accent, bevel=0.3)       # frame stops, inboard of the wall, overlapped by the door
        tr.rbox(f"{name}_outside", (1.0, 24.0, 38.0), (xw + 6.0, 0.0, 3.0), m.pane_s, bevel=0.3)               # the sky beyond the hole
        ns.root = tr.empty(f"{name}_doorroot", (xw - 4.2, 0.0, 0.0))
        ns.root.rotation_euler = (0.0, 0.0, -math.pi / 2)
        jet_door(m, ns, name + "dr", "sky", s=1.0, x=-4.0, ys=0.0, zc=3.0, open_dy=40.0)          # the opening panel is parked far behind the wall
        ns.hinge.scale = (1.4, 1.0, 1.0)                                                           # 28 wide against a 20 hole
        ns.hinge0 = tuple(ns.hinge.location)
    return ns


def door_plug(ns, t, t_in, t_turn, t_out, t_end):
    """The plug door of the aisle set: pressed against the stops, then slides inward (toward the cabin, 26 cm), turns 90 degrees about its vertical axis and goes out through the hole edge-first."""
    k_in, k_turn, k_out = ease((t - t_in) / 1.0), ease((t - t_turn) / 0.7), ease((t - t_out) / max(0.1, t_end - t_out))
    x0, y0, z0 = ns.hinge0
    ns.hinge.location = (x0 + 14.0 * k_turn, y0 - 26.0 * k_in + 52.0 * k_out, z0)
    ns.hinge.rotation_euler = (0.0, 0.0, k_turn * math.radians(90))


# ------------------------------------------------------------------ accent air
def air(S, n, bounds, seed=7, r=0.9, mat=None, name="air"):
    """n accent blobs at fixed random spots inside bounds ((x0,x1),(y0,y1),(z0,z1)); returns (objs, places): the scene script sets each one's visibility."""
    rnd = random.Random(seed)
    base = S.ball(f"{name}_src", mat or S.accent, r)
    objs = S.swarm(n, base, lambda i, t: None)
    spots = [(rnd.uniform(*bounds[0]), rnd.uniform(*bounds[1]), rnd.uniform(*bounds[2])) for _ in range(n)]
    return objs, spots


# ------------------------------------------------------------------ the whole airliner (scenes 5 and 6 closes)
JET_R = 10.0


def _jet_radius(x):
    if x > 52.0:
        k = min(1.0, (x - 52.0) / 24.0)
        return max(0.6, JET_R * math.sqrt(max(0.0, 1.0 - k * k)))
    if x < -44.0:
        k = (-44.0 - x) / 34.0
        return max(0.8, JET_R * (1.0 - 0.8 * min(1.0, k)))
    return JET_R


JET_DOOR_X, JET_DOOR_S = 44.0, 0.3


def jet_door(m, ns, name, pane, s=JET_DOOR_S, x=JET_DOOR_X, ys=None, zc=0.0, open_dy=-0.05, open_mat=None):
    """The door of the airliner (same parts as the section's door, scaled by s): opening, hinge, slab, porthole, grip bar. Sets ns.hinge and ns.handle_loc (hinge space).
    ys = the wall surface (default the fuselage side, -JET_R); zc = door centre height; open_dy/open_mat = the opening panel behind the door."""
    pm = m.pane_s if pane == "sky" else m.pane_g
    ys = -JET_R if ys is None else ys
    tr.rbox(f"{name}_opening", ((DOOR_W + 2.4) * s, 1.6 * s, (DOOR_H + 2.4) * s), (x, ys + open_dy, zc), open_mat or m.ink, bevel=0.3 * s, parent=ns.root)
    ns.hinge = tr.empty(f"{name}_hinge", (x - DOOR_W * s / 2, ys - 0.5 * s, zc), parent=ns.root)
    tr.rbox(f"door_{name}_slab", (DOOR_W * s, DOOR_T * s, DOOR_H * s), (DOOR_W * s / 2, 0, 0), m.door, bevel=0.7 * s, parent=ns.hinge)
    tr.rbox(f"door_{name}_porthole", (4.6 * s, 0.6 * s, 5.6 * s), (DOOR_W * s / 2, -DOOR_T * s / 2 - 0.1 * s, 11.0 * s), pm, bevel=0.6 * s, parent=ns.hinge)
    ns.handle_loc = (DOOR_W * s / 2 + 4.0 * s, -DOOR_T * s / 2 - 1.6 * s, 1.0 * s)
    ns.bar_pivot = tr.empty(f"{name}_barpivot", (ns.handle_loc[0] - 4.0 * s, ns.handle_loc[1] - 0.3 * s, ns.handle_loc[2]), parent=ns.hinge)    # the grip bar pivots about its left post: pulled down by an unseen hand (rung 2 of the 019 reshape)
    tr.cyl(f"door_{name}_bar", 0.9 * s, 8.0 * s, (4.0 * s, 0, 0), m.ink, axis="X", parent=ns.bar_pivot, verts=20)
    for dx in (-3.6, 3.6):
        tr.cyl(f"door_{name}_post{dx}", 0.6 * s, 1.8 * s, (ns.handle_loc[0] + dx * s, -DOOR_T * s / 2 - 0.9 * s, ns.handle_loc[2]), m.ink, axis="Y", parent=ns.hinge, verts=12)


def jet_hand(ns, s=JET_DOOR_S):
    """The sealed hand on the jet door's grip bar (rides the hinge)."""
    off = (0.0, -3.6 * s, 0.74 * s)
    root, objs = place("hand-articulated", ns.hinge, 62.0 * s, loc=tuple(a + b for a, b in zip(ns.handle_loc, off)), rot=(0, 0, math.pi))
    pose_armature(next(o for o in objs if o.type == "ARMATURE"), "pose_lever")
    ns.hand_off = off
    return root, objs


def airliner(S, m, loc=(0, 0, 0), pane="sky", door=None, name="jet"):
    """door: None (the blow-out panel is built) or "ground" / "sky" (a boarding door near the nose with its hinge, for the hook)."""
    ns = type("Jet", (), {})()
    ns.root = tr.empty(f"{name}_root", loc)
    r = ns.root
    tube("jet_fuselage", -78.0, 76.0, _jet_radius, 0.0, 2 * math.pi, m.skin, parent=r, thick=0, nx=70, na=40)
    for s in (-1, 1):
        w = tr.rbox(f"jet_wing{s}", (22.0, 62.0, 1.6), (4.0 + 6.0, s * 32.0, -3.5), m.door, bevel=0.5, parent=r, rot=(0, 0, s * 0.5))
        tr.cyl(f"jet_engine{s}", 4.6, 15.0, (10.0, s * 19.0, -9.0), m.panel, axis="X", parent=r, verts=28, bevel=0.5)
        tr.cyl(f"jet_inlet{s}", 3.2, 1.0, (17.8, s * 19.0, -9.0), m.ink, axis="X", parent=r, verts=24)
        tr.rbox(f"jet_stab{s}", (10.0, 22.0, 1.0), (-66.0, s * 11.0, 2.0), m.door, bevel=0.3, parent=r, rot=(0, 0, s * 0.45))
    tr.rbox("jet_fin", (16.0, 1.8, 20.0), (-64.0, 0.0, 14.0), m.door, bevel=0.5, parent=r, rot=(0, 0.35, 0))
    pm = m.pane_s if pane == "sky" else m.pane_g
    for k in range(14):                                                                  # the cabin window row on the camera side
        x = -38.0 + k * 6.0
        if door is None and -34.0 < x < -4.0:
            continue                                                                       # the plug panel sits aft of the wing, leaving room
        if x > 36.0:
            continue                                                                       # room for the boarding door and the cockpit
        o = tr.cyl(f"jet_win{k}", 0.5, 0.5, (x, -JET_R - 0.15, 3.0), pm, axis="Y", parent=r, verts=20)
        o.scale = (1.5, 2.0, 1.0)
    tr.cyl("jet_cockpit", 0.5, 0.5, (62.0, -JET_R * 0.55, 3.4), m.pane_s, axis="Y", parent=r, verts=12).scale = (3.0, 1.4, 1.0)
    if door is not None:
        jet_door(m, ns, name, door)
        return ns
    ns.frame = tr.rbox("jet_frame", (11.0, 1.0, 13.0), (-20.0, -JET_R + 0.2, 1.0), m.ink, bevel=0.3, parent=r)
    ns.panel = tr.rbox("jet_panel", (9.0, 1.2, 11.5), (-20.0, -JET_R - 0.4, 1.0), m.panel, bevel=0.5, parent=r)
    ns.bolts = []
    for sx in (-1, 1):
        for sz in (-1, 1):
            b = tr.cyl(f"jet_bolt{sx}{sz}", 0.55, 0.8, (-20.0 + sx * 4.0, -JET_R - 1.1, 1.0 + sz * 5.0), m.red, axis="Y", parent=r, verts=16)
            ns.bolts.append(b)
    return ns


def clouds(S, m, n, bounds, seed=3):
    """Cloud puffs for motion past the airplane: static balls the scene script moves; returns [(obj, home)]."""
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        puff = tr.empty(f"cloud_{i}_root", (0, 0, 0))
        for j in range(3):
            o = S.ball(f"cloud_{i}_{j}", m.cloud, rnd.uniform(5, 9), (j * 6.0 - 6.0, rnd.uniform(-1, 1), rnd.uniform(-1, 2)), shape=(1.4, 0.8, 0.8), parent=puff)
        out.append((puff, (rnd.uniform(*bounds[0]), rnd.uniform(*bounds[1]), rnd.uniform(*bounds[2]))))
    return out
