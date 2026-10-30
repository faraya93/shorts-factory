"""Hero rig for the toilet video (inodoro-donde-va-todo): a CUTAWAY toilet, side profile in the XZ plane (camera looks along +y, the bowl faces +x).
Porcelain front layer = one extruded outline minus the cavity cutters (tank, flush channel, bowl, S-trap); the cavities open onto a teal back layer.
Water = translucent blue solid volumes (rect pieces scaled per frame, the bowl clipped analytically): NO fluid simulation. Waste = a few matte rounded brown forms.
Units: 1 BU ~ 5 cm; floor z = 0. Dimensions chosen so the whole cutaway reads in a portrait frame."""
import math
import sys
from pathlib import Path

import bmesh
import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

Y0, Y1 = -0.8, 0.6                 # porcelain front layer (the cut face is at y = Y0)
YB0, YB1 = 0.6, 1.2                # back layer
WY0, WY1 = -0.62, 0.58             # water volumes sit just behind the cut face
OUTLINE = [(-5.4, 15.2), (-5.4, 8.0), (-3.8, 8.0), (-3.8, 0.0), (3.2, 0.0), (3.2, 2.0), (5.6, 2.6), (6.9, 4.6), (6.9, 8.6), (0.0, 8.6), (0.0, 15.2)]
TANK = (-5.0, -0.4, 8.4, 16.0)                           # x0, x1, z0, z1 (open top)
HOLE = (-1.8, -0.6, 7.4, 8.6)
CHAN = (-1.8, 1.4, 6.5, 7.6)
BOWL = [(1.0, 9.4), (1.0, 5.0), (1.5, 3.9), (2.5, 3.0), (4.0, 2.7), (5.4, 3.2), (6.2, 4.4), (6.3, 9.4)]
TUBE_PIECES = {"H": (0.45, 2.4, 2.55, 3.85), "L1": (-0.85, 0.45, 2.55, 5.9), "APEX": (-1.55, -0.85, 4.6, 5.9), "LEG2": (-2.85, -1.55, -1.8, 5.9)}
WATERLINE, TANK_FULL, TANK_EMPTY = 4.6, 14.2, 8.4
# centre line of the trap for the waste (x, z): sump -> across -> up the ascending leg -> over the apex -> down the descending leg -> out through the floor
PATH = [(3.6, 4.5), (3.3, 3.2), (2.2, 3.2), (-0.2, 3.2), (-0.2, 5.25), (-2.2, 5.25), (-2.2, 0.0), (-2.2, -1.6)]


def material_set():
    import looks
    p = looks.current()
    ink = tr.plain("ink", p["plinth"] if p else "#1E1E22", rough=0.55)
    water = tr.plain("water", "#2F7DE6", rough=0.1)
    nt = water.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Alpha"].default_value = 0.86
    water.surface_render_method = "BLENDED"
    return {"ink": ink, "porcelain": tr.plain("plate", p["support_plate"] if p else "#F0E6D2", rough=0.25, coat=0.3),
            "back": tr.plain("g_board", p["support_board"] if p else "#CFC1A6", rough=0.7),
            "water": water, "waste": tr.plain("waste", "#8A3E1C", rough=0.55),
            "steel": tr.plain("blade", "#4E586A", rough=0.35, metallic=0.25), "lever": tr.plain("g_pin", "#4A2BC4", rough=0.4, coat=0.2)}


def prism(name, poly, y0, y1, material, smooth=False):
    bm = bmesh.new()
    verts = [bm.verts.new((x, y0, z)) for x, z in poly]
    face = bm.faces.new(verts)
    ext = bmesh.ops.extrude_face_region(bm, geom=[face])
    top = [v for v in ext["geom"] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, y1 - y0, 0), verts=top)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    if material is not None:
        o.data.materials.append(material)
    if smooth:
        for p in o.data.polygons:
            p.use_smooth = True
    return o


