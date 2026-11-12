"""micro 2 (ondas): see productions/mecanalia-es/022*/script.json. Accent wave fronts bounce between the cavity walls, and a glow of charge sloshes back and forth inside the fork and the spoon in time with them; the camera travels sideways across the cavity."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import micro_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(320, floor_z=-0.6)
n = mr.build(S)
W = mr.waves(S, n.m)
t_w = S.t("rebotan", default=1.2)
t_b = S.t("campo", default=3.2)
SPEED = 24.0


def slosh(i, t, lo, hi):
    if t < t_b:
        return None
    k = sp.interp([(t_b + 0.05 * i, 0.0), (t_b + 0.05 * i + 0.4, 1.0)], t)
    x = (lo + hi) / 2 + (hi - lo) / 2 * 0.8 * math.sin(2 * math.pi * 0.62 * (t - t_b) + 0.35 * i * 0.0) + (i - 4) * 0.5
    return (max(lo, min(hi, x)), 0.0, 0.55), 0.8 * k


fb = mr.beads(S, n.m, n.fork, "charge_f", 9, lambda i, t: slosh(i, t, -10.0, 12.0))
sb = mr.beads(S, n.m, n.spoon, "charge_s", 9, lambda i, t: slosh(i, t, -10.0, 11.0))


def upd(t):
    mr.spin_plate(n, mr.plate_angle(t, 0.3))
    n.m.wave_k(0.3 *sp.interp([(t_w, 0.0), (t_w + 0.8, 1.0)], t))
    mr.set_waves(W, t, SPEED)
    tx = sp.interp([(0, -22.0), (S.T, 4.0)], t)
    az = sp.interp([(0, -12.0), (S.T, 16.0)], t)
    rad = sp.interp([(0, 150.0), (S.T, 118.0)], t)
    mr.look(S, (tx, 0.0, 14.0), rad, 14.0, az)
    n.lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(-5, -30, 22))
S.go()
