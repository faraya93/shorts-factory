"""micro 3 (puntas): see productions/mecanalia-es/022*/script.json. Close-up side by side: the glow of charge spreads evenly over the spoon's bowl, while on the fork it drains into the four tine tips, which brighten one by one; the camera pushes from the spoon to the tines."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import micro_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(240, floor_z=-0.6)
n = mr.build(S)
TS = mr.spoon_pt((4.0, 0.0, 0.0), 0.0)
TF = mr.fork_pt((8.0, 0.0, 0.0), 0.0)
t_s = S.t("cuchara", default=0.5)
t_f = S.t("tenedor", default=3.0)
NB = 16


def spoon_bead(i, t):
    if i < NB:                                              # over the bowl: a sunflower spread
        r = math.sqrt((i + 0.5) / NB)
        a = i * 2.4
        p = (7.2 + 4.6 * r * math.cos(a), 3.0 * r * math.sin(a), 0.4)
    else:                                                   # and along the handle
        p = (-10.0 + (i - NB) * 2.6, 0.0, 0.4)
    return p, 0.55 * sp.interp([(t_s + 0.04 * i, 0.0), (t_s + 0.04 * i + 0.4, 1.0)], t)


def fork_bead(i, t):
    j = i % 4                                               # which tine it drains into
    start = (-10.0 + (i * 1.37) % 19.0, ((i * 5) % 7 - 3) * 0.5, 0.4)
    tip = n.tips[j]
    ta = t_f + 0.12 * i
    k = sp.interp([(ta, 0.0), (ta + 1.1, 1.0)], t)
    p = tuple(a + (b - a) * k for a, b in zip(start, (tip[0] - 0.3, tip[1], 0.4)))
    s = sp.interp([(t_s + 0.04 * i, 0.0), (t_s + 0.04 * i + 0.4, 1.0)], t) * (1.0 - sp.interp([(ta + 0.95, 0.0), (ta + 1.15, 1.0)], t))
    return p, 0.55 * s


mr.beads(S, n.m, n.spoon, "charge_s", NB + 4, spoon_bead)
mr.beads(S, n.m, n.fork, "charge_f", 20, fork_bead)
tipb = []
for j in range(4):
    o = S.ball(f"tipglow_{j}", S.accent, 0.6, n.tips[j], shape=(1.0, 1.0, 0.8), parent=n.fork)
    S.pop(o, t_f + 1.2 + 0.45 * j, 0.4)
    tipb.append(o)


def upd(t):
    mr.spin_plate(n, 0.0)
    k = sp.interp([(0.6, 0.0), (S.T - 0.4, 1.0)], t)
    tx = sp.interp([(0, TS[0]), (S.T, TF[0])], t)
    ty = sp.interp([(0, TS[1] + 3.0), (S.T, TF[1] + 4.0)], t)
    rad = sp.interp([(0, 66.0), (S.T, 34.0)], t)
    mr.look(S, (tx, ty, 4.5), rad, sp.interp([(0, 64.0), (S.T, 66.0)], t), sp.interp([(0, 8.0), (S.T, -4.0)], t))
    n.lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(-5, -30, 22))
S.go()
