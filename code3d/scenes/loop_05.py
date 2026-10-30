"""alcohol scene 5: tolerance (more tokens for the same gauge mark) and the motive flipping from pleasure to avoiding discomfort."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import loop_rig as lr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(270, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 5)
M = lr.mats()
mk.board(M, lr.Z0, w=11.6, h=11.4)
A = lr.Machine(0, m, M)
B = lr.Machine(1, m, M)
Z0 = lr.Z0
t_tol, t_men, t_mas, t_pla, t_eva, t_mal = (W.t("tolerancia,", default=2.0), W.t("menos", default=3.8), W.t("más;", default=5.1), W.t("placer", default=6.7),
                                             W.t("evitar", default=7.1), W.t("malestar.", default=7.6))
lamp_bad = mk.lamp("bad", m.red, M["off"], lr.GAUGE_X, B.cz + 2.35, r=0.3)
feed = mk.Stream("feedtok", M["token"], [(lr.BOTTLE_X, B.cz + 1.2), (lr.GAUGE_X, B.cz + 0.1)], n=6, r=0.15, y=-0.6)
pleas = mk.lamp("pl", m.gold, M["off"], lr.GAUGE_X + 1.4, B.cz + 2.35, r=0.3)


def update(scene_):
    t = scene_.frame_current / c.FPS
    n = 2 if t < t_mas else 4
    eff = mk.keys(t, [(t_tol, 1.0), (t_men, 1.0), (t_men + 1.0, 0.5)])
    fill = mk.keys(t, [(t_tol - 0.5, 0.0), (t_tol + 0.6, 1.0)])
    level = n * eff * fill * 1.0 if t < t_mas else 4 * 0.5 * mk.keys(t, [(t_mas, 0.5), (t_mas + 0.9, 1.0)]) 
    B.gauge.set([min(3.3, level)])
    feed.set(t, t_tol - 0.5, T, amount=n / 6.0, speed=0.5)
    mk.lit(pleas, 1.0 if (t_pla <= t < t_eva) else 0.0)
    mk.lit(lamp_bad, 1.0 if t >= t_eva else 0.0)
    lr.run_tokens(A.full, lr.phase(lambda x: 0.1, t), t, 0.0, amount=0.4)
    lr.run_tokens(B.full, lr.phase(lambda x: 0.14, t), t, 0.0, amount=0.5)
    p = c.smooth(0, T, t)
    tr.look(stage, (-1.2, 0, B.cz + 0.3), 29.0 - 2.0 * p, 6.0, -4.0 + 8.0 * p)

stage.run(update, args, SLOT, "loop-05")
