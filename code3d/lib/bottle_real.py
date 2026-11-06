"""Real bottles for 010 (every-element remake 2026-11-05): a transparent PET water bottle (lathe shell with wall thickness, refracting), the liquid inside it (a separate lathe whose z scale is the fill level),
a white cap, a clear pumping tube with red slugs that travel along it. Runs inside Blender, Cycles `transparent` profile."""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import real_kit as rk  # noqa: E402

R, H_BODY, NECK_R, H_TOT = 3.3, 11.5, 1.45, 17.0
OUT = [(0.0, 0.0), (2.4, 0.0), (3.0, 0.5), (R, 1.4), (R, H_BODY), (2.9, 12.8), (2.0, 14.0), (NECK_R, 15.0), (NECK_R, H_TOT - 0.4), (NECK_R + 0.25, H_TOT - 0.3), (NECK_R + 0.25, H_TOT)]


def _inner(wall):
    pts = [(max(r - wall, 0.0), z + (wall if i < 3 else 0.0)) for i, (r, z) in enumerate(OUT)]
    return pts


def pet_mat():
    m = rk.glass("clear_pet", "#EAF4FA", rough=0.04)
    next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["IOR"].default_value = 1.45
    return m


def parts(S, loc=(0, 0, 0), wall=0.16, tint="#C8323C", density=0.0, level=1.0, with_cap=True, seg=40):
    """Returns dict(shell, liquid, cap). liquid z-scale (about the bottle base) is the fill level: set it with S.size or directly."""
    outer = OUT
    inner = _inner(wall)
    prof = outer[:-1] + [(outer[-1][0], outer[-1][1])] + [(inner[-1][0], inner[-1][1])] + inner[::-1][1:]
    shell = rk.lathe("bottle_shell", [(0.0, 0.0)] + outer[1:] + [(NECK_R + 0.25 - wall, H_TOT)] + inner[::-1][:-1][1:] + [(0.0, wall)], pet_mat(), loc=loc, seg=seg, max_len=2.5)
    liq_prof = [(0.0, wall + 0.05)] + [(max(r - wall - 0.06, 0.0), z) for r, z in inner[1:9]] + [(0.0, inner[8][1])]
    mat = rk.water("clear_water", "#F6DADA" if tint else "#E8F6FB", density=0.0)
    liquid = rk.lathe("bottle_liquid", liq_prof, mat, loc=loc, seg=seg, max_len=2.5)
    rk.noshadow(shell, liquid)
    P = {"shell": S.reg(shell), "liquid": S.reg(liquid)}
    if with_cap:
        cap = S.cyl("bottle_cap", NECK_R + 0.35, 1.5, (loc[0], loc[1], loc[2] + H_TOT + 0.4), rk.wet_tissue("g_mark", "#FFFFFF", sss=0.0, rough=0.4, coat=0.2), axis="Z", verts=32, bevel=0.15)
        P["cap"] = cap
    return P


def tube_path(S, pts, radius=0.32):
    """A clear tube along pts (list of xyz). Returns the object."""
    o, cu = rk.tube(S, "pump_tube", pts, [radius] * len(pts), rk.glass("clear_glass", "#EAF6F3"))
    rk.noshadow(o)
    return o


def path_point(pts, u):
    """Position at fraction u (0..1) along the polyline."""
    segs = [(Vector(a), Vector(b)) for a, b in zip(pts, pts[1:])]
    lens = [(b - a).length for a, b in segs]
    d = max(0.0, min(1.0, u)) * sum(lens)
    for (a, b), L in zip(segs, lens):
        if d <= L:
            return tuple(a + (b - a) * (d / L if L else 0))
        d -= L
    return tuple(segs[-1][1])
