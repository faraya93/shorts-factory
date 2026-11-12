"""paper 3 (persona): the stack shoots up beside a standing person (the viewer's stand-in) to 1.6 m of paper, taller than the figure; the camera pulls back to a medium shot."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import paper_rig as pr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(126, floor_z=-0.05)
m = pr.Mats(S)
H = 19.0                                            # stack height in units; the figure is 15.7 units tall
col = pr.column(m, "stack", w=5.0, d=6.5, loc=(8.0, 10.0, 0.0), pitch=0.8)
fig_root, fig = pr.figure(S, m, "viewer", (-3.0, -12.0, 0.0), rot_z=math.radians(25))
lift = pr.av.lights(S, 1.5)
t_up = S.t("catorce,", default=0.6)


def upd(t):
    pr.set_height(col, 1.6 + (H - 1.6) * pr.smooth(t_up, t_up + 0.9, t))
    tgt = sp.interp([(0, (0.0, 0.0, 7.0)), (S.T, (0.0, 0.0, 10.0))], t)
    rad = sp.interp([(0, 46.0), (S.T, 84.0)], t)
    pr.look(S, tgt, rad, sp.interp([(0, 5.0), (S.T, 9.0)], t), sp.interp([(0, -6.0), (S.T, 12.0)], t))
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -20, 20))
S.go()
