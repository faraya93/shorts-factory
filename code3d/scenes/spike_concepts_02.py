"""SPIKE (concept first, not a production): three cartoon-native concepts for scene 2's beat — a needle passes through BOTH
edges of an open wound and the thread pulls the edges together. Each concept is a bold, simple metaphor with ONE hero
action that must read without narration. One static draft frame each, through the toon pass.

  lace    LACE-UP    two boot flaps with eyelets, a criss-cross lace, a chunky needle skewering the eyelets of both sides
  zipper  ZIPPER     a half-zipped seam: interlocked teeth below, open above, the needle sits where the slider would be
  rip     MEND-RIP   a round cushion with a jagged tear, stitched at the bottom, a giant needle sewing the rest

Run: blender -b --python code3d/scenes/spike_concepts_02.py -- production=<spike dir> concept=lace|zipper|rip mode=draft-full out=<dir>
"""

import colorsys
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import shapes as sh  # noqa: E402
import stage as st  # noqa: E402
import suture as s  # noqa: E402
import toon  # noqa: E402

args = c.parse_args()
production = Path(args["production"])
concept = args["concept"]
stage = st.Stage(production, args.get("mode", "draft-full"))
pal = stage.pal


def dark_steel(hex_color: str, value_factor: float = 0.5) -> str:      # palette steel grey, HSV value x0.5
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, sat, v = colorsys.rgb_to_hsv(r, g, b)
    return "#{:02X}{:02X}{:02X}".format(*(round(255 * x) for x in colorsys.hsv_to_rgb(h, sat, v * value_factor)))


skin = toon.make_material("skin", pal["skin peach"])
shaded = toon.make_material("shaded", pal["shaded skin"])
red = toon.make_material("red", pal["tissue red"])
steel = toon.make_material("steel", pal["steel grey"])
needle_m = toon.make_material("needle_dark", dark_steel(pal["steel grey"]))
cord_m = toon.make_material("cord", "#17171B")


def cord(points, thickness=0.12, n=90):
    t = s.Thread(cord_m, points=n, thickness=thickness)
    t.set([Vector(p) for p in points])
    return t


def arch(p0, p1, lift, steps=14):
    """A straight cord segment with a gentle arch (so it rests above the surface instead of cutting through it)."""
    p0, p1 = Vector(p0), Vector(p1)
    return [p0.lerp(p1, i / steps) + Vector((0, 0, lift * math.sin(math.pi * i / steps))) for i in range(steps + 1)]


def needle_with_eye(p_tail: Vector, p_tip: Vector, r_tail=0.24) -> Vector:
    """A chunky needle plus its EYE: a ring behind the tail with the thread running through it (what makes it a needle)."""
    sh.cone_needle("needle", p_tail, p_tip, r_tail, 0.03, needle_m)
    d = (p_tip - p_tail).normalized()
    eye = p_tail - d * 0.36
    sh.ring("eye", 0.27, 0.085, needle_m, loc=eye)
    return eye


# ------------------------------------------------------------------------------------------------ concept 1: LACE-UP
def lace():
    gap = lambda y: 1.15 + 0.19 * y                                   # the gap narrows toward the bottom (already laced)
    phi = math.atan(0.19 / 2)
    for side in (-1, 1):                                              # the two flaps, tilted to follow the V-shaped gap
        sh.rounded_bar(f"flap_{side}", 1.5, 4.7, 0.35, skin, loc=(side * (0.575 + 1.5), 0, 0), rot=(0, 0, -side * phi))
    sh.rounded_bar("tongue", 0.9, 4.9, 0.2, red, loc=(0, 0, -0.32))
    rows = [-3.4, -1.7, 0.0, 1.7, 3.4]
    eyelet = lambda side, y: Vector((side * (gap(y) / 2 + 0.7), y, 0.4))
    for y in rows:
        for side in (-1, 1):
            sh.ring("eyelet", 0.3, 0.1, steel, loc=eyelet(side, y))
    zl = 0.62                                                          # lace height above the flaps
    lift = lambda v: Vector((v.x, v.y, zl))
    # needle through the eyelets of BOTH flaps on the 4th row (y = 1.7)
    y_n = rows[3]
    p_tail, p_tip = eyelet(-1, y_n) + Vector((-1.5, 0, 0)), eyelet(+1, y_n) + Vector((1.6, 0, 0))
    eye = needle_with_eye(p_tail, p_tip, 0.2)
    # two strands criss-cross up the closed part and feed the needle: A ends at its tail, B at its tip side
    A = [lift(eyelet(-1, rows[0])), lift(eyelet(+1, rows[1])), lift(eyelet(-1, rows[2])), Vector((eye.x, eye.y, zl))]
    B = [lift(eyelet(+1, rows[0])), lift(eyelet(-1, rows[1])), lift(eyelet(+1, rows[2])), lift(eyelet(+1, rows[3])) + Vector((0.9, -0.4, 0))]
    for strand in (A, B):
        pts = []
        for a, b in zip(strand, strand[1:]):
            pts += arch(a, b, 0.07)[:-1]
        cord(pts + [strand[-1]], thickness=0.13, n=120)
    return dict(el=74, radius=19.5, az=0, target=(0, 0.3, 0.2))


