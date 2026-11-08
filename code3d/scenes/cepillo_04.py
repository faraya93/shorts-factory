"""cepillo 4 (carga): see productions/mecanalia-es/012*/script.json. The cloud hangs in the air while part of it turns yellow-green; the camera orbits it."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import cepillo_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(198, floor_z=0.0)
COL = {"ceramic": "#F5F2EC", "seat": "#E9E2D6", "cup": "#E8B23A", "toothbrush": "#B8327E", "brush": "#2B3442"}
B = cr.bathroom(S, COL)
rk.softboxes(0.7, centre=(0, 0, 70))
N = 2200
P = cr.Plume(N, seed=12, flat=0.7)
clear = cr.Beads(S, "drops", N, cr.bead_mat("clear_drops", "#1E46FF", 0.2))
tinted = cr.Beads(S, "drops_tint", N, cr.bead_mat("clear_tint", "#CBD764", 0.3))
tc = S.t("caca", default=3.4)
delay = P.delay * 3.2


def set_streaked(b, xyz, radii, k):
    """Beads drawn out vertically: hanging wet drops with a highlight (reshape rung 1: readers took round white beads for particles)."""
    co = (xyz[:, None, :] + radii[:, None, None] * (b.unit * np.array([1.0, 1.0, k], dtype=np.float32))[None, :, :]).astype(np.float32)
    b.obj.data.vertices.foreach_set("co", co.reshape(-1))
    b.obj.data.update()


def upd(t):
    p = P.hang(t)
    k = np.clip((t - tc - delay) / 0.3, 0.0, 1.0) * P.tint
    set_streaked(clear, p, P.size * 0.8 * (1.0 - k), 1.0)
    set_streaked(tinted, p, P.size * 0.8 * k, 1.0)


S.every_frame(upd)
S.cam([(0, (10, -8, 100), 320, 5, -34), (S.T / 2, (12, -8, 104), 300, 9, 0), (S.T, (16, -8, 104), 285, 14, 34)])
S.go()
