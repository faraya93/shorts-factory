"""Rig for 011 (palomitas-por-que-explota-el-maiz): palette, kernel layers (shell, starch, water drop), popcorn puff (one joined mesh of cream spheres), pressure dial."""
import math
import random
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402

KERNEL, SHELL, STARCH, DROP, FOAM, STEEL, OIL, GEL = "#A8650F", "#C98A1E", "#FFE9B8", "#2E7FE0", "#FFF6E6", "#C9CED6", "#E8A33D", "#FFD98A"


def palette(S):
    return {"kernel": S.hero("housing", KERNEL, rough=0.4, coat=0.4), "shell": S.hero("housing", SHELL, rough=0.25, coat=0.3, alpha=0.5), "starch": S.hero("blade", STARCH, rough=0.5, alpha=0.62),
            "gel": S.hero("blade", GEL, rough=0.35, coat=0.3), "drop": S.hero("big", DROP, rough=0.1, coat=0.6), "steam": S.glass("#FFFFFF", alpha=0.5, rough=0.1, name="foam"),
            "foam": S.hero("big", FOAM, rough=0.8, coat=0.0), "steel": S.hero("rubber", STEEL, rough=0.3, metal=0.6, coat=0.0), "oil": S.hero("small", OIL, rough=0.15, coat=0.0, alpha=0.8),
            "shard": S.hero("mark", "#7A430C", rough=0.5), "plate": S.plate_mat(), "board": S.board_mat()}


def puff(S, M, name="puff", mat=None):
    """Popcorn piece as ONE mesh: six overlapping cream spheres (about 3 units across)."""
    m = mat or M["foam"]
    parts = [mk.sphere(f"{name}{i}", m, r, p, seg=16) for i, (p, r) in enumerate((((0, 0, 0), 1.0), ((0.9, 0.2, 0.3), 0.8), ((-0.8, 0.1, 0.4), 0.8), ((0.2, 0.8, 0.9), 0.7), ((-0.1, -0.7, 0.8), 0.7), ((0.1, 0, 1.3), 0.75)))]
    bpy.ops.object.select_all(action="DESELECT")
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = name
    return S.reg(o)


def kernel_layers(S, M, C, big=3.4, t_xray=1.3, pop_at=0.2):
    """Big kernel: opaque gold kernel that fades out at t_xray while the translucent shell, starch core and the water drop show. Returns dict of objects."""
    k = S.ball("kern", M["kernel"], 1.0, C, shape=(1.0 * big, 0.85 * big, 1.3 * big), pop=(pop_at, 0.5), seg=40)
    S.gone(k, t_xray, 0.4)
    sh = S.ball("shell", M["shell"], 1.0, C, shape=(1.0 * big, 0.85 * big, 1.3 * big), pop=(t_xray, 0.4), seg=40)
    core = S.ball("core", M["starch"], 1.0, C, shape=(0.82 * big, 0.68 * big, 1.1 * big), pop=(t_xray, 0.4), seg=32)
    drop = S.ball("drop", M["drop"], 0.6, (C[0], C[1] - 0.2, C[2] - 0.2), shape=(big * 0.55 / 1.0,) * 3 if False else (1, 1, 1), pop=(t_xray + 0.3, 0.4), seg=24)
    return {"kern": k, "shell": sh, "core": core, "drop": drop}


def dial(S, M, loc, r=2.4, t0=0.3, max_ang=2.2):
    """Pressure dial facing the camera: disc, ring, needle (rotates about y). Returns (needle, set_pressure(k in 0..1))."""
    disc = S.cyl("dial", r, 0.5, loc, M["plate"], axis="Y", verts=48, bevel=0.05, pop=(t0, 0.4))
    ring = S.torus("dring", r, 0.18, (loc[0], loc[1] - 0.2, loc[2]), M["steel"], rot=(math.pi / 2, 0, 0), pop=(t0, 0.4))
    needle = S.box("needle", (0.18, 0.14, r * 0.85), (loc[0], loc[1] - 0.45, loc[2]), S.accent, bevel=0.04, pop=(t0 + 0.1, 0.3))
    for i in range(9):
        a = -max_ang + 2 * max_ang * i / 8
        S.box(f"tick{i}", (0.14, 0.1, 0.45), (loc[0] + math.sin(a) * r * 0.86, loc[1] - 0.3, loc[2] + math.cos(a) * r * 0.86), S.ink, bevel=0.03, rot=(0, a, 0), pop=(t0 + 0.1, 0.3))

    def setp(k):
        a = -max_ang + 2 * max_ang * k
        needle.rotation_euler = (0, a, 0)
        needle.location = (loc[0] + math.sin(a) * r * 0.42, loc[1] - 0.45, loc[2] + math.cos(a) * r * 0.42)
    return needle, setp
