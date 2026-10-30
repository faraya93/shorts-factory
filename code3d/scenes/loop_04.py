"""alcohol scene 4: cue lamps connect to the loop on machine B; repetition grows a shortcut, speeds the tokens and deepens the track."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import loop_rig as lr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(324, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 4)
M = lr.mats()
mk.board(M, lr.Z0, w=11.6, h=11.4)
A = lr.Machine(0, m, M)
B = lr.Machine(1, m, M)
Z0 = lr.Z0
t_bot, t_lug, t_tri, t_rep, t_aco, t_ace, t_dif = (W.t("botella,", default=3.4), W.t("lugar", default=4.1), W.t("tristeza.", default=4.6), W.t("repetición", default=6.3),
                                                    W.t("acorta,", default=6.9), W.t("acelera", default=7.7), W.t("interrumpir.", default=9.3))
t_cir = W.t("circuito:", default=1.7)


def update(scene_):
    t = scene_.frame_current / c.FPS
    for i, tl in enumerate((t_bot, t_lug, t_tri)):
        mk.lit(B.cues[i], 1.0 if t >= tl else 0.0)
    short = c.smooth(t_aco - 0.3, t_aco + 0.7, t)
    if short > 0.01:
        if "_s" not in B.short:
            B.short["_s"] = list(B.short.scale)
        mk.scale_to(B.short, short)
    else:
        mk.hide(B.short)
    ph = lr.phase(lambda x: 0.1 + 0.12 * c.smooth(t_rep, t_aco, x) + 0.28 * c.smooth(t_ace - 0.2, t_ace + 1.0, x), t)
    lr.run_tokens(B.full, ph, t, t_cir, amount=1.0 - short)
    lr.run_tokens(B.cut, ph * 1.0, t, t_cir, amount=short)
    B.track_depth(c.smooth(t_ace, t_dif, t))
    lr.run_tokens(A.full, lr.phase(lambda x: 0.1, t), t, t_cir, amount=0.5)
    p = c.smooth(0, T, t)
    tr.look(stage, (0.3 - 0.5 * p, 0, B.cz + 0.4 - 0.6 * p), 30.0 - 5.0 * p, 6.0, -4.0 + 8.0 * p)

stage.run(update, args, SLOT, "loop-04")
