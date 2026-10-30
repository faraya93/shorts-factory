"""palta scene 5: the avocado carries almost only texture (fat); two persons read it differently; ripeness changes the signal."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import flavour_rig as fr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(302, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 5)
M = fr.mats()
mk.board(M, fr.Z0 + 0.3, h=11.4)
Z0 = fr.Z0
P = [fr.Person(i, M, None) for i in range(3)]
A = fr.Avocado(M)
t_sug, t_fat, t_man, t_pas, t_mad = W.t("azúcar", default=2.3), W.t("grasa:", default=3.9), W.t("mantecosa,", default=7.2), W.t("pastosa,", default=8.4), W.t("madurez", default=9.7)
rg1 = mr.ring(m, "ring1", 1.0, 1.0, (0.0, -0.4, Z0 - 2.0))
rg2 = mr.ring(m, "ring2", 1.0, 1.0, (fr.COLS[0], -0.4, Z0 - 2.0))
for r in (rg1, rg2):
    r.scale = (1e-4,) * 3


def update(scene_):
    t = scene_.frame_current / c.FPS
    kk = mk.keys(t, [(t_mad, 0.0), (t_mad + 0.9, 0.0), (t_mad + 1.4, 0.5), (t_mad + 2.0, 1.0)])
    A.ripeness(kk if t > t_mad else 0.0)
    tex = mk.keys(t, [(t_mad - 0.2, 0.9), (t_mad + 0.5, 0.45), (t_mad + 1.0, 0.9), (t_mad + 1.9, 0.55)])
    for p in P:
        h = [p.play_ch(t, 0, t_sug, T, a=(0.12, 0, 0)), p.play_ch(t, 1, t_sug, T, a=(0, 0.3, 0)), p.play_ch(t, 2, t_fat, T, a=(0, 0, tex))]
        p.gauge.set(h)
    s = 1e-4 if t < t_man else 0.9 * min(1.0, (t - t_man) / 0.4)
    rg1.scale = (s, 1.0, s)
    s2 = 1e-4 if t < t_pas else 0.9 * min(1.0, (t - t_pas) / 0.4)
    rg2.scale = (s2, 1.0, s2)
    tr.look(stage, (0.0, 0, Z0 + 0.3), 34.0 - 2.0 * c.smooth(0, T, t), 6.0, -5.0 + 10.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "flavour-05")
