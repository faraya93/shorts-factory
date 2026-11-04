"""hielo 2 (expansion): water molecules packed in a beaker; they open into a lattice (bonds drawn), and the level rises 9 % over the marker."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_rig as ir  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(260)
M = ir.palette(S)
t_cong, t_exp, t_red, t_nue = S.t("congelarse,", default=1.2), S.t("expande:", default=2.5), S.t("red", default=4.5), S.t("nueve", default=6.2)
S.box("plate", (9.0, 5.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
bk = S.box("beaker", (6.0, 3.4, 10.0), (0, 0, 5.0), M["glass"], bevel=0.25, pop=(0.1, 0.45))
lvl = S.box("level", (5.7, 3.1, 6.0), (0, 0, 3.2), M["water"], bevel=0.15, pop=(0.2, 0.45))
def level_fn(t):
    k = 1.0 + 0.09 * c.smooth(t_nue - 0.4, t_nue + 0.9, t)
    lvl.scale = (1.0, 1.0, k)
    lvl.location = (0, 0, 0.2 + 3.0 * k)
S.every_frame(level_fn)
# marker at the original level
S.box("mark", (6.4, 3.8, 0.12), (0, 0, 6.35), S.accent, bevel=0.04, pop=(1.0, 0.3))
N = 36
rnd = random.Random(21)
liq = []
while len(liq) < N:                                                    # blue-noise-ish packing in the liquid
    p = (rnd.uniform(-2.2, 2.2), rnd.uniform(-1.1, 1.1), rnd.uniform(0.8, 5.5))
    if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2 > 0.95 for q in liq):
        liq.append(p)
lat = ir.lattice_points(4, 3, 3, 1.3, 1.0, 1.35, 0.9)
ox = S.ball("ox", M["ox"], 0.62, (0, 0, 0), seg=18)
hy = S.ball("hy", M["hy"], 0.34, (0, 0, 0), seg=12)
def opos(i, t):
    a = liq[i]
    b = lat[i]
    k = c.smooth(t_exp, t_exp + 1.6, t)
    jit = (1 - k) * 0.22
    return (a[0] * (1 - k) + b[0] * k + jit * math.sin(5.1 * t + i), a[1] * (1 - k) + b[1] * k + jit * math.sin(4.3 * t + 2 * i), a[2] * (1 - k) + b[2] * k + jit * math.sin(6.1 * t + 3 * i))
def oxy(i, t):
    return (opos(i, t), 1.0) if t > 0.5 + 0.02 * i else None
def hyd(i, t):
    o = opos(i // 2, t)
    if t <= 0.5 + 0.02 * (i // 2):
        return None
    s = 1 if i % 2 == 0 else -1
    ang = 0.9 * math.sin(2.0 * t + i)
    return (o[0] + s * 0.68 * math.cos(0.9 + ang), o[1], o[2] + 0.62 * math.sin(0.9 + ang) * (1 if True else 0)), 1.0
S.swarm(N, ox, oxy)
S.swarm(2 * N, hy, hyd)
# open-lattice bonds between neighbours of the front layer, drawn on "red abierta"
front = [i for i, p in enumerate(lat) if abs(p[1] - lat[0][1]) < 1e-6]
for a in front:
    for b in front:
        if a < b and abs(math.dist(lat[a], lat[b]) - 1.3) < 0.05 or a < b and abs(math.dist(lat[a], lat[b]) - 1.35) < 0.4 and abs(lat[a][0] - lat[b][0]) < 1e-6:
            pa, pb = lat[a], lat[b]
            S.line("bond", [(pa[0], pa[1] - 0.2, pa[2]), (pb[0], pb[1] - 0.2, pb[2])], 0.07, S.accent, grow=(t_red, t_red + 0.8), smooth=False)
S.cam([(0, (0, 0, 5), 32, 10, -26), (2.4, (0, 0, 4.5), 26, 8, -6), (4.6, (0, 0, 4.2), 18, 6, 10), (t_nue, (0, 0, 5.5), 28, 10, 4), (S.T, (0, 0, 5.5), 34, 14, -10)])
S.go()
