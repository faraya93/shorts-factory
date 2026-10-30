"""inodoro scene 9 (cta): the whole system; a pulse travels from the toilet to the river while the camera pulls back."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import toilet_rig as tl  # noqa: E402
import sewer_rig as sw  # noqa: E402

args, production, stage, m, SLOT = tr.begin(326, floor_z=-1.2)
tl.cpu_draft(stage, args)
T = SLOT / c.FPS
K = tl.Toilet()
K.state(tank=tl.TANK_FULL)
M = sw.Materials(K.mats)
P = sw.Plant(M)
sw.add_grate(M)
for o in (K.waste[0], K.waste[1]):
    o.scale = (1e-4,) * 3
pulse = P.new_blob("pulse", M.waste, 0.9, (1, 0.8, 0.8))
FULL = [(-2.2, 0.0)] + sw.P1 + [(7.0, -20.0), (7.0, -24.5), (1.0, -24.5), (1.0, -34.0), (1.0, -36.0), (7.0, -36.0), (7.0, -45.0), (1.0, -48.5), (1.0, -57.5), (7.0, -58.5), (7.0, -66.5)]


def update(scene_):
    t = scene_.frame_current / c.FPS
    s = tl.keys(t, [(0.6, 0.0), (8.2, 1.0)])
    x, z = sw.path_point(FULL, s)
    P.put(pulse, x, z, s=1.0 if t > 0.55 else 1e-4)
    p = c.smooth(0.8, 8.4, t)
    rad = 24.0 + (118.0 - 24.0) * p
    cx = 0.8 + (1.6 - 0.8) * p
    cz = 6.0 + (-32.0 - 6.0) * p
    tr.look(stage, (cx, 0, cz), rad, 6.0 + 3.0 * p, -3.0 + 5.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "toilet-09")
