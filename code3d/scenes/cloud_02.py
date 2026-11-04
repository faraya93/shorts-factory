"""nube 2 (cubo): the cloud turns into millions of droplets; a 1 km cube outlines it; the droplets fall into one block of water (500,000 kg)."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import cloud_rig as cr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(268)
M = cr.palette(S)
t_got, t_km, t_q = S.t("gotitas", default=1.6), S.t("kilómetro", default=4.9), S.t("quinientos", default=6.6)
C = (0, 0, 10)
for p in cr.puffs(S, M, C, n=26, rx=4.4, ry=2.4, rz=2.6, seed=2, pop0=0.1, stagger=0.03, r=(1.1, 2.0)):
    S.gone(p, t_got, 0.5)
N = 170
pts = cr.blob_points(N, 4.4, 2.4, 3.0, seed=9, flat_bottom=False)
rnd = random.Random(5)
ph = [(rnd.uniform(0, 6.3), rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)) for _ in range(N)]
drop = S.ball("drop", M["drop_solid"], 0.4, (0, 0, 0), seg=14)
water = S.box("block", (9.4, 4.8, 3.2), (0, 0, 1.6), M["drop"], bevel=0.3)
S.size(water, [(0, (1, 1, 1e-3)), (t_q + 0.3, (1, 1, 1e-3)), (t_q + 2.2, (1, 1, 1.0))])
water.location = (0, 0, 1.6 * 0)  # grows from the floor: re-anchored in the frame callback
def grow(t):
    k = max(1e-3, sp.interp([(0, 1e-3), (t_q + 0.3, 1e-3), (t_q + 2.2, 1.0)], t))
    water.location = (0, 0, 1.6 * k)
S.every_frame(grow)
def droplets(i, t):
    if t < t_got - 0.2:
        return None
    x, y, z = pts[i]
    a = ph[i]
    tt = t - t_got
    s = min(1.0, tt / 0.5 + 0.05)
    pos = (C[0] + x + 0.25 * math.sin(2.1 * t + a[0]), y + 0.25 * math.sin(1.7 * t + a[1]), C[2] + z + 0.25 * math.sin(2.6 * t + a[2]))
    tf = t_q + (i / N) * 1.4
    if t > tf:
        k = min(1.0, (t - tf) / 0.9)
        k2 = k * k
        pos = (pos[0] * (1 - k2) + (x * 0.9) * k2 * 0.9, pos[1] * (1 - k2) + y * 0.6 * k2, pos[2] * (1 - k2) + 2.0 * k2)
        if k >= 1.0:
            return None
        s *= 1.0 - 0.3 * k
    return pos, s
S.swarm(N, drop, droplets)
cube = cr.cube_frame(S, S.accent, C, 10.6, r=0.1, grow=(t_km - 0.2, t_km + 0.9))
S.cam([(0, (0, 0, 10), 38, 8, -26), (t_got, (0, 0, 10), 24, 8, -6), (t_km, (0, 0, 8), 36, 14, 24), (t_q, (0, 0, 6), 40, 14, 10), (S.T, (0, 0, 5), 34, 18, -14)])
S.go()
