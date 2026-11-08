"""cepillo 7 (cierre): see productions/mecanalia-es/012*/script.json. One last flush: the spray blooms out of the bowl like a sneeze while the camera pulls back to the whole bathroom."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import cepillo_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(280, floor_z=0.0)
COL = {"ceramic": "#F5F2EC", "seat": "#E9E2D6", "cup": "#E8B23A", "toothbrush": "#B8327E", "brush": "#2B3442"}
B = cr.bathroom(S, COL)
rk.softboxes(0.7, centre=(10, 0, 70))
W = cr.Water(S)
N = 2400
P = cr.Plume(N, seed=21, flat=0.9)
beads = cr.Beads(S, "sneeze", N, cr.bead_mat())
ts = S.t("estornuda", default=3.3)
c0 = np.array([cr.BOWL[0], cr.BOWL[1], cr.RIM_Z])


def upd(t):
    amp = sp.interp([(ts - 0.5, 0.2), (ts, 1.5)], t)
    W.update(cr.turbulence(W.R, W.TH, t, amp))
    u = np.clip((t - ts + 0.15) / 1.1, 0.0, 1.0)
    p, on = P.rise(np.full(N, u))
    out = c0 + (p - c0) * np.array([2.6, 1.8, 0.62])                           # wide and low: a burst, not a column
    beads.set(out, P.size * 0.72 * on)


S.every_frame(upd)
S.cam([(0, (0, -11, 52), 130, 18, -12), (ts, (2, -9, 62), 190, 13, -4), (S.T, (24, 4, 84), 385, 8, 12)])
S.go()
