"""corr 3 (voltaje): see productions/mecanalia-es/023*/script.json. The charged person walks along the car toward the door, the glow climbing one notch per step; the camera stays ahead of the person and backs away."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import corr_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(204, floor_z=-0.6)
m = cr.Mats(S)
cr.ground(S, m)
car = cr.car(S, m)
lift = cr.lights(S)
P = cr.Person(S)
FACE = -math.pi / 2
X0, X1, Y = 30.0, 4.0, -15.5
px = lambda t: sp.interp([(0.0, X0), (S.T - 0.3, X1)], t)
steps = lambda t: math.floor(t * 2.2) / (S.T * 2.2)
level = lambda t: min(1.0, 0.25 + 0.95 * steps(t) / 0.97)
cr.aura(S, m, lambda t: (px(t), Y, 0.0), level, n=30, rad=4.6)


def upd(t):
    P.set((px(t), Y, 0.0), FACE, "standing", "walking", 0.5 + 0.5 * math.sin(t * 8.0))
    P.glow(level(t))
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (X0 - 6.0, Y, 9.0), 48.0, 10.0, -75.0), (S.T, (X1 - 6.0, Y, 10.0), 62.0, 14.0, -55.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
