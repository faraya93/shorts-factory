"""corr 2 (asiento): see productions/mecanalia-es/023*/script.json. The roof of the sealed car slides away so the seat is visible; the person slides on the seat, gets up and the accent glow builds over the body
while a few ink beads (the opposite charge) stay on the seat; then the person steps out over the side. Camera travels low and lateral."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import corr_rig as cr  # noqa: E402
import rayo_rig as ry  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(262, floor_z=-0.6)
m = cr.Mats(S)
cr.ground(S, m)
car = cr.car(S, m)
ry.set_roof(car, 1.0)
lift = cr.lights(S)
P = cr.Person(S)
FACE = -math.pi / 2
SEAT = (1.0, -2.6)
T_RUB, T_UP, T_STAND = S.t("frota", default=1.6), S.t("despegan.", default=2.8), S.t("roce", default=4.5)
T_OUT = S.t("asiento", 1, default=5.9)
T_END = S.T - 0.4


def pos(t):
    k = sp.interp([(T_UP, 0.0), (T_STAND, 1.0)], t)
    x = SEAT[0] + 1.0 * math.sin((t - T_RUB) * 6.0) * sp.interp([(T_RUB, 0.0), (T_RUB + 0.3, 1.0), (T_UP - 0.2, 1.0), (T_UP, 0.0)], t)
    kk = sp.interp([(T_OUT, 0.0), (T_END, 1.0)], t)
    y = SEAT[1] + (-15.0 - SEAT[1]) * kk
    z = 5.4 + (3.4 - 5.4) * k + 4.0 * math.sin(math.pi * kk)
    z = z if kk < 0.999 else 0.0
    if 0.0 < kk < 1.0:
        z = 3.4 + (0.0 - 3.4) * kk + 5.0 * math.sin(math.pi * kk)
    return (x, y, z)


level = lambda t: sp.interp([(T_UP, 0.0), (T_STAND, 0.5), (T_OUT + 1.0, 1.0)], t)
cr.aura(S, m, lambda t: (pos(t)[0] + (0.0), pos(t)[1], pos(t)[2]), level, n=24, rad=4.5, h0=2.0, h1=15.0)
cr.aura(S, m, lambda t: (SEAT[0], SEAT[1], 3.0), lambda t: sp.interp([(T_OUT, 0.0), (T_OUT + 1.0, 0.5)], t), n=10, rad=2.4, h0=0.5, h1=4.0, r=0.3, name="seatbead", mat=m.ink)


def upd(t):
    p = pos(t)
    kk = sp.interp([(T_OUT, 0.0), (T_END, 1.0)], t)
    sit = sp.interp([(T_UP, 0.0), (T_STAND, 1.0)], t)
    walking = 0.5 + 0.5 * math.sin(t * 8.0) if 0.0 < kk < 1.0 else 0.0
    if kk > 0.0:
        P.set(p, FACE, "standing", "walking", walking)
    else:
        P.set(p, FACE, "seated", "standing", sit)
    P.glow(level(t))
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (0.0, -3.0, 10.0), 62.0, 26.0, -35.0), (T_UP, (0.0, -3.0, 10.0), 55.0, 22.0, -12.0), (S.T, (0.0, -6.0, 9.0), 58.0, 12.0, 22.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
