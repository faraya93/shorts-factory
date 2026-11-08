"""cepillo 6 (giro): see productions/mecanalia-es/012*/script.json. The lid drops and the spray still escapes; the marks stay. The lid opens, a brush scrubs the bowl clean, the cup leaves."""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import cepillo_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(328, floor_z=0.0)
COL = {"ceramic": "#F5F2EC", "seat": "#E9E2D6", "cup": "#E8B23A", "toothbrush": "#B8327E", "brush": "#2B3442"}
B = cr.bathroom(S, COL)
rk.softboxes(0.7, centre=(10, 0, 70))
W = cr.Water(S)
N = 1400
P = cr.Plume(N, seed=12, flat=0.7)
head = cr.head_of(B.brush_b)
marks_at, seat, br, fl = P.landing(head)
marks = cr.Beads(S, "marks", N, cr.bead_mat("clear_tint", "#CBD764", 0.3))
M = 500
rng = np.random.default_rng(8)
ang, spd, sz = rng.uniform(0, 2 * math.pi, M), rng.uniform(26, 80, M), rng.uniform(0.25, 0.55, M)
leak = cr.Beads(S, "leak", M, cr.bead_mat())

tl = S.t("bajas", default=0.7)
tu = S.t("Lo", default=5.6)
td = S.t("desinfectar", default=6.6)
ta = S.t("aleja", default=9.3)
H = cr.HOLDER_AT
over, down = (0.0, -11.0, 66.0), (0.0, -11.0, 21.0)
n = 14
circle = [(td + 0.55 + i * (ta - td - 1.1) / n, (3.2 * math.cos(i * 1.3), -11.0 + 4.5 * math.sin(i * 1.3), 21.0 + 0.7 * math.sin(i * 2.1))) for i in range(n + 1)]
S.move(B.tb_root, [(0, H), (td - 0.75, H), (td - 0.3, (H[0], H[1], 44.0)), (td + 0.1, over), (td + 0.5, down)] + circle + [(ta + 0.25, over), (ta + 0.8, (H[0], H[1], 44.0)), (ta + 1.1, H)])
C = cr.CUP_AT
S.move(B.cup_root, [(0, C), (ta, C), (ta + 0.95, (C[0] + 170.0, C[1], C[2]))])


def upd(t):
    cr.lid_angle(B, sp.interp([(tl, 0.0), (tl + 0.5, 90.0), (tu - 0.2, 90.0), (tu + 0.45, 0.0)], t))
    W.update(cr.turbulence(W.R, W.TH, t, sp.interp([(0, 0.2), (tl + 0.3, 1.1), (td, 0.4), (td + 0.5, 1.0)], t)))
    clean = sp.interp([(td + 0.5, 1.0), (ta - 0.2, 0.0)], t)                   # the scrub clears the marks
    marks.set(marks_at, np.where(br, 0.0, P.size * 0.42 * clean))
    k = np.clip((t - tl - 0.35) / 1.3, 0.0, 1.0)
    fade = 1.0 - sp.interp([(tl + 1.5, 0.0), (tl + 2.2, 1.0)], t)
    x = cr.BOWL[0] + np.cos(ang) * (19.0 + spd * k)
    y = cr.BOWL[1] + np.sin(ang) * (22.0 + spd * 0.7 * k)
    z = np.full(M, cr.RIM_Z + 1.0) + 3.0 * k * np.sin(ang * 3.0)
    leak.set(np.stack([x, y, z], axis=1), sz * float(k > 0) * fade)


S.every_frame(upd)
S.cam([(0, (0, -8, 62), 190, 10, -10), (tl + 0.8, (0, -8, 56), 165, 12, 4), (td, (-8, -8, 52), 150, 16, 10), (ta, (6, -6, 58), 215, 12, 2), (S.T, (40, 8, 74), 360, 9, -6)])
S.go()
