"""reloj-coral scene 5 (comprueba). Slot 183 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import clock_rig as cr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(183, floor_z=-2.7)
T = SLOT / c.FPS
K = cr.Clock(m)
cx, zc = cr.CENTRE


def update(scene_):
    t = scene_.frame_current / c.FPS
    K.dial_to(1.0 - c.smooth(0.0, 1.2, t))
    K.set_gears(1.0 - c.smooth(0.5, 1.2, t))
    K.set_minute_turns(c.smooth(1.4, 5.2, t), 0.0)
    u = c.smooth(0, T, t)
    tr.look(stage, (cx, 0, zc - 0.2), 29.0 - 3.0 * u, 3.0, 8.0 - 14.0 * u)

stage.run(update, args, SLOT, "clock-05")
