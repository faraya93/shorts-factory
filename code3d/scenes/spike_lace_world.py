"""SPIKE (concept first): the other scenes of the stitches story in the owner-picked LACE-UP graphic system. One static draft
frame per scene through the toon pass; same backdrop, palette, flaps, eyelets, lace and needle.

  2  the picked concept with the floating lace end fixed (the lace is folded double through the needle's eye)
  1  the setup: a gap too wide to meet; two chubby tabs reach toward each other and stop short
  3  tying off: the laces crossed all the way up and finished in a bold bow
  4  the thread dissolving: the lace is a chain of beads that shrink and pop away as bubbles, the closure stays shut
  5  removal: one smooth whole plate, a cord lifted out of a tiny hole by chunky tweezers
  6  the ant: a literal cartoon ant (primitives, flat colours) whose jaws pinch two raised lips together like a staple

Run: blender -b --python code3d/scenes/spike_lace_world.py -- production=<spike dir> scene=1|2|3|4|5|6 mode=draft-full out=<dir>
"""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402
import stage as st  # noqa: E402
import suture as s  # noqa: E402
import toon  # noqa: E402

args = c.parse_args()
production = Path(args["production"])
which = args["scene"]
stage = st.Stage(production, args.get("mode", "draft-full"))
pal = stage.pal
m = lw.materials(pal)
ROWS = [-3.4, -1.7, 0.0, 1.7, 3.4]


def scene2():
    g = lw.gap_fn(1.15, 0.19)
    lw.flaps(m, 1.15, 0.19)
    lw.eyelets(m, ROWS, g)
    y_n = ROWS[3]
    p_tail, p_tip = lw.eyelet(-1, y_n, g) + Vector((-1.5, 0, 0)), lw.eyelet(+1, y_n, g) + Vector((1.6, 0, 0))
    eye = lw.needle_with_eye(m, p_tail, p_tip, 0.2)
    end = Vector((eye.x, eye.y, 0.62))                                  # BOTH strands converge into the eye: a doubled thread
    lw.x_lacing(m, ROWS, g, 2, end, end)
    return dict(el=74, radius=19.5, target=(0, 0.3, 0.2))


def scene1():
    g = lw.gap_fn(3.4, 0.0)                                             # a very wide gap
    lw.flaps(m, 3.4, 0.0, hx=1.4)
    lw.eyelets(m, ROWS, g)
    for side in (-1, 1):                                                # two chubby tabs reach toward each other and stop short
        sh.rounded_bar(f"tab_{side}", 0.62, 0.45, 0.3, m.skin, loc=(side * 1.07, 0.0, 0.0))
    return dict(el=74, radius=19.5, target=(0, 0.0, 0.2))


def scene3():
    g = lw.gap_fn(0.3, 0.07)                                            # closed, with the boot's flared top
    lw.flaps(m, 0.3, 0.07)
    lw.eyelets(m, ROWS, g)
    knot = Vector((0.0, ROWS[-1] + 1.2, 0.78))
    lw.x_lacing(m, ROWS, g, 4, knot, knot)                              # the strands run up and into the knot
    sh.ellipsoid("knot", 0.36, 0.34, 0.3, m.cord, loc=knot)
    for side in (-1, 1):                                                # the bow: two bold loops and two tails
        a, b, rot = 1.05, 0.55, math.radians(24) * side
        cx, cy = side * 1.15, knot.y + 0.28
        pts = [Vector((cx + a * math.cos(th) * math.cos(rot) - b * math.sin(th) * math.sin(rot),
                       cy + a * math.cos(th) * math.sin(rot) + b * math.sin(th) * math.cos(rot), 0.95 + 0.12 * math.sin(th)))
               for th in [i * 2 * math.pi / 40 for i in range(41)]]
        t_ = s.Thread(m.cord, points=140, thickness=0.17)
        t_.set(pts)
        lw.cord(m, [knot + Vector((0, -0.1, -0.1)), Vector((side * 0.45, knot.y - 1.0, 0.8)), Vector((side * 1.35, knot.y - 2.1, 0.7))],
                thickness=0.17, n=60, smooth_arch=0.0, rounds=2)
    return dict(el=74, radius=19.5, target=(0, 0.6, 0.2))