# ------------------------------------------------------------------------------------------------- concept 2: ZIPPER
def zipper():
    y_front = 0.3                                                       # the needle ("slider") sits here
    gap = lambda y: 0.12 + max(0.0, y - y_front) * 0.32                 # closed below the slider, a V above it
    ys = [-5.0 + i * 0.5 for i in range(21)]
    for side in (-1, 1):
        edge = [(side * gap(y) / 2, y) for y in ys]
        outer = [(side * 3.3, ys[-1]), (side * 3.3, ys[0])]
        sh.extruded_polygon(f"panel_{side}", edge + outer, 0.6, skin, bevel=0.22)
    open_ys = [y for y in ys if y >= y_front - 0.01]                    # red lining visible only in the open part
    fill = [(-gap(y) / 2 - 0.05, y) for y in open_ys] + [(gap(y) / 2 + 0.05, y) for y in reversed(open_ys)]
    sh.extruded_polygon("lining", fill, 0.4, red, loc=(0, 0, 0.05), bevel=0.04)
    k = 0
    for y in [-4.6 + 0.62 * i for i in range(16)]:                      # teeth: interlocked below, facing each other above
        for side in (-1, 1):
            yy = y + (0.31 if side > 0 else 0.0)
            if yy > 4.7:
                continue
            x = side * (0.17 if yy < y_front else gap(yy) / 2 + 0.2)
            sh.rounded_bar("tooth", 0.27, 0.24, 0.2, steel, loc=(x, yy, 0.72))
            k += 1
    p_tail, p_tip = Vector((-2.4, y_front, 0.95)), Vector((2.6, y_front, 0.95))
    eye = needle_with_eye(p_tail, p_tip, 0.26)                          # the needle IS the slider
    # the thread hangs from the needle's eye like a pull tab
    tab = [eye, eye + Vector((-0.5, -0.8, -0.05)), Vector((-1.4, -1.8, 0.85)), Vector((-1.0, -3.0, 0.8))]
    cord([v for a, b in zip(tab, tab[1:]) for v in arch(a, b, 0.08)[:-1]] + [tab[-1]], thickness=0.15)
    return dict(el=68, radius=21, az=0, target=(0, 0, 0.4))


# --------------------------------------------------------------------------------------------------- concept 3: MEND-RIP
def rip():
    R = 3.7
    ys = [-R + 0.12 + i * (2 * R - 0.24) / 28 for i in range(29)]
    tri = lambda y: abs(((y / 0.75) % 2) - 1) * 2 - 1                    # a jagged triangle wave in [-1, 1]
    zig = lambda y: 0.34 * tri(y)
    g = lambda y: 0.10 + max(0.0, y - 0.2) * 0.36                        # closed (stitched) below, a widening tear above
    w = lambda y: math.sqrt(max(R * R - y * y, 0.0))
    for side in (-1, 1):
        arc = [(side * w(y), y) for y in ys]
        seam = [(zig(y) + side * g(y) / 2, y) for y in reversed(ys)]
        sh.extruded_polygon(f"cushion_{side}", arc + seam, 1.0, shaded, bevel=0.38)
    sh.extruded_polygon("stuffing", [(R * 0.93 * math.cos(a), R * 0.93 * math.sin(a)) for a in [i * math.pi / 18 for i in range(36)]],
                        0.3, red, loc=(0, 0, -0.25), bevel=0.05)
    for i, y in enumerate([-3.0 + 0.52 * j for j in range(6)]):          # stitches across the closed part (whip-stitch)
        sh.rounded_bar("stitch", 0.62, 0.08, 0.09, cord_m, loc=(zig(y), y, 1.1), rot=(0, 0, math.radians(18 if i % 2 else -18)))
    p_tail, p_tip = Vector((-2.3, -0.5, 1.28)), Vector((2.0, 1.0, 1.28))
    eye = needle_with_eye(p_tail, p_tip, 0.26)                          # sewing the next stitch across the open tear
    loop = [eye, Vector((-3.0, -1.2, 1.9)), Vector((-2.7, -2.4, 1.6)), Vector((-1.0, zig(-2.5) - 0.3, 1.25))]
    cord([v for a, b in zip(loop, loop[1:]) for v in arch(a, b, 0.1)[:-1]] + [loop[-1]], thickness=0.14)
    return dict(el=66, radius=19.5, az=0, target=(0, 0, 0.5))


cam = {"lace": lace, "zipper": zipper, "rip": rip}[concept]()


def update(scene_):
    c.orbit(stage.cam, Vector(cam["target"]), cam["radius"], cam["el"], cam["az"])
    sun = bpy.data.objects.get("toon_sun")                              # lighting for readable volume (spike-only)
    if sun:
        sun.rotation_euler = (-Vector((-2.0, -5.0, 7.0))).to_track_quat("-Z", "Y").to_euler()


stage.args_hint = None
stage.run(update, {**args, "stills": "1"}, 1, f"concept-{concept}")
