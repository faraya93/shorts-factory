"""inodoro scene 2 (tanque): clean water in the tank; the lever and the flapper lift; water rushes along the channel into the bowl."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import toilet_rig as tl  # noqa: E402

args, production, stage, m, SLOT = tr.begin(299, floor_z=-1.2)
tl.cpu_draft(stage, args)
T = SLOT / c.FPS
K = tl.Toilet()


def update(scene_):
    t = scene_.frame_current / c.FPS
    press = tl.keys(t, [(4.9, 0.0), (5.4, 1.0), (7.6, 1.0), (8.2, 0.0)])
    lift = tl.keys(t, [(6.0, 0.0), (6.9, 1.0), (9.0, 1.0), (9.9, 0.7)])
    tank = tl.keys(t, [(0.0, tl.TANK_FULL), (6.6, tl.TANK_FULL), (7.0, tl.TANK_FULL - 0.3), (9.9, 9.3)])
    chan = tl.keys(t, [(6.7, 0.0), (8.0, 1.0)])
    bowl = tl.keys(t, [(0.0, tl.WATERLINE), (7.6, tl.WATERLINE), (9.9, 5.5)])
    K.state(tank=tank, bowl=bowl, chan=chan, hole=1.0 if t > 6.7 else 0.0)
    K.flap(lift); K.press(press)
    K.put_waste(0, 3.7, bowl - 0.05 + 0.06 * math.sin(2.0 * t))
    K.put_waste(1, 4.7, bowl - 0.08 + 0.05 * math.sin(2.4 * t + 1.0))
    p = c.smooth(5.2, 8.6, t)
    tr.look(stage, (-2.4 + 3.6 * p, 0, 11.0 - 3.6 * p), 25.0 + 3.0 * p, 6.0, -6.0 + 8.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "toilet-02")
