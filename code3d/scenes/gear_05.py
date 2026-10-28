"""scene 5: force. The output gear's arm (ink) lifts a heavy block; the camera stays on the last stages. Output sweeps -35 -> +35 deg (6.8 s)
while shafts 3-4 follow at 4x/16x its rate (only they are in frame). Slot 285 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import gear_rig as gr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(285, floor_z=-5.1)
T = SLOT / c.FPS
A = gr.Train(m)
ex, ez = A.shaft[5]
mats = gr.Train._materials(m)
block = gr.block_and_floor(m, ex + 3.0, ez - 1.0)
ARM_L = 3.9


def update(scene_):
    t = scene_.frame_current / c.FPS
    s = c.smooth(1.2, 8.0, t)
    th5 = A.angles(0.0)[5]
    ang = math.radians(-35 + 70 * s)
    A.set_input(A.input_for_output(ang))                          # output gear angle = ang (arm local +x points along the gear's own angle)
    tipx, tipz = ex + ARM_L * math.cos(ang), ez + ARM_L * math.sin(ang)
    block.location = (tipx + 0.2, A.arm_y, tipz + 1.55)
    u = c.smooth(0, T, t)
    tr.look(stage, (ex + 0.8, 0, ez - 0.5 + 1.2 * s), 26.0 - 2.0 * u, 6.0 + 2.0 * u, -10.0 - 10.0 * u)


stage.run(update, args, SLOT, "gear-05")
