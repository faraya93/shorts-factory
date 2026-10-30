"""inodoro scene 5 (ruta): the waste leaves the house drain, runs along the street sewer and reaches the treatment plant (S1)."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import toilet_rig as tl  # noqa: E402
import sewer_rig as sw  # noqa: E402

args, production, stage, m, SLOT = tr.begin(232, floor_z=-1.2)
tl.cpu_draft(stage, args)
T = SLOT / c.FPS
K = tl.Toilet()
M = sw.Materials(K.mats)
P = sw.Plant(M)
sw.add_grate(M)
blob = [P.new_blob("pk0", M.waste, 0.55, (1.0, 0.8, 0.8)), P.new_blob("pk1", M.waste, 0.45, (1.0, 0.8, 0.8))]
PK = [(-2.2, 0.0)] + sw.P1 + [(7.0, -19.5)]
P.water_box("s1_water", M.sewage, 0.5, 7.5, -25.5, -23.4)


def update(scene_):
    t = scene_.frame_current / c.FPS
    K.state(tank=12.0, bowl=tl.WATERLINE)
    K.put_waste(0, 3.7, 9.0, s=0.0); K.put_waste(1, 4.7, 9.0, s=0.0)
    s = tl.keys(t, [(0.2, 0.0), (6.6, 1.0)])
    for i, b in enumerate(blob):
        x, z = sw.path_point(PK, max(0.0, s - 0.03 * i))
        P.put(b, x, z, s=1.0 if t > 0.05 else 1e-4)
    cam_x = tl.keys(t, [(0.0, 0.8), (1.6, -0.5), (3.0, 2.0), (4.8, 5.4), (7.7, 3.4)])
    cam_z = tl.keys(t, [(0.0, 3.0), (1.6, -3.0), (3.0, -9.0), (4.8, -12.5), (7.7, -19.0)])
    rad = tl.keys(t, [(0.0, 30.0), (3.0, 27.0), (7.7, 26.0)])
    tr.look(stage, (cam_x, 0, cam_z), rad, 6.0, -3.0 + 4.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "toilet-05")
