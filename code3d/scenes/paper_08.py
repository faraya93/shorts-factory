"""paper 8 (cierre): one sheet folds once more, then the doubling replays as one continuous climb: the column rises from the ground, the sky goes black, the Moon comes into view and the tip touches it."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import math  # noqa: E402

import paper_rig as pr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(311, floor_z=-0.05)
m = pr.Mats(S)
pr.big(S)
MOON_Z, MOON_R = 1500.0, 70.0
earth = pr.earth(m)
sheet = pr.Sheet(m, "sheet", loc=(0.0, 0.0, 0.0))
col = pr.column(m, "stack", w=7.0, d=9.0, loc=(0.0, 0.0, 0.0), pitch=2.0)
moon = pr.moon(S, "moon", R=MOON_R, loc=(0.0, 0.0, MOON_Z))
sky = pr.Sky(S)
pr.sun(S, 2.4)
lift = pr.av.lights(S, 5.0)
cam_t = [(0.0, 0.0, 10.0)]
stars = pr.stars(S, m, 70, lambda t: cam_t[0], lambda t: pr.smooth(4.6, 6.4, t), dist=1600.0, seed=23)
T0, T1 = 1.9, 9.3                                   # the climb


def height(t):
    k = pr.smooth(T0, T1, t)
    return 4.0 * math.exp(k * math.log((MOON_Z - MOON_R + 1.0) / 4.0)) if t >= T0 else 0.0


def upd(t):
    sheet.fold(pr.smooth(0.5, 1.5, t))
    h = height(t)
    pr.vis(sheet.root, t < T0 + 0.1)
    pr.set_height(col, h if t >= T0 else pr.EPS)
    col.scale = (1.0, 1.0, max(pr.EPS, h)) if t >= T0 else (pr.EPS, pr.EPS, pr.EPS)
    pr.set_pitch(col, max(1.0, h / 45.0))
    sky.set(pr.smooth(3.2, 6.2, t), hide_floor=t > 3.0)
    rad = 40.0 + 0.24 * h
    tz = max(8.0, h + 0.12 * rad) if t >= T0 else 8.0
    cam_t[0] = (0.0, 0.0, tz)
    az = sp.interp([(0, -25.0), (T0, -25.0), (S.T, 20.0)], t)
    pr.look(S, (0.0, 0.0, tz), rad if t >= T0 else 40.0, sp.interp([(0, 12.0), (T0, 4.0), (S.T, 8.0)], t), az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.6, centre=(0, -30, 60))
S.go()
