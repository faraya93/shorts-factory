"""jabon 2 (agua-aceite): oil molecules scattered among water molecules; the water closes in (bonds drawn) and squeezes the oil into one ball."""
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
t_mez, t_atr, t_emp = S.t("mezclan:", default=1.4), S.t("atraen", default=3.1), S.t("empujan", default=4.0)
C = (0, 0, 7.0)
rnd = random.Random(3)
oil = S.ball("oil", M["oil"], 0.78, (0, 0, 0), seg=18)
op = sr.sphere_points(28, 1.0)
orr = [rnd.uniform(0.2, 1.0) for _ in range(28)]
def oil_f(i, t):
    if t < 0.3 + 0.03 * i:
        return None
    k = c.smooth(t_atr, t_emp + 1.2, t)
    R = (1.0 - k) * 4.2 * orr[i] + k * 1.7 * (0.55 + 0.45 * orr[i])
    p = op[i]
    return (C[0] + p[0] * R + 0.15 * math.sin(3 * t + i), C[1] + p[1] * R * 0.7, C[2] + p[2] * R + 0.15 * math.sin(2.7 * t + 2 * i)), 1.0
S.swarm(28, oil, oil_f)
wat = S.ball("wat", M["water_solid"], 0.42, (0, 0, 0), seg=12)
wp = sr.sphere_points(90, 0.3)
wr = [rnd.uniform(0.0, 1.0) for _ in range(90)]
def wat_f(i, t):
    if t < 0.2 + 0.015 * i:
        return None
    p = wp[i]
    R0 = 5.2 + 5.5 * wr[i]
    k = c.smooth(t_atr, t_emp + 1.4, t)
    R = R0 * (1 - 0.2 * k) if R0 > 5.0 else R0
    # water outside the oil: it closes in
    Rm = max(R, 3.4 * k + 2.0 * (1 - k) * 0 + R0 * (1 - k))
    return (C[0] + p[0] * Rm + 0.25 * math.sin(2.1 * t + i), C[1] + p[1] * Rm * 0.8, C[2] + p[2] * Rm + 0.25 * math.sin(2.5 * t + 3 * i)), 1.0
S.swarm(90, wat, wat_f)
import itertools
pts_b = [(C[0] + wp[i][0] * 5.8, C[1] - 2.2, C[2] + wp[i][2] * 5.8) for i in range(90)]
pairs = []
for i in range(0, 90, 6):
    j = min((k for k in range(90) if k != i), key=lambda k: (pts_b[i][0] - pts_b[k][0]) ** 2 + (pts_b[i][2] - pts_b[k][2]) ** 2)
    pairs.append((i, j))
for n_, (a, b) in enumerate(pairs):
    S.line("bond", [pts_b[a], pts_b[b]], 0.1, S.accent, grow=(t_atr + 0.04 * n_, t_atr + 0.5 + 0.04 * n_), smooth=False)
S.cam([(0, (0, 0, 7), 44, 10, -24), (t_mez, (0, 0, 7), 32, 8, -6), (t_emp, (0, 0, 7), 24, 6, 12), (S.T, (0, 0, 7), 34, 14, 28)])
S.go()
