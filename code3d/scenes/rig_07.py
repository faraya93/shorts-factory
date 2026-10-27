"""v7-drawn scene 7 (reframe + CTA backdrop): the single image of the video. A grey, inert thread holds the two lips; beneath it a
gold fibre bridge grows across the gap from the bottom up until it is complete. Nothing else moves; slow orbit only.
Slot 332 frames (11.07 s)."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import dark_rig as dr  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = dr.begin(332)
T = SLOT / c.FPS
W = dr.Wound(m)
G = 0.62
W.set_gap(G)
FR = dr.FRONT
stitch = s.Thread(m.thread, points=80, thickness=0.06)
Z = [-1.25 + 0.17 * i for i in range(7)]                                   # fibre levels from the bottom of the V upward
fibres = []
for z in Z:
    half = (G / 2) * max(0.0, 1.0 - (-z) / dr.APEX) + 0.05
    fibres.append((sh.rounded_bar("fibre", half, 0.05, 0.045, m.gold, loc=(0, FR + 0.1, z)), half))
glow = sh.ellipsoid("bridge_glow", 1.0, 0.2, 1.0, m.gold_soft, loc=(0, FR + 0.1, -0.7), segments=24, rings=12)


def update(scene_):
    t = scene_.frame_current / c.FPS
    top = [Vector((-0.9 + 1.8 * u / 30, FR, 0.15 + 0.25 * math.sin(math.pi * u / 30))) for u in range(31)]
    stitch.set(s.resample(top + [top[-1]], 80))
    dim = 1.0 - 0.5 * c.smooth(0.4, 1.0, t)                                  # "no cierra": the thread stays, inert
    grow = c.smooth(1.0, 6.2, t) * len(fibres)
    for i, (f, half) in enumerate(fibres):
        k = min(1.0, max(0.0, grow - i))
        f.scale = (max(0.001, k), 1.0, 1.0)
        dr.show(f, k > 0.01)
    gz = (-1.25 + 0.17 * min(len(fibres) - 1, grow)) if grow > 0.01 else -5.0
    glow.scale = (0.5 + 0.15 * min(grow, 7.0) / 7.0, 0.2, 0.15 + 0.35 * min(grow, 7.0) / 7.0)
    glow.location = (0.0, FR + 0.15, -1.25 + 0.17 * 3.0 * min(1.0, grow / 7.0) if grow > 0.01 else -500.0)
    p = c.smooth(0.0, T, t)
    dr.look(stage, (0.0, 0, -0.9), 12.0 - 2.0 * p, 8 + 8 * p, -22 + 40 * p)


stage.run(update, args, SLOT, "rig-07")
