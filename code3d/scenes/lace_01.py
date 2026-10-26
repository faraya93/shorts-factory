"""v5-drawn scene 1 (setup): a closed boot seam opens into a very wide gap; two chubby fingers reach toward each other and stop short.
Slot 242 frames (8.07 s). Run through factory/code3d_render.py (scene_script_prefix 'lace')."""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402

args, production, stage, m, SLOT = lw.begin(242)
T, ROWS, HX = SLOT / c.FPS, lw.ROWS, 1.4

tongue = sh.rounded_bar("tongue", 2.0, 5.25, 0.2, m.red, loc=(0, 0.35, -0.32))
roots, tabs = {}, {}
for side in (-1, 1):
    root = lw.empty(f"root_{side}")
    roots[side] = root
    lw.parent(sh.rounded_bar(f"flap_{side}", HX, 4.7, 0.35, m.skin), root, (side * HX, 0, 0))
    for y in ROWS:
        lw.parent(sh.ring("eyelet", 0.3, 0.1, m.steel), root, (side * 0.7, y, 0.4))
    tabs[side] = sh.ellipsoid(f"tab_{side}", 0.8, 0.4, 0.3, m.skin)       # a tapered finger, hidden inside its flap at first
    lw.parent(tabs[side], root)


def update(scene_):
    t = scene_.frame_current / c.FPS
    g = 0.3 + 3.1 * c.smooth(1.2, 3.6, t)                                   # the cut opens into a very wide gap
    reach = -0.9 + 2.0 * c.smooth(3.8, 6.2, t) + 0.05 * math.sin(2 * math.pi * 2.2 * (t - 6.2)) * c.smooth(6.2, 6.8, t) * (t > 6.2)
    for side in (-1, 1):
        roots[side].location.x = side * g / 2
        tabs[side].location.x = -side * reach + side * 0.8                  # tip at the flap edge minus `reach`, body behind it
    tongue.scale.x = (g / 2 + 0.1) / 2.0
    k = c.smooth(0.0, T, t)
    lw.look(stage, (0, 0, 0.2), 22.0 - 2.5 * k, 74)


lw.finish(stage, args, SLOT, update, "lace-01")
