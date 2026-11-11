"""avion 1 (hook): see productions/mecanalia-es/019*/script.json. Two airliners on one stage, one on the ground (warm apron light in its windows), one in flight (dark sky): the same pull on each boarding door's grip bar, the ground door swings open, the flight door does not move. (The hand of the first script is off screen and the cabin staging of the door was tried and dropped: both failed the likeness gate, see notes.md.)"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import avion_rig as av  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(246, floor_z=-av.JET_R - 3.0)
m = av.Mats(S)
UP = 52.0
low = av.airliner(S, m, loc=(0, 0, 0), pane="ground", door="ground", name="jet_low")
high = av.airliner(S, m, loc=(0, 0, UP), pane="sky", door="sky", name="jet_high")
clouds = av.clouds(S, m, 7, ((-90, 90), (12, 50), (UP - 40, UP + 50)))
lift = av.lights(S)
t_pull, t_try, t_cam = 1.3, 4.2, 3.3


def lever(ns, k):
    ns.bar_pivot.rotation_euler = (0.0, av.ease(k) * math.radians(38), 0.0)


def upd(t):
    lever(low, sp.interp([(t_pull - 0.5, 0.0), (t_pull, 1.0)], t))
    av.door_swing(low, sp.interp([(t_pull, 0.0), (t_pull + 1.5, 1.0)], t))
    lever(high, sp.interp([(t_try - 0.4, 0.0), (t_try, 1.0)], t))
    av.door_swing(high, 0.012 * max(0.0, math.sin(30.0 * (t - t_try))) if t > t_try else 0.0)
    for i, (p, home) in enumerate(clouds):
        p.location = (home[0] - 6.0 * t, home[1], home[2])
    tz = sp.interp([(0, 0.0), (t_cam, 0.0), (t_cam + 1.4, UP), (S.T, UP)], t)
    az = sp.interp([(0, 52.0), (t_cam, 50.0), (S.T, 40.0)], t)
    rad = sp.interp([(0, 120.0), (1.2, 52.0), (2.4, 56.0), (3.4, 100.0), (t_cam + 1.4, 100.0), (S.T, 66.0)], t)       # close on the grip bar as it is pulled, then out to the plane with its door open
    av.look(S, (av.JET_DOOR_X - 4.0, -av.JET_R, tz + 1.0), rad, 7.0, az)
    lift(av.JET_DOOR_X, tz)


for ns in (low, high):
    av.door_swing(ns, 0.0)
S.every_frame(upd)
rk.softboxes(0.7, centre=(40, -30, 30))
S.go()
