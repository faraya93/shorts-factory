"""hielo 4 (lago): the imagined lake in cross-section: ice forms at the surface, sinks, and the lake fills from the bottom up."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_rig as ir  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(241)
M = ir.palette(S)
t_hie, t_sup, t_hun, t_aba, t_sol = S.t("hielo", default=1.9), S.t("superficie,", default=2.2), S.t("hundiría,", default=3.3), S.t("abajo", default=5.5), S.t("sólido.", default=6.7)
W, D, DEPTH = 16.0, 3.6, 8.0
S.box("bank", (W + 3.0, D + 1.5, 1.0), (0, 0, -0.5), S.ink, bevel=0.3, pop=(0.05, 0.4))
S.box("lake", (W, D, DEPTH), (0, 0, DEPTH / 2), M["water"], bevel=0.3, pop=(0.1, 0.5))
S.box("cold", (W, D, 4.0), (0, 0, DEPTH + 2.2), M["glass"], bevel=0.3, pop=(0.5, 0.5))
rnd = random.Random(2)
flk = S.ball("flake", M["ice"], 0.22, (0, 0, 0), seg=8)
fp = [(rnd.uniform(-7, 7), rnd.uniform(-1.4, 1.4), rnd.uniform(0, 1)) for _ in range(40)]
S.swarm(40, flk, lambda i, t: ((fp[i][0] + 0.6 * math.sin(2 * t + i), fp[i][1], DEPTH + 4.2 - ((t * 0.9 + fp[i][2]) % 1.0) * 4.6), 1.0) if t > 0.8 else None)
# plates: form at the surface, then drop to the growing bed
PL = 16
plate = S.box("plate_t", (W - 1.0, D - 0.7, 0.5), (0, 0, 0), M["ice"], bevel=0.12)
def landed(t):
    return sum(1 for i in range(PL) if t > 2.0 + 0.30 * i + 0.9)
def plates(i, t):
    t0 = 2.0 + 0.30 * i
    if t < t0:
        return None
    bed = 0.25 * 0 + 0.5 * i + 0.3
    k = (t - t0 - 0.3) / 0.6
    z = DEPTH - 0.4 if k <= 0 else (DEPTH - 0.4) * (1 - k * k) + bed * k * k
    return (0, 0, max(z, bed)), (1.0 if k < 1 else 1.0)
S.swarm(PL, plate, plates)
# sinking marker arrow (accent) from the surface to the bed
S.line("sink", [(-6.0, -D / 2 - 0.3, DEPTH - 0.5), (-6.0, -D / 2 - 0.3, 3.0)], 0.16, S.accent, grow=(t_hun, t_hun + 0.7), smooth=False)
S.cone("sinkhead", 0.5, 0.0, 1.2, (-6.0, -D / 2 - 0.3, 2.7), S.accent, rot=(math.pi, 0, 0), pop=(t_hun + 0.6, 0.2))
S.cam([(0, (0, 0, 6), 40, 8, -34), (2.5, (-2, 0, 6), 34, 6, -14), (5.5, (2, 0, 5), 30, 8, 10), (S.T, (0, 0, 5.5), 36, 14, 26)])
S.go()
