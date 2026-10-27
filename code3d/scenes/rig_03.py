"""v7-drawn scene 3 (knots): seen from above, a thread end ties a small knot; the stitch repeats along the closed wound, each
knot popping in; one stitch with no knot slips out sideways while the knotted ones hold (gold tension). Slot 133 frames (4.43 s)."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import dark_rig as dr  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = dr.begin(133)
T = SLOT / c.FPS
W = dr.Wound(m)
W.set_gap(0.16)
YS = [-1.2, -0.6, 0.0, 0.6, 1.2]
UNKNOTTED = 3
stitches, knots = [], []
for i, y in enumerate(YS):
    stitches.append(s.Thread(m.gold if i != UNKNOTTED else m.dark, points=60, thickness=0.06))
    knots.append(sh.ellipsoid("knot", 1.0, 1.0, 1.0, m.gold, loc=(0, y, 0.12), segments=24, rings=12))


def update(scene_):
    t = scene_.frame_current / c.FPS
    for i, y in enumerate(YS):
        t0 = 0.15 + 0.5 * i                                    # each stitch lays down, then ties
        lay = c.smooth(t0, t0 + 0.35, t)
        slip = c.smooth(2.8, 3.4, t) if i == UNKNOTTED else 0.0
        x0, x1 = -1.2 + 2.6 * slip, 1.2 + 2.6 * slip
        pts = [Vector((x0 + (x1 - x0) * u * lay, y, 0.10 + 0.12 * math.sin(math.pi * u))) for u in [k / 20 for k in range(21)]]
        stitches[i].set(s.resample(pts + [pts[-1]], 60))
        kp = dr.back((t - (t0 + 0.4)) / 0.3, 2.2) if i != UNKNOTTED else 0.0
        knots[i].scale = (0.16 * kp,) * 3
        dr.show(knots[i], kp > 0.02)
        stitches[i].obj.location.x = 0.0
    k = c.smooth(0.0, T, t)
    dr.look(stage, (0, 0.0 + 0.4 * k, 0.0), 12.0 - 3.5 * k, 50 - 10 * k, -12 + 22 * k)


stage.run(update, args, SLOT, "rig-03")
