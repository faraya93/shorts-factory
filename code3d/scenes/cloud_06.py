"""nube 6 (millon): one raindrop bursts into a cloud of tiny droplets (about a million of them: drawn as hundreds); the camera pulls back."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import cloud_rig as cr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(135)
M = cr.palette(S)
t_mil = S.t("millón", default=2.4)
big = S.ball("rain", M["drop_solid"], 3.0, (0, 0, 8), seg=48, pop=(0.1, 0.5))
S.gone(big, t_mil, 0.2)
S.move(big, [(0, (0, 0, 8.4)), (t_mil, (0, 0, 7.6))])
N = 700
rnd = random.Random(12)
dirs = []
while len(dirs) < N:
    v = (rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1))
    n2 = sum(a * a for a in v)
    if 0.05 < n2 <= 1.0:
        n = math.sqrt(n2)
        dirs.append((v[0] / n, v[1] / n, v[2] / n, rnd.uniform(0.35, 1.0)))
tiny = S.ball("tiny", M["drop_solid"], 0.28, (0, 0, 0), seg=8)
def burst(i, t):
    if t < t_mil:
        return None
    dx, dy, dz, rr = dirs[i]
    k = c.smooth(t_mil, t_mil + 1.6, t)
    R = 2.6 + 11.0 * rr * k
    return (dx * R, dy * R * 0.8, 8.0 + dz * R), 0.6 + 0.4 * k
S.swarm(N, tiny, burst)
S.cam([(0, (0, 0, 8), 24, 8, -22), (t_mil, (0, 0, 8), 21, 8, 0), (S.T, (0, 0, 8), 52, 12, 22)])
S.go()
