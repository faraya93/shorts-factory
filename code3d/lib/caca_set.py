"""Set pieces of production 016 beyond the frozen hero (caca_rig): the lighter pile for big heaps, retinting of the library props (suitcase, horse, cars), the see-saw balance,
the glass tank, and the unit flight helpers. Runs inside Blender. Scene units are centimetres."""
import math
import sys
from pathlib import Path

import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_rig as ar  # noqa: E402
import caca_rig as cr  # noqa: E402
import common as c  # noqa: E402
import real_kit as rk  # noqa: E402
import tape_rig as tr  # noqa: E402
import setpiece as sp  # noqa: E402

SUITCASE = "#2E6E86"
HORSE = "#A9B0BE"
MANE = "#5A5560"
CAR = "#3C7DA6"
GLASS_TINT = "#BFE6F2"
N_UNITS = 330


class LitePile(cr.Pile):
    """Same as Pile with a lighter unit mesh (a heap of hundreds of units): fewer rings and segments, so one mesh stays under ~250k vertices."""

    def __init__(self, S, name, n, mat, seed=1, variants=4, flat=True, rings=34, segs=14):
        self.n = n
        rnd = np.random.default_rng(seed)
        tmpls = [cr.swirl_template(rings=rings, segs=segs, seed=k * 7 + 1) for k in range(variants)]
        self.faces_unit = tmpls[0][1]
        self.nv = len(tmpls[0][0])
        self.tm = np.stack([tmpls[i % variants][0] for i in range(n)])
        self.R = cr.rot_matrices(n, rnd, flat)
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


def lerp_mound(n, a, b, k, seed=2):
    """Positions of n units on a mound blending layout a -> b by k (each a dict centre/radius/height); the same random draws, so the heap swells in place."""
    pa = cr.mound(n, a["centre"], a["radius"], a["height"], seed=seed)
    pb = cr.mound(n, b["centre"], b["radius"], b["height"], seed=seed)
    return pa + (pb - pa) * k


def flight(i, n, t, t0, t1, src, dst, arc=28.0, fly=0.55, power=1.1):
    """Unit i of n: released between t0 and t1 (later units later), flies src -> dst in an arc, then rests. Returns (xyz, shown)."""
    ti = t0 + (t1 - t0) * (i / max(1, n - 1)) ** power
    k = (t - ti) / fly
    if k <= 0.0:
        return src, 0.0
    if k >= 1.0:
        return dst, 1.0
    e = k * k * (3 - 2 * k)
    p = src + (dst - src) * e
    p = p + np.array([0.0, 0.0, arc * math.sin(math.pi * k)])
    return p, min(1.0, k * 6.0)


def retint_prop(objs, rules):
    """rules: list of (name substring or '*', hex, role, rough, coat); first match wins per material."""
    done = set()
    for o in objs:
        if o.type != "MESH":
            continue
        for slot in o.material_slots:
            m = slot.material
            if m is None or m.name in done or not m.use_nodes:
                continue
            for sub, hx, role, rough, coat in rules:
                if sub == "*" or sub.lower() in m.name.lower():
                    if not any(n.type == "BSDF_PRINCIPLED" for n in m.node_tree.nodes):          # a non-Principled source material: rebuild it as one
                        m.node_tree.nodes.clear()
                        b = m.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
                        out = m.node_tree.nodes.new("ShaderNodeOutputMaterial")
                        m.node_tree.links.new(b.outputs["BSDF"], out.inputs["Surface"])
                    cr._retint(m, hx, role, rough=rough, coat=coat)
                    done.add(m.name)
                    break


def suitcase(S, loc, rot=(0, 0, 0), name_root="suitcase"):
    a = ar.load(S, "suitcase", loc=loc, rot=rot)
    retint_prop(a.objs, [("*", SUITCASE, "g_mark", 0.45, 0.2)])
    return a


def horse(S, loc, rot=(0, 0, 0)):
    a = ar.load(S, "horse", loc=loc, rot=rot)
    for o in a.objs:
        if o.type in ("CURVES", "CURVE"):
            o.hide_render = True
            o.hide_viewport = True
        for m in o.modifiers:
            if m.type == "PARTICLE_SYSTEM":                                              # tail and mane hair: tens of minutes per Cycles frame (measured 2026-11-09), horse reads without it
                m.show_render = False
                m.show_viewport = False
    retint_prop([o for o in a.objs if o.name == "Horse mane"], [("*", MANE, "rubber_k", 0.7, 0.0)])
    retint_prop([o for o in a.objs if o.type == "MESH" and o.name not in ("Horse mane",)], [("*", HORSE, "g_pin", 0.7, 0.0)])
    return a


