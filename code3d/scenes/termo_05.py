"""termo 5 (espejo): the inner wall is a mirror: infrared light bounces back to the coffee."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import flask_rig as fr  # noqa: E402

S = sp.Shot(158, floor_z=0.0)
M = fr.palette(S)
P = fr.section(S, M, mirror=True)
te = S.t("rebota", default=2.4)
def photon(i, t):
    t0 = 0.6 + 0.35 * i
    u = (t - t0) / 2.4
    if u < 0 or u > 1.0:
        return None
    z = 5.0 + 1.8 * i
    xhit = fr.XC + 0.5
    if u < 0.5:
        x = 0.0 + xhit * (u / 0.5)
        zz = z
    else:
        x = xhit - xhit * ((u - 0.5) / 0.5)
        zz = z + 1.6 * ((u - 0.5) / 0.5) * (1 if i % 2 else -1)
    return ((x, -1.0, zz), 0.7)
fr.heat(S, M, 6, photon)
S.cam([(0, (2, 0, 9), 50, 1, -10), (S.T, (3, 0, 9), 28, 0, 6)])
S.go()
