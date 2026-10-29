"""reloj-coral scene 2 (detras-de-la-esfera). Slot 296 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import clock_rig as cr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(296, floor_z=-2.7)
T = SLOT / c.FPS
K = cr.Clock(m)
cx, zc = cr.CENTRE


def update(scene_):
    t = scene_.frame_current / c.FPS
    lift = c.smooth(0.5, 3.2, t)
    K.dial_to(lift)
    K.set_gears(c.smooth(0.7, 1.5, t))
    K.set_minute_turns(0.5 * t)
    u = c.smooth(0.3, T, t)
    tr.look(stage, (cx, 0, zc + 0.5 * u), 34.0 - 11.0 * u, 5.0 + 2.0 * u, 6.0 - 16.0 * u)

stage.run(update, args, SLOT, "clock-02")
