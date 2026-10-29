"""reloj-coral scene 1 (hook-contraste). Slot 279 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import clock_rig as cr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(279, floor_z=-2.7)
T = SLOT / c.FPS
K = cr.Clock(m)
cx, zc = cr.CENTRE


def update(scene_):
    t = scene_.frame_current / c.FPS
    K.dial_to(0.0)
    K.set_gears(0.0)
    K.set_minute_turns(1.1 * c.smooth(0.2, T, t) + 0.05 * t)
    u = c.smooth(0, T, t)
    tr.look(stage, (cx, 0, zc - 0.2), 31.0 - 3.0 * u, 13.0, -8.0 + 14.0 * u)

stage.run(update, args, SLOT, "clock-01")
