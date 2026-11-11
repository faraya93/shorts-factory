"""avion 4 (empuje): see productions/mecanalia-es/019*/script.json. The door laid flat on a pad of accent air that presses it up; five cars drop one by one onto its outline and stack, the camera pulling back and climbing."""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import avion_rig as av  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

S = sp.Shot(173, floor_z=-4.0)
m = av.Mats(S)
tr.rbox("pad_air", (40.0, 26.0, 1.6), (0, 0, -2.6), m.accent, bevel=0.5)
slab = tr.rbox("door_flat", (av.DOOR_H, av.DOOR_W + 4.0, 2.4), (0, 0, 0.0), m.door, bevel=0.6)
tr.rbox("door_flat_handle", (8.0, 1.2, 0.9), (4.0, 0, 1.6), m.ink, bevel=0.3)
for s in (-1, 1):
    tr.rbox(f"door_flat_edge{s}", (4.0, av.DOOR_W + 4.2, 2.6), (s * (av.DOOR_H / 2 - 2.0), 0, 0), m.accent, bevel=0.3)
CAR_K, CAR_H = 6.0, 1.62 * 6.0
rnd = random.Random(4)
cars = []
t_drop = [S.t("fuerza", default=3.3) - 2.2 + 0.0, 0, 0, 0, 0]
t_drop = [0.6, 1.4, 2.2, 3.0, 3.8]
for i in range(5):
    root, car_objs = av.place("cartoon-car", None, CAR_K, loc=(0, 0, 0), rot=(0, 0, math.pi / 2 + rnd.uniform(-0.08, 0.08)))
    for j, o in enumerate(car_objs):
        o.name = f"car_{i}_{j}"                                       # so the visibility check can find them
    cars.append((root, rnd.uniform(-1.4, 1.4), rnd.uniform(-1.0, 1.0)))
lift = av.lights(S)
src = S.ball("press_src", S.accent, 0.8)
N = 34
spots = [(rnd.uniform(-17, 17), rnd.uniform(-11, 11)) for _ in range(N)]


def blob(i, t):
    k = ((t * 0.7 + i / N) % 1.0)
    x, y = spots[i]
    return ((x, y, -1.0 + 7.0 * k), 0.5 + 0.5 * math.sin(k * math.pi))


S.swarm(N, src, blob)


def car_z(i, t):
    t0 = t_drop[i]
    base = -0.238 * CAR_K + 1.2 + i * (CAR_H + 0.4)
    if t < t0:
        return base + 140.0, False
    k = min(1.0, (t - t0) / 0.5)
    return base + 140.0 * (1.0 - k * k), k >= 1.0


def upd(t):
    top = 0.0
    for i, (root, ox, oy) in enumerate(cars):
        z, down = car_z(i, t)
        root.location = (ox, oy, z)
        if down:
            top = 1.2 + (i + 1) * (CAR_H + 0.4)
            root.location = (ox, oy, z + 0.5 * math.sin(max(0.0, 1.0 - (t - t_drop[i] - 0.5) * 4.0) * math.pi) * 0.6 if t - t_drop[i] < 0.75 else z)
    slab.scale = (1.0, 1.0, 1.0 - 0.18 * min(1.0, top / 40.0))
    rad = sp.interp([(0, 95.0), (S.T, 230.0)], t)
    el = sp.interp([(0, 10.0), (S.T, 26.0)], t)
    az = sp.interp([(0, -28.0), (S.T, 14.0)], t)
    tz = sp.interp([(0, 4.0), (S.T, 28.0)], t)
    av.look(S, (0.0, 0.0, tz), rad, el, az)
    lift(0.0, tz * 0.5)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -10, 40))
S.go()
