"""micro 6 (cierre): see productions/mecanalia-es/022*/script.json. The single reframe image: the fork's four tips spark once more beside the dark, smooth spoon, while the whole oven glows calmly around them; the camera recoils from the tips to the entire oven."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import micro_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(240, floor_z=-0.6)
n = mr.build(S)
TF = mr.fork_pt((10.0, 0.0, 0.0), 0.0)
t_sp = S.t("chispean", default=1.7)
for j in range(4):
    S.ball(f"tipglow_{j}", S.accent, 0.6, n.tips[j], shape=(1.0, 1.0, 0.8), parent=n.fork)
pairs = [(n.tips[j], n.tips[j + 1]) for j in range(3)]
mr.burst_arcs(S, S.accent, "arc_fork", pairs, [(t_sp, 0.6)], parent=n.fork, r=0.15 / mr.CS, amp=0.55 / mr.CS)


def upd(t):
    mr.spin_plate(n, 0.0)
    n.m.wall_k(0.45 * sp.interp([(t_sp + 0.4, 0.0), (t_sp + 1.6, 1.0)], t))
    tx = sp.interp([(0, TF[0]),(t_sp + 2.0, -8.0), (S.T, -8.0)], t)
    ty = sp.interp([(0, TF[1] + 4.0), (t_sp + 2.0, 0.0), (S.T, 0.0)], t)
    tz = sp.interp([(0, 4.5), (t_sp + 2.0, 20.0), (S.T, 20.0)], t)
    rad = sp.interp([(0, 30.0), (t_sp + 0.8, 34.0), (S.T, 190.0)], t)
    el = sp.interp([(0, 68.0), (t_sp + 0.8, 64.0), (S.T, 12.0)], t)
    az = sp.interp([(0, 12.0), (S.T, 16.0)], t)
    mr.look(S, (tx, ty, tz), rad, el, az)
    n.lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(-5, -30, 22))
S.go()
