"""manz 3 (entera): see productions/mecanalia-es/025*/script.json. A closed seed rolls along a half tube while juice drops fall on its shell and slide off; it leaves the far end unchanged."""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import manz_rig as mz  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

S = sp.Shot(270, floor_z=-1.0)
m = mz.Mats(S)
sd = mz.Seed(S, m)
tr.rbox("plinth_plate", (260, 90, 2.0), (0, 0, -1.0), m.plate, bevel=0.6)
TR, ZCT = 17.0, 17.5
mz.half_pipe("tube_wall", -95.0, 95.0, TR, ZCT, m.tube)
mz.tube_bands(S, m, "tube_rib", 9, -80.0, 80.0, TR, ZCT)
dr = mz.drops(S, m, 16)
lift = mz.lights(S, mz.LIGHT_K)
rnd = random.Random(4)
T_IN, T_OUT = 0.4, S.T - 0.4
DROPS = [(rnd.uniform(0.9, S.T - 2.2), rnd.uniform(-4.0, 6.0), rnd.uniform(-1.6, 1.6)) for _ in dr]


def xs(t):
    return sp.interp([(T_IN, -62.0), (T_OUT, 62.0)], t)


def upd(t):
    x = xs(t)
    roll = (x + 62.0) / 5.3
    sd.set((x, 4.0, 5.6), (roll, 0.0, 0.0), gap=0.0, kernel=0.0)
    for (td, dx, dy), o in zip(DROPS, dr):
        d = next(dd for ob, dd in S.items if ob is o)
        u = t - td
        if u < 0 or u > 1.5:
            d["sw"] = None
            continue
        xd = xs(t) + dx
        if u < 0.5:                                                                  # falls from the tube roof onto the shell
            z = sp.lerp(32.0, 11.0, (u / 0.5) ** 2)
            d["sw"] = ((xd, 5.0 + dy, z), 1.0)
        else:                                                                        # slides down the shell toward the floor and fades
            w = (u - 0.5) / 1.0
            d["sw"] = ((xd + dx * 0.15 * w, 5.0 + dy + 6.0 * w, sp.lerp(11.0, 1.0, w)), max(0.05, 1.0 - w))
    lift(x * 0.4, 0.0)


S.every_frame(upd)
S.cam([(0.0, (-52, 0, 9), 150, 9.0, -22.0), (S.T * 0.5, (0, 0, 9), 125, 7.0, 4.0), (S.T, (52, 0, 9), 150, 9.0, 24.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
