"""palomitas 4 (cede): thermometer and dial hit their limits; the shell shatters into shards in a flash of steam."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import pop_rig as pr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(165)
M = pr.palette(S)
t_nue, t_cie, t_ced = S.t("nueve", default=1.0), S.t("ciento", default=2.0), S.t("cede", default=3.8)
S.box("table", (26.0, 12.0, 0.8), (0, 0, -0.4), M["plate"], bevel=0.3, pop=(0.05, 0.4))
C = (0, 0, 6.0)
big = 2.6
shell = S.ball("shell", M["shell"], 1.0, C, shape=(1.0 * big * 1.16, 0.85 * big * 1.16, 1.3 * big * 1.16), pop=(0.02, 0.3), seg=40)
core = S.ball("core", M["starch"], 1.0, C, shape=(0.82 * big, 0.68 * big, 1.1 * big), pop=(0.02, 0.3), seg=32)
S.gone(shell, t_ced, 0.05)
S.every_frame(lambda t: (setattr(shell, "location", (C[0] + 0.12 * math.sin(60 * t) * (1 if t < t_ced else 0), C[1], C[2])), setattr(core, "location", (C[0] + 0.1 * math.sin(55 * t) * (1 if t < t_ced else 0), C[1], C[2]))))
# thermometer (left) and dial (right)
S.cyl("thermo", 0.7, 9.0, (-8.0, -0.5, 5.0), M["steel"], axis="Z", verts=24, bevel=0.05, pop=(0.1, 0.4))
tf = S.cyl("thermof", 0.46, 8.4, (-8.0, -1.1, 0.8), S.error, axis="Z", verts=24, pop=(0.15, 0.3))
S.every_frame(lambda t: (setattr(tf, "scale", (1, 1, max(1e-3, c.smooth(0.2, t_cie + 0.4, t)))), setattr(tf, "location", (-8.0, -1.1, 0.8 + 4.2 * max(1e-3, c.smooth(0.2, t_cie + 0.4, t))))))
needle, setp = pr.dial(S, M, (8.0, -0.5, 6.2), r=2.4, t0=0.1)
S.every_frame(lambda t: setp(min(1.0, 0.55 + 0.45 * c.smooth(0.2, t_nue + 1.0, t))))
sh = S.box("shard", (0.9, 0.4, 0.7), (0, 0, 0), M["shard"], bevel=0.12)
rnd = random.Random(9)
dirs = []
for _ in range(16):
    v = (rnd.uniform(-1, 1), rnd.uniform(-1, 0.4), rnd.uniform(-0.4, 1))
    n = math.sqrt(sum(a * a for a in v)) or 1
    dirs.append((v[0] / n, v[1] / n, v[2] / n, rnd.uniform(0.7, 1.4)))
def shards(i, t):
    if t < t_ced:
        return None
    k = t - t_ced
    d = dirs[i]
    R = 3.0 + 9.0 * d[3] * (1 - math.exp(-3 * k))
    return (C[0] + d[0] * R, C[1] + d[1] * R, max(0.5, C[2] + d[2] * R - 2.0 * k * k)), 1.0, (k * 6 * d[0], k * 5 * d[1], k * 7 * d[2])
S.swarm(16, sh, shards)
fl = S.ball("flash", S.accent, 1.0, C, seg=24)
S.size(fl, [(t_ced - 0.01, 1e-3), (t_ced + 0.08, 5.0), (t_ced + 0.5, 6.0)]); S.pop(fl, t_ced, 0.05); S.gone(fl, t_ced + 0.06, 0.3)
st = S.ball("puff", M["steam"], 1.2, (0, 0, 0), seg=14)
S.swarm(12, st, lambda i, t: ((C[0] + dirs[i][0] * (2.0 + 6.0 * (t - t_ced)), C[1] - 1.0, C[2] + dirs[i][2] * (2.0 + 5.0 * (t - t_ced))), min(2.0, 0.5 + 2.0 * (t - t_ced))) if t > t_ced else None)
S.cam([(0, (0, 0, 6), 34, 8, -16), (t_ced - 0.3, (0, 0, 6), 26, 6, 0), (t_ced + 0.1, (0, 0, 6), 22, 6, 4), (S.T, (0, 0, 6), 34, 10, 14)])
S.go()
