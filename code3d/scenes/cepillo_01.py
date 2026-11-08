"""cepillo 1 (hook): see productions/mecanalia-es/012*/script.json. The camera travels from the toothbrushes to the toilet; the flush starts and a faint spray drifts toward the cup."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import cepillo_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(286, floor_z=0.0)
COL = {"ceramic": "#F5F2EC", "seat": "#E9E2D6", "cup": "#E8B23A", "toothbrush": "#B8327E", "brush": "#2B3442"}
B = cr.bathroom(S, COL)
rk.softboxes(0.7, centre=(10, 0, 70))
tf = S.t("cadena", default=4.2)
P = cr.Plume(420, seed=5)
beads = cr.Beads(S, "haze", 420, cr.bead_mat())
cup = np.array(cr.CUP_AT) + np.array([0.0, 0.0, 22.0])


def upd(t):
    u = np.clip((t - tf) / 5.0, 0.0, 1.0)
    p, on = P.rise(np.full(P.n, u))
    drift = np.clip((u - 0.25) / 0.75, 0.0, 1.0)[None] ** 1.5
    p = p + (cup - p) * (0.55 * drift * P.rad[:, None])          # the outer droplets lean toward the cup
    beads.set(p, P.size * 0.5 * on)


S.every_frame(upd)
S.cam([(0, (63, 28, 100), 78, 8, 10), (tf, (48, 18, 88), 170, 9, 4), (S.T, (30, 6, 66), 345, 9, -8)])
S.go()
