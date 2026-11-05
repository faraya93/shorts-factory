"""termo 3 (tres): three heat trails try to leave the coffee: contact (hopping through the walls), air (an arc through the gap), light (straight line)."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import flask_rig as fr  # noqa: E402

S = sp.Shot(178, floor_z=0.0)
M = fr.palette(S)
P = fr.section(S, M)
t1, t2, t3 = S.t("tocando", default=1.0), S.t("aire", default=2.6), S.t("luz", default=4.2)
X0, X1 = 0.5, 9.0
def lane(i, t):
    g, k = divmod(i, 6)                 # group 0 contact (z=14), 1 air (z=10), 2 light (z=6)
    t0 = (t1, t2, t3)[g] + 0.12 * k
    u = (t - t0) / 1.7
    if u < 0 or u > 1.0:
        return None
    x = X0 + (X1 - X0) * u
    if g == 0:
        hop = 0.5 * abs(math.sin(u * 14))
        return ((x, -1.0, 14.0 + hop), 1.0)
    if g == 1:
        return ((x, -1.0, 10.0 + 2.2 * math.sin(u * math.pi) * (1 if k % 2 else -1)), 1.0)
    return ((x, -1.0, 6.0), 0.55)
fr.heat(S, M, 18, lane)
S.cam([(0, (4, 0, 10), 50, 2, -8), (S.T, (5, 0, 10), 34, 1, 6)])
S.go()
