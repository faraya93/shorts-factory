"""corr 5 (giro): see productions/mecanalia-es/023*/script.json. The turn: at a fuel pump (nozzle in the car's filler) the person gets back into the car and out again while the pump runs; the glow builds on the way, and
as the hand returns to the nozzle a small arc jumps (the beat stops at the spark, no fire). The camera travels from the pump to the hand on the nozzle."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import corr_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(286, floor_z=-0.6)
m = cr.Mats(S)
cr.ground(S, m)
car = cr.car(S, m)
lift = cr.lights(S)
P = cr.Person(S)
PI = math.pi
XP, GAP = 17.0, 4.2
P.set((XP, -15.0, 0.0), PI, reach=1.0)
YP = -15.0 + (cr.DOOR_Y - GAP - P.hand().y)
P.set((XP, YP, 0.0), PI, reach=1.0)
H = P.hand()
NOZ = (H.x, cr.DOOR_Y - 0.2, H.z)
cr.pump(S, m, (XP + 17.0, -17.0, 0.0), NOZ)
T_SP = S.T - 1.1
cr.spark(S, (H.x, H.y, H.z), (NOZ[0], cr.DOOR_Y - 2.9, NOZ[2]), T_SP, T_SP + 0.9, flashes=3, r=0.22)
X = [(0, XP), (4.2, XP), (5.0, 3.0), (7.9, 3.0), (8.6, XP)]
Y = [(0, YP), (5.0, YP), (5.9, -2.6), (7.0, -2.6), (7.9, YP)]
Z = [(0, 0.0), (5.0, 0.0), (5.9, 5.4), (6.4, 5.4), (6.9, 3.4), (7.9, 0.0)]
SIT = [(5.0, 0.0), (5.9, 1.0), (6.4, 1.0), (6.9, 0.0)]
ROT = [(0, PI), (4.2, PI), (4.8, 1.5 * PI), (6.9, 1.5 * PI), (7.6, 0.5 * PI), (8.6, 0.5 * PI), (8.9, PI)]
REACH = [(T_SP - 0.5, 0.0), (T_SP, 1.0)]
pos = lambda t: (sp.interp(X, t), sp.interp(Y, t), sp.interp(Z, t))
level = lambda t: sp.interp([(5.6, 0.0), (6.6, 0.5), (7.7, 1.0)], t)
cr.aura(S, m, pos, level, n=24, rad=4.5, h0=2.0, h1=15.0)


def upd(t):
    a, b = pos(t), pos(t + 0.05)
    moving = math.dist(a, b) > 0.12
    sit = sp.interp(SIT, t)
    if sit > 0.0:
        P.set(a, sp.interp(ROT, t), "standing", "seated", sit)
    else:
        P.set(a, sp.interp(ROT, t), "standing", "walking", (0.5 + 0.5 * math.sin(t * 8.0)) if moving else 0.0, sp.interp(REACH, t))
    P.glow(level(t))
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (30.0, -14.0, 12.0), 72.0, 10.0, -22.0), (4.5, (16.0, -10.0, 10.0), 84.0, 12.0, -5.0), (7.0, (10.0, -8.0, 9.0), 80.0, 14.0, 12.0), (S.T, (XP, -11.0, 9.0), 34.0, 9.0, -35.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
