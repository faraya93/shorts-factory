"""caca 6 (cierre): see productions/mecanalia-es/016*/script.json. Single reframe image: the camera pulls back from the toilet to show it tiny in front of the water tank, the small green-and-brown solids pile and the two cars, which slide in as the camera retreats."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caca_rig as cr  # noqa: E402
import caca_set as cs  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(334, floor_z=0.0)
S.stage.cam.data.clip_end = 40000.0
S.stage.cam.data.lens = 32.0
cs.widen_floor(8.0)
B = cr.bathroom(S)
B.root.location = (-20.0, -140.0, 0.0)
m = 82
PB = cs.LitePile(S, "units", m, cr.stool_material(S), seed=7)
PG = cs.LitePile(S, "units_bio", m, cr.stool_material(S, cr.GREEN, "bio"), seed=7)
solid = cr.mound(m, (40.0, 170.0), 85.0, 75.0, seed=5, floor=2.0)
green = np.arange(m) % 2 == 0
TANK_AT = (-250.0, 180.0, 0.0)
water, level, _walls = cs.tank(S, TANK_AT, size=(210.0, 130.0, 230.0))
tp = S.t("agua", default=3.0)
tc = S.t("autos", default=4.5)


def upd(t):
    k = sp.interp([(0.8, 0.0), (2.6, 1.0)], t)
    pos = solid.copy()
    pos[:, 2] = solid[:, 2] * k
    szb = np.where(green, 1e-4, 2.2 * k + 1e-4)
    szg = np.where(green, 2.2 * k + 1e-4, 1e-4)
    PB.set(pos, szb)
    PG.set(pos, szg)
    level(0.72 * sp.interp([(0.4, 0.0), (2.4, 1.0)], t))


S.every_frame(upd)
import math  # noqa: E402
CA = cs.car(S, loc=(1100.0, 175.0, -23.8), rot=(0, 0, math.radians(-90)))
CB = cs.car(S, loc=(1100.0, 300.0, -23.8), rot=(0, 0, math.radians(-90)))
S.move(CA.root, [(0, (1100.0, 175.0, -23.8)), (tc, (1100.0, 175.0, -23.8)), (tc + 1.6, (330.0, 175.0, -23.8)), (S.T, (330.0, 175.0, -23.8))])
S.move(CB.root, [(0, (1100.0, 300.0, -23.8)), (tc + 0.4, (1100.0, 300.0, -23.8)), (tc + 2.0, (470.0, 300.0, -23.8)), (S.T, (470.0, 300.0, -23.8))])
rk.softboxes(0.8, centre=(40, 100, 80))
S.cam([(0, (-20.0, -140.0, 45.0), 150, 8, -14), (S.T * 0.4, (0.0, -20.0, 70.0), 520, 12, 4), (S.T, (160.0, 90.0, 120.0), 1550, 18, 6)])
S.go()
