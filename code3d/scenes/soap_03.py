"""jabon 3 (molecula): one big soap molecule: the head attracts water, the tail attracts grease; then it multiplies into a ring."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import soap_rig as sr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(214)
M = sr.palette(S)
t_cab, t_agu, t_col, t_gra = S.t("cabeza", default=2.6), S.t("agua", default=4.0), S.t("cola", default=4.6), S.t("grasa.", default=5.9)
tpl = sr.molecule(S, M, "mol")
big = S.clone(tpl, "big")
S.items[-1][1]["base"] = (3.2, 3.2, 3.2)
d = S.items[-1][1]; d["sw"] = None; del d["sw"]
S.move(big, [(0, (0, 0, 7.0))]); S.pop(big, 0.3, 0.5)
S.spin(big, [(0, (0, 0, 0)), (6.0, (0, 0, 2.2))])
wat = S.ball("wat", M["water_solid"], 0.42, (0, 0, 0), seg=12)
oil = S.ball("oil", M["oil"], 0.6, (0, 0, 0), seg=14)
rnd = random.Random(5)
wo = [(rnd.uniform(-6, 6), rnd.uniform(-2, 2), rnd.uniform(9, 14)) for _ in range(14)]
oo = [(rnd.uniform(-6, 6), rnd.uniform(-2, 2), rnd.uniform(0, 4)) for _ in range(10)]
def wat_f(i, t):
    if t < t_cab:
        return None
    k = c.smooth(t_agu - 0.7 + 0.05 * i, t_agu + 0.9 + 0.05 * i, t)
    th = i * 0.9
    goal = (2.4 * math.cos(th), -0.4 + 1.2 * math.sin(th * 1.3), 7.0 + 3.6 + 1.2 * math.sin(th))
    return tuple(a * (1 - k) + b * k for a, b in zip(wo[i], goal)), 1.0
def oil_f(i, t):
    if t < t_col - 0.6:
        return None
    k = c.smooth(t_col - 0.2 + 0.05 * i, t_col + 1.2 + 0.05 * i, t)
    th = i * 1.1
    goal = (1.9 * math.cos(th), -0.4 + 1.0 * math.sin(th * 1.2), 7.0 - 4.4 + 1.2 * math.sin(th))
    return tuple(a * (1 - k) + b * k for a, b in zip(oo[i], goal)), 1.0
S.swarm(14, wat, wat_f)
S.swarm(10, oil, oil_f)
ring = []
RN = 14
def ringf(i, t):
    t0 = t_gra - 0.3 + 0.07 * i
    if t < t0:
        return None
    th = 2 * math.pi * i / RN + 0.4 * (t - t0)
    R = 7.5
    k = min(1.0, (t - t0) / 0.4)
    return (R * math.cos(th), R * math.sin(th) * 0.5, 7.0 + 0.6 * math.sin(th * 2)), 1.0, (math.pi / 2 * 0.0, 0, 0)
S.swarm(RN, tpl, ringf)
S.cam([(0, (0, 0, 7), 40, 8, -24), (t_cab, (0, 0, 9.0), 22, 6, 6), (t_col, (0, 0, 5.5), 24, 6, -8), (t_gra, (0, 0, 7), 30, 10, 10), (S.T, (0, 0, 7), 44, 18, 28)])
S.go()
