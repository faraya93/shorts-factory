"""scene 4: the first gear turns once per second (0-2.1 s, input vermilion) then the camera climbs to the LAST gear, which makes ONE full turn
while the Editor timer runs to 17 min (a time-lapse: only the last stages are in frame). Slot 172 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import gear_rig as gr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(172, floor_z=-5.1)
T = SLOT / c.FPS
A = gr.Train(m)
sx, sz = A.shaft[0]
ex, ez = A.shaft[5]


def update(scene_):
    t = scene_.frame_current / c.FPS
    if t < 2.35:                                   # real speed: 1 turn per second at the input
        A.set_input(2 * math.pi * t)
    else:                                          # time-lapse on the output gear: exactly one turn between 2.7 s and 5.3 s
        th5 = 2 * math.pi * c.smooth(2.7, 5.3, t) * 1.0
        th0_real = 2 * math.pi * 2.35
        A.set_input(A.input_for_output(A.angles(th0_real)[5] - th5))   # continuous at 2.35 s, then the output advances one turn
    u = c.smooth(1.4, 3.0, t)
    tr.look(stage, (sx + (ex - sx) * u, 0, sz + (ez - sz) * u), 14.0 + 10.0 * u, 6.0, -6.0 - 8.0 * c.smooth(0, T, t))


stage.run(update, args, SLOT, "gear-04")
