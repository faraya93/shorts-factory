"""palta scene 6: practice lowers a tower's gain, a bad experience raises it with a wine mark; energy lamp vs danger lamp."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import flavour_rig as fr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(413, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 6)
M = fr.mats()
mk.board(M, fr.Z0 + 0.3, h=11.4)
Z0 = fr.Z0
P = [fr.Person(i, M, None) for i in range(3)]
A = fr.Avocado(M)
t_rep, t_bad, t_evo, t_en, t_dan = W.t("veces", default=4.7), W.t("mala", default=6.4), W.t("evolución", default=8.9), W.t("energía;", default=10.7), W.t("peligro.", default=12.4)
lamp_en = mk.lamp("en", m.gold, M["off"], -4.55, Z0 + 4.4, r=0.5)
lamp_da = mk.lamp("da", m.red, M["off"], 4.55, Z0 + 4.4, r=0.5)
s_en = mk.Stream("en", M["tex"], [fr.AVOCADO_AT, (-4.55, Z0 + 4.4)], n=5, r=0.16)
s_da = mk.Stream("da", M["taste"], [fr.AVOCADO_AT, (4.55, Z0 + 4.4)], n=5, r=0.16)
mark = mk.sphere("bad", m.red, 0.28, (fr.COLS[1] - 1.15, -0.3, Z0 + 3.4))
mk.scale_to(mark, 1e-4)
P[0].set_gain((1.9, 1.0, 0.8))


def update(scene_):
    t = scene_.frame_current / c.FPS
    g0 = mk.keys(t, [(t_rep - 0.8, 1.9), (t_rep - 0.5, 1.9), (t_rep + 0.8, 1.2)])
    P[0].set_gain((g0, 1.0, 0.8))
    g1 = 0.7 + 1.5 * c.smooth(t_bad, t_bad + 0.8, t)
    P[1].set_gain((g1, 1.0, 1.8))
    mk.scale_to(mark, 1.0 if t > t_bad else 1e-4)
    for p in P:
        h = p.play_ch(t, 0, 0.3, T, a=(0.6, 0, 0))
        p.gauge.set([h, 0, 0])
    mk.lit(lamp_en, 1.0 if t >= t_en else 0.0)
    mk.lit(lamp_da, 1.0 if t >= t_dan else 0.0)
    s_en.set(t, t_en, T)
    s_da.set(t, t_dan, T)
    tr.look(stage, (0.0, 0, Z0 + 0.8), 37.0, 6.0, -4.0 + 8.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "flavour-06")
