"""nube 4 (reparto): one cubic metre holds three droplets; the camera pulls back over a grid of thousands of such cubes."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import cloud_rig as cr  # noqa: E402

S = sp.Shot(186)
M = cr.palette(S)
t_cub, t_med = S.t("cúbico", default=2.9), S.t("medio", default=4.3)
cube0 = S.box("cube0", (6.0, 6.0, 6.0), (0, 0, 7), M["glass"], bevel=0.3, pop=(0.2, 0.5))
for k, (x, y, z) in enumerate([(-1.2, 0.5, 6.0), (1.4, -0.8, 8.1), (0.2, 1.0, 5.1)]):
    S.ball(f"d{k}", M["drop_solid"], 0.45, (x, y, z), pop=(0.6 + 0.2 * k, 0.4))
cr.cube_frame(S, S.accent, (0, 0, 7), 6.0, r=0.1, grow=(0.3, 1.2))
G = 9
tmpl = S.box("cube", (6.0, 6.0, 6.0), (0, 0, 7), M["glass"], bevel=0.3)
dtmpl = S.ball("dd", M["drop_solid"], 0.45, (0, 0, 7), seg=12)
cells = [(i, j) for i in range(G) for j in range(G)]
cells.sort(key=lambda ij: (ij[0] - G // 2) ** 2 + (ij[1] - G // 2) ** 2)
rnd = random.Random(2)
offs = [[(rnd.uniform(-2, 2), rnd.uniform(-2, 2), rnd.uniform(-2, 2)) for _ in range(3)] for _ in cells]
def cubep(i, t):
    a, b = cells[i]
    if i == 0:
        return None
    born = t_cub + 0.25 * (math.sqrt((a - G // 2) ** 2 + (b - G // 2) ** 2))
    if t < born:
        return None
    k = min(1.0, (t - born) / 0.4)
    return ((a - G // 2) * 6.6, (b - G // 2) * 6.6, 7), k
def dropp(i, t):
    ci, d = i // 3, i % 3
    r = cubep(ci, t)
    if r is None:
        return None
    (x, y, z), k = r
    o = offs[ci][d]
    return (x + o[0], y + o[1], z + o[2]), k
S.swarm(G * G, tmpl, cubep)
S.swarm(G * G * 3, dtmpl, dropp)
S.cam([(0, (0, 0, 7), 24, 8, -20), (t_cub, (0, 0, 7), 28, 12, -4), (t_med + 1.0, (0, 0, 5), 70, 28, 12), (S.T, (0, 0, 2), 96, 40, 26)])
S.go()
