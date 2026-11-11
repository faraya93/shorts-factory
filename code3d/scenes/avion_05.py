"""avion 5 (giro): see productions/mecanalia-es/019*/script.json. The turn: an airliner in the sky, the camera tracking from the tail; a door-plug panel aft of the wing with its four bolt points empty (red) creeps up off its stops and blows outward; the cabin air rushes out after it."""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import avion_rig as av  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(314, floor_z=-400.0)
m = av.Mats(S)
jet = av.airliner(S, m)
cl = av.clouds(S, m, 9, ((-160, 160), (30, 90), (-30, 40)), seed=6)
rnd = random.Random(8)
N = 40
src = S.ball("whoosh_src", S.accent, 0.9)
t_creep, t_blow = S.t("soltó", default=5.5) - 0.7, S.t("soltó", default=5.5) + 0.3
jit = [(rnd.uniform(-2, 2), rnd.uniform(-1, 1), rnd.uniform(-3, 3)) for _ in range(N)]


def whoosh(i, t):
    k = (t - t_blow - 0.5 * i / N) / 1.4
    if k <= 0 or k > 1.0:
        return None
    j = jit[i]
    return ((-20.0 + j[0] - 40.0 * k, -av.JET_R - 3.0 - 30.0 * k + j[1], 1.0 + j[2] + 6.0 * k), 0.4 + 0.8 * math.sin(k * math.pi))


S.swarm(N, src, whoosh)
lift = av.lights(S)


def upd(t):
    creep = av.ease((t - t_creep) / 0.9) * 2.0
    blow = max(0.0, t - t_blow)
    p = jet.panel
    if t < t_blow:
        p.location = (-20.0, -av.JET_R - 0.4, 1.0 + creep)
        p.rotation_euler = (0.0, 0.0, 0.0)
    else:
        p.location = (-20.0 - 38.0 * blow, -av.JET_R - 0.4 - 42.0 * blow * blow - 6.0 * blow, 3.0 + 6.0 * blow - 4.0 * blow * blow)
        p.rotation_euler = (2.4 * blow, 1.8 * blow, 1.2 * blow)
    for i, (puff, home) in enumerate(cl):
        puff.location = (home[0] - 70.0 * t, home[1], home[2])
    tx = sp.interp([(0, 14.0), (4.2, -26.0), (S.T, -26.0)], t)
    rad = sp.interp([(0, 330.0), (4.2, 130.0), (S.T, 100.0)], t)
    el = sp.interp([(0, 14.0), (S.T, 8.0)], t)
    az = sp.interp([(0, 30.0), (S.T, -10.0)], t)
    av.look(S, (tx, 0.0, 3.0), rad, el, az)
    lift(tx, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(-20, -20, 30))
S.go()
