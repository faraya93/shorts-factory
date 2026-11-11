"""avion 3 (presion): see productions/mecanalia-es/019*/script.json. The cabin seen down its aisle with its passengers: accent air streams in from the ceiling and packs the cabin; on 'Afuera' the camera pulls out of the open end and around the cabin, where the air outside is a few sparse pale beads."""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import avion_rig as av  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(231, floor_z=av.FLOOR_Z - 4.0)
m = av.Mats(S)
ai = av.aisle(S, m, door=True, passengers=((-8, -14, 1), (8, 24, 2), (-24, 14, 0), (24, -24, 3)))
rnd = random.Random(5)
N_IN, N_OUT = 90, 18
in_spots = [(rnd.uniform(-50, 50), rnd.uniform(-30, 30), rnd.uniform(-10, 34)) for _ in range(N_IN)]
out_spots = []
for _ in range(N_OUT):
    a = rnd.uniform(0, 2 * math.pi)
    r = rnd.uniform(50, 85)
    out_spots.append((rnd.uniform(-60, 60), -r * math.cos(a), r * math.sin(a)))
t_fill, t_out = S.t("aire", default=1.8), S.t("Afuera,", default=4.7)
src_in, src_out = S.ball("in_src", S.accent, 1.0), S.ball("out_src", m.cloud, 0.9)


def air_in(i, t):
    k = av.ease((t - (t_fill - 0.3 + 1.3 * i / N_IN)) / 0.4)
    return None if k <= 1e-3 else (in_spots[i], k)


def air_out(i, t):
    k = av.ease((t - t_out - 0.3 - 0.8 * i / N_OUT) / 0.5)
    return None if k <= 1e-3 else (out_spots[i], 0.3 + 0.5 * k)


S.swarm(N_IN, src_in, air_in)
S.swarm(N_OUT, src_out, air_out)
lift = av.lights(S)


def upd(t):
    rad = sp.interp([(0, 190.0), (t_out - 0.4, 150.0), (t_out + 1.6, 260.0), (S.T, 280.0)], t)
    az = sp.interp([(0, -97.0), (t_out - 0.4, -92.0), (S.T, -30.0)], t)
    el = sp.interp([(0, 5.0), (t_out - 0.4, 6.0), (S.T, 14.0)], t)
    tx = sp.interp([(0, 30.0), (t_out - 0.4, 30.0), (t_out + 1.6, 0.0), (S.T, 0.0)], t)
    av.look(S, (tx, 0.0, 6.0), rad, el, az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(10, 0, 40))
S.go()
