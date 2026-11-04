"""hielo 5 (tapa): the real lake: an ice lid floats on top and insulates; fish swim under it all winter."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_rig as ir  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(186)
M = ir.palette(S)
t_flo, t_tap, t_ais, t_pez = S.t("flota,", default=0.8), S.t("tapa", default=1.8), S.t("aísla", default=2.1), S.t("peces", default=3.8)
W, D, DEPTH = 16.0, 3.6, 8.0
S.box("bank", (W + 3.0, D + 1.5, 1.0), (0, 0, -0.5), S.ink, bevel=0.3, pop=(0.05, 0.4))
S.box("lake", (W, D, DEPTH), (0, 0, DEPTH / 2), M["water"], bevel=0.3, pop=(0.05, 0.5))
lid = S.box("lid", (W, D, 1.3), (0, 0, DEPTH + 0.2), M["ice"], bevel=0.25)
S.size(lid, [(0, (1e-3, 1, 1)), (t_flo - 0.4, (1e-3, 1, 1)), (t_flo + 0.9, (1, 1, 1))])
S.every_frame(lambda t: setattr(lid, "location", (-W / 2 * (1 - max(1e-3, sp.interp([(0, 1e-3), (t_flo - 0.4, 1e-3), (t_flo + 0.9, 1)], t))), 0, DEPTH + 0.2)))
rnd = random.Random(2)
flk = S.ball("flake", M["ice"], 0.22, (0, 0, 0), seg=8)
fp = [(rnd.uniform(-7, 7), rnd.uniform(-1.4, 1.4), rnd.uniform(0, 1)) for _ in range(46)]
S.swarm(46, flk, lambda i, t: ((fp[i][0] + 0.6 * math.sin(2 * t + i), fp[i][1], DEPTH + 7.0 - ((t * 0.8 + fp[i][2]) % 1.0) * 6.2), 1.0))
# insulation: accent bars between the cold above and the water below
for k, x in enumerate((-5.0, 0.0, 5.0)):
    S.cone(f"stop{k}", 0.6, 0.0, 1.5, (x, -D / 2 - 0.4, DEPTH + 2.6), S.accent, rot=(math.pi, 0, 0), pop=(t_ais + 0.1 * k, 0.3))
    S.box(f"shield{k}", (2.4, 0.3, 0.35), (x, -D / 2 - 0.4, DEPTH + 1.6), S.accent, bevel=0.1, pop=(t_ais + 0.25 + 0.1 * k, 0.3))
fishes = []
for k in range(3):
    f = ir.Fish(S, M, f"fish{k}", pop=(0.6 + 0.15 * k, 0.4))
    ph = k * 2.1
    f.swim(S, lambda t, k=k, ph=ph: (-5.5 + 11.0 * ((t * 0.09 * (1 + 0.2 * k) + 0.33 * k) % 1.0) * 1.0 - 0.0, 0.0, 3.0 + 1.1 * k + 0.5 * math.sin(1.3 * t + ph), 0.0 if True else 0))
    fishes.append(f)
S.cam([(0, (0, 0, 6), 38, 8, -34), (3.0, (0, 0, 5.5), 30, 6, 0), (S.T, (2, 0, 5), 28, 8, 28)])
S.go()
