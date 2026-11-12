"""paper 2 (duplica): the edge of a stack in macro. One layer; on 'dos hojas' a second drops on it, on 'cuatro' two more, on 'ocho' four more (1, 2, 4, 8); the camera climbs the edge as it grows."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import paper_rig as pr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(236, floor_z=-0.05)
m = pr.Mats(S)
T_L = 1.6                                           # slab thickness (exaggerated: a real sheet is 0.1 mm)
slabs = pr.layers(m, 8, t=T_L)
when = [0.0, S.t("dos", default=5.4), S.t("cuatro,", default=6.14), S.t("cuatro,", default=6.14), S.t("ocho.", default=6.64),
        S.t("ocho.", default=6.64) + 0.12, S.t("ocho.", default=6.64) + 0.24, S.t("ocho.", default=6.64) + 0.36]
lift = pr.av.lights(S, 1.2)


def upd(t):
    top = 0.0
    for i, (o, t0) in enumerate(zip(slabs, when)):
        k = pr.smooth(t0, t0 + 0.35, t)
        on = t >= t0
        pr.vis(o, on)
        o.location.z = i * T_L + T_L / 2 + 12.0 * (1.0 - k)
        if on:
            top = max(top, (i + 1) * T_L)
    az = sp.interp([(0, -22.0), (S.T, 20.0)], t)
    tz = sp.interp([(0, 1.0), (3.0, 1.0), (S.T, top / 2 + 1.0)], t)
    rad = sp.interp([(0, 64.0), (3.0, 52.0), (S.T, 66.0)], t)
    pr.look(S, (0.0, -4.0, tz), rad, sp.interp([(0, 4.0), (S.T, 10.0)], t), az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.4, centre=(0, -20, 14))
S.go()
