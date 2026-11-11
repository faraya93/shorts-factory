"""avion 6 (cierre): see productions/mecanalia-es/019*/script.json. The reframe image: the cabin seen down its aisle, the door at the far end held against its frame by the packed accent air (a glowing rim and a crowd of accent beads); the camera then pulls out of the open end and up to take in the whole cabin section in the sky."""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import avion_rig as av  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

S = sp.Shot(297, floor_z=av.FLOOR_Z - 4.0)
m = av.Mats(S)
ai = av.aisle(S, m, door=True, passengers=((-8, -14, 1), (8, 24, 2), (-24, 14, 0)))
xw = av.AISLE_L / 2
glow = tr.rbox("door_glow", (0.8, 34.0, 42.0), (xw - 1.5, 0.0, 3.0), S.accent, bevel=0.3)
rnd = random.Random(12)
N = 70
spots = [(rnd.uniform(20, 56), rnd.uniform(-26, 26), rnd.uniform(-10, 34)) for _ in range(N)]
t_air = S.t("aire", default=3.4)
src = S.ball("press_src", S.accent, 1.0)


def beads(i, t):
    k = av.ease((t - (t_air - 1.4 + 1.2 * i / N)) / 0.4)
    if k <= 1e-3:
        return None
    x, y, z = spots[i]
    return ((x + 1.2 * math.sin(5.0 * t + i), y, z), k * (0.8 + 0.2 * math.sin(7.0 * t + i)))


S.swarm(N, src, beads)
lift = av.lights(S)


def upd(t):
    k = av.ease((t - (t_air - 1.0)) / 0.8)
    glow.scale = (1.0, (1.0 + 0.05 * math.sin(6.0 * t) * k) * max(k, 1e-3), (1.0 + 0.05 * math.sin(6.0 * t) * k) * max(k, 1e-3))
    rad = sp.interp([(0, 120.0), (4.4, 128.0), (6.0, 200.0), (S.T, 300.0)], t)
    az = sp.interp([(0, -96.0), (4.4, -94.0), (S.T, -32.0)], t)
    el = sp.interp([(0, 5.0), (4.4, 5.0), (S.T, 14.0)], t)
    tx = sp.interp([(0, 44.0), (4.4, 42.0), (S.T, 0.0)], t)
    av.look(S, (tx, 0.0, 6.0), rad, el, az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(10, 0, 40))
S.go()
