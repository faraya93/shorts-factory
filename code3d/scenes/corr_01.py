"""corr 1 (hook): see productions/mecanalia-es/023*/script.json. A person walks up to a closed car and reaches for the door; a spark snaps between the hand and the metal; the camera orbits low between the two;
then the glow gathers on the PERSON (the tag TÚ), not on the car."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import corr_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(250, floor_z=-0.6)
m = cr.Mats(S)
cr.ground(S, m)
car = cr.car(S, m)
lift = cr.lights(S)
P = cr.Person(S)
FACE = math.pi
X0, GAP = 3.0, 2.6
P.set((X0, -17.0, 0.0), FACE, reach=1.0)
Y1 = -17.0 + (cr.DOOR_Y - GAP - P.hand().y)
P.set((X0, Y1, 0.0), FACE, reach=1.0)
H = P.hand()
T_SPARK = S.t("auto?", default=2.0)
cr.spark(S, (H.x, H.y, H.z), (H.x, cr.DOOR_Y + 0.2, H.z), T_SPARK, T_SPARK + 1.0, flashes=4, r=0.4)
T_TU = S.t("llevas", default=6.9)
level = lambda t: sp.interp([(T_TU - 0.7, 0.0), (T_TU + 0.7, 0.85)], t)
cr.aura(S, m, lambda t: (X0, Y1, 0.0), level)


def upd(t):
    y = sp.interp([(0.0, Y1 - 15.0), (T_SPARK - 0.2, Y1)], t)
    walk = 0.5 + 0.5 * math.sin(t * 9.0) if t < T_SPARK - 0.2 else 0.0
    reach = sp.interp([(T_SPARK - 0.9, 0.0), (T_SPARK - 0.15, 1.0), (T_SPARK + 1.0, 1.0), (T_SPARK + 1.7, 0.0)], t)
    P.set((X0, y, 0.0), FACE, "standing", "walking", walk, reach)
    P.glow(level(t))
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (3.0, -8.0, 12.0), 80.0, 7.0, -85.0), (T_SPARK + 0.5, (3.0, -10.0, 12.0), 58.0, 8.0, -62.0), (S.T, (3.0, -8.0, 12.0), 68.0, 12.0, 28.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
