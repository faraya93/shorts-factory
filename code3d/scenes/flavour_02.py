"""palta scene 2: taste, smell and texture are three channels that stack into one flavour (all three columns neutral here)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import flavour_rig as fr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(340, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 2)
M = fr.mats()
mk.board(M, fr.Z0 + 0.3, h=11.4)
Z0 = fr.Z0
P = [fr.Person(i, M, None) for i in range(3)]
A = fr.Avocado(M)
for p in P:
    p.set_gain((1.0, 1.0, 1.0))
t_taste, t_smell, t_tex = W.t("lengua", default=1.8), W.t("olfato", default=7.2), W.t("textura", default=8.8)


def update(scene_):
    t = scene_.frame_current / c.FPS
    for p in P:
        h = [p.play_ch(t, 0, t_taste, T), p.play_ch(t, 1, t_smell, T, a=(0.35, 1.4, 0.9)), p.play_ch(t, 2, t_tex, T)]
        p.gauge.set(h)
    p_ = c.smooth(0, T, t)
    tr.look(stage, (0.0, 0, Z0 + 0.3), 36.0 - 5.0 * p_, 6.0, -3.0 + 6.0 * p_)

stage.run(update, args, SLOT, "flavour-02")
