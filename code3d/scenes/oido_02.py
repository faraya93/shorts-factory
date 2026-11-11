"""oido 2 (cinta): see productions/mecanalia-es/024*/script.json. Dust specks drift in at the entrance and stick to the wax; the skin bands of the canal wall slide outward like a slow
conveyor carrying wax flakes and the trapped dust to the opening, where they fade away; the camera travels along the canal from the eardrum toward the opening."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import oido_rig as od  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(242, floor_z=-2.0 * od.KS)
m = od.Mats(S)
ear = od.Ear(S, m)
cv = od.Conveyor(S, m, nb=7, nf=9, nd=6)
lift = od.lights(S, od.LIGHT_K)
T_DUST = S.t("polvo", default=2.4)
SPEED = 6.0


def dust_in(i):
    t0 = T_DUST - 1.2 + 0.28 * i
    return (t0, t0 + 1.3, 5.0 + 2.6 * i)


def upd(t):
    cv.update(t, SPEED, bands_on=1.0, flakes_on=1.0, dust_on=1.0, dust_in=dust_in)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, od.P(50, 0, 34), od.R(130), 8.0, 12.0), (S.T * 0.5, od.P(24, 0, 34), od.R(185), 10.0, 4.0), (S.T, od.P(2, 0, 34), od.R(215), 10.0, -36.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
