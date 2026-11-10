"""caca 5 (giro): see productions/mecanalia-es/016*/script.json. The turn. Three quarters of the heap lifts off unit by unit and drains into a glass tank as water; the solid remainder packs into a smaller pile, and half of it tints yellow-green (bacteria). Pre-written fallback rung 1: the solids stay a pile of units, no block."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caca_rig as cr  # noqa: E402
import caca_set as cs  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(289, floor_z=0.0)
B = cr.bathroom(S)
n = cs.N_UNITS
PB = cs.LitePile(S, "units", n, cr.stool_material(S), seed=7)
PG = cs.LitePile(S, "units_bio", n, cr.stool_material(S, cr.GREEN, "bio"), seed=7)
TANK_AT = (160.0, -60.0, 0.0)
TANK_TOP = np.array([TANK_AT[0], TANK_AT[1], 150.0])
water, level, _walls = cs.tank(S, TANK_AT, size=(120.0, 80.0, 140.0))
idx = np.arange(n)
solid = idx % 4 == 0
green = idx % 8 == 0
big = cr.mound(n, (60.0, -60.0), 72.0, 62.0, seed=2, floor=2.0)
compact = cr.mound(int(solid.sum()), (60.0, -60.0), 34.0, 30.0, seed=5, floor=2.0)
rest = big.copy()
rest[solid] = compact
melt_ids = np.where(~solid)[0]
ta = S.t("cuartas", default=3.0) - 0.2
tb = S.t("bacterias", default=6.0)
RELEASE = 2.6
FLY = 0.8


def upd(t):
    pos = big.copy()
    szb = np.full(n, 1.4)
    szg = np.full(n, 1e-4)
    k_s = sp.interp([(ta, 0.0), (ta + 2.0, 1.0)], t)
    pos[solid] = big[solid] + (compact - big[solid]) * k_s
    arrived = 0
    for r, i in enumerate(melt_ids):
        ti = ta - 0.3 + RELEASE * (r / len(melt_ids)) ** 0.9
        k = (t - ti) / FLY
        if k <= 0.0:
            continue
        k = min(k, 1.0)
        e = k * k * (3 - 2 * k)
        p = big[i] + (TANK_TOP - big[i]) * e
        p[2] += 60.0 * np.sin(np.pi * k)
        pos[i] = p
        szb[i] = 1.4 * (1.0 - sp.interp([(0.7, 0.0), (1.0, 1.0)], k))
        if k >= 1.0:
            arrived += 1
    for i in np.where(green)[0]:
        f = sp.interp([(tb, 0.0), (tb + 0.5, 1.0)], t)
        szb[i] = 1.4 * (1.0 - f) + 1e-4
        szg[i] = 1.4 * f + 1e-4
    PB.set(pos, szb)
    PG.set(pos, szg)
    level(0.72 * arrived / len(melt_ids))


S.every_frame(upd)
rk.softboxes(0.8, centre=(130, -40, 60))
S.cam([(0, (85.0, -60.0, 70.0), 470, 10, -34), (S.T * 0.5, (85.0, -60.0, 72.0), 440, 9, -10), (S.T, (140.0, -60.0, 72.0), 330, 9, 14)])
S.go()
