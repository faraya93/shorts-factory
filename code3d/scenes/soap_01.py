"""jabon 1 (mano): water pours on a palm plate and the grease stays; a soap bar slides in pushing the grease (the false 'it just slips' idea)."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import soap_rig as sr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(242)
M = sr.palette(S)
t_agua, t_jab, t_res, t_raro = S.t("agua", default=0.5), S.t("jabón", default=4.1), S.t("resbalar,", default=5.0), S.t("raro.", default=6.8)
S.box("palm", (15.0, 8.0, 0.9), (0, 0, 0.0), M["plate"], bevel=0.35, pop=(0.05, 0.45))
blob = S.ball("grease", M["oil"], 2.4, (0, 0, 0.7), shape=(1.0, 1.0, 0.32), pop=(0.5, 0.45), seg=32)
S.move(blob, [(0, (0, 0, 0.8)), (t_jab + 0.7, (0, 0, 0.8)), (t_res + 0.8, (7.0, 0, 0.8)), (S.T, (7.4, 0, 0.8))])
bar = S.box("bar", (5.0, 3.0, 1.8), (-14, 0, 1.8), M["bar"], bevel=0.5, pop=(t_jab - 0.4, 0.3))
S.move(bar, [(t_jab - 0.4, (-14.0, 0, 1.8)), (t_jab + 0.8, (-3.4, 0, 1.8)), (t_res + 0.9, (3.6, 0, 1.8)), (S.T, (4.0, 0, 1.8))])
rnd = random.Random(4)
dr = S.ball("drop", M["water"], 0.5, (0, 0, 0), seg=14)
dd = [(rnd.uniform(-4, 4), rnd.uniform(-1.5, 1.5), rnd.uniform(0, 1), rnd.choice((-1, 1))) for _ in range(46)]
def drops(i, t):
    x, y, ph, side = dd[i]
    a = t_agua + 0.2
    if t < a or t > t_jab + 0.8:
        return None
    k = ((t - a) * 0.8 + ph) % 1.0
    if k < 0.45:
        return (x, y, 15.0 - (k / 0.45) ** 2 * 14.0), 1.0                    # fall
    j = (k - 0.45) / 0.55
    return (x + side * 2.0 * j * 3.0, y + 4.0 * j, 0.9 + 0.4 * math.sin(math.pi * j)), 1.0 - 0.6 * j      # splash and run off the palm
S.swarm(46, dr, drops)
# bubbles around the bar at the end
bb = S.ball("bub", M["foam"], 0.5, (0, 0, 0), seg=12)
S.swarm(14, bb, lambda i, t: ((bar.location[0] + 2.8 * math.cos(i * 1.7), -2.2 + 0.4 * math.sin(i), bar.location[2] + 0.4 + ((t - t_raro) * 0.6 + i * 0.13) % 1.0 * 3.0), 0.8) if t > t_raro else None)
S.cam([(0, (0, 0, 3), 32, 20, -34), (2.5, (0, 0, 2.2), 24, 10, -12), (t_res, (2, 0, 2.2), 26, 12, 14), (S.T, (3, 0, 2.5), 30, 22, 30)])
S.go()
