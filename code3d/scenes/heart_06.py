"""corazon 6 (vida): one pool, then more than eighty in a grid, the camera rising to a top view."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import heart_rig as hr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(179)
M = hr.palette(S)
t_och, t_pis = S.t("ochenta", default=0.3), S.t("piscinas", default=4.0)
S.box("floor", (200.0, 120.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
rim = S.box("rim", (9.2, 5.2, 0.5), (0, 0, 0.25), M["board"], bevel=0.2)
water = S.box("water", (8.2, 4.2, 0.9), (0, 0, 0.7), M["pool"], bevel=0.2)
NX, NY = 10, 9
cells = [(i, j) for i in range(NX) for j in range(NY)]
cells.sort(key=lambda ij: math.hypot(ij[0] - 4.5, (ij[1] - 4.0) * 1.2))
cells = cells[:84]
def pl(i, t):
    a, b = cells[i]
    born = 0.25 if i == 0 else 2.0 + 0.03 * i
    if t < born:
        return None
    return ((a - 4.5) * 11.0, (b - 4.0) * 7.0, 0.0), min(1.0, (t - born) / 0.35)
S.swarm(len(cells), rim, pl)
S.swarm(len(cells), water, pl)
S.cam([(0, (0, 0, 1), 16, 14, -26), (2.0, (0, 0, 1), 20, 22, -8), (4.0, (0, 0, 0), 84, 50, 8), (S.T, (0, 0, 0), 130, 76, 12)])
S.go()
