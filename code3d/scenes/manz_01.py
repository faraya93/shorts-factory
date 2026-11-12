"""manz 1 (hook): see productions/mecanalia-es/025*/script.json. An apple stands on the plinth; the camera orbits in; it splits in two, the halves hop and fall open like a book with the
cut faces toward the camera, showing the cores and their seeds."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import manz_rig as mz  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

S = sp.Shot(204, floor_z=-1.0)
m = mz.Mats(S)
fr = mz.Fruit(S, m)
tr.rbox("plinth_plate", (170, 90, 2.0), (0, 0, -1.0), m.plate, bevel=0.6)
lift = mz.lights(S, mz.LIGHT_K)
T0 = 2.2


def upd(t):
    k = sp.interp([(T0, 0.0), (T0 + 1.7, 1.0)], t)
    hop = 7.0 * math.sin(math.pi * min(1.0, k))
    fr.split(k, lift=hop) if k > 0 else fr.whole_only()
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (0, 0, 30), 215, 12.0, 30.0), (T0, (0, 0, 30), 215, 12.0, 8.0), (S.T, (0, 0, 32), 270, 12.0, 0.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
