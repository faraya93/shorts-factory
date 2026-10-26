"""v5-drawn scene 5 (removal): chunky tweezers pinch a cord sticking out of a tiny hole in one smooth plate and pull it out;
the hole closes and the plate is whole again. Slot 185 frames (6.17 s)."""

import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = lw.begin(185)
T = SLOT / c.FPS
sh.rounded_bar("plate", 2.95, 4.7, 0.35, m.skin)                          # ONE smooth whole plate: no seam, no eyelets
hole = sh.ellipsoid("hole", 0.5, 0.3, 0.14, m.red, loc=(0.0, -1.1, 0.34))
cord = s.Thread(m.cord, points=120, thickness=0.17)
H = Vector((0.0, -1.1, 0.4))                                              # where the cord leaves the plate
STUB = Vector((0.15, -1.0, 1.4))                                          # a short stub sticking out of the hole

V = Vector((2.7, 1.9, 3.1))                                               # the tweezers' vertex, relative to the pinch point
tw_root = lw.empty("tweezers")
pivots = []
for dx in (-0.4, 0.4):                                                    # two arms, hinged at the vertex, visible gap at the tips
    pivot = lw.empty(f"pivot_{dx}")
    lw.parent(pivot, tw_root, V)
    arm = sh.bar_between(f"arm_{dx}", Vector((dx, 0, 0)) - V, Vector((0, 0, 0)), 0.17, m.steel)
    arm.parent = pivot
    pivots.append((pivot, 1 if dx > 0 else -1))

WAY = [(0.0, Vector((4.2, 3.4, 5.2))), (2.5, Vector((0.15, -1.0, 1.4))), (3.2, Vector((0.15, -1.0, 1.4))),
       (4.4, Vector((-0.4, 2.2, 3.3))), (5.6, Vector((-1.4, 3.6, 5.4))), (T, Vector((-1.4, 3.6, 5.4)))]


def path(t):
    for (t0, p0), (t1, p1) in zip(WAY, WAY[1:]):
        if t <= t1:
            return p0.lerp(p1, c.smooth(t0, t1, t))
    return WAY[-1][1]


def update(scene_):
    t = scene_.frame_current / c.FPS
    P = path(t)
    tw_root.location = P
    Q = P if t >= 2.5 else STUB                                           # the cord's free tip: the stub, then wherever the tweezers hold it
    opening = 0.13 * (1 - c.smooth(2.2, 2.6, t)) * (0.3 + 0.7 * c.smooth(0.3, 1.8, t))   # open on the way in, closed on the cord
    for pivot, sign in pivots:
        pivot.rotation_euler.z = sign * opening
    detach = c.smooth(4.7, 5.3, t)                                        # the cord comes out of the hole and hangs from the tweezers
    E = H.lerp(Q + Vector((0.2, 0.3, -3.0)), detach)
    sag = max(0.0, 0.5 - 0.12 * (Q - E).length) + 0.7 * detach
    C = (E + Q) / 2 + Vector((0.25, 0, -sag))
    cord.set([E * ((1 - u) ** 2) + C * (2 * u * (1 - u)) + Q * (u * u) for u in [i / 40 for i in range(41)]])
    h = 1 - c.smooth(4.8, 5.6, t)                                         # the hole closes: the surface is whole again
    hole.scale = (h, h, h)
    lw.show(hole, h >= 0.03)
    k = c.smooth(0.0, T, t)
    lw.look(stage, (0, 1.2, 1.4), 22.0 - 1.5 * k, 60)


lw.finish(stage, args, SLOT, update, "lace-05")
