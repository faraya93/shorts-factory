"""micro 5 (giro): see productions/mecanalia-es/022*/script.json. The turn: the camera pulls back from the last spark to the whole oven; its walls light evenly without a single spark; the door swings shut and the camera pushes to it, where the metal screen behind the glass lights as a fine grid."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import micro_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(250, floor_z=-0.6)
n = mr.build(S)
TF = mr.fork_pt((10.0, 0.0, 0.0), 0.0)
t_pull = 0.3
t_wall = S.t("chispean:", default=2.9)
t_door = S.t("Hasta", default=5.4)
t_scr = S.t("rejilla", default=6.4)
for j in range(4):
    g = S.ball(f"tipglow_{j}", S.accent, 0.6, n.tips[j], shape=(1.0, 1.0, 0.8), parent=n.fork)
    S.gone(g, t_pull + 0.4, 0.5)
pairs = [(n.tips[j], n.tips[j + 1]) for j in range(3)]
mr.burst_arcs(S, S.accent, "arc_fork", pairs, [(0.1, 0.5)], parent=n.fork, r=0.15 / mr.CS, amp=0.55 / mr.CS)


def upd(t):
    mr.spin_plate(n, 0.0)
    n.m.wall_k(0.55 * sp.interp([(t_wall, 0.0), (t_wall + 1.0, 1.0)], t))
    n.m.screen_k(sp.interp([(t_scr, 0.0), (t_scr + 0.6, 1.0)], t))
    mr.set_door(n.o, 1.0 - sp.interp([(t_door, 0.0), (t_door + 1.3, 1.0)], t))
    tx = sp.interp([(0, TF[0]),(t_pull + 1.4, -8.0), (t_door, -8.0), (S.T, -11.0)], t)
    ty = sp.interp([(0, TF[1] + 4.0), (t_pull + 1.4, 0.0), (t_door, 0.0), (S.T, -21.0)], t)
    tz = sp.interp([(0, 4.5), (t_pull + 1.4, 20.0), (t_door, 20.0), (S.T, 22.0)], t)
    rad = sp.interp([(0, 30.0), (t_pull + 1.4, 190.0), (t_door, 190.0), (S.T, 75.0)], t)
    el = sp.interp([(0, 76.0), (t_pull + 1.4, 14.0), (S.T, 4.0)], t)
    az = sp.interp([(0, 12.0), (t_pull + 1.4, 10.0), (S.T, 0.0)], t)
    mr.look(S, (tx, ty, tz), rad, el, az)
    n.lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(-5, -30, 22))
S.go()
