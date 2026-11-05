"""termo 4 (vacío): the contact and air trails reach the inner wall and have no path: they stop and fall back; marks on the gap."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import flask_rig as fr  # noqa: E402

S = sp.Shot(172, floor_z=0.0)
M = fr.palette(S)
P = fr.section(S, M)
ts = S.t("sin", default=0.8)
def lane(i, t):
    g, k = divmod(i, 5)
    t0 = ts + 0.15 * k + (0.0 if g == 0 else 0.5)
    z = 14.0 if g == 0 else 9.0
    u = (t - t0) / 2.0
    if u < 0 or u > 1.0:
        return None
    stop = fr.XC + 0.6
    if u < 0.55:
        x = 0.5 + (stop - 0.5) * (u / 0.55)
    else:
        x = stop - 3.0 * ((u - 0.55) / 0.45)
    return ((x, -1.0, z + 0.4 * math.sin(u * 20 + i)), 1.0 - 0.8 * max(0.0, u - 0.55) / 0.45)
fr.heat(S, M, 10, lane)
for j, z in enumerate((14.0, 9.0)):
    S.torus(f"x{j}", 1.1, 0.14, (fr.XG, -1.2, z), M["ring"], rot=(math.pi / 2, 0, 0), pop=(ts + 1.3 + 0.4 * j, 0.3))
S.cam([(0, (3, 0, 11), 54, 1, -6), (S.T, (fr.XG - 0.5, 0, 11.5), 24, 0, 6)])
S.go()
