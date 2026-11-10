"""Rig of production 016 (how many kilos of poop in a lifetime): the stylised stool unit, its pile (ONE mesh of many units, rewritten per frame), the kitchen scale and the
bathroom context from library assets. Runs inside Blender. Scene units are centimetres (assets K=100)."""
import math
import sys
from pathlib import Path

import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_rig as ar  # noqa: E402
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

UNIT_LEN = 15.0                       # cm: a chunky, exaggerated unit (a real one is about 15 cm too, but it is drawn thick)
BOWL = (0.0, -10.8)
RIM_Z = 45.0
SCALE_AT = (40.0, -32.0)             # kitchen scale on the floor beside the toilet
CERAMIC = "#F1F6FD"
SEAT = "#E3E9F1"
BROWN = "#85502C"
GREEN = "#B7C46A"                     # yellow-green = bacteria / biology (reference doctrine)


# ------------------------------------------------------------------ the unit
def unit_template(rings=26, segs=20, seed=0):
    """Unit-length (x, -0.5..0.5) stool: a bent, lumpy, tapered log, one end rounded and fat, the other drawn to a soft tip. Returns (verts (n,3), faces)."""
    rnd = np.random.default_rng(seed)
    s = np.linspace(0.0, 1.0, rings)
    ph = rnd.uniform(0, 2 * np.pi, 4)
    prof = np.sin(np.pi * np.clip(s, 0, 1)) ** 0.3                        # fat, blunt ends
    prof = prof * (1.0 - 0.18 * s) * (1.0 + 0.55 * np.clip(s - 0.82, 0, None) * -2.0)  # blunt head, tail drawn to a short soft tip
    r = 0.21 * prof * (1.0 + 0.11 * np.sin(17.0 * s + ph[0]))              # pinched segments along the length
    cx = (s - 0.5) * 1.0
    cy = 0.11 * np.sin(np.pi * s * 1.15 + 0.4)                             # gentle bend
    cz = 0.03 * np.sin(2.0 * np.pi * s + ph[1])
    th = np.linspace(0, 2 * np.pi, segs, endpoint=False)
    verts = []
    for i in range(rings):
        for j in range(segs):
            wob = 1.0 + 0.10 * np.sin(3 * th[j] + 9.0 * s[i] + ph[2]) + 0.05 * np.sin(5 * th[j] - 17.0 * s[i] + ph[3])
            verts.append((cx[i], cy[i] + r[i] * wob * np.cos(th[j]), cz[i] + 0.95 * r[i] * wob * np.sin(th[j])))
    faces = [(i * segs + j, i * segs + (j + 1) % segs, (i + 1) * segs + (j + 1) % segs, (i + 1) * segs + j) for i in range(rings - 1) for j in range(segs)]
    return np.array(verts, dtype=np.float32), faces


def swirl_template(rings=72, segs=22, seed=0):
    """A coiled, tapering soft-serve swirl (2.5 turns, tip curling over): the form viewers name as poop. Unit width ~0.7 (x, y), base at z = 0, centred on x, y."""
    rnd = np.random.default_rng(seed)
    ph = rnd.uniform(0, 2 * np.pi, 3)
    s = np.linspace(0.0, 1.0, rings)
    turns = 2.5
    ang = 2 * np.pi * turns * s + ph[0]
    R = 0.30 * (1.0 - 0.86 * s) ** 1.05
    r = 0.115 * (1.0 - 0.62 * s) * np.clip(s / 0.04, 0.0, 1.0) ** 0.5 * (1.0 - s ** 12) ** 0.5 * (1.0 + 0.05 * np.sin(11.0 * s + ph[1]))
    z = 0.19 * turns * s * (1.0 - 0.28 * s) + 0.105
    C = np.stack([R * np.cos(ang), R * np.sin(ang), z], axis=1)
    T = np.gradient(C, axis=0)
    T /= np.linalg.norm(T, axis=1)[:, None] + 1e-9
    N = np.cross(T, np.array([0.0, 0.0, 1.0]))
    N /= np.linalg.norm(N, axis=1)[:, None] + 1e-9
    Bv = np.cross(T, N)
    th = np.linspace(0, 2 * np.pi, segs, endpoint=False)
    verts = []
    for i in range(rings):
        for j in range(segs):
            wob = 1.0 + 0.05 * np.sin(3 * th[j] + 7.0 * s[i] + ph[2])
            verts.append(C[i] + r[i] * wob * (np.cos(th[j]) * N[i] + np.sin(th[j]) * Bv[i]))
    faces = [(i * segs + j, i * segs + (j + 1) % segs, (i + 1) * segs + (j + 1) % segs, (i + 1) * segs + j) for i in range(rings - 1) for j in range(segs)]
    v = np.array(verts, dtype=np.float32)
    v[:, 2] -= 0.10
    return v, faces


def stool_material(S, hex_color=BROWN, name="waste"):
    """Matte, slightly satin; never wet (the gross stays conceptual)."""
    return S.hero(name, hex_color, rough=0.72, coat=0.0)


