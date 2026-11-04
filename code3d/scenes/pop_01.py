"""palomitas 1 (olla): kernels bob in hot oil over blue flames (the false culprit crossed out); the camera dives into one kernel."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import pop_rig as pr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(242)
M = pr.palette(S)
t_ace, t_ady = S.t("aceite", default=4.8), S.t("adentro.", default=6.8)
S.box("table", (30.0, 14.0, 0.8), (0, 0, -0.4), M["plate"], bevel=0.3, pop=(0.05, 0.4))
S.cyl("pot", 4.8, 3.8, (0, 0, 2.1), M["steel"], axis="Z", verts=64, bevel=0.2, pop=(0.1, 0.45))
S.cyl("oil", 4.4, 0.25, (0, 0, 4.1), M["oil"], axis="Z", verts=64, pop=(0.4, 0.4))
rnd = random.Random(2)
kk = S.ball("k", M["kernel"], 0.55, (0, 0, 0), shape=(1.0, 0.85, 1.3), seg=20)
ks = [(rnd.uniform(-3.4, 3.4), rnd.uniform(-3.0, 3.0), rnd.uniform(0, 6.3)) for _ in range(30)]
ks = [p for p in ks if p[0] ** 2 + p[1] ** 2 < 3.6 ** 2][:24]
def kern(i, t):
    x, y, ph = ks[i]
    if t < 0.6 + 0.04 * i:
        return None
    return (x + 0.15 * math.sin(2 * t + ph), y, 4.6 + 0.18 * abs(math.sin(3 * t + ph))), 1.0
S.swarm(len(ks), kk, kern)
hero = S.ball("hero", M["kernel"], 0.8, (0.8, -2.3, 4.9), shape=(1.0, 0.85, 1.3), pop=(0.9, 0.4), seg=28)
bub = S.ball("bub", M["steam"], 0.22, (0, 0, 0), seg=10)
bp = [(rnd.uniform(-3.5, 3.5), rnd.uniform(-3, 3), rnd.uniform(0, 1)) for _ in range(40)]
S.swarm(40, bub, lambda i, t: ((bp[i][0], bp[i][1], 4.3 + ((t * 0.9 + bp[i][2]) % 1.0) * 2.2), 0.5 + 0.5 * math.sin(math.pi * ((t * 0.9 + bp[i][2]) % 1.0))) if t > 1.0 and bp[i][0] ** 2 + bp[i][1] ** 2 < 14 else None)
fl = S.cone("flame", 0.7, 0.0, 2.2, (0, 0, -0.2), S.accent)
def flames(i, t):
    a = 2 * math.pi * i / 9
    return (2.6 * math.cos(a), 2.6 * math.sin(a), 0.7), 0.7 + 0.35 * math.sin(11 * t + i * 1.7)
S.swarm(9, fl, flames)
for nm, a in (("xa", 1), ("xb", -1)):
    S.box(nm, (5.0, 0.4, 0.6), (0, -5.6, 8.6), S.error, bevel=0.2, rot=(0, math.radians(45 * a), 0), pop=(t_ace + 0.05, 0.3))
S.cam([(0, (0, 0, 4.5), 34, 22, -34), (2.5, (0, 0, 4.5), 26, 18, 10), (t_ace + 0.5, (0, 0, 4.8), 22, 16, 30), (t_ady, (0.8, -2.3, 4.9), 9, 10, 8), (S.T, (0.8, -2.3, 5.0), 5.5, 6, 0)])
S.go()
