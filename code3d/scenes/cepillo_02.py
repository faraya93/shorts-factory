"""cepillo 2 (descarga): see productions/mecanalia-es/012*/script.json. Looking down into the bowl: calm water, then rim jets crash in and swirl it."""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import cepillo_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(165, floor_z=0.0)
COL = {"ceramic": "#F5F2EC", "seat": "#E9E2D6", "cup": "#E8B23A", "toothbrush": "#B8327E", "brush": "#2B3442"}
B = cr.bathroom(S, COL)
rk.softboxes(0.7, centre=(0, -10, 70))
W = cr.Water(S)
t0 = S.t("entra", default=1.2)
N = 1100
rng = np.random.default_rng(3)
th0, ph, sz = rng.uniform(0, 2 * math.pi, N), rng.uniform(0, 1, N), rng.uniform(0.2, 0.5, N)
jets = cr.Beads(S, "jets", N, cr.bead_mat("clear_foam", "#FBFDFD", 0.05))


def upd(t):
    amp = 0.6 * sp.interp([(t0, 0.0), (t0 + 0.7, 1.0)], t)
    W.update(cr.turbulence(W.R, W.TH, t, amp))
    q = (ph + t * 1.25) % 1.0
    th = th0 + q * 1.5
    rad = 1.0 - 0.3 * q
    x = cr.BOWL[0] + 12.5 * rad * np.cos(th)
    y = cr.BOWL[1] + 18.0 * rad * np.sin(th)
    z = 43.0 - 13.0 * q ** 1.6
    on = np.clip((t - t0 - ph * 0.4) / 0.15, 0.0, 1.0)
    jets.set(np.stack([x, y, z], axis=1), sz * on)


S.every_frame(upd)
S.cam([(0, (0, -11, 34), 135, 78, -6), (t0, (0, -11, 33), 105, 74, 6), (S.T, (0, -11, 31), 72, 68, 26)])
S.go()
