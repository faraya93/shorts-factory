"""v7-drawn scene 6 (the ants): a chunky black ant walks to the wound, bites both lips and clamps them together like a staple; two
more clamp along the wound until it is closed. Stylized, no gore. Slot 227 frames (7.57 s)."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import dark_rig as dr  # noqa: E402

args, production, stage, m, SLOT = dr.begin(227)
T = SLOT / c.FPS
W = dr.Wound(m)
ants = []
for i, (y, t_arrive) in enumerate(((-1.3, 2.3), (-0.1, 4.0), (1.1, 5.4))):          # the farthest ant first, so nobody walks through another
    root, jaws = dr.ant(m, 0.9)
    ants.append((root, jaws, y, t_arrive))


def update(scene_):
    t = scene_.frame_current / c.FPS
    for root, jaws, y, ta in ants:
        walk = c.smooth(ta - 1.8, ta - 0.5, t)
        turn = c.smooth(ta - 0.6, ta, t)
        bite = c.smooth(ta, ta + 0.4, t)
        live = t > ta - 1.8
        root.location = (0.55 * turn, y + 5.0 * (1 - walk), 0.30 + 0.05 * math.sin(10 * t) * (1 - turn))
        root.rotation_euler.z = math.radians(90 - 90 * turn)
        for pivot, side in jaws:
            pivot.rotation_euler.z = -side * math.radians(60) * (1 - bite)
        root["home_z"] = 0.30
        root.location.z = root.location.z if live else -500.0
    W.set_gap(1.0 - 0.80 * min(1.0, sum(c.smooth(ta + 0.1, ta + 0.8, t) for _, _, _, ta in ants) / 3.0))
    p = c.smooth(0.0, T, t)
    dr.look(stage, (0.0, 0.0 - 0.2 * p, -0.2), 12.5 - 3.0 * p, 40 - 6 * p, -30 + 44 * p)


stage.run(update, args, SLOT, "rig-06")
