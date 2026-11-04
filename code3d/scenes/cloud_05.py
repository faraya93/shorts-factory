"""nube 5 (lluvia): droplets collide and merge, grow, and one grows too heavy and falls; splash and rain."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import cloud_rig as cr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(226)
M = cr.palette(S)
t_cho, t_cre, t_cae, t_llu = S.t("chocan", default=0.9), S.t("crecen.", default=2.0), S.t("cae:", default=5.4), S.t("lluvia.", default=6.3)
CZ = 13.0
for p in cr.puffs(S, M, (0, 0, CZ + 2.5), n=22, rx=6.0, ry=2.4, rz=2.2, seed=6, pop0=0.1, stagger=0.02, r=(1.2, 2.0)):
    pass
N = 48
pts = cr.blob_points(N, 5.0, 1.6, 1.0, seed=11, flat_bottom=False)
drop = S.ball("drop", M["drop_solid"], 0.4, (0, 0, 0), seg=14)
def drops(i, t):
    x, y, z = pts[i]
    base = (x, y, CZ - 0.6 + z)
    if t < 0.3 + i * 0.01:
        return None
    wob = (0.2 * math.sin(2.0 * t + i), 0.0, 0.25 * math.sin(2.3 * t + 2 * i))
    pos = (base[0] + wob[0], base[1], base[2] + wob[2])
    pair = i // 2
    if t > t_cho + 0.1 * pair / 3:                                    # merge: pairs close in on their midpoint, the second vanishes, the first grows
        mate = i ^ 1
        mid = ((pts[i][0] + pts[mate][0]) / 2, (pts[i][1] + pts[mate][1]) / 2, CZ - 0.6 + (pts[i][2] + pts[mate][2]) / 2)
        k = c.smooth(t_cho + 0.1 * pair / 3, t_cho + 0.1 * pair / 3 + 0.9, t)
        pos = (pos[0] * (1 - k) + mid[0] * k, pos[1] * (1 - k) + mid[1] * k, pos[2] * (1 - k) + mid[2] * k)
        if i % 2 == 1:
            return None if k > 0.85 else (pos, 1.0)
        return pos, 1.0 + 0.5 * k + 0.6 * c.smooth(t_cre - 0.2, t_cre + 1.2, t) * (1 if i % 8 == 0 else 0.35)
    return pos, 1.0
S.swarm(N, drop, drops)
big = S.ball("big", M["drop_solid"], 1.5, (0, -1.0, CZ - 0.6), seg=32, pop=(t_cre + 1.0, 0.5))
S.move(big, [(t_cre + 1.0, (0.5, -1.0, CZ - 0.6)), (t_cae, (0.5, -1.0, CZ - 0.9)), (t_cae + 0.9, (0.8, -1.0, 1.2))])
S.gone(big, t_cae + 0.85, 0.15)
for k in range(3):
    r = S.torus(f"splash{k}", 1.0, 0.1, (0.8, -1.0, 0.3), M["drop"], rot=(0, 0, 0))
    a = t_cae + 0.85 + 0.2 * k
    S.size(r, [(a, 0.3), (a + 1.2, 4.0 + k)]); S.pop(r, a, 0.05); S.gone(r, a + 0.8, 0.5)
ground = S.box("ground", (22.0, 8.0, 0.5), (0, 0, -0.1), M["plate"], bevel=0.2, pop=(t_cae - 1.0, 0.5))
rn = random.Random(3)
rx = [(rn.uniform(-9, 9), rn.uniform(-2, 2), rn.uniform(0, 1)) for _ in range(40)]
streak = S.cyl("streak", 0.12, 1.3, (0, 0, 0), M["drop_solid"], axis="Z", verts=8)
def rain(i, t):
    if t < t_llu:
        return None
    x, y, ph = rx[i]
    k = ((t - t_llu) * 1.2 + ph) % 1.0
    return (x, y, CZ - 0.5 - k * (CZ - 0.2)), 1.0
S.swarm(40, streak, rain)
S.cam([(0, (0, 0, 13), 40, 4, -20), (3.0, (0, 0, 13), 34, 6, 0), (t_cae, (0, 0, 11), 34, 8, 10), (t_cae + 1.0, (0, 0, 5), 30, 14, 6), (S.T, (0, 0, 5.5), 40, 20, -8)])
S.go()
