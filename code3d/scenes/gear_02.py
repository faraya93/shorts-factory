"""scene 2: ONE stage close up (pinion 10 teeth -> big 40). Slow while the teeth are explained; from 'cuando el chico da cuatro vueltas'
(8.7 s) the pinion turns exactly 4 times in 3.0 s and the big gear once. Slot 365 frames."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import gear_rig as gr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(365, floor_z=-5.2)
T = SLOT / c.FPS
mats = gr.Train._materials(m)
Y = 0.6
pin = gr.Gear("pin", gr.NP, (-2.0, 0.0), Y, mats["input"], marker=mats["marker"])
big = gr.Gear("big", gr.NB, (2.0, 0.0), Y, mats["big"], marker=mats["marker"], holes=mats["ink"])
shelf = tr.rbox("shelf", (11.0, 1.4, 0.7), (0.0, Y + 0.5, -4.6), mats["ink"], bevel=0.25)
T0, T1 = 8.7, 11.7
K = round(0.35 * T0) / T0              # whole turns by T0 so the marker is upright when the count starts


def turns(t):
    if t < T0:
        return K * t
    return K * T0 + 4.0 * min(1.0, (t - T0) / (T1 - T0)) + (0.0 if t < T1 else 0.12 * (t - T1))


def update(scene_):
    t = scene_.frame_current / c.FPS
    th = 2 * math.pi * turns(t)
    pin.set_angle(th)
    big.set_angle(math.pi - math.pi / gr.NB - (gr.NP / gr.NB) * th)
    u = c.smooth(0, 3.5, t)
    v = c.smooth(0, T, t)
    tr.look(stage, (1.0, 0, 0.6), 30.0 - 10.0 * u, 4.0 + 6.0 * v, -4.0 + 20.0 * v)


stage.run(update, args, SLOT, "gear-02")
