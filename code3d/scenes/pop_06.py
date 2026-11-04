"""palomitas 6 (olla llena): kernels in a pot pop one after another into popcorn that fills the pot and spills over."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import pop_rig as pr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(175)
M = pr.palette(S)
t_seg, t_dec = S.t("segundos,", default=0.3), S.t("decenas", default=3.6)
S.box("table", (40.0, 20.0, 0.8), (0, 0, -0.4), M["plate"], bevel=0.3, pop=(0.05, 0.4))
S.cyl("pot", 4.8, 3.8, (0, 0, 2.1), M["steel"], axis="Z", verts=64, bevel=0.2, pop=(0.05, 0.4))
S.cyl("oil", 4.4, 0.25, (0, 0, 4.1), M["oil"], axis="Z", verts=64, pop=(0.1, 0.4))
rnd = random.Random(12)
N = 44
pos = []
while len(pos) < N:
    p = (rnd.uniform(-3.6, 3.6), rnd.uniform(-3.6, 3.6))
    if p[0] ** 2 + p[1] ** 2 < 3.5 ** 2:
        pos.append(p)
tpop = sorted(rnd.uniform(0.5, 3.9) for _ in range(N))
kk = S.ball("k", M["kernel"], 0.55, (0, 0, 0), shape=(1.0, 0.85, 1.3), seg=18)
S.swarm(N, kk, lambda i, t: ((pos[i][0], pos[i][1], 4.6 + 0.12 * math.sin(9 * t + i)), 1.0) if 0.2 < t < tpop[i] else None)
pf = pr.puff(S, M, "pc")
over = [(rnd.uniform(0, 6.3), rnd.uniform(5.0, 10.5)) for _ in range(N)]
def popc(i, t):
    t0 = tpop[i]
    if t < t0:
        return None
    k = (t - t0)
    layer = 5.2 + 3.4 * (i / N) + 0.6 * math.sin(i * 1.7)
    up = 6.0 * math.sin(min(1.0, k / 0.6) * math.pi) * (1 if k < 0.6 else 0)
    s = 0.25 + 0.5 * min(1.0, k / 0.25)
    x, y = pos[i]
    if i > N * 0.55 and t > t_dec + 0.4 + (i - N * 0.55) * 0.05:      # spill over the rim and roll onto the table
        j = min(1.0, (t - (t_dec + 0.4 + (i - N * 0.55) * 0.05)) / 0.9)
        ang, R = over[i]
        return (x + (R * math.cos(ang) - x) * j, y + (R * math.sin(ang) - y) * j, layer * (1 - j) + 0.9 * j + 2.5 * math.sin(math.pi * j)), s, (0, 0, ang)
    return (x * 0.8, y * 0.8, layer + up), s, (0, 0, i)
S.swarm(N, pf, popc)
lid = S.cyl("lid", 4.9, 0.3, (0, 0, 10.0), M["steel"], axis="Z", verts=48)
S.move(lid, [(0, (0, 0, 40.0)), (t_dec - 0.2, (0, 0, 40.0)), (t_dec, (0, 0, 14.0))])
S.cam([(0, (0, 0, 5), 24, 20, -30), (t_dec, (0, 0, 6), 34, 16, 6), (S.T, (0, 0, 5), 52, 28, 24)])
S.go()
