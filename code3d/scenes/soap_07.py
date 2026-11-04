"""jabon 7 (cierre): water on one side, grease on the other; rows of soap molecules bridge them (heads to the water, tails into the grease); pull-back."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import soap_rig as sr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(274)
M = sr.palette(S)
t_res, t_pue, t_sig = S.t("resbalón:", default=1.6), S.t("puente", default=2.6), S.t("Sígueme,", default=5.6)
S.box("floor", (26.0, 8.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
S.box("water", (6.0, 5.0, 8.0), (-8.5, 0, 4.0), M["water"], bevel=0.4, pop=(0.2, 0.5))
S.box("grease", (6.0, 5.0, 8.0), (8.5, 0, 4.0), M["oil"], bevel=0.4, pop=(0.3, 0.5))
tpl = sr.molecule(S, M, "mol")
rows = [(z, y) for z in (1.6, 3.6, 5.6) for y in (-1.2, 1.2)]
e = sr.face((-1, 0, 0))                        # head toward the water (-x), tail toward the grease (+x)
def bridge(i, t):
    r, k = i // 6, i % 6
    z, y = rows[r]
    t0 = t_pue - 0.4 + 0.12 * k + 0.05 * r
    if t < t0:
        return None
    x = -3.5 + 1.4 * k
    drop = max(0.0, 1.0 - (t - t0) / 0.5) ** 2 * 6.0
    return (x, y, z + drop), 1.0, e
S.swarm(36, tpl, bridge)
S.line("arc", [(-8.0, -3.0, 9.5), (-3.0, -3.0, 11.5), (3.0, -3.0, 11.5), (8.0, -3.0, 9.5)], 0.2, S.accent, grow=(t_pue + 0.8, t_pue + 1.8))
S.cam([(0, (0, 0, 5), 34, 10, -26), (t_pue, (0, 0, 4.5), 24, 6, 0), (t_sig, (0, 0, 5), 34, 12, 14), (S.T, (0, 0, 5), 50, 18, -12)])
S.go()
