"""jabon 6 (enjuague): the coated droplets drift in the water and the current carries them out of frame; the palm is left clean."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import soap_rig as sr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(151)
M = sr.palette(S)
t_cub, t_enj = S.t("Cubiertas", default=0.1), S.t("enjuague", default=3.6)
S.box("palm", (30.0, 8.0, 0.9), (4.0, 0, 0.0), M["plate"], bevel=0.35, pop=(0.05, 0.4))
sm = S.ball("small", M["oil"], 1.1, (0, 0, 0), seg=24)
tpl = sr.molecule(S, M, "mol")
msd = sr.sphere_points(8, 0.3)
meul = [sr.face(d) for d in msd]
rnd = random.Random(8)
cen0 = [(-2.0 + 3.2 * (i % 4) + rnd.uniform(-0.6, 0.6), rnd.uniform(-1.4, 1.4), 3.4 + 2.6 * (i // 4) + rnd.uniform(-0.4, 0.4)) for i in range(8)]
def cen(i, t):
    k = c.smooth(t_enj - 0.6, t_enj + 1.4, t)
    x0, y0, z0 = cen0[i]
    return (x0 + 24.0 * k * k + 0.4 * math.sin(2 * t + i), y0, z0 + 0.4 * math.sin(2.3 * t + 2 * i) - 1.6 * k)
S.swarm(8, sm, lambda i, t: (cen(i, t), 1.0))
S.swarm(64, tpl, lambda i, t: ((lambda ctr, d: (ctr[0] + d[0] * 1.25, ctr[1] + d[1] * 1.25, ctr[2] + d[2] * 1.25))(cen(i // 8, t), msd[i % 8]), 0.6, meul[i % 8]))
wat = S.ball("wat", M["water"], 0.42, (0, 0, 0), seg=12)
wr_ = [(rnd.uniform(-8, 24), rnd.uniform(-2.5, 2.5), rnd.uniform(1.0, 9.0), rnd.uniform(0, 1)) for _ in range(70)]
def wat_f(i, t):
    x, y, z, ph = wr_[i]
    k = c.smooth(t_enj - 0.8, t_enj + 1.6, t)
    return (x + 18.0 * k * k + 0.4 * math.sin(2 * t + i) + 0.8 * t * 0.0, y, z + 0.3 * math.sin(1.9 * t + i)), 1.0
S.swarm(70, wat, wat_f)
S.cam([(0, (0, 0, 5), 32, 10, -22), (t_enj - 0.5, (2, 0, 5), 30, 8, -8), (S.T, (10, 0, 5), 34, 8, 8)])
S.go()
