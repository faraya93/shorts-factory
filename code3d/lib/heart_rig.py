"""Rig for 010 (corazon-botellas-al-dia): palette, a stylised pump-heart (chunky solids, beating), soda-like bottles (one joined mesh), pools. No anatomy, no realism."""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402

WINE, FLUID, CAP, SHIRT, SKINTONE, POOL = "#1F2F7A", "#E8553C", "#F6F1E8", "#2F7DE6", "#FFD9B8", "#3FC1E8"
BEAT = 0.857            # 70 beats per minute


def palette(S):
    return {"wine": S.hero("big", WINE, rough=0.35, coat=0.4), "fluid": S.hero("housing", FLUID, rough=0.2, coat=0.4), "glass": S.glass("#FFFFFF", alpha=0.3, rough=0.05, name="foam"),
            "cap": S.hero("blade", CAP, rough=0.4), "shirt": S.hero("small", SHIRT, rough=0.5), "skin": S.hero("mark", SKINTONE, rough=0.55), "pool": S.glass(POOL, alpha=0.7, rough=0.05),
            "plate": S.plate_mat(), "board": S.board_mat()}


def beat(t, t0=0.0):
    """0..1 heartbeat bump, a sharp squeeze every BEAT seconds."""
    if t < t0:
        return 0.0
    k = ((t - t0) % BEAT) / BEAT
    return math.sin(min(1.0, k * 2.4) * math.pi) ** 2 if k < 0.42 else 0.0


def pump_heart(S, M, loc, scale=1.0, pop=0.2, amp=0.1, t_beat=0.0):
    """Heart-shaped pump on an UNREGISTERED root (so the beat can drive its scale); pops in at `pop`, beats every BEAT s from t_beat."""
    root = tr.empty("heart", loc)
    S.ball("hA", M["wine"], 2.6, (0, 0, 0), shape=(1.0, 0.85, 1.1), parent=root, seg=32)
    S.ball("hB", M["wine"], 2.1, (1.9, -0.1, 0.9), parent=root, seg=32)
    S.cone("hC", 2.5, 0.35, 3.0, (-0.6, 0, -2.8), M["wine"], rot=(0, math.radians(15), 0), parent=root)
    S.cyl("hT1", 0.55, 2.8, (0.2, 0, 3.4), M["wine"], axis="Z", parent=root, verts=24)
    S.cyl("hT2", 0.45, 2.4, (1.9, 0, 3.0), M["wine"], axis="Z", parent=root, verts=24)

    def upd(t):
        f = 1e-4 if t < pop else max(1e-4, tr.back((t - pop) / 0.5))
        k = 1.0 + amp * beat(t, t_beat)
        root.scale = (scale * f * k,) * 3
    S.every_frame(upd)
    return root


def bottle(S, M, name="bottle"):
    """Full bottle standing on z=0: glass body + fluid + neck + cap, ONE mesh (3 materials)."""
    parts = [tr.cyl(name + "_g", 0.95, 3.0, (0, 0, 1.5), M["glass"], axis="Z", verts=24, bevel=0.1), tr.cyl(name + "_f", 0.82, 2.3, (0, 0, 1.3), M["fluid"], axis="Z", verts=24),
             tr.cyl(name + "_n", 0.38, 0.9, (0, 0, 3.4), M["glass"], axis="Z", verts=16), tr.cyl(name + "_c", 0.46, 0.3, (0, 0, 3.95), M["cap"], axis="Z", verts=16)]
    bpy.ops.object.select_all(action="DESELECT")
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = name
    return S.reg(o)
