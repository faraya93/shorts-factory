"""engranajes-papel scene 1 (HOOK = contrast): two meshing pairs on one stage, same input speed. Top: equal gears 1:1 (both turn alike);
bottom: pinion 10 -> big 40 (the big one barely moves). Slot 249 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import gear_rig as gr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(249, floor_z=-7.6)
T = SLOT / c.FPS
mats = gr.Train._materials(m)
Y = 0.6
tp = gr.Gear("t_pin", 20, (-1.6, 4.0), Y, mats["input"], marker=mats["marker"])
tq = gr.Gear("t_par", 20, (1.6, 4.0), Y, mats["pinion"], marker=mats["marker"])
bp = gr.Gear("b_pin", gr.NP, (-2.0, -2.9), Y, mats["input"], marker=mats["marker"])
bb = gr.Gear("b_big", gr.NB, (2.0, -2.9), Y, mats["big"], marker=mats["marker"], holes=mats["ink"])
shelf = tr.rbox("shelf", (13.0, 1.4, 0.7), (0.0, Y + 0.5, -6.4), mats["ink"], bevel=0.25)


def update(scene_):
    t = scene_.frame_current / c.FPS
    th = 2 * math.pi * 0.9 * t
    th2 = 2 * math.pi * 0.6 * t                  # 20-tooth pair: 0.6 turns/s keeps its 18-degree tooth pitch strobe-free
    tp.set_angle(th2)
    tq.set_angle(math.pi - math.pi / 20 - th2)      # 1:1 partner (phi = 0)
    bp.set_angle(th)
    bb.set_angle(math.pi - math.pi / gr.NB - (gr.NP / gr.NB) * th)       # 4:1 big gear (phi = 0)
    u = c.smooth(0, T, t)
    tr.look(stage, (0.5, 0, 0.5 + 0.6 * u), 30.0 - 5.0 * u, 5.0, -2.0 - 12.0 * u)


stage.run(update, args, SLOT, "gear-01")
