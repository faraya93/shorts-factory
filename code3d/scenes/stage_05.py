"""v6-staged scene 5 (removal): chunky glossy steel tweezers pinch the last cord end out of a small hole in the boot's leather;
the hole closes and the boot sits whole, no seam. Slot 185 frames (6.17 s). The camera orbits and pushes in throughout."""

import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import boot_world as bw  # noqa: E402
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = bw.begin(185)
T = SLOT / c.FPS
panel = bw.build_boot(m)
sh.rounded_bar("seamless", 3.15, 4.7, 0.45, m.skin)                       # ONE smooth leather panel: no seam, no eyelets
hole = sh.ellipsoid("hole", 0.8, 0.5, 0.2, m.red, loc=(0.0, -1.1, 0.42))
cord = s.Thread(m.cord, points=120, thickness=0.26)
H = Vector((0.0, -1.1, 0.5))
STUB = Vector((0.15, -1.0, 1.6))
V = Vector((3.4, 2.4, 4.0))                                               # the tweezers' vertex, relative to the pinch point
tw_root = lw.empty("tweezers")
pivots = []
for dx in (-0.55, 0.55):
    pivot = lw.empty(f"pivot_{dx}")
    lw.parent(pivot, tw_root, V)
    arm = sh.bar_between(f"arm_{dx}", Vector((dx, 0, 0)) - V, Vector((0, 0, 0)), 0.27, m.steel)
    arm.parent = pivot
    pivots.append((pivot, 1 if dx > 0 else -1))
bw.adopt(panel)
WAY = [(0.0, Vector((5.4, 4.4, 6.4))), (2.3, Vector((0.15, -1.0, 1.6))), (3.0, Vector((0.15, -1.0, 1.6))),
       (4.3, Vector((-0.5, 2.6, 4.0))), (5.5, Vector((-1.8, 4.2, 6.6))), (T, Vector((-1.8, 4.2, 6.6)))]


def path(t):
    for (t0, p0), (t1, p1) in zip(WAY, WAY[1:]):
        if t <= t1:
            return p0.lerp(p1, c.smooth(t0, t1, t))
    return WAY[-1][1]


def update(scene_):
    t = scene_.frame_current / c.FPS
    P = path(t)
    tw_root.location = P
    Q = P if t >= 2.4 else STUB
    opening = 0.16 * (1 - c.smooth(2.0, 2.4, t)) * (0.3 + 0.7 * c.smooth(0.3, 1.7, t)) + 0.05 * c.smooth(1.9, 2.2, t) * (1 - c.smooth(2.2, 2.5, t))
    for pivot, sign in pivots:
        pivot.rotation_euler.z = sign * opening
    detach = c.smooth(4.5, 5.2, t)
    E = H.lerp(Q + Vector((0.2, 0.3, -3.2)), detach)
    sag = max(0.0, 0.5 - 0.12 * (Q - E).length) + 0.7 * detach
    C = (E + Q) / 2 + Vector((0.25, 0, -sag))
    cord.set([E * ((1 - u) ** 2) + C * (2 * u * (1 - u)) + Q * (u * u) for u in [i / 40 for i in range(41)]])
    h = 1 - bw.back((t - 4.7) / 0.9, 0.0)                                 # the hole closes: the leather is whole again
    hole.scale = (h, h, h)
    lw.show(hole, h >= 0.03)
    p = c.smooth(0.0, T, t)
    bw.look(stage, bw.to_world((0, 1.0, 1.0)) + Vector((0, 0, 0.8)), 34.0 - 8.0 * p, 38 + 4 * p, 26 - 42 * p)


stage.run(update, args, SLOT, "stage-05")
