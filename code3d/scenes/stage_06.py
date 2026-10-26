"""v6-staged scene 6 (the ant): a chunky glossy cartoon ant on the boot raises two folds of leather and clamps them together
between its jaws (the jaws open wide first, then snap). Slot 227 frames (7.57 s). The camera orbits and pushes in throughout."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import boot_world as bw  # noqa: E402
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402

args, production, stage, m, SLOT = bw.begin(227)
T = SLOT / c.FPS
panel = bw.build_boot(m)
sh.rounded_bar("seamless", 3.15, 4.7, 0.45, m.skin)
top = 0.45
ant = lw.empty("ant")
on_ant = lambda obj, loc=None: (lw.parent(obj, ant, loc), obj)[1]
for name, rad, loc in (("head", (1.05, 1.0, 0.95), (0, -1.5, top + 1.5)), ("thorax", (0.8, 1.2, 0.8), (0, 0.6, top + 1.7)),
                       ("abdomen", (1.35, 1.9, 1.15), (0, 3.2, top + 1.5))):
    on_ant(sh.ellipsoid(name, *rad, m.ant), loc)
jaws = {}
for side in (-1, 1):
    on_ant(sh.ellipsoid("eye", 0.3, 0.2, 0.34, m.black), (side * 0.62, -2.35, top + 1.95))
    on_ant(sh.ellipsoid("eye_shine", 0.09, 0.06, 0.1, m.sole), (side * 0.7, -2.5, top + 2.1))
    for y, dk, df in ((-0.2, -0.6, -1.3), (0.6, 0.0, -0.1), (1.4, 0.8, 1.6)):
        leg = lw.cord(m, [Vector((side * 0.6, y, top + 1.5)), Vector((side * 1.7, y + dk, top + 2.4)), Vector((side * 2.4, y + df * 0.8, top + 0.15))],
                      thickness=0.2, n=50, smooth_arch=0.0, rounds=2, material=m.ant)
        leg.obj.parent = ant
    an = lw.cord(m, [Vector((side * 0.45, -2.3, top + 2.3)), Vector((side * 1.1, -3.3, top + 3.1)), Vector((side * 1.9, -3.8, top + 2.7))],
                 thickness=0.12, n=40, smooth_arch=0.0, rounds=2, material=m.ant)
    an.obj.parent = ant
    pivot = lw.empty(f"jaw_pivot_{side}")
    lw.parent(pivot, ant, (side * 1.0, -2.3, top + 1.2))
    jaw = sh.bar_between("jaw", Vector((0, 0, 0)), Vector((-side * 0.5, -1.3, 0)), 0.32, m.black)
    jaw.parent = pivot
    jaws[side] = pivot
lips = {}
for side in (-1, 1):
    root = lw.empty(f"lip_root_{side}", (0, -3.7, top))
    lw.parent(sh.rounded_bar("lip", 0.3, 1.1, 1.0, m.skin), root, (0, 0, 0.95))
    lips[side] = root
bw.adopt(panel)


def update(scene_):
    t = scene_.frame_current / c.FPS
    rise = bw.back((t - 0.3) / 1.5, 1.8)
    wind = c.smooth(1.9, 2.6, t)                                          # anticipation: the jaws gape wider...
    snap = bw.back((t - 2.6) / 0.6, 2.2)                                  # ...then snap shut (with a little overshoot)
    for side in (-1, 1):
        lips[side].scale = (1, 1, max(0.02, rise))
        lips[side].location.x = side * (0.3 + 0.8 * (1 - c.smooth(2.4, 3.3, t)))
        jaws[side].rotation_euler.z = -side * math.radians(42 + 14 * wind) * (1 - snap)
    ant.location.z = 0.07 * math.sin(2 * math.pi * 0.8 * t) - 0.12 * math.sin(math.pi * c.smooth(2.6, 3.4, t))
    p = c.smooth(0.0, T, t)
    bw.look(stage, bw.to_world((0, -0.8 + 1.4 * p, 1.2)) + Vector((0, 0, 0.8)), 33.0 - 8.0 * p, 34 + 7 * p, -34 + 44 * p)


stage.run(update, args, SLOT, "stage-06")
