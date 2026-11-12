"""corr 6 (cierre): see productions/mecanalia-es/023*/script.json. The reframe as ONE image: the glowing person touches the door and the charge visibly flows from the person INTO the car, whose cage of accent bars lights up
while the person's glow drains. The camera pulls back from the hand to the person and the whole car."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import corr_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(272, floor_z=-0.6)
m = cr.Mats(S)
cr.ground(S, m)
car = cr.car(S, m)
lift = cr.lights(S)
P = cr.Person(S)
FACE, X0 = math.pi, 3.0
P.set((X0, -17.0, 0.0), FACE, reach=1.0)
Y1 = -17.0 + (cr.DOOR_Y - 1.4 - P.hand().y)
P.set((X0, Y1, 0.0), FACE, reach=1.0)
H = P.hand()
T_GIVE = S.t("se", 1, default=2.3)
T_END = T_GIVE + 1.6
cr.spark(S, (H.x, H.y, H.z), (H.x, cr.DOOR_Y + 0.1, H.z), T_GIVE - 0.2, T_GIVE + 0.8, flashes=3, r=0.3)
level = lambda t: sp.interp([(T_GIVE - 0.2, 1.0), (T_END, 0.0)], t)
cr.aura(S, m, lambda t: (X0, Y1, 0.0), level, n=26, rad=4.5)
cr.cage(S, T_GIVE, dt=1.5)
src = S.ball("flow_src", S.accent, 0.5)
N = 22


def flow(i, t):
    if t < T_GIVE or t > T_GIVE + 5.0:
        return None
    k = ((t - T_GIVE) * 0.55 + i / N) % 1.0
    tx, ty, tz = -4.0 + 16.0 * ((i * 0.37) % 1.0), 0.0, 19.3
    p = (H.x + (tx - H.x) * k, cr.DOOR_Y + (ty - cr.DOOR_Y) * k, H.z + (tz - H.z) * k + 4.0 * math.sin(math.pi * k))
    return (p, 1.0)


S.swarm(N, src, flow)


def upd(t):
    reach = sp.interp([(0.0, 0.0), (1.2, 1.0)], t)
    P.set((X0, Y1, 0.0), FACE, "standing", "standing", 0.0, reach)
    P.glow(level(t))
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (X0, cr.DOOR_Y - 3.0, 10.0), 40.0, 8.0, -58.0), (T_GIVE, (X0, -8.0, 10.0), 62.0, 10.0, -42.0), (S.T, (2.0, -4.0, 9.0), 112.0, 14.0, 10.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
