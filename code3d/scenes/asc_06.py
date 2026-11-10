"""asc 6 (cierre): see productions/mecanalia-es/017*/script.json. The reframe image: the camera opens on a wedge clamped on the right rail (accent), pulls back to the whole car on its six ropes, the ropes are cut one after another on 'cortara el cable' and nothing moves ('Nada'); the pull-back ends on the tall shaft with the rails the brightest lines."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import asc_rig as ar  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(392, floor_z=0.0)
H, Z0 = 360.0, 250.0
m = ar.Mats(S)
sh = ar.shaft(S, H, m)
cab = ar.Cab(S, m, Z0)
XS = [-6.5, -3.9, -1.3, 1.3, 3.9, 6.5]
rp = ar.Ropes(S, cab, m, XS, Z0 + ar.ROOF_ABOVE, H)
t0 = S.t("cortara", default=5.5)
cuts = [t0 + 0.13 * i for i in range(6)]
lift = ar.lights(S)


def upd(t):
    cab.set_z(Z0 - sum(sp.pulse(t, tc, 0.4, 0.12) for tc in cuts))
    ar.gear_set(cab, 1.0)
    rp.set(t, cut=cuts)
    ar.gov_set(cab.gov, 0.0, 0.0)
    tx = sp.interp([(0, 15.0), (3.4, 0.0), (S.T, 0.0)], t)
    tz = sp.interp([(0, Z0 - 2.0), (3.4, Z0 + 40.0), (7.0, Z0 + 55.0), (S.T, Z0 + 55.0)], t)
    rad = sp.interp([(0, 55.0), (1.6, 90.0), (3.4, 190.0), (7.0, 230.0), (S.T, 300.0)], t)
    el = sp.interp([(0, 6.0), (3.4, 3.0), (S.T, 14.0)], t)
    az = sp.interp([(0, -20.0), (3.4, -4.0), (S.T, 14.0)], t)
    ar.look(S, (tx, 0.0, tz), rad, el, az)
    lift(tz - 20.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -20, 30))
S.go()
