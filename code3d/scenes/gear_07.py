"""scene 7: the chain at rest behind the CTA phone (Editor overlay): slow input, slow orbit. Slot 155 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import gear_rig as gr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(155, floor_z=-5.1)
T = SLOT / c.FPS
A = gr.Train(m)
ex, ez = A.shaft[5]
block = gr.block_and_floor(m, ex + 3.0, ez - 1.0)
cx, cz = 1.9, 8.2


def update(scene_):
    t = scene_.frame_current / c.FPS
    ang = math.radians(41)
    A.set_input(A.input_for_output(ang) + 2 * math.pi * 0.25 * t)
    tipx, tipz = ex + 3.9 * math.cos(ang), ez + 3.9 * math.sin(ang)
    block.location = (tipx + 0.2, A.arm_y, tipz + 1.55)
    u = c.smooth(0, T, t)
    tr.look(stage, (cx, 0, cz - 1.6), 48.0, 6.0, -6.0 - 8.0 * u)


stage.run(update, args, SLOT, "gear-07")