def _mesh_obj(name, verts, faces, mat):
    me = bpy.data.meshes.new(name)
    me.from_pydata(verts.tolist(), [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat)
    return o


def rot_matrices(n, rnd, flat=True):
    """n random rotations; flat keeps the unit mostly lying down (yaw free, small tilt) so a pile reads as units resting on units."""
    yaw = rnd.uniform(0, 2 * np.pi, n)
    tilt = 0.06 if flat == "upright" else (0.4 if flat else 1.2)
    pitch = rnd.normal(0, tilt, n)
    roll = rnd.normal(0, tilt * 0.8, n)
    cz_, sz_ = np.cos(yaw), np.sin(yaw)
    cy_, sy_ = np.cos(pitch), np.sin(pitch)
    cx_, sx_ = np.cos(roll), np.sin(roll)
    R = np.zeros((n, 3, 3))
    Rz = np.stack([np.stack([cz_, -sz_, 0 * cz_], 1), np.stack([sz_, cz_, 0 * cz_], 1), np.stack([0 * cz_, 0 * cz_, 1 + 0 * cz_], 1)], 1)
    Ry = np.stack([np.stack([cy_, 0 * cy_, sy_], 1), np.stack([0 * cy_, 1 + 0 * cy_, 0 * cy_], 1), np.stack([-sy_, 0 * cy_, cy_], 1)], 1)
    Rx = np.stack([np.stack([1 + 0 * cx_, 0 * cx_, 0 * cx_], 1), np.stack([0 * cx_, cx_, -sx_], 1), np.stack([0 * cx_, sx_, cx_], 1)], 1)
    R = Rz @ Ry @ Rx
    return R.astype(np.float32)


class Pile:
    """n stool units in ONE mesh (variants of the template cycle so a pile has no repeats in a row). set(pos (n,3), size (n,)) rewrites every vertex: size 0 hides a unit."""

    def __init__(self, S, name, n, mat, seed=1, variants=4, flat=True, kind="swirl"):
        self.n = n
        rnd = np.random.default_rng(seed)
        make = swirl_template if kind == "swirl" else unit_template
        tmpls = [make(seed=k * 7 + 1) for k in range(variants)]
        self.faces_unit = tmpls[0][1]
        self.nv = len(tmpls[0][0])
        self.tm = np.stack([tmpls[i % variants][0] for i in range(n)])        # (n, nv, 3)
        self.R = rot_matrices(n, rnd, flat)
        verts = np.zeros((n * self.nv, 3))
        faces = [tuple(i * self.nv + x for x in f) for i in range(n) for f in self.faces_unit]
        me = bpy.data.meshes.new(name)
        me.from_pydata(verts.tolist(), [], faces)
        me.update()
        for p in me.polygons:
            p.use_smooth = True
        self.obj = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(self.obj)
        me.materials.append(mat)
        S.reg(self.obj)
        self.rnd = rnd

    def set(self, pos, size, yaw=None):
        R = self.R
        local = np.einsum("nij,nvj->nvi", R, self.tm)
        co = (local * np.asarray(size)[:, None, None] * UNIT_LEN + np.asarray(pos)[:, None, :]).astype(np.float32)
        self.obj.data.vertices.foreach_set("co", co.reshape(-1))
        self.obj.data.update()
        self.obj.data.update_tag()


def mound(n, centre, radius, height, seed=2, floor=0.0):
    """Resting positions of n units heaped into a cone-ish mound (low units first in index order, so a growing count builds the pile from the bottom up)."""
    rnd = np.random.default_rng(seed)
    u = rnd.uniform(0, 1, n)
    rr = radius * np.sqrt(u) ** 1.0
    th = rnd.uniform(0, 2 * np.pi, n)
    top = height * (1.0 - (rr / radius) ** 1.5)
    z = floor + 3.0 + top * rnd.uniform(0.55, 1.0, n)
    order = np.argsort(z)
    pos = np.stack([centre[0] + rr * np.cos(th), centre[1] + rr * np.sin(th) * 0.8, z], axis=1)[order]
    return pos


# ------------------------------------------------------------------ the set
class Set:
    pass


def bathroom(S, colours=None):
    """The library toilet (lid down, seat up) on the stage floor. Returns the parts the scenes animate."""
    colours = colours or {"ceramic": CERAMIC, "seat": SEAT}
    B = Set()
    t = ar.load(S, "toilet")
    B.root = t.root
    B.lid = next(o for o in t.objs if o.name.startswith("toilet_lid"))
    for o in t.objs:
        if o.name.startswith("toilet_body"):
            _retint(o.material_slots[0].material, colours["ceramic"], "g_big", rough=0.14, coat=0.6)
        elif o.name.startswith(("toilet_seat", "toilet_lid")):
            _retint(o.material_slots[0].material, colours["seat"], "shell_y", rough=0.25, coat=0.4)
    return B


def _retint(mat, hex_color, role, rough=0.25, coat=0.4):
    b = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    for name in ("Base Color", "Roughness", "Metallic", "Transmission Weight"):
        for l in list(b.inputs[name].links):
            mat.node_tree.links.remove(l)
    b.inputs["Base Color"].default_value = c.linear(hex_color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 0.0
    b.inputs["Transmission Weight"].default_value = 0.0
    b.inputs["Coat Weight"].default_value = coat
    mat.name = role
    return mat


def bathroom_scale(S, loc=(SCALE_AT[0], SCALE_AT[1], 0.0)):
    """Kitchen scale: slab body, steel platter, a dark display window. Geometric and reads instantly (route: code primitive). Returns (root, display_empty)."""
    root = S.empty("scale_root", loc)
    body = S.box("scale_body", (26.0, 20.0, 3.4), (0, 0, 1.7), S.hero("big", "#E7E4DE", rough=0.35, coat=0.3), bevel=1.2, parent=root)
    S.box("scale_face", (22.0, 1.0, 2.0), (0, -9.6, 1.7), S.hero("ink", "#1D1B2E", rough=0.3, coat=0.4), bevel=0.4, parent=root)
    S.cyl("scale_stem", 3.0, 1.2, (0, 0, 4.0), S.hero("small", "#9AA3AD", rough=0.3, metal=0.8), parent=root, bevel=0.3)
    S.cyl("scale_platter", 10.5, 0.8, (0, 0, 5.0), S.hero("small", "#B9C0C8", rough=0.25, metal=0.8), parent=root, bevel=0.35)
    return root
