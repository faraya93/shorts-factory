"""oido 5 (cierre): see productions/mecanalia-es/024*/script.json. The reframe in one image: the swab withdraws and swings away, the plug dissolves back into the thin wax layer, the skin bands
carry wax flakes out of the canal on their own, and the camera pulls back to the whole ear (the framing the video opened with)."""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import oido_rig as od  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(317, floor_z=-2.0 * od.KS)
m = od.Mats(S)
ear = od.Ear(S, m, lining=(0.8, 23.0))
cv = od.Conveyor(S, m, nb=7, nf=9, nd=0 + 1)
sw = od.Swab(S, m)
lift = od.lights(S, od.LIGHT_K)
T_REFRAME = S.t("cinta", default=3.0)
rnd = random.Random(11)
pts = [(rnd.uniform(37.0, 47.5), rnd.uniform(2.8, 4.2), od.CZ + rnd.uniform(-5.2, 5.2)) for _ in range(30)]
plug = od.lumps(S, m, "plug", pts, r=3.6, seed=4)
for i, o in enumerate(plug):
    S.gone(o, 0.8 + 1.6 * i / len(plug), 0.45)


S.size(sw.root, [(0.0, 1.0), (3.2, 1.0), (3.5, 1e-4)])                                      # the swab is gone once it has swung away


def upd(t):
    k_out = sp.interp([(0.0, 0.0), (1.4, 1.0)], t)
    k_away = sp.interp([(1.4, 0.0), (3.0, 1.0)], t)
    x = sp.lerp(16.0, -4.0, k_out)
    sw.tip_at(x, sp.lerp(1.5, -26.0, k_away), od.CZ + sp.lerp(0.0, 30.0, k_away), tilt=sp.lerp(0.0, 1.9, k_away), pitch=sp.lerp(0.0, 0.5, k_away))
    ear.lining.scale = (1e-4,) * 3 if t < 2.0 else (1.0, 1.0, 1.0)                        # the thin wax layer is back once the plug has dissolved
    on = sp.interp([(1.6, 0.0), (2.6, 1.0)], t)
    cv.update(t, 6.0, bands_on=1.0, flakes_on=on, dust_on=0.0)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, od.P(36, 0, 34), od.R(125), 8.0, -10.0), (S.T * 0.3, od.P(10, 0, 34), od.R(255), 8.0, -38.0), (S.T, od.P(0, 0, 34), od.R(330), 8.0, -48.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
