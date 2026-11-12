"""paper 7 (giro): the turn. The column topples and collapses to nothing; a very long paper strip unrolls to the horizon and the camera travels along it to a student at its end, beside the thick wad of its twelve folds."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import paper_rig as pr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(256, floor_z=-0.05)
m = pr.Mats(S)
pr.big(S)
LEN = 260.0
col = pr.column(m, "stack", w=7.0, d=9.0, loc=(0.0, 12.0, 0.0), pitch=2.0)
band = pr.strip(m, "strip", w=5.0, loc=(0.0, 8.0, 0.0))
wad = pr.column(m, "wad", w=7.0, d=8.0, loc=(0.0, 8.0 + LEN + 1.0, 0.0), pitch=0.34)
pr.set_height(wad, 4.6)
fig_root, fig = pr.figure(S, m, "student", (6.0, 8.0 + LEN + 3.0, 0.0), rot_z=math.radians(-25), cols=pr.STUDENT)
pr.sun(S, 2.6)
lift = pr.av.lights(S, 3.0)
t_roll = S.t("estudiante", default=4.5)


def upd(t):
    # the column falls over its foot and shrinks away
    k = pr.smooth(0.15, 1.6, t)
    pr.set_height(col, max(1e-3, 70.0 * (1.0 - k)))
    col.rotation_euler = (0.0, 0.0, 0.0)
    pr.vis(col, t < 1.7)
    if t < 1.7:
        pr.set_height(col, max(1e-3, 70.0 * (1.0 - k)))
    # the strip unrolls
    band.scale = (1.0, max(pr.EPS, LEN * pr.smooth(1.2, t_roll + 0.6, t)), 1.0)
    cz = sp.interp([(0, (0.0, 12.0, 20.0)), (1.8, (0.0, 20.0, 8.0)), (5.6, (0.0, 8.0 + LEN * 0.6, 7.0)), (S.T, (2.0, 8.0 + LEN, 8.0))], t)
    rad = sp.interp([(0, 90.0), (1.8, 36.0), (5.6, 60.0), (S.T, 44.0)], t)
    el = sp.interp([(0, 8.0), (1.8, 5.0), (S.T, 8.0)], t)
    az = sp.interp([(0, -30.0), (1.8, 0.0), (S.T, 18.0)], t)
    pr.look(S, cz, rad, el, az)
    lift(0.0, cz[1] - 12.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, 60, 40))
S.go()
