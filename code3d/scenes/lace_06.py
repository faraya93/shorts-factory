"""v5-drawn scene 6 (the ant): a cartoon ant raises two folds of skin and clamps them together between its pincers like a staple.
Slot 227 frames (7.57 s). The camera keeps the lower 3/4 view and pulls back and up."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402

args, production, stage, m, SLOT = lw.begin(227)
T = SLOT / c.FPS
sh.rounded_bar("plate", 2.95, 4.9, 0.35, m.skin)
top, red_ant, black = 0.35, m.red, m.cord

ant = lw.empty("ant")                                                      # everything of the ant hangs off one root (a gentle bob)
def on_ant(obj, loc=None):
    lw.parent(obj, ant, loc)
    return obj
for name, rad, loc in (("head", (0.85, 0.8, 0.8), (0, -1.3, top + 1.15)), ("thorax", (0.6, 1.0, 0.6), (0, 0.5, top + 1.3)),
                       ("abdomen", (1.0, 1.5, 0.9), (0, 2.75, top + 1.15))):
    on_ant(sh.ellipsoid(name, *rad, red_ant), loc)
jaws = {}
for side in (-1, 1):
    on_ant(sh.ellipsoid("eye", 0.17, 0.14, 0.2, black), (side * 0.52, -1.9, top + 1.5))
    for y, dk, df in ((-0.1, -0.5, -1.1), (0.5, 0.0, -0.1), (1.1, 0.7, 1.4)):          # front, middle, rear leg
        leg = lw.cord(m, [Vector((side * 0.45, y, top + 1.15)), Vector((side * 1.4, y + dk, top + 1.9)),
                          Vector((side * 2.0, y + df * 0.8, top + 0.12))], thickness=0.13, n=50, smooth_arch=0.0, rounds=2, material=red_ant)
        leg.obj.parent = ant
    ant_t = lw.cord(m, [Vector((side * 0.35, -1.85, top + 1.85)), Vector((side * 0.9, -2.7, top + 2.5)), Vector((side * 1.6, -3.1, top + 2.2))],
                    thickness=0.08, n=40, smooth_arch=0.0, rounds=2, material=red_ant)
    ant_t.obj.parent = ant
    pivot = lw.empty(f"jaw_pivot_{side}")                                  # a pincer hinged at the head, pointing forward and inward
    lw.parent(pivot, ant, (side * 0.85, -1.9, top + 1.0))
    jaw = sh.bar_between("jaw", Vector((0, 0, 0)), Vector((-side * 0.38, -1.0, 0)), 0.23, black)
    jaw.parent = pivot
    jaws[side] = pivot
lips = {}
for side in (-1, 1):                                                       # the two folds of skin that rise between the jaws
    root = lw.empty(f"lip_root_{side}", (0, -2.9, top))
    lw.parent(sh.rounded_bar("lip", 0.16, 0.9, 0.85, m.skin), root, (0, 0, 0.8))
    lips[side] = root


def update(scene_):
    t = scene_.frame_current / c.FPS
    rise = c.smooth(0.3, 1.8, t)
    close = c.smooth(2.2, 3.8, t)
    for side in (-1, 1):
        lips[side].scale = (1, 1, max(0.02, rise))
        lips[side].location.x = side * (0.16 + 0.55 * (1 - close))                    # the folds slide together as the jaws close
        jaws[side].rotation_euler.z = -side * math.radians(40) * (1 - close)          # open -> clamped
    ant.location.z = 0.05 * math.sin(2 * math.pi * 0.7 * t)
    k = c.smooth(1.8, T - 0.4, t)
    lw.look(stage, (0, -0.4 + 1.2 * k, 1.2), 21.0 + 5.0 * k, 30 + 6 * k, 38)


lw.finish(stage, args, SLOT, update, "lace-06")
