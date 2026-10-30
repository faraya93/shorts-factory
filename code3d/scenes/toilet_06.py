"""inodoro scene 6 (rejas): rubbish stays on the grate, the toilet paper dissolves, the wipes pile up and back the water up."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import toilet_rig as tl  # noqa: E402
import sewer_rig as sw  # noqa: E402

args, production, stage, m, SLOT = tr.begin(240, floor_z=-1.2)
tl.cpu_draft(stage, args)
T = SLOT / c.FPS
K = tl.Toilet()
K.state(tank=12.0)
M = sw.Materials(K.mats)
P = sw.Plant(M)
sw.add_grate(M)
low = P.water_box("s1_low", M.sewage, 0.5, 7.5, -25.5, -23.4)
up = P.water_box("s1_up", M.sewage, 0.5, 7.5, -21.8, -21.8)
bits = [P.new_blob(f"bit{i}", M.waste, 0.2, (1, 0.8, 0.8)) for i in range(6)]
paper = [P.new_blob(f"paper{i}", M.paper, 0.45, (1.0, 0.8, 0.35)) for i in range(4)]
wipes = [P.new_blob(f"wipe{i}", M.wipe, 0.62, (1.0, 0.9, 0.18)) for i in range(8)]
ring = tl.ring(m, "wipe_ring", (4.0, -1.0, -21.5), 1e-4, 1e-4)
GX = [2.2, 3.3, 4.4, 5.3, 6.2, 3.0, 4.8, 5.8]
for o in (K.waste[0], K.waste[1]):
    o.scale = (1e-4,) * 3


def update(scene_):
    t = scene_.frame_current / c.FPS
    for i, b in enumerate(bits):                                     # organic bits fall through the gaps
        k = (t - (0.2 + 0.25 * i)) / 1.4
        x = 3.0 + 0.7 * i
        P.put(b, x, tl.keys(k, [(0.0, -17.6), (0.45, sw.GRATE_Z + 0.4), (0.5, sw.GRATE_Z), (1.0, -24.8)]), s=1.0 if 0.0 < k < 1.0 else 1e-4)
    for i, w in enumerate(wipes):                                    # wipes arrive and stay on the grate
        t0 = 0.5 + 0.3 * i if i < 3 else 6.0 + 0.2 * (i - 3)
        k = (t - t0) / 0.7
        z = tl.keys(k, [(0.0, -17.6), (1.0, sw.GRATE_Z + 0.5 + 0.08 * (i // 3))])
        P.put(w, GX[i], z, s=(1.0 if k > 0 else 1e-4), rot=0.12 * (i % 3 - 1))
    for i, pp in enumerate(paper):                                   # toilet paper arrives, lies, then dissolves
        t0 = 1.0 + 0.3 * i
        k = (t - t0) / 0.6
        z = tl.keys(k, [(0.0, -17.6), (1.0, sw.GRATE_Z + 0.4)])
        dis = tl.keys(t, [(2.6 + 0.35 * i, 1.0), (3.9 + 0.35 * i, 0.0)])
        P.put(pp, 2.6 + 1.1 * i, z, s=(dis if k > 0 else 1e-4), rot=0.2 * (i - 1.5))
    r = tl.keys(t, [(4.9, 0.0), (5.4, 1.0), (6.0, 1.0), (6.3, 0.0)])
    ring.scale = (max(1e-4, 3.2 * r), 1.0, max(1e-4, 1.3 * r))
    lvl = tl.keys(t, [(6.0, -21.6), (7.6, -19.6)])
    up.set(0.5, 7.5, sw.GRATE_Z + 0.2, lvl) if t > 6.0 else up.set(0, 0, 0, 0)
    tr.look(stage, (4.0, 0, -21.4), 23.0 - 2.0 * c.smooth(0, T, t), 8.0, -3.0 + 6.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "toilet-06")
