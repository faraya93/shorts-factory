"""reloj-coral scene 4 (un-dia). Slot 229 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import clock_rig as cr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(229, floor_z=-2.7)
T = SLOT / c.FPS
K = cr.Clock(m)
cx, zc = cr.CENTRE


def update(scene_):
    t = scene_.frame_current / c.FPS
    K.dial_to(1.0)
    K.set_gears(1.0)
    K.set_minute_turns(1.35 * t)
    u = c.smooth(0, T, t)
    tr.look(stage, (cx, 0, zc + 0.3 - 0.5 * u), 30.0 - 8.0 * c.smooth(0, 3.0, t) + 10.0 * c.smooth(3.5, T, t), 5.0, -2.0 + 6.0 * u)

stage.run(update, args, SLOT, "clock-04")
