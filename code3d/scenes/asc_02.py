"""asc 2 (cables): see productions/mecanalia-es/017*/script.json. The same car, one rope; on 'varios' five more ropes grow in beside it, then three are cut one after the other ('unos pocos basta') and the car does not move; the camera pulls back and up to the top beam."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import asc_rig as ar  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(221, floor_z=0.0)
H, Z0 = 330.0, 215.0
m = ar.Mats(S)
sh = ar.shaft(S, H, m)
cab = ar.Cab(S, m, Z0)
XS = [-6.5, -3.9, -1.3, 1.3, 3.9, 6.5]
rp = ar.Ropes(S, cab, m, XS, Z0 + ar.ROOF_ABOVE, H)
t_var = S.t("varios", default=2.7)
appear = [None if i == 3 else t_var + 0.16 * (i if i < 3 else i - 1) for i in range(6)]
t_b = [S.t("unos", default=4.3), S.t("pocos", default=4.6), S.t("basta", default=4.9)]
cut = [t_b[0], None, t_b[1], None, t_b[2], None]
lift = ar.lights(S)


def upd(t):
    sag = sum(sp.pulse(t, tc, 0.35, 0.5) for tc in t_b)
    cab.set_z(Z0 - sag)
    ar.gear_set(cab, 0.0)
    rp.set(t, appear=appear, cut=cut)
    tz = sp.interp([(0, Z0 + 40.0), (t_var, Z0 + 55.0), (4.0, 280.0), (S.T, 275.0)], t)
    rad = sp.interp([(0, 150.0), (t_var, 175.0), (4.0, 215.0), (S.T, 205.0)], t)
    el = sp.interp([(0, 3.0), (S.T, 8.0)], t)
    az = sp.interp([(0, -10.0), (4.0, 0.0), (S.T, 12.0)], t)
    ar.look(S, (0.0, 0.0, tz), rad, el, az)
    lift(tz - 20.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -20, 30))
S.go()
