"""palomitas 3 (presion): the drop boils into steam that bounces faster inside; the dial climbs; the shell swells and shakes."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import pop_rig as pr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(184)
M = pr.palette(S)
t_hie, t_cas, t_pre = S.t("hierve,", default=1.6), S.t("cáscara", default=2.4), S.t("presión", default=4.2)
S.box("table", (24.0, 12.0, 0.8), (0, 0, -0.4), M["plate"], bevel=0.3, pop=(0.05, 0.4))
C = (-2.2, 0, 6.2)
big = 3.0
shell = S.ball("shell", M["shell"], 1.0, C, shape=(1.0 * big, 0.85 * big, 1.3 * big), pop=(0.05, 0.4), seg=40)
core = S.ball("core", M["starch"], 1.0, C, shape=(0.82 * big, 0.68 * big, 1.1 * big), pop=(0.1, 0.4), seg=32)
drop = S.ball("drop", M["drop"], 1.6, (C[0], C[1] - 0.2, C[2] - 0.5), pop=(0.2, 0.4), seg=24)
S.gone(drop, t_hie, 0.5)
def swell(t):
    k = c.smooth(t_hie, t_pre + 1.2, t)
    j = 0.05 * k * math.sin(40 * t)
    shell.scale = tuple(b * (1.0 + 0.16 * k + j) for b in (1.0 * big, 0.85 * big, 1.3 * big))
S.every_frame(swell)
rnd = random.Random(6)
st = S.ball("steam", M["steam"], 0.34, (0, 0, 0), seg=10)
sp_ = [(rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(0, 6.3)) for _ in range(46)]
def steam(i, t):
    if t < t_hie + 0.02 * i:
        return None
    k = c.smooth(t_hie, t_pre + 1.2, t)
    a = sp_[i]
    sp = 4.0 + 16.0 * k
    return (C[0] + a[0] * 1.9 * math.sin(sp * 0.25 * t + a[3]) * 0.9, C[1] + a[1] * 1.3 * math.cos(sp * 0.21 * t + a[3]), C[2] + a[2] * 2.6 * math.sin(sp * 0.19 * t + 2 * a[3])), 1.0
S.swarm(46, st, steam)
needle, setp = pr.dial(S, M, (6.4, -0.5, 6.4), r=2.5, t0=t_hie - 0.2)
S.every_frame(lambda t: setp(c.smooth(t_hie, t_pre + 1.4, t)))
ar = S.cone("arrow", 0.6, 0.0, 1.8, (0, 0, 0), S.accent)
S.swarm(3, ar, lambda i, t: ((C[0] - 2.0 + 2.0 * i, -1.5, 0.9 + 0.5 * math.sin(7 * t + i)), 0.7 + 0.3 * math.sin(7 * t + i)) if t > 0.3 else None)
S.cam([(0, (1.5, 0, 6.2), 36, 10, -26), (t_hie, (1.5, 0, 6.2), 26, 8, -8), (S.T, (0.5, 0, 6.2), 19, 6, 10)])
S.go()