def rect(x0, x1, z0, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def carve(obj, cutters):
    """Boolean-difference every cutter out of obj (exact solver), apply, delete the cutters."""
    bpy.context.view_layer.objects.active = obj
    for i, ct in enumerate(cutters):
        mod = obj.modifiers.new(f"cut{i}", "BOOLEAN")
        mod.operation, mod.object, mod.solver = "DIFFERENCE", ct, "EXACT"
    for mod in list(obj.modifiers):
        bpy.ops.object.modifier_apply(modifier=mod.name)
    for ct in cutters:
        bpy.data.objects.remove(ct, do_unlink=True)


def cavities(y0, y1):
    ex = 0.3
    out = [prism("c_tank", rect(*TANK), y0 - ex, y1 + ex, None), prism("c_hole", rect(*HOLE), y0 - ex, y1 + ex, None),
           prism("c_chan", rect(*CHAN), y0 - ex, y1 + ex, None), prism("c_bowl", BOWL, y0 - ex, y1 + ex, None)]
    for k, r in TUBE_PIECES.items():
        out.append(prism(f"c_{k}", rect(*r), y0 - ex, y1 + ex, None))
    return out


def bevel(o, width=0.06):
    mod = o.modifiers.new("bevel", "BEVEL")
    mod.width, mod.segments, mod.limit_method, mod.angle_limit = width, 2, "ANGLE", math.radians(35)


class Box:
    """A unit cube positioned/scaled each frame: used for the rectangular water pieces."""

    def __init__(self, name, material, y0=WY0, y1=WY1):
        bpy.ops.mesh.primitive_cube_add(size=1)
        self.o = bpy.context.object
        self.o.name = name
        for p in self.o.data.polygons:
            p.use_smooth = False
        self.o.data.materials.append(material)
        self.o.visible_shadow = False
        self.y0, self.y1 = y0, y1

    def set(self, x0, x1, z0, z1):
        if z1 - z0 < 1e-3 or x1 - x0 < 1e-3:
            self.o.scale = (1e-4, 1e-4, 1e-4)
            return
        self.o.location = ((x0 + x1) / 2, (self.y0 + self.y1) / 2, (z0 + z1) / 2)
        self.o.scale = (x1 - x0, self.y1 - self.y0, z1 - z0)


class PolyWater:
    """A convex polygon prism clipped by z <= level (analytic Sutherland-Hodgman on the horizontal plane): the bowl water."""

    def __init__(self, name, poly, material):
        self.poly = poly
        self.o = prism(name, poly, WY0, WY1, material)
        self.o.visible_shadow = False
        self.name, self.mat = name, material

    def set(self, level):
        pts = []
        n = len(self.poly)
        for i in range(n):
            a, b = self.poly[i], self.poly[(i + 1) % n]
            ina, inb = a[1] <= level, b[1] <= level
            if ina:
                pts.append(a)
            if ina != inb:
                t = (level - a[1]) / (b[1] - a[1])
                pts.append((a[0] + (b[0] - a[0]) * t, level))
        mesh = self.o.data
        mesh.clear_geometry()
        if len(pts) < 3:
            return
        bm = bmesh.new()
        vs = [bm.verts.new((x, WY0, z)) for x, z in pts]
        f = bm.faces.new(vs)
        ext = bmesh.ops.extrude_face_region(bm, geom=[f])
        top = [v for v in ext["geom"] if isinstance(v, bmesh.types.BMVert)]
        bmesh.ops.translate(bm, vec=(0, WY1 - WY0, 0), verts=top)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        bm.to_mesh(mesh)
        bm.free()
        if not mesh.materials:
            mesh.materials.append(self.mat)


class Toilet:
    def __init__(self, with_floor=True):
        fl = bpy.data.objects.get("floor")
        if fl:
            fl.hide_render = True
        self.mats = mats = material_set()
        self.shell = prism("porcelain", OUTLINE, Y0, Y1, mats["porcelain"])
        carve(self.shell, cavities(Y0, Y1))
        bevel(self.shell)
        self.back = prism("pocket_back", OUTLINE, YB0, YB1, mats["back"])
        bevel(self.back, 0.05)
        self.slab = None
        if with_floor:
            self.slab = prism("floor_slab", rect(-9.0, 9.0, -2.4, 0.0), Y0, Y1, mats["ink"])
            carve(self.slab, [prism("c_floor", rect(*TUBE_PIECES["LEG2"]), Y0 - 0.3, Y1 + 0.3, None)])
            bevel(self.slab, 0.06)
            self.slab_back = prism("floor_slab_back", rect(-9.0, 9.0, -2.4, 0.0), YB0, YB1, mats["ink"])
        self.tank_w = Box("w_tank", mats["water"])
        self.hole_w = Box("w_hole", mats["water"])
        self.chan_w = Box("w_chan", mats["water"])
        self.bowl_w = PolyWater("w_bowl", BOWL, mats["water"])
        self.tube_w = {k: Box(f"w_{k}", mats["water"]) for k in TUBE_PIECES}
        # flapper on a hinge, lever on the tank wall, fill valve (post + float)
        self.hinge = tr.empty("flap_hinge", (-1.95, (Y0 + Y1) / 2, 8.5))
        tr.rbox("flapper", (1.5, 1.0, 0.2), (0.75, 0, 0), mats["lever"], bevel=0.06, parent=self.hinge)
        self.lever = tr.empty("lever_pivot", (-5.5, (Y0 + Y1) / 2, 13.6))
        tr.rbox("lever_arm", (1.9, 0.6, 0.45), (-0.8, 0, 0), mats["lever"], bevel=0.12, parent=self.lever)
        tr.cyl("lever_knob", 0.5, 0.8, (-1.8, 0, 0), mats["lever"], axis="Y", parent=self.lever, verts=32, bevel=0.06)
        tr.rbox("fill_post", (0.5, 0.7, 6.0), (-4.2, 0.2, 11.4), mats["steel"], bevel=0.1)
        self.float = tr.cyl("fill_float", 0.5, 0.6, (-4.2, -0.2, 13.0), mats["steel"], axis="Y", verts=32, bevel=0.05)
        self.waste = []
        for i, (rx, rz) in enumerate(((0.55, 0.42), (0.45, 0.36))):
            bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1.0)
            o = bpy.context.object
            o.name = f"waste{i}"
            o.scale = (rx, 0.42, rz)
            for p in o.data.polygons:
                p.use_smooth = True
            o.data.materials.append(mats["waste"])
            self.waste.append(o)
        self.state(tank=TANK_FULL, bowl=WATERLINE)

    # ---- water --------------------------------------------------------------------------
    def state(self, tank=TANK_FULL, bowl=WATERLINE, chan=0.0, hole=0.0, tube=None, leg2=(5.9, 5.9)):
        """tank = tank water level; bowl = bowl water level; chan = fill fraction of the flush channel (0..1, from the tank end);
        hole = 1 shows water in the flush opening; tube = water level in the sump/ascending/apex pieces (default: the bowl level);
        leg2 = (lo, hi) z-range of the water in the descending leg (lo >= hi means empty)."""
        self.tank_w.set(TANK[0] + 0.02, TANK[1] - 0.02, TANK[2], tank)
        self.hole_w.set(HOLE[0], HOLE[1], HOLE[2], HOLE[3] if hole > 0.5 else HOLE[2])
        self.chan_w.set(CHAN[0], CHAN[0] + (CHAN[1] - CHAN[0]) * max(0.0, min(1.0, chan)), CHAN[2], CHAN[3])
        self.bowl_w.set(bowl)
        lvl = bowl if tube is None else tube
        x0, x1, z0, z1 = TUBE_PIECES["H"]; self.tube_w["H"].set(x0, x1, z0, min(z1, lvl))
        x0, x1, z0, z1 = TUBE_PIECES["L1"]; self.tube_w["L1"].set(x0, x1, z0, min(z1, lvl))
        x0, x1, z0, z1 = TUBE_PIECES["APEX"]; self.tube_w["APEX"].set(x0, x1, z0, min(z1, lvl))
        x0, x1, z0, z1 = TUBE_PIECES["LEG2"]; lo, hi = leg2
        self.tube_w["LEG2"].set(x0, x1, max(z0, lo), min(z1, hi) if hi > lo else lo)
        self.float.location.z = max(tank, TANK_EMPTY) - 0.3

    def flap(self, lift):
        self.hinge.rotation_euler = (0, -math.radians(70) * lift, 0)

    def press(self, k):
        self.lever.rotation_euler = (0, math.radians(28) * k, 0)

    def put_waste(self, i, x, z, s=1.0, tumble=0.0):
        o = self.waste[i]
        o.location = (x, -0.1, z)
        o.scale = tuple(v * max(1e-4, s) for v in ((0.55, 0.42, 0.42), (0.45, 0.42, 0.36))[i])
        o.rotation_euler = (0, tumble, 0)

    @staticmethod
    def path_point(s):
        """Point on PATH at arc-length fraction s (0..1)."""
        segs = [(PATH[i], PATH[i + 1]) for i in range(len(PATH) - 1)]
        ls = [math.dist(a, b) for a, b in segs]
        d = max(0.0, min(1.0, s)) * sum(ls)
        for (a, b), l in zip(segs, ls):
            if d <= l or (a, b) == segs[-1]:
                k = min(1.0, d / l)
                return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
            d -= l


