"""The lace-up graphic system (runs inside Blender): the shared parts of the owner-picked concept, so every scene is built from
the same bold vocabulary: two skin flaps with eyelets, a red tongue in the gap, thick black lace, a chunky dark-steel needle
with an eye. Toon materials only (exact palette hexes); the toon pass supplies cel bands and outlines."""

import colorsys
import math
from types import SimpleNamespace

from mathutils import Vector

import shapes as sh
import suture as s
import toon


def dark_steel(hex_color: str, value_factor: float = 0.5) -> str:      # palette steel grey, HSV value x0.5
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, sat, v = colorsys.rgb_to_hsv(r, g, b)
    return "#{:02X}{:02X}{:02X}".format(*(round(255 * x) for x in colorsys.hsv_to_rgb(h, sat, v * value_factor)))


def materials(pal: dict) -> SimpleNamespace:
    return SimpleNamespace(skin=toon.make_material("skin", pal["skin peach"]),
                           shaded=toon.make_material("shaded", pal["shaded skin"]),
                           red=toon.make_material("red", pal["tissue red"]),
                           steel=toon.make_material("steel", pal["steel grey"]),
                           needle=toon.make_material("needle_dark", dark_steel(pal["steel grey"])),
                           cord=toon.make_material("cord", "#17171B"))


def gap_fn(g0: float, k: float):
    return lambda y: g0 + k * y


def flaps(m, g0: float, k: float = 0.0, hx: float = 1.5, hy: float = 4.7, hz: float = 0.35, tongue: bool = True) -> None:
    """Two rounded flaps tilted to follow the gap (gap(y) = g0 + k*y), and the red tongue showing in it."""
    phi = math.atan(k / 2)
    for side in (-1, 1):
        sh.rounded_bar(f"flap_{side}", hx, hy, hz, m.skin, loc=(side * (g0 / 2 + hx), 0, 0), rot=(0, 0, -side * phi))
    if tongue:
        # the boot's tongue: red in the gap, peeking out above the flaps (the cue that this is a boot, not a gift box)
        sh.rounded_bar("tongue", (g0 + abs(k) * hy) / 2 + 0.05, hy + 0.55, 0.2, m.red, loc=(0, 0.35, -0.32))


def eyelet(side: int, y: float, g, z: float = 0.4) -> Vector:
    return Vector((side * (g(y) / 2 + 0.7), y, z))


def eyelets(m, rows, g) -> None:
    for y in rows:
        for side in (-1, 1):
            sh.ring("eyelet", 0.3, 0.1, m.steel, loc=eyelet(side, y, g))


def needle_with_eye(m, p_tail: Vector, p_tip: Vector, r_tail: float = 0.22) -> Vector:
    """A chunky needle plus its EYE (a ring behind the tail): what makes it read as a needle. Returns the eye's centre."""
    sh.cone_needle("needle", p_tail, p_tip, r_tail, 0.03, m.needle)
    eye = p_tail - (p_tip - p_tail).normalized() * 0.36
    sh.ring("eye", 0.27, 0.085, m.needle, loc=eye)
    return eye


def arch(p0, p1, lift: float = 0.07, steps: int = 14) -> list:
    p0, p1 = Vector(p0), Vector(p1)
    return [p0.lerp(p1, i / steps) + Vector((0, 0, lift * math.sin(math.pi * i / steps))) for i in range(steps + 1)]


def chaikin(points, rounds: int = 2) -> list:
    """Corner-cutting smoothing: keeps the end points, rounds every bend (cartoon-round cords)."""
    pts = [Vector(p) for p in points]
    for _ in range(rounds):
        out = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            out += [a.lerp(b, 0.25), a.lerp(b, 0.75)]
        pts = out + [pts[-1]]
    return pts


def cord(m, points, thickness: float = 0.13, n: int = 120, smooth_arch: float = 0.07, rounds: int = 0, material=None):
    if rounds:
        points = chaikin(points, rounds)
    pts = []
    for a, b in zip(points, points[1:]):
        pts += arch(a, b, smooth_arch)[:-1]
    t = s.Thread(material or m.cord, points=n, thickness=thickness)
    t.set(pts + [Vector(points[-1])])
    return t


def x_lacing(m, rows, g, upto: int, end_a: Vector, end_b: Vector, zl: float = 0.62, thickness: float = 0.13) -> None:
    """Criss-cross lace from the bottom row up to row `upto`; the two strands finish at end_a / end_b."""
    lift = lambda v: Vector((v.x, v.y, zl))
    A = [lift(eyelet(-1 if i % 2 == 0 else 1, rows[i], g)) for i in range(upto + 1)]
    B = [lift(eyelet(1 if i % 2 == 0 else -1, rows[i], g)) for i in range(upto + 1)]
    cord(m, A + [end_a], thickness)
    cord(m, B + [end_b], thickness)


# ---------------------------------------------------------------------------- animation helpers (v5 production)
import sys as _sys
from pathlib import Path as _Path

import bpy as _bpy

_sys.path.insert(0, str(_Path(__file__).resolve().parent))
import common as _c  # noqa: E402
import stage as _st  # noqa: E402

SUN_FROM = Vector((-2.0, -5.0, 7.0))
ROWS = [-3.4, -1.7, 0.0, 1.7, 3.4]


def begin(default_slot: int):
    """Common start of a lace scene script: returns (args, production, stage, materials, slot_frames)."""
    args = _c.parse_args()
    production = _Path(args["production"])
    stage = _st.Stage(production, args.get("mode", "draft"))
    return args, production, stage, materials(stage.pal), int(args.get("slot", default_slot))


def finish(stage, args, slot: int, update, name: str) -> None:
    def wrapped(scene_):
        update(scene_)
        sun = _bpy.data.objects.get("toon_sun")
        if sun:
            sun.rotation_euler = (-SUN_FROM).to_track_quat("-Z", "Y").to_euler()
    stage.run(wrapped, args, slot, name)


def look(stage, target, radius: float, el: float, az: float = 0.0) -> None:
    _c.orbit(stage.cam, Vector(target), radius, el, az)


def pop(k: float) -> float:
    """0 -> 1 with a small overshoot (a cartoon 'pop'); k in 0..1."""
    k = min(1.0, max(0.0, k))
    return k * k * (3 - 2 * k) * (1 + 0.16 * math.sin(math.pi * k))


def empty(name: str, loc=(0, 0, 0)):
    obj = _bpy.data.objects.new(name, None)
    obj.location = loc
    _bpy.context.scene.collection.objects.link(obj)
    return obj


def parent(child, root, loc=None) -> None:
    child.parent = root
    if loc is not None:
        child.location = loc
