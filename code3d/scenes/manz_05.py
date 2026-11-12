"""manz 5 (muchas): see productions/mecanalia-es/025*/script.json. One apple stands on the plinth; seeds rain down on its right and heap up into a mound bigger than the apple while the camera
pulls back and climbs along the heap."""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import manz_rig as mz  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

S = sp.Shot(221, floor_z=-1.0)
m = mz.Mats(S)
fr = mz.Fruit(S, m, seeds=False)
N = 96
pile = mz.pile_seeds(S, m, N)
tr.rbox("plinth_plate", (230, 110, 2.0), (0, 0, -1.0), m.plate, bevel=0.6)
lift = mz.lights(S, mz.LIGHT_K)
rnd = random.Random(9)
HX, HR, HH = 33.0, 27.0, 17.0
T_START = S.t("tendrías", default=2.0)
SPAN = S.T - T_START - 1.6
SPOTS = []
for i in range(N):
    r = HR * math.sqrt(rnd.random())
    a = rnd.uniform(0, 2 * math.pi)
    z = HH * (1 - r / HR) ** 0.9 + 2.2
    SPOTS.append((HX + r * math.cos(a), 6.0 + r * math.sin(a) * 0.8, z, rnd.uniform(0, 6.3), rnd.uniform(0, 6.3), rnd.uniform(0, 6.3)))
ORDER = sorted(range(N), key=lambda i: SPOTS[i][2])                                    # low seeds land first so the heap builds from the base


def upd(t):
    fr.whole_only((-30.0, 6.0, 0.0), (0, 0, 0.5))
    for rank, i in enumerate(ORDER):
        o = pile[i]
        d = next(dd for ob, dd in S.items if ob is o)
        x, y, z, rx, ry, rz = SPOTS[i]
        t0 = T_START + SPAN * (rank / N) ** 0.8
        u = (t - t0) / 0.55
        if u < 0:
            d["sw"] = None
        else:
            h = sp.lerp(95.0, z, min(1.0, u) ** 2)
            d["sw"] = ((x, y, h), 1.0, (rx + 2.0 * (1 - min(1.0, u)), ry, rz))
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (-28, 0, 18), 115, 8.0, -18.0), (S.T * 0.5, (0, 0, 20), 215, 14.0, 6.0), (S.T, (6, 4, 18), 320, 26.0, 14.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
