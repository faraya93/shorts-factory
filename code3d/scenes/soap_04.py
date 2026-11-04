"""jabon 4 (rodean): a bare grease drop; soap molecules fly in and stick their tails in, heads out; the drop ends coated."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import soap_rig as sr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(178)
M = sr.palette(S)
t_col, t_cab, t_rod = S.t("colas", default=0.3), S.t("cabezas", default=2.0), S.t("rodean", default=4.2)
C = (0, 0, 7.0)
blob = S.ball("grease", M["oil"], 3.3, C, pop=(0.1, 0.5), seg=40)
S.every_frame(lambda t: setattr(blob, "location", (C[0], C[1], C[2] + 0.12 * math.sin(3 * t))))
tpl = sr.molecule(S, M, "mol")
N = 34
dirs = sr.sphere_points(N, 0.7)
rnd = random.Random(7)
far = [(d[0] * 13 + rnd.uniform(-2, 2), d[1] * 13, d[2] * 13) for d in dirs]
eul = [sr.face(d) for d in dirs]
def mol(i, t):
    t0 = 0.5 + 0.08 * i
    if t < t0:
        return None
    k = c.smooth(t0, t0 + 1.1, t)
    R = 3.7 * k + 13.0 * (1 - k)
    p = dirs[i]
    pos = (C[0] + p[0] * R, C[1] + p[1] * R, C[2] + p[2] * R)
    return pos, 1.0, eul[i]
S.swarm(N, tpl, mol)
S.cam([(0, (0, 0, 7), 44, 8, -24), (2.0, (0, 0, 7), 26, 10, 40), (4.2, (0, 0, 7), 20, 6, 120), (S.T, (0, 0, 7), 24, 14, 200)])
S.go()
