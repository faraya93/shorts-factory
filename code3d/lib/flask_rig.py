"""Rig for 009 (termo-por-que-mantiene-el-calor): a vacuum flask (lathe-turned body + cap), its flat section (two walls, a vacuum gap, coffee), and heat as accent particles.
Geometric hero ('thermos', code-primitive). Section dimensions are in the module constants."""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402

STEEL, CAP, COFFEE = "#6E7886", "#2B2B33", "#6B3E1F"
PROFILE = [(0.0, 0.0), (3.6, 0.0), (4.1, 0.8), (4.2, 3.5), (4.2, 27.0), (4.0, 28.5), (3.2, 29.4), (2.9, 29.8), (2.9, 30.2), (0.0, 30.2)]
CAP_Z, CAP_UP = 32.8, 43.0
HW, T, GAP = 5.0, 0.45, 0.9          # section: outer half-width, wall thickness, gap
XO, XG, XI = HW - T / 2, HW - T - GAP / 2, HW - T - GAP - T / 2      # centres: outer wall, gap, inner wall
XC = HW - 2 * T - GAP                 # coffee half-width


def palette(S):
    return {"steel": S.hero("big", STEEL, rough=0.25, metal=0.85, coat=0.1), "enamel": S.hero("big", "#2D6FB7", rough=0.3, coat=0.3), "mirror": S.hero("blade", "#4F6070", rough=0.04, metal=1.0, coat=0.0),
            "cap": S.hero("rubber", CAP, rough=0.5), "coffee": S.hero("housing", COFFEE, rough=0.35, alpha=0.92), "plate": S.plate_mat(),
            "heat": S.emit("#3A2BD0", 1.0, "gold"), "photon": S.emit("#3A2BD0", 1.0, "gold_dim"), "steam": S.hero("foam", "#FFFFFF", rough=0.9, coat=0.0, alpha=0.6),
            "ring": S.emit("#B3261E", 1.0, "red")}


def flask(S, M, loc=(0, 0, 0), cap_pop=None, cap=True):
    """Exterior: a lathe body (one mesh) and a dark cap. Returns (body, cap or None)."""
    seg, verts, faces = 40, [], []
    rings = []
    for (r, z) in PROFILE:
        rings.append(len(verts))
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((r * math.cos(a), r * math.sin(a), z))
    for ri in range(len(PROFILE) - 1):
        for i in range(seg):
            a, b = rings[ri] + i, rings[ri] + (i + 1) % seg
            c_, d = rings[ri + 1] + (i + 1) % seg, rings[ri + 1] + i
            faces.append((a, b, c_, d))
    mesh = bpy.data.meshes.new("flask")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for p in mesh.polygons:
        p.use_smooth = True
    mesh.materials.append(M["enamel"])
    o = bpy.data.objects.new("flask", mesh)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    S.reg(o)
    c = None
    S.torus("flask_handle", 3.4, 0.5, (loc[0] + 4.8, loc[1], loc[2] + 15.0), M["cap"], rot=(math.pi / 2, 0, 0))
    for i, zz in enumerate((2.2, 26.0)):
        S.torus(f"flask_band{i}", 4.25, 0.35, (loc[0], loc[1], loc[2] + zz), M["steel"])
    if cap:
        c = S.empty("flask_cupcap", (loc[0], loc[1], loc[2] + CAP_Z))
        S.cyl("cup", 4.55, 5.6, (0, 0, 0), M["cap"], axis="Z", verts=48, bevel=0.5, parent=c)
        S.cyl("cup_knob", 1.0, 1.2, (0, 0, 3.2), M["steel"], axis="Z", verts=24, bevel=0.2, parent=c)
        for i, dz in enumerate((-1.6, 0.0, 1.6)):
            S.torus(f"cup_rib{i}", 4.6, 0.22, (0, 0, dz), M["cap"], parent=c)
    return o, c


def section(S, M, mirror=False, lid=True):
    """Flat section facing the camera. Returns a dict of the parts."""
    P = {}
    S.box("sec_plate", (30, 1.0, 34), (0, 2.4, 11), M["plate"], bevel=0.4)
    wall = M["mirror"] if mirror else M["steel"]
    P["outer"] = [S.box(f"outer{s}", (T, 1.0, 20.0), (s * XO, 0, 10.0), M["steel"], bevel=0.12) for s in (-1, 1)]
    P["inner"] = [S.box(f"inner{s}", (T, 1.0, 17.6), (s * XI, 0, 10.4), wall, bevel=0.12) for s in (-1, 1)]
    P["base_o"] = S.box("base_o", (2 * HW, 1.0, T), (0, 0, T / 2), M["steel"], bevel=0.1)
    P["base_i"] = S.box("base_i", (2 * (XI + T / 2), 1.0, T), (0, 0, 1.6), wall, bevel=0.1)
    P["coffee"] = S.box("coffee", (2 * XC, 0.8, 14.6), (0, 0.0, 1.85 + 7.3), M["coffee"], bevel=0.3)
    if lid:
        P["lid"] = S.box("sec_lid", (2 * HW - 0.4, 1.1, 2.6), (0, 0, 21.3), M["cap"], bevel=0.4)
    return P


def heat(S, M, n, fn, r=0.8):
    """n heat particles (one template + linked copies); fn(i, t) -> (xyz, scale) or None."""
    tpl = S.ball("heat_tpl", M["heat"], r, (0, 0, 0))
    return S.swarm(n, tpl, fn)