def cpu_draft(stage, args):
    """Development previews that must not touch the GPU while a final render runs: Cycles on 4 CPU threads, tiny and noisy."""
    if not args.get("cpu"):
        return
    sc = stage.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = 10
    sc.cycles.use_denoising = False
    sc.render.threads_mode, sc.render.threads = "FIXED", 4
    sc.render.resolution_percentage = 40


def keys(t, pts):
    """Smoothstep-interpolated value of the piecewise key list [(t0, v0), (t1, v1), ...] at time t (holds the ends)."""
    if t <= pts[0][0]:
        return pts[0][1]
    for (ta, va), (tb, vb) in zip(pts, pts[1:]):
        if t <= tb:
            k = (t - ta) / (tb - ta) if tb > ta else 1.0
            k = k * k * (3 - 2 * k)
            return va + (vb - va) * k
    return pts[-1][1]


def ring(m, name, loc, sx, sz, minor=0.07):
    """Accent torus facing the camera (x, z radii): marks a region; hidden by scale."""
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=minor, major_segments=96, minor_segments=10, location=loc, rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object
    o.name = name
    o.scale = (max(1e-4, sx), 1.0, max(1e-4, sz))
    o.data.materials.append(m.gold)
    o.visible_shadow = False
    return o


def gas_material():
    mat = tr.plain("gas", "#B7C46A", rough=0.5)
    mat.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = 0.8
    mat.surface_render_method = "BLENDED"
    return mat
