"""corazon 5 (dia): a few bottles grow into a huge block of bottles (3,000+), camera pulling back and rising."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import heart_rig as hr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(152)
M = hr.palette(S)
t_sie, t_tres = S.t("siete", default=1.1), S.t("tres", default=2.6)
S.box("floor", (80.0, 40.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
tpl = hr.bottle(S, M, "bt")
NX, NY, NZ = 18, 8, 5
cells = [(i, j, k) for k in range(NZ) for j in range(NY) for i in range(NX)]
cells.sort(key=lambda c_: (c_[2] * 3.0 + abs(c_[0] - NX / 2) * 0.35 + abs(c_[1] - NY / 2) * 0.45))
def bot(i, t):
    a, b, k = cells[i]
    born = 0.3 + 0.01 * i * 0.9 + (0.0 if i > 6 else 0.0)
    if t < born:
        return None
    return ((a - NX / 2) * 2.2, (b - NY / 2) * 2.2, k * 4.4), min(1.0, (t - born) / 0.3)
S.swarm(NX * NY * NZ, tpl, bot)
S.cam([(0, (0, 0, 3), 22, 8, -24), (1.5, (0, 0, 6), 40, 14, -4), (S.T, (0, 0, 7), 78, 26, 16)])
S.go()
