"""nube 3 (corriente): droplets hang in a rising air current; one falls and is pushed back up; a dandelion-like fluff rides the wind."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import cloud_rig as cr  # noqa: E402

S = sp.Shot(174)
M = cr.palette(S)
t_sube, t_pel = S.t("sube", default=2.5), S.t("pelusa", default=4.0)
N = 80
pts = cr.blob_points(N, 5.0, 2.2, 3.6, seed=4, flat_bottom=False)
rnd = random.Random(8)
ph = [rnd.uniform(0, 6.3) for _ in range(N)]
drop = S.ball("drop", M["drop_solid"], 0.5, (0, 0, 0), seg=14)
def drops(i, t):
    if t < 0.2 + i * 0.012:
        return None
    x, y, z = pts[i]
    return (x + 0.2 * math.sin(1.3 * t + ph[i]), y, 11 + z + 0.45 * math.sin(2.0 * t + ph[i])), 1.0
S.swarm(N, drop, drops)
hero = S.ball("hero", M["drop_solid"], 0.9, (0, -2.6, 13), pop=(0.4, 0.4), seg=24)
S.move(hero, [(0.4, (0, -2.6, 14.5)), (1.8, (0, -2.6, 7.0)), (t_sube - 0.1, (0, -2.6, 6.3)), (t_sube + 1.3, (0, -2.6, 12.6)), (S.T, (0, -2.6, 13.0))])
# the current: accent lines and arrowheads rising under the cloud
for k, x in enumerate((-4.5, -2.2, 0.0, 2.2, 4.5)):
    S.line(f"cur{k}", [(x, -3.2, 0.5), (x + 0.4, -3.2, 3.0), (x - 0.3, -3.2, 5.5), (x + 0.2, -3.2, 8.0)], 0.14, S.accent, grow=(t_sube - 0.4 + 0.12 * k, t_sube + 0.5 + 0.12 * k))
    S.cone(f"head{k}", 0.45, 0.0, 1.2, (x + 0.2, -3.2, 8.3), S.accent, pop=(t_sube + 0.4 + 0.12 * k, 0.25))
# fluff on the wind
fluff = S.empty("fluff", (-1.0, -3.0, 2.0))
for i, (x, y, z) in enumerate(cr.blob_points(16, 0.7, 0.7, 0.7, seed=3, flat_bottom=False)):
    S.ball(f"fz{i}", M["cloud"], 0.16, (x, y, z), parent=fluff, seg=10, pop=(t_pel, 0.3))
S.ball("fcore", M["cloud"], 0.3, (0, 0, 0), parent=fluff, seg=12, pop=(t_pel, 0.3))
S.move(fluff, [(t_pel - 0.1, (-3.6, -3.0, 1.0)), (t_pel + 0.8, (-2.4, -3.0, 5.0)), (t_pel + 1.6, (-3.2, -3.0, 9.0)), (S.T, (-2.8, -3.0, 12.5))])
S.cam([(0, (0, 0, 8), 36, 4, -24), (2.8, (0, 0, 9), 30, 10, 0), (S.T, (0, 0, 12), 36, 6, 20)])
S.go()
