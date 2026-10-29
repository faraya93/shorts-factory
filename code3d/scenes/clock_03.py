"""reloj-coral scene 3 (tres-por-cuatro). Slot 186 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import clock_rig as cr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(186, floor_z=-2.7)
T = SLOT / c.FPS
K = cr.Clock(m)
cx, zc = cr.CENTRE


def update(scene_):
    t = scene_.frame_current / c.FPS
    K.dial_to(1.0)
    K.set_gears(1.0)
    K.set_minute_turns(1.0 * t)
    u = c.smooth(0, T, t)
    tr.look(stage, (cx, 0, zc), 23.0 + 11.0 * u, 7.0 - 2.0 * u, -10.0 + 8.0 * u)

stage.run(update, args, SLOT, "clock-03")
