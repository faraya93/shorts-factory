"""termo 1 (hook): the open flask lets steam out; the cap drops on and the steam stops."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import flask_rig as fr  # noqa: E402

S = sp.Shot(285, floor_z=0.0)
M = fr.palette(S)
body, cap = fr.flask(S, M, (0, 0, 0))
tc = S.t("espuma", default=5.0)
S.move(cap, [(0, (0, 0, fr.CAP_UP)), (tc - 0.3, (0, 0, fr.CAP_UP)), (tc + 0.25, (0, 0, fr.CAP_Z))])
steam = S.ball("steam", M["steam"], 0.8, (0, 0, 0))
def puff(i, t):
    if t > tc:
        return None
    a = 0.3 + i * 0.22
    if t < a:
        return None
    u = (t - a) % 2.4
    k = u / 2.4
    return ((math.sin(i * 2.1 + u * 3) * (0.8 + 1.4 * k), math.cos(i * 1.3) * 0.8, 31.0 + 9 * k), (0.5 + 1.1 * k) * (1 - k))
S.swarm(12, steam, puff)
S.cam([(0, (0, 0, 17), 98, 8, -35), (S.T * 0.5, (0, 0, 17), 82, 10, 5), (S.T, (0, 0, 17), 72, 8, 38)])
S.go()
