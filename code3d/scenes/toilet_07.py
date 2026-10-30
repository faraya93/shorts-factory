"""inodoro scene 7 (decantacion): heavy solids sink and form sludge in S2; microbes eat the fine organic matter in S3."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import toilet_rig as tl  # noqa: E402
import sewer_rig as sw  # noqa: E402

args, production, stage, m, SLOT = tr.begin(191, floor_z=-1.2)
tl.cpu_draft(stage, args)
T = SLOT / c.FPS
K = tl.Toilet()
K.state(tank=12.0)
M = sw.Materials(K.mats)
P = sw.Plant(M)
sw.add_grate(M)
for o in (K.waste[0], K.waste[1]):
    o.scale = (1e-4,) * 3
P.water_box("s2_w", M.sewage, 0.5, 7.5, -37.5, -32.4)
P.water_box("s3_w", M.sewage, 0.5, 7.5, -49.5, -44.4)
sludge = tl.Box("sludge", M.waste)
heavy = [P.new_blob(f"hv{i}", M.waste, 0.3, (1, 0.8, 0.8)) for i in range(7)]
fine = [P.new_blob(f"fn{i}", M.waste, 0.22, (1, 0.8, 0.8)) for i in range(3)]
mic = [P.new_blob(f"mic{i}", M.microbe, 0.24, (1, 0.8, 0.8)) for i in range(11)]
foam = [P.new_blob(f"foam{i}", M.foam, 0.13, (1, 1, 1)) for i in range(10)]
HX = [1.2, 2.4, 3.6, 4.8, 3.0, 5.8, 1.8]


def update(scene_):
    t = scene_.frame_current / c.FPS
    s_h = tl.keys(t, [(1.7, 0.0), (2.4, 1.2)])                    # sludge layer height
    sludge.set(0.5, 7.5, -37.5, -37.5 + s_h) if s_h > 0.02 else sludge.set(0, 0, 0, 0)
    for i, b in enumerate(heavy):                                  # solids drop in and sink to the bottom
        k = (t - (0.3 + 0.18 * i)) / 1.7
        z = tl.keys(k, [(0.0, -29.6), (0.3, -33.0), (1.0, -37.0 + 0.3 * (i % 3))])
        P.put(b, 1.0 + (HX[i] - 1.0) * c.smooth(0.2, 0.8, k) if k > 0 else 1.0, z, s=(1.0 if 0 < k < 1.0 else (1e-4 if k <= 0 else 0.0)))
    for i, f in enumerate(fine):                                   # fine matter drifts on to S3
        k = (t - (1.6 + 0.2 * i)) / 1.4
        if k <= 0:
            P.put(f, 1.0, -33.0, s=1e-4)
        elif k < 1.0:
            P.put(f, tl.keys(k, [(0.0, 2.0), (0.6, 7.0), (1.0, 7.0)]), tl.keys(k, [(0.0, -33.4), (0.6, -33.6), (1.0, -42.2)]))
        else:
            kk = (t - (3.0 + 0.2 * i))
            P.put(f, 7.0 - 1.4 * (i + 1) * min(1.0, max(0.0, (t - 3.0) / 1.2)), -46.0 - 0.25 * i, s=tl.keys(t, [(3.6 + 0.35 * i, 1.0), (5.0 + 0.35 * i, 0.0)]))
    for i, mm in enumerate(mic):                                   # microbes swarm in on "microbios"
        a = tr.back((t - (2.8 + 0.05 * i)) / 0.4) if t > 2.8 else 1e-4
        tx = 7.0 - 1.4 * (i % 3 + 1) + 0.5 * math.cos(3.0 * t + i)
        P.put(mm, tx, -46.0 - 0.25 * (i % 3) + 0.5 * math.sin(2.5 * t + i), s=a)
    for i, fo in enumerate(foam):
        k = ((t * 0.7 + 0.1 * i) % 1.0)
        P.put(fo, 1.2 + 0.65 * i, -49.2 + 4.2 * k, s=math.sin(math.pi * k) if t > 2.0 else 1e-4)
    p = c.smooth(2.2, 3.0, t)
    tr.look(stage, (4.0, 0, -34.5 - 12.0 * p), 24.0, 8.0, -3.0 + 6.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "toilet-07")
