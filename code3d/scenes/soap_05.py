"""jabon 5 (bolitas): the coated drop is rubbed (shakes), then breaks into eight small coated droplets that fly apart; pull-back."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import soap_rig as sr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(188)
M = sr.palette(S)
t_fro, t_rom, t_bol = S.t("frotar,", default=0.7), S.t("rompe", default=2.3), S.t("bolitas", default=3.5)
C = (0, 0, 7.0)
blob = S.ball("grease", M["oil"], 3.3, C, pop=(0.05, 0.4), seg=40)
S.gone(blob, t_rom, 0.2)
S.every_frame(lambda t: blob.__setattr__("location", (C[0] + 0.5 * math.sin(26 * t) * c.smooth(t_fro, t_fro + 0.4, t) * (1 - c.smooth(t_rom - 0.2, t_rom, t)), C[1], C[2])))
tpl = sr.molecule(S, M, "mol")
N = 30
dirs = sr.sphere_points(N, 0.7)
eul = [sr.face(d) for d in dirs]
def big_coat(i, t):
    if t > t_rom:
        return None
    jx = 0.5 * math.sin(26 * t) * c.smooth(t_fro, t_fro + 0.4, t)
    p = dirs[i]
    return (C[0] + p[0] * 3.7 + jx, C[1] + p[1] * 3.7, C[2] + p[2] * 3.7), 1.0, eul[i]
S.swarm(N, tpl, big_coat)
# eight small coated droplets
sm = S.ball("small", M["oil"], 1.15, (0, 0, 0), seg=24)
cen = [(1, 1, 1), (-1, 1, 1), (1, -1, 1), (-1, -1, 1), (1, 1, -1), (-1, 1, -1), (1, -1, -1), (-1, -1, -1)]
rnd = random.Random(2)
far = [(x * rnd.uniform(5.5, 8), y * rnd.uniform(3, 4.5), z * rnd.uniform(4, 6.5)) for x, y, z in cen]
def centre(i, t):
    k = c.smooth(t_rom, t_rom + 1.3, t)
    f = far[i]
    return (C[0] + f[0] * k + 0.3 * math.sin(2 * t + i) * k, C[1] + f[1] * k, C[2] + f[2] * k + 0.3 * math.cos(2.4 * t + i) * k)
S.swarm(8, sm, lambda i, t: (centre(i, t), 1.0 if t >= t_rom else None) if t >= t_rom else None)
msd = sr.sphere_points(8, 0.3)
meul = [sr.face(d) for d in msd]
def mini(i, t):
    if t < t_rom:
        return None
    ci, j = i // 8, i % 8
    ctr = centre(ci, t)
    d = msd[j]
    k = c.smooth(t_rom, t_rom + 0.5, t)
    return (ctr[0] + d[0] * 1.3, ctr[1] + d[1] * 1.3, ctr[2] + d[2] * 1.3), 0.6 * k, meul[j]
S.swarm(64, tpl, mini)
S.cam([(0, (0, 0, 7), 34, 8, -24), (t_rom, (0, 0, 7), 24, 6, 6), (t_bol + 0.5, (0, 0, 7), 44, 10, 20), (S.T, (0, 0, 7), 60, 14, 34)])
S.go()
