"""hielo 6 (congelado): without floating ice: the lake freezes from the bottom up, the fish are trapped; the sun only melts a thin top layer."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_rig as ir  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(198)
M = ir.palette(S)
t_rar, t_con, t_fon, t_viv = S.t("rareza", default=0.6), S.t("congelarían", default=2.4), S.t("fondo,", default=3.2), S.t("vivir", default=4.9)
W, D, DEPTH = 16.0, 3.6, 8.0
S.box("bank", (W + 3.0, D + 1.5, 1.0), (0, 0, -0.5), S.ink, bevel=0.3, pop=(0.05, 0.4))
S.box("lake", (W, D, DEPTH), (0, 0, DEPTH / 2), M["water"], bevel=0.3, pop=(0.05, 0.5))
bed = S.box("bed", (W - 0.5, D - 0.4, DEPTH), (0, 0, 0), M["ice"], bevel=0.2)
def grow(t):
    k = max(1e-3, c.smooth(t_con - 0.3, t_fon + 1.6, t))
    bed.scale = (1.0, 1.0, k)
    bed.location = (0, 0, DEPTH * k / 2 + 0.1)
S.every_frame(grow)
for k in range(3):
    f = ir.Fish(S, M, f"fish{k}", pop=(0.3 + 0.1 * k, 0.4))
    x0, z0 = -4.5 + 4.5 * k, 2.4 + 1.6 * k
    f.swim(S, lambda t, x0=x0, z0=z0, k=k: (x0 + 1.2 * math.sin(0.9 * t + k) * (1 - c.smooth(t_con + 0.5 * k, t_con + 0.5 * k + 1.0, t)), 0.0, z0 + 0.4 * math.sin(1.4 * t + k), 0.0))
sun = S.ball("sun", S.accent, 1.6, (-7.0, 0, 17.0), pop=(t_viv - 1.2, 0.5))
S.move(sun, [(0, (-7.0, 0, 17.0)), (S.T, (6.0, 0, 18.0))])
thin = S.box("thin", (W - 0.6, D - 0.5, 0.7), (0, 0, DEPTH + 0.1), M["water"], bevel=0.15, pop=(t_viv - 0.4, 0.5))
S.cam([(0, (0, 0, 6), 36, 6, -30), (2.4, (0, 0, 6), 32, 8, -6), (S.T, (0, 0, 8), 56, 18, 22)])
S.go()
