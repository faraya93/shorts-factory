"""oido 4 (tapon): see productions/mecanalia-es/024*/script.json. The turn. The swab goes in and out again and again; every pass leaves more wax packed against the eardrum until a dense plug
fills the canal. Slim accent rings (sound) travel in from the entrance: the first one reaches the drum and lights it; once the plug stands they stop at its face and the drum stays dark.
The camera pushes to the drum and pulls back."""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import oido_rig as od  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(217, floor_z=-2.0 * od.KS)
m = od.Mats(S)
ear = od.Ear(S, m, lining=None)
cv = od.Conveyor(S, m, nb=7, nf=0 + 1, nd=0 + 1)
sw = od.Swab(S, m)
lift = od.lights(S, od.LIGHT_K)
T_PLUG = S.t("tapón", default=2.4)
GROUPS = [(0.0, 44.0), (T_PLUG - 0.4, 41.0), (T_PLUG + 1.4, 38.0), (T_PLUG + 2.8, 35.0)]       # (pop time, x of the plug face once the group stands)

rnd = random.Random(11)
pts, pops = [], []
for gi, (tp, xf) in enumerate(GROUPS):
    for _ in range(9):
        dz = rnd.uniform(-5.2, 5.2)
        pts.append((rnd.uniform(xf + 2.0, 47.5), rnd.uniform(2.8, 4.2), od.CZ + dz))
        pops.append(None if gi == 0 else (tp + rnd.uniform(0.0, 0.5), 0.35))
plug = od.lumps(S, m, "plug", pts, r=4.1, seed=4, pops=pops)

rings = [od.ring(S, f"ring_{i}", S.accent, r=7.0, minor=0.6) for i in range(8)]
RING_T0 = [0.1 + 0.85 * i for i in range(8)]
RING_V = 30.0


def face_x(t):
    x = 99.0
    for tp, xf in GROUPS:
        if t >= tp + 0.3:
            x = min(x, xf)
    return x


def swab_tip(t):
    return sp.interp([(0.0, 36.0), (0.7, 20.0), (1.6, 38.0), (2.4, 20.0), (3.3, 40.0), (4.2, 18.0), (5.1, 42.0), (6.0, 16.0), (S.T, 2.0)], t)


def upd(t):
    cv.update(t, 4.0, bands_on=1.0, flakes_on=0.0, dust_on=0.0)
    sw.tip_at(swab_tip(t), 1.5, od.CZ, tilt=0.0)
    stop = face_x(t) - 1.2
    for o, t0 in zip(rings, RING_T0):
        d = next(dd for ob, dd in S.items if ob is o)
        x = -6.0 + RING_V * (t - t0)
        if t < t0:
            d["sw"] = None
        elif x >= stop:                                                  # arrived: the ring stops and shrinks away at the plug face
            u = (x - stop) / 5.0
            d["sw"] = None if u > 0.98 else (od.P(stop, 0, od.CZ), max(0.02, 1.0 - u))
        else:
            d["sw"] = (od.P(x, 0, od.CZ), 0.85 + 0.15 * math.sin(6.0 * t))
    lift(0.0, 0.0)


for o in rings:
    d = next(dd for ob, dd in S.items if ob is o)
    d["pop"] = None
    d["sw"] = None
S.every_frame(upd)
S.cam([(0.0, od.P(30, 0, 34), od.R(190), 10.0, -14.0), (S.T * 0.3, od.P(42, 0, 34), od.R(105), 8.0, -6.0), (S.T * 0.62, od.P(14, 0, 34), od.R(270), 9.0, -40.0), (S.T, od.P(8, 0, 34), od.R(285), 8.0, -44.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
