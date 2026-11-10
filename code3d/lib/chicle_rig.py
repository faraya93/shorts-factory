"""Rig of production 014 (what happens if you swallow gum): the library digestive system in x-ray, the lumen path a swallowed piece travels, the chewed gum piece, the gum stick and its wrapper,
the squeeze ring, the stomach acid and food pieces. Runs inside Blender. Scene units are centimetres; the tract asset is 0.41 m tall, so K=100 gives 41 cm."""
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_library as al  # noqa: E402,F401
import asset_rig as ar  # noqa: E402
import common as c  # noqa: E402
import setpiece as sp  # noqa: E402

K = ar.K
GUM = "#F58FB5"                                                                 # chewed gum, pink
CORE = "#E8548F"                                                                # the rubbery base that stays, deeper pink, after the sugar and flavour coat washes off
COAT = "#FFE3EE"                                                                # the pale sugar and flavour coat
WRAP = "#DCE3EA"
BAND = "#1D1B2E"

# Lumen centre line of the asset (metres, asset space): oesophagus, stomach, pylorus, small bowel, ascending / transverse / descending colon, rectum. Checked against the x-ray mesh on 2026-11-09.
PATH = [(-0.007, -0.026, 0.41), (-0.007, -0.02, 0.37), (-0.007, -0.005, 0.33), (-0.006, 0.012, 0.30), (0.005, 0.014, 0.275), (0.04, 0.01, 0.25), (0.05, 0.0, 0.215), (0.02, -0.01, 0.195),
        (0.0, 0.0, 0.18), (-0.02, -0.015, 0.15), (0.03, -0.02, 0.13), (-0.03, -0.02, 0.11), (0.03, -0.02, 0.095), (-0.02, -0.02, 0.075), (-0.065, -0.02, 0.05), (-0.075, -0.02, 0.1),
        (-0.075, -0.02, 0.15), (-0.04, -0.03, 0.185), (0.0, -0.03, 0.185), (0.04, -0.03, 0.18), (0.075, -0.02, 0.15), (0.075, -0.02, 0.1), (0.06, -0.015, 0.06), (0.02, 0.0, 0.045),
        (-0.002, 0.01, 0.02), (-0.002, 0.01, 0.0)]
# Named stretches of the path, as fractions of its length (set once from the table below).
_TAB = None


def _table():
    global _TAB
    if _TAB is None:
        keys = [(float(i), p) for i, p in enumerate(PATH)]
        pts = [sp.spline(keys, i / 20.0) for i in range(0, 20 * (len(PATH) - 1) + 1)]
        acc = [0.0]
        for a, b in zip(pts, pts[1:]):
            acc.append(acc[-1] + (Vector(b) - Vector(a)).length)
        _TAB = (pts, acc)
    return _TAB


def lumen(s):
    """Asset-space point (metres) at arc-length fraction s of the whole tract (0 = mouth, 1 = anus)."""
    pts, acc = _table()
    s = min(1.0, max(0.0, s)) * acc[-1]
    lo, hi = 0, len(acc) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if acc[mid] <= s:
            lo = mid
        else:
            hi = mid
    k = (s - acc[lo]) / max(1e-9, acc[hi] - acc[lo])
    return tuple(a + (b - a) * k for a, b in zip(pts[lo], pts[hi]))


def frac_of(index):
    """Arc-length fraction of the PATH waypoint `index`."""
    pts, acc = _table()
    return acc[index * 20] / acc[-1]


S_STOMACH_IN, S_PYLORUS, S_COLON = frac_of(4), frac_of(8), frac_of(14)


class Tract:
    def __init__(self, hero, loc, k):
        self.hero, self.loc, self.k = hero, Vector(loc), k

    def at(self, s):
        """Scene-space point (cm) of path fraction s (the tract root is not rotated)."""
        p = lumen(s)
        return tuple(self.loc[i] + p[i] * self.k for i in range(3))

    def point(self, p):
        return tuple(self.loc[i] + p[i] * self.k for i in range(3))


