"""alcohol scene 6: the cue lamps light and the loop runs BEFORE the bottle reaches the machine; price and availability feed it."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import loop_rig as lr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(295, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 6)
M = lr.mats()
mk.board(M, lr.Z0, w=11.6, h=11.4)
A = lr.Machine(0, m, M)
B = lr.Machine(1, m, M)
Z0 = lr.Z0
t_sen, t_luc, t_ant, t_pre, t_dis = W.t("señales", default=0.3), W.t("luces", default=3.3), W.t("antes", default=4.1), W.t("Precio", default=6.8), W.t("disponibilidad", default=7.2)
supply = mk.Stream("sup", M["token"], [(-7.4, B.cz - 2.2), (lr.BOTTLE_X, B.cz - 0.9)], n=6, r=0.18, y=-0.6)
B.bottle.location = (-7.6, 0.0, B.cz)


def update(scene_):
    t = scene_.frame_current / c.FPS
    for i, p_ in enumerate(B.cues):
        mk.lit(p_, 1.0 if t >= t_sen + 0.35 * i else 0.0)
    run_on = W.t("parar:", default=2.5)
    ph = lr.phase(lambda x: 0.0 if x < run_on else 0.2 + 0.1 * c.smooth(run_on, run_on + 2.0, x), t)
    lr.run_tokens(B.full, ph, t, run_on)
    bx = mk.keys(t, [(t_luc, -7.6), (t_luc + 2.4, lr.BOTTLE_X - 1.1)])
    B.bottle.location = (bx, 0.0, B.cz)
    supply.set(t, t_pre, T, amount=1.0, speed=0.4)
    lr.run_tokens(A.full, lr.phase(lambda x: 0.1, t), t, 0.0, amount=0.4)
    p = c.smooth(0, T, t)
    tr.look(stage, (-0.5 + 0.5 * p, 0, B.cz + 0.3 - 1.5 * p), 32.0 + 4.0 * p, 6.0, -4.0 + 8.0 * p)

stage.run(update, args, SLOT, "loop-06")
