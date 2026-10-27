"""v7-drawn scene 5 (the risk): a dark thread stays in the wound while new skin, gold with growth, rises from both lips and buries
it; tweezers pull and the new skin tents upward and resists (red flash). Slot 185 frames (6.17 s)."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import dark_rig as dr  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = dr.begin(185)
T = SLOT / c.FPS
W = dr.Wound(m)
W.set_gap(1.0)
FR = dr.FRONT
thread = s.Thread(m.dark, points=60, thickness=0.06)
grow = {side: sh.rounded_bar(f"new_skin_{side}", 0.5, 0.8, 0.45, m.skin_new, loc=(side * 0.45, FR + 0.1, -0.45)) for side in (-1, 1)}
flash = sh.ellipsoid("flash", 1.0, 1.0, 1.0, m.red, loc=(0, FR - 0.1, -0.1), segments=24, rings=12)
tw_root, tw_piv = dr.tweezers(m)


def update(scene_):
    t = scene_.frame_current / c.FPS
    g = c.smooth(0.8, 3.6, t)
    for side, b in grow.items():
        b.scale = (0.05 + 0.95 * g, 1.0, 0.1 + 0.9 * g)
        b.location = (side * (0.55 - 0.18 * g), FR + 0.1, -0.35 - 0.2 * g + 0.25 * g)
    tent = c.smooth(4.3, 5.1, t) * (1 - c.smooth(5.5, 6.1, t))
    top = Vector((0.0, FR, -0.2 + 0.7 * tent))
    pts = [Vector((0.0, FR, -1.2)), Vector((0.0, FR, -0.7)), top]
    thread.set(s.resample(pts + [pts[-1]], 60))
    tw_root.location = (0.0, FR - 0.15, top.z + 0.1 + 1.4 * (1 - c.smooth(2.4, 3.6, t)))
    for pivot, sign in tw_piv:
        pivot.rotation_euler.y = sign * (0.12 * (1 - c.smooth(3.4, 3.9, t)) + 0.02)
    fs = tent * 0.55
    flash.scale = (fs, fs * 0.4, fs)
    dr.show(flash, fs > 0.03)
    k = c.smooth(0.0, T, t)
    dr.look(stage, (0.0, 0, -0.8 - 0.4 * k), 14.0 - 4.0 * k, 8 + 8 * k, -12 + 24 * k)


stage.run(update, args, SLOT, "rig-05")
