"""rayo 5 (sin_techo): see productions/mecanalia-es/020*/script.json. The turn: the same car on the same road, the camera craning up as the roof (pillars, glass, panel) lifts, slides back and is gone, leaving the driver in the open."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import rayo_rig as ry  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(150, floor_z=-0.6)
m = ry.Mats(S)
dashes = ry.road(S, m)
car = ry.car(S, m, "hero")
lift = ry.lights(S)
t_go = S.t("descapotable", default=1.6) - 0.4


def upd(t):
    ry.scroll_dashes(dashes, t, 0.0)
    ry.set_roof(car, sp.interp([(t_go, 0.0), (t_go + 1.5, 1.0)], t))
    az = sp.interp([(0, 8.0), (S.T, 36.0)], t)
    rad = sp.interp([(0, 115.0), (S.T, 125.0)], t)
    el = sp.interp([(0, 4.0), (t_go + 1.0, 14.0), (S.T, 42.0)], t)
    tz = sp.interp([(0, 12.0), (S.T, 8.0)], t)
    ry.look(S, (0.0, 0.0, tz), rad, el, az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
