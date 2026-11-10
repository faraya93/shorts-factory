"""caca 2 (anio): see productions/mecanalia-es/016*/script.json. Units rain from the toilet onto the scale until it is buried; two suitcases slide in beside the heap; the camera pulls back and rises."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caca_rig as cr  # noqa: E402
import caca_set as cs  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(227, floor_z=0.0)
B = cr.bathroom(S)
cr.bathroom_scale(S)
sx, sy = cr.SCALE_AT
P = cs.LitePile(S, "units", cs.N_UNITS, cr.stool_material(S), seed=7)
HEAP = {"centre": (sx, sy), "radius": 30.0, "height": 22.0}
rest = cr.mound(cs.N_UNITS, HEAP["centre"], HEAP["radius"], HEAP["height"], seed=2, floor=5.0)
src = np.array([0.0, -10.8, 52.0])
t0, t1 = S.t("cuarenta", default=2.6) - 2.4, S.t("cuarenta", default=2.6) + 0.5
SZ = 0.8


def upd(t):
    pos, sz = [], []
    for i in range(cs.N_UNITS):
        p, sh = cs.flight(i, cs.N_UNITS, t, t0, t1, src, rest[i])
        pos.append(p)
        sz.append(SZ * sh + 1e-4)
    P.set(np.array(pos), np.array(sz))


S.every_frame(upd)
tm = S.t("maletas", default=5.0) - 0.4
ta = cs.suitcase(S, loc=(175.0, sy - 4.0, 0.0))
tb = cs.suitcase(S, loc=(175.0, sy - 4.0, 19.0))
S.move(ta.root, [(0, (175.0, sy - 4.0, 0.0)), (tm, (175.0, sy - 4.0, 0.0)), (tm + 0.8, (92.0, sy - 4.0, 0.0)), (S.T, (92.0, sy - 4.0, 0.0))])
S.move(tb.root, [(0, (175.0, sy - 4.0, 19.0)), (tm + 0.3, (175.0, sy - 4.0, 19.0)), (tm + 1.1, (92.0, sy - 4.0, 19.0)), (S.T, (92.0, sy - 4.0, 19.0))])
rk.softboxes(0.7, centre=(40, -20, 30))
S.cam([(0, (30.0, -25.0, 14.0), 105, 9, -12), (S.T * 0.5, (45.0, -26.0, 22.0), 230, 14, -2), (S.T, (92.0, -26.0, 22.0), 175, 12, 10)])
S.go()
