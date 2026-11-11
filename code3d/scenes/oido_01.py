"""oido 1 (hook): see productions/mecanalia-es/024*/script.json. The sealed ear with its canal in section on the plate; amber wax lines the canal near the opening, a few flakes sit on it;
the camera orbits from the whole ear in to the canal entrance while a cotton swab slides in from the left toward the entrance."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import oido_rig as od  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(210, floor_z=-2.0 * od.KS)
m = od.Mats(S)
ear = od.Ear(S, m, lining=(0.8, 23.0))
cv = od.Conveyor(S, m, nb=1, nf=9, nd=1)
sw = od.Swab(S, m)
lift = od.lights(S, od.LIGHT_K)


def upd(t):
    cv.update(t, 0.0, bands_on=0.0, dust_on=0.0)
    k = sp.interp([(0.0, 0.0), (S.T * 0.5, 0.0), (S.T, 1.0)], t)                       # the swab only enters the frame after the ear has been seen whole
    sw.tip_at(sp.lerp(-10.0, 2.0, k), sp.lerp(-110.0, -20.0, k), sp.lerp(60.0, od.CZ + 2.0, k), tilt=sp.lerp(2.0, 1.75, k), pitch=sp.lerp(0.5, 0.1, k))
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, od.P(0, 0, 34), od.R(330), 8.0, -48.0), (S.T * 0.52, od.P(0, 0, 34), od.R(285), 8.0, -44.0), (S.T, od.P(14, 0, 34), od.R(195), 12.0, -16.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