def scene4():
    g = lw.gap_fn(0.3, 0.07)
    lw.flaps(m, 0.3, 0.07)
    lw.eyelets(m, ROWS, g)
    for strand in (0, 1):                                               # the same X lacing, but made of beads
        path = [Vector((e.x, e.y, 0.6)) for e in (lw.eyelet((-1 if (i + strand) % 2 == 0 else 1), ROWS[i], g) for i in range(5))]
        pts = []
        for a, b in zip(path, path[1:]):
            L = (b - a).length
            pts += [a.lerp(b, k * 0.28 / L) for k in range(int(L / 0.28))]
        for i, p in enumerate(pts):                                     # whole at the bottom, shrinking, gone near the top
            f = i / len(pts)
            scale = 1.0 if f < 0.30 else max(0.0, 1.0 - (f - 0.30) / 0.42)
            if scale > 0.12:
                r = 0.2 * scale + 0.03
                sh.ellipsoid("bead", r, r, r, m.cord, loc=p, segments=24, rings=12)
    for k, (x, y, z, r) in enumerate([(0.0, 1.0, 1.4, 0.36), (-0.55, 2.0, 2.0, 0.26), (0.5, 2.9, 2.5, 0.42), (-0.2, 3.9, 3.1, 0.3),
                                      (0.7, 4.7, 3.6, 0.22), (-0.8, 5.3, 4.0, 0.34)]):   # what dissolved floats up as bubbles
        sh.ring("bubble", r, 0.055, m.steel, loc=(x, y, z))             # a bubble = an outline ring
    return dict(el=66, radius=21, target=(0, 1.2, 1.2))


def scene5():
    sh.rounded_bar("plate", 2.95, 4.7, 0.35, m.skin, loc=(0, 0, 0))     # ONE smooth whole plate: no seam, no eyelets
    sh.ellipsoid("hole", 0.5, 0.3, 0.14, m.red, loc=(0.0, -1.1, 0.34))
    p = [Vector((0.0, -1.1, 0.4)), Vector((0.2, -0.2, 1.1)), Vector((-0.9, 1.0, 2.2)), Vector((-0.4, 2.2, 3.3))]
    lw.cord(m, p, thickness=0.17, n=100, smooth_arch=0.0, rounds=3)
    pinch = p[-1]
    vertex = pinch + Vector((2.7, 1.9, 3.1))                              # tweezers: a thin V, arms meeting at the back
    for k, dx in enumerate((-0.26, 0.26)):
        sh.bar_between(f"arm_{k}", pinch + Vector((dx, 0, 0)), vertex, 0.2, m.steel)
    return dict(el=60, radius=21, target=(0, 1.2, 1.4))


def scene6():
    sh.rounded_bar("plate", 2.95, 4.9, 0.35, m.skin, loc=(0, 0, 0))
    top, red_ant, black = 0.35, m.red, m.cord
    sh.ellipsoid("head", 0.85, 0.8, 0.8, red_ant, loc=(0, -1.3, top + 1.15))
    sh.ellipsoid("thorax", 0.6, 1.0, 0.6, red_ant, loc=(0, 0.5, top + 1.3))
    sh.ellipsoid("abdomen", 1.0, 1.5, 0.9, red_ant, loc=(0, 2.75, top + 1.15))
    for side in (-1, 1):
        sh.ellipsoid("eye", 0.17, 0.14, 0.2, black, loc=(side * 0.52, -1.9, top + 1.5))
        for y, dk, df in ((-0.1, -0.5, -1.1), (0.5, 0.0, -0.1), (1.1, 0.7, 1.4)):       # front, middle, rear leg
            lw.cord(m, [Vector((side * 0.45, y, top + 1.15)), Vector((side * 1.4, y + dk, top + 1.9)),
                        Vector((side * 2.0, y + df * 0.8, top + 0.12))], thickness=0.13, n=50, smooth_arch=0.0, rounds=2, material=red_ant)
        lw.cord(m, [Vector((side * 0.35, -1.85, top + 1.85)), Vector((side * 0.9, -2.7, top + 2.5)), Vector((side * 1.6, -3.1, top + 2.2))],
                thickness=0.08, n=40, smooth_arch=0.0, rounds=2, material=red_ant)   # antennae
        sh.bar_between("jaw", Vector((side * 0.85, -1.9, top + 1.0)), Vector((side * 0.47, -2.9, top + 1.0)), 0.23, black)   # pincers
        sh.rounded_bar("lip", 0.16, 0.9, 0.85, m.skin, loc=(side * 0.16, -2.9, top + 0.8))   # the two lips drawn up between the jaws
    return dict(el=30, radius=21, target=(0, -0.4, 1.2), az=38)


cam = {"1": scene1, "2": scene2, "3": scene3, "4": scene4, "5": scene5, "6": scene6}[which]()


def update(scene_):
    c.orbit(stage.cam, Vector(cam["target"]), cam["radius"], cam["el"], cam.get("az", 0.0))
    sun = bpy.data.objects.get("toon_sun")
    if sun:
        sun.rotation_euler = (-Vector((-2.0, -5.0, 7.0))).to_track_quat("-Z", "Y").to_euler()


stage.run(update, {**args, "stills": "1"}, 1, f"lace-world-{which}")
