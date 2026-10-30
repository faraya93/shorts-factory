"""alcohol scene 3: many small gene nudges (no single gene), a crossed-out DESTINO sign, risk weights drop on machine B's stress control."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import loop_rig as lr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(274, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 3)
M = lr.mats()
mk.board(M, lr.Z0, w=11.6, h=11.4)
A = lr.Machine(0, m, M)
B = lr.Machine(1, m, M)
Z0 = lr.Z0
import machine_kit as mk
t_gen, t_des, t_anx, t_tra, t_joven = W.t("gen", default=1.8), W.t("destino.", default=3.6), W.t("Ansiedad,", default=4.9), W.t("trauma", default=5.7), W.t("joven", default=6.8)
import random
random.seed(5)
dots = [mk.sphere(f"gene{i}", M["stress"], 0.17, (0, -0.7, 0)) for i in range(14)]
seeds = [(random.uniform(-4.8, 4.8), random.uniform(-0.3, 0.3), random.random()) for _ in dots]
weights = [mk.sphere(f"w{i}", M["off"], 0.34, (lr.SLIDER_X[2], -0.7, 0)) for i in range(3)]
tw = [t_anx, t_tra, t_joven]
for w_ in weights:
    mk.scale_to(w_, 1e-4)


def update(scene_):
    t = scene_.frame_current / c.FPS
    for i, (d, (sx, sz, ph)) in enumerate(zip(dots, seeds)):
        k = (t - t_gen - ph * 1.2) / 1.2
        if k < 0 or k > 1.0:
            mk.scale_to(d, 1e-4)
            continue
        tx, tz = lr.SLIDER_X[i % 3], B.cz - 1.5 + 3.0 * lr.SETTINGS[1][i % 3]
        x = sx * (1 - k) + tx * k
        z = (Z0 + 4.8 + sz * 3) * (1 - k) + tz * k
        d.location = (x, -0.7, z)
        mk.scale_to(d, 1.0)
    stress = lr.SETTINGS[1][2]
    brake = lr.SETTINGS[1][1]
    for j, (w_, tj) in enumerate(zip(weights, tw)):
        k = max(0.0, min(1.0, (t - tj) / 0.5))
        if t < tj:
            mk.scale_to(w_, 1e-4)
            continue
        zk = B.cz - 1.5 + 3.0 * (stress + 0.08 * j)
        w_.location = (lr.SLIDER_X[2], -0.7, zk + 2.2 * (1 - k) + 0.55 + 0.55 * j)
        mk.scale_to(w_, 1.0)
    inc = sum(0.08 for tj in tw if t > tj + 0.4)
    B.set_sliders((lr.SETTINGS[1][0], brake - inc * 0.6, stress + inc))
    for mc in (A, B):
        lr.run_tokens(mc.full, lr.phase(lambda x: 0.12, t), t, 0.0, amount=0.5)
    p = c.smooth(0, T, t)
    tr.look(stage, (0.5, 0, Z0), 33.0 - 2.0 * p, 6.0, -4.0 + 8.0 * p)

stage.run(update, args, SLOT, "loop-03")
