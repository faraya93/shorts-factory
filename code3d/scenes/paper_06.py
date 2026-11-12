"""paper 6 (luna): black space. The Moon lies ahead; the column's tip rises the last stretch and reaches its surface while the camera swings around the Moon and looks back down the thin column."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import paper_rig as pr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(168, floor_z=-0.05)
m = pr.Mats(S)
pr.big(S)
MOON_Z, MOON_R = 1500.0, 70.0
moon = pr.moon(S, "moon", R=MOON_R, loc=(0.0, 0.0, MOON_Z))
col = pr.column(m, "stack", w=7.0, d=9.0, loc=(0.0, 0.0, 0.0), pitch=22.0)
sky = pr.Sky(S)
sky.set(1.0, hide_floor=True)
pr.sun(S, 2.2, rot=(1.0, 0.0, 0.9))
lift = pr.av.lights(S, 8.0)
cam_t = [(0.0, 0.0, MOON_Z - 60.0)]
stars = pr.stars(S, m, 70, lambda t: cam_t[0], lambda t: 1.0, dist=1600.0, seed=17)
t_arrive = S.t("Luna.", default=4.4)


def upd(t):
    top = MOON_Z - MOON_R + 1.0
    pr.set_height(col, 1180.0 + (top - 1180.0) * pr.smooth(0.3, t_arrive, t))
    tz = sp.interp([(0, MOON_Z - 140.0), (S.T, MOON_Z - 70.0)], t)
    cam_t[0] = (0.0, 0.0, tz)
    rad = sp.interp([(0, 560.0), (S.T, 330.0)], t)
    pr.look(S, (0.0, 0.0, tz), rad, sp.interp([(0, -6.0), (S.T, 16.0)], t), sp.interp([(0, -75.0), (S.T, 35.0)], t))
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.5, centre=(0, -30, MOON_Z - 100))
S.go()
