"""reloj-coral scene 7 (cta). Slot 162 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import clock_rig as cr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(162, floor_z=-2.7)
T = SLOT / c.FPS
K = cr.Clock(m)
cx, zc = cr.CENTRE


def update(scene_):
    t = scene_.frame_current / c.FPS
    K.dial_to(0.0)
    K.set_gears(0.0)
    K.set_minute_turns(0.3 * t, 0.0)
    u = c.smooth(0, T, t)
    tr.look(stage, (cx, 0, zc - 0.2), 31.0 + 2.0 * u, 4.0, 0.0 + 4.0 * u)

stage.run(update, args, SLOT, "clock-07")
