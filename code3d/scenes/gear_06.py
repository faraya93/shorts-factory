"""scene 6 (REFRAME, one single image): the whole chain, tiny vermilion crank at the bottom, heavy block lifted at the top. Slow input, camera
pulls back and settles. Slot 151 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import gear_rig as gr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(151, floor_z=-5.1)
T = SLOT / c.FPS
A = gr.Train(m)
ex, ez = A.shaft[5]
block = gr.block_and_floor(m, ex + 3.0, ez - 1.0)
ARM_L = 3.9
cx, cz = 1.9, 8.2


def update(scene_):
    t = scene_.frame_current / c.FPS
    ang = math.radians(35 + 6 * c.smooth(0, T, t))
    A.set_input(A.input_for_output(ang))
    tipx, tipz = ex + ARM_L * math.cos(ang), ez + ARM_L * math.sin(ang)
    block.location = (tipx + 0.2, A.arm_y, tipz + 1.55)
    u = c.smooth(0, 2.2, t)
    tr.look(stage, (cx + 0.6 * (1 - u) + 0.0, 0, cz + 0.6 - 2.2 * u), 30.0 + 18.0 * u, 6.0, -12.0 + 6.0 * c.smooth(0, T, t))


stage.run(update, args, SLOT, "gear-06")