def xray_material(S, hexc="#F6D5C4", centre=0.16, edge=0.92, name="g_big"):
    """The tract as an x-ray: translucent in the middle of every wall, opaque at the grazing edges, so the gum inside shows through."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    mix = nt.nodes.new("ShaderNodeMixShader")
    tr_ = nt.nodes.new("ShaderNodeBsdfTransparent")
    b = nt.nodes.new("ShaderNodeBsdfPrincipled")
    b.inputs["Base Color"].default_value = c.linear(hexc)
    b.inputs["Roughness"].default_value = 0.45
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.35
    ramp = nt.nodes.new("ShaderNodeMapRange")
    ramp.inputs["From Min"].default_value, ramp.inputs["From Max"].default_value = 0.0, 1.0
    ramp.inputs["To Min"].default_value, ramp.inputs["To Max"].default_value = centre, edge
    nt.links.new(lw.outputs["Fresnel"], ramp.inputs["Value"])
    nt.links.new(ramp.outputs["Result"], mix.inputs["Fac"])
    nt.links.new(tr_.outputs["BSDF"], mix.inputs[1])
    nt.links.new(b.outputs["BSDF"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    return m


def tract(S, loc=(0.0, 0.0, 0.0), k=K, xray=True, hexc="#F6D5C4"):
    """The library digestive system at scene scale; its texture is replaced by the x-ray material (hero colour hexc)."""
    h = ar.load(S, "digestive-system", loc=loc, k=k)
    mat = xray_material(S, hexc) if xray else S.hero("g_big", hexc, rough=0.5)
    for o in h.objs:
        o.data.materials.clear()
        o.data.materials.append(mat)
    h.mat = mat
    return Tract(h, loc, k)


def gum_material(S, name="g_pin"):
    """Pink gum with a `coat` control: 1 = pink sugar and flavour coat, 0 = the grey rubbery base underneath."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Roughness"].default_value = 0.35
    b.inputs["Coat Weight"].default_value = 0.4
    coat = nt.nodes.new("ShaderNodeValue")
    coat.name = "coat"
    coat.outputs[0].default_value = 1.0
    mix = nt.nodes.new("ShaderNodeMixRGB")
    mix.inputs["Color1"].default_value = c.linear(CORE)
    mix.inputs["Color2"].default_value = c.linear(COAT)
    nt.links.new(coat.outputs["Value"], mix.inputs["Fac"])
    nt.links.new(mix.outputs["Color"], b.inputs["Base Color"])
    return m


def set_coat(mat, v):
    mat.node_tree.nodes["coat"].outputs[0].default_value = v


def gum_piece(S, mat, name="gum", r=1.0, loc=(0, 0, 0), seed=3, **tk):
    """A chewed piece: a lumpy flattened blob with pressed ridges (a smooth ball would read as a pill)."""
    rnd = random.Random(seed)
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=4, radius=1.0)
    for v in bm.verts:
        n = v.co.normalized()
        bump = 1.0 + 0.17 * math.sin(3.2 * n.x + 1.3 * seed) * math.cos(2.8 * n.y + seed) + 0.1 * math.sin(4.5 * n.z + 2.0 * seed) + 0.06 * math.sin(7.0 * n.x + 5.0 * n.y + seed)
        v.co = Vector((n.x * 1.15, n.y * 0.85, n.z * 0.62)) * bump
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat)
    o.scale = (r, r, r)
    o.location = loc
    return S.reg(o, **tk)