def car(S, loc, rot=(0, 0, 0)):
    a = ar.load(S, "cartoon-car", loc=loc, rot=rot)
    retint_prop(a.objs, [("glass", "#CFE4EE", "g_big", 0.1, 0.5), ("black", "#2B2A2E", "rubber_k", 0.5, 0.1), ("tyre", "#2B2A2E", "rubber_k", 0.7, 0.0), ("tire", "#2B2A2E", "rubber_k", 0.7, 0.0),
                         ("rubber", "#2B2A2E", "rubber_k", 0.7, 0.0), ("chrom", "#B9C0C8", "g_pin", 0.2, 0.2), ("*", CAR, "shell_y", 0.35, 0.4)])
    return a


def tank(S, loc, size=(90.0, 60.0, 120.0), wall=1.4):
    """Glass tank (five thin glass slabs) and a water block whose height is set per frame: returns (water_obj, set_level(frac))."""
    frame = S.hero("ink", "#1D1B2E", rough=0.4, coat=0.2)
    wm = rk.water("tank_water", tint="#BFE6F2", density=0.007, absorb="#3C9CC8")
    root = S.empty("tank_root", loc)
    w, d, h = size
    objs = [S.box("tank_base", (w + 2 * wall, d + 2 * wall, wall * 2), (0, 0, wall), frame, bevel=0.4, parent=root)]
    for sx_ in (-1, 1):                                                               # one transmission layer (the water): an opaque frame of four posts and a top rim, no glass walls
        for sy_ in (-1, 1):
            objs.append(S.box(f"tank_post{sx_}{sy_}", (wall * 2, wall * 2, h), (sx_ * (w / 2), sy_ * (d / 2), h / 2), frame, bevel=0.4, parent=root))
    for sy_ in (-1, 1):
        objs.append(S.box(f"tank_rim{sy_}", (w + 2 * wall, wall * 2, wall * 2), (0, sy_ * (d / 2), h), frame, bevel=0.4, parent=root))
    for sx_ in (-1, 1):
        objs.append(S.box(f"tank_rimx{sx_}", (wall * 2, d + 2 * wall, wall * 2), (sx_ * (w / 2), 0, h), frame, bevel=0.4, parent=root))
    full = h - 2 * wall - wall * 2
    water = tr.rbox("tank_water", (w - 2 * wall, d - 2 * wall, 1.0), (0, 0, wall * 2), wm, bevel=0.2, parent=root)      # NOT registered with the shot: the shot's per-frame update would reset its scale
    water.visible_shadow = False

    def level(frac):
        f = max(1e-3, min(1.0, frac))
        water.scale = (1.0, 1.0, full * f)
        water.location = (0, 0, wall * 2 + full * f / 2)
    level(1e-3)
    return water, level, objs


def seesaw(S, pivot, length=1000.0, width=150.0, thick=16.0):
    """Plank on a triangular fulcrum. Returns (root, angle_setter(deg)): positive = right end down. Parts of the heap are rotated about the pivot by the caller."""
    ink = S.hero("ink", "#1D1B2E", rough=0.45, coat=0.2)
    plank_m = S.hero("g_board", "#4B3A5A", rough=0.5, coat=0.2)
    fulc = S.box("fulcrum", (60.0, width * 0.7, 70.0), (pivot[0], pivot[1], 35.0), ink, bevel=3.0)
    root = S.empty("plank_root", pivot)
    S.box("plank", (length, width, thick), (0, 0, 0), plank_m, bevel=2.0, parent=root)
    return root, fulc


def widen_floor(k=6.0):
    """The stage floor is a finite shadow-catcher plane: scale it for wide shots so its edge never shows."""
    fl = bpy.data.objects.get("floor")
    if fl is not None:
        fl.scale = (fl.scale[0] * k, fl.scale[1] * k, fl.scale[2])


def rot_y(points, ang_deg, pivot):
    """Rotate (n,3) points about the y axis through pivot; positive angle = +x end goes down."""
    a = math.radians(ang_deg)
    p = np.asarray(points, dtype=float) - np.asarray(pivot)
    x = p[:, 0] * math.cos(a) + p[:, 2] * math.sin(a)
    z = -p[:, 0] * math.sin(a) + p[:, 2] * math.cos(a)
    return np.stack([x, p[:, 1], z], axis=1) + np.asarray(pivot)
