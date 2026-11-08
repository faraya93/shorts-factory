"""cepillo 5 (aterrizaje): see productions/mecanalia-es/012*/script.json. The droplets settle on the seat, the floor and, last, the bristles; the camera follows them to the toothbrush."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import cepillo_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(173, floor_z=0.0)
COL = {"ceramic": "#F5F2EC", "seat": "#E9E2D6", "cup": "#E8B23A", "toothbrush": "#B8327E", "brush": "#2B3442"}
B = cr.bathroom(S, COL)
rk.softboxes(0.7, centre=(30, 0, 70))
N = 2200
P = cr.Plume(N, seed=12, flat=0.7)
head = cr.head_of(B.brush_b)
target, seat, br, fl = P.landing(head)
start = P.hang(0.0)
beads = cr.Beads(S, "drops", N, cr.bead_mat("clear_drops", "#1E46FF", 0.2))
ts, tf, tc = S.t("asiento", default=1.7), S.t("suelo", default=2.7), S.t("cepillo", default=5.0)
land = np.zeros(N)
land[seat], land[fl], land[br] = ts, tf, tc
span = 1.5 + P.delay * 2.0
sparse = (np.arange(N) % 6 == 0).astype(float)


def upd(t):
    u = np.clip((t - (land - span)) / span, 0.0, 1.0)
    p = P.settle(start, target, u)
    r = P.size * (0.72 - 0.32 * u)
    r[br] = P.size[br] * (0.72 - 0.56 * u[br]) * sparse[br]                     # a few fine drops on the bristles: a dense clump hid the head and read as cotton
    beads.set(p, r)


S.every_frame(upd)
S.cam([(0, (8, -6, 118), 320, 6, -12), (ts, (10, -4, 86), 260, 9, -4), (tf, (34, 8, 90), 190, 9, 4), (S.T, (head[0], head[1], head[2] - 2.0), 44, 5, 16)])
S.go()