def kernel(S, mat, name="kernel", r=1.0, loc=(0, 0, 0), **tk):
    """A whole corn kernel: a flat tooth, broad rounded crown with a small dimple, tapering to a point (the egg-shaped 011 primitive read as a lemon without a cob around it)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=4, radius=1.0)
    for v in bm.verts:
        x, y, z = v.co
        w = 1.0 if z >= 0.0 else max(0.05, 1.0 + 0.85 * z)
        dimple = -0.10 * max(0.0, 1.0 - (x * x + y * y) * 6.0) if z > 0.6 else 0.0
        v.co = Vector((x * w * 0.95, y * w * 0.5, z * 1.15 + dimple))
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat)
    o.scale = (r, r, r)
    o.location = loc
    return S.reg(o, **tk)


def bubble(S, name="bubble", r=1.0, loc=(0, 0, 0), **tk):
    """A thin glossy pink gum bubble: the one cue every viewer knows for chewing gum (a stick in its wrapper read as a lipstick, 55/40/40)."""
    mat = S.glass(GUM, alpha=0.55, rough=0.03, name="water")
    return S.ball(name, mat, r, loc, seg=48, **tk)


def strand(S, name, top, bottom, r=0.12, mat=None, **tk):
    """A stretched gum thread from `top` to `bottom` (scene cm): an hourglass tube, thin in the middle (a chewed wad pulled off a surface)."""
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings, seg = 14, 12
    t0, t1 = Vector(top), Vector(bottom)
    mid = (t0 + t1) * 0.5
    ax = (t1 - t0)
    rows = []
    for i in range(rings + 1):
        u = i / rings
        rad = r * (0.12 + 3.2 * abs(2.0 * u - 1.0) ** 3.0)
        cen = ax * (u - 0.5)
        row = [bm.verts.new(cen + Vector((math.cos(a) * rad, math.sin(a) * rad, 0.0))) for a in [k * math.tau / seg for k in range(seg)]]
        rows.append(row)
    for i in range(rings):
        for k in range(seg):
            bm.faces.new((rows[i][k], rows[i][(k + 1) % seg], rows[i + 1][(k + 1) % seg], rows[i + 1][k]))
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat)
    o.location = mid
    return S.reg(o, **tk)


def stick(S, loc=(0, 0, 0), name="stick"):
    """A gum stick half out of its foil wrapper: pale foil sleeve, ink paper band, the pink stick sliding out. Geometric, the wrapper is the cue. Returns the root empty."""
    root = S.empty(name, loc)
    foil = S.hero("g_big", WRAP, rough=0.25, metal=0.8, coat=0.0)
    paper = S.hero("g_big", WRAP, rough=0.25, metal=0.8, coat=0.0)               # foil-wrapped, not a dark box (a dark pack read as a pill box, scene 6)
    band = S.hero("g_pin", "#F58FB5", rough=0.5, coat=0.0)
    pink = S.hero("g_pin", GUM, rough=0.4, coat=0.3)
    groove = S.hero("ink", "#C2527F", rough=0.5, coat=0.0)
    S.box(name + "_pack", (3.4, 1.0, 8.0), (0, 0, 4.0), paper, bevel=0.14, parent=root)
    S.box(name + "_band", (3.5, 1.05, 1.7), (0, 0, 3.0), band, bevel=0.1, parent=root)
    S.box(name + "_foil", (3.0, 0.8, 1.1), (0, 0, 8.3), foil, bevel=0.12, parent=root)
    bar = S.box(name + "_gum", (2.6, 0.22, 6.2), (0, -0.05, 6.5), pink, bevel=0.08, parent=root)
    for i in range(5):
        S.box(f"{name}_groove{i}", (2.6, 0.06, 0.12), (0, -0.1, -2.4 + i * 1.2), groove, bevel=0.02, parent=bar)
    return root, bar


def ring(S, name, mat, major, minor, loc, rot=(0, 0, 0), **tk):
    """The muscle squeeze: a torus that slides along the tube."""
    return S.torus(name, major, minor, loc, mat, rot=rot, **tk)


def acid(S, loc, shape, name="acid"):
    """Stomach acid: a shallow transmissive pool (one transmission layer)."""
    return S.ball(name, S.glass("#C6E36B", alpha=0.55, rough=0.04, name="water"), 1.0, loc, shape=shape, seg=48)


def food(S, slug, loc, k, rot=(0, 0, 0)):
    return ar.load(S, slug, loc=loc, rot=rot, k=k)


def kernel_pal(S):
    import corn_rig as cr
    return cr, cr.palette(S)


def route_line(S, tract_, s0, s1, mat, r=0.7, n=60, grow=None):
    pts = [tract_.at(s0 + (s1 - s0) * i / n) for i in range(n + 1)]
    return S.line("route", pts, r, mat, grow=grow, smooth=False)


def backing(S, mat=None, loc=(0.0, 14.0, 40.0), size=(420.0, 1.0, 320.0)):
    """The teal board behind the x-ray body (the cream-pink tract separates from it; the pink gum too)."""
    return S.box("board", size, loc, mat or S.board_mat(), bevel=0.6)


def tangent(T, s):
    a, b = Vector(T.at(max(0.0, s - 0.004))), Vector(T.at(min(1.0, s + 0.004)))
    return (b - a).normalized()


def aim(vec):
    """Euler rotation that points a torus's axis (local z) along vec."""
    return tuple(vec.to_track_quat("Z", "Y").to_euler())
