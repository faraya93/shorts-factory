"""caca 3 (decada): see productions/mecanalia-es/016*/script.json. The heap swells into a mound beside the toilet while the camera travels along it to a horse standing at its far end (rung 1 of the pre-written fallback: the horse is revealed by the travel, no walk cycle)."""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caca_rig as cr  # noqa: E402
import caca_set as cs  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(150, floor_z=0.0)
cs.widen_floor(6.0)
B = cr.bathroom(S)
sx, sy = cr.SCALE_AT
P = cs.LitePile(S, "units", cs.N_UNITS, cr.stool_material(S), seed=7)
A = {"centre": (sx, sy), "radius": 30.0, "height": 22.0}
Z = {"centre": (95.0, -45.0), "radius": 85.0, "height": 75.0}
t0 = S.t("diez", default=0.3)
t1 = S.t("media", default=2.0) + 0.6


def upd(t):
    k = sp.interp([(t0, 0.0), (t1, 1.0)], t)
    pos = cs.lerp_mound(cs.N_UNITS, A, Z, k)
    pos[:, 2] += 5.0 * (1.0 - k)
    sz = np.full(cs.N_UNITS, 0.8 + (1.4 - 0.8) * k)
    P.set(pos, sz)


S.every_frame(upd)
H = cs.horse(S, loc=(215.0, -55.0, 0.0), rot=(0, 0, math.radians(-90)))
S.pop(H.root, S.t("caballo", default=3.0) - 0.7, 0.5)
rk.softboxes(0.7, centre=(100, -20, 40))
S.cam([(0, (30.0, -30.0, 30.0), 240, 9, -18), (S.T * 0.55, (110.0, -45.0, 55.0), 430, 8, -6), (S.T, (205.0, -55.0, 90.0), 470, 7, 6)])
S.go()
