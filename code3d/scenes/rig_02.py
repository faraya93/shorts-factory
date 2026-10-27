"""v7-drawn scene 2 (the curved needle): a steel needle holder drives the curved needle in through the left lip, under the gap
and out of the right lip, dragging a thread; the thread pulls tight (gold = tension) and the lips slide together to a hairline.
Slot 367 frames (12.23 s). Camera: orbit + push-in the whole time."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import dark_rig as dr  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = dr.begin(367)
T = SLOT / c.FPS
W = dr.Wound(m)
R, CZ, FR = 1.55, 0.0, dr.FRONT
needle, TIP0, ARC = dr.curved_needle(m, R, CZ, 105.0, 150.0)
needle.location = (0, FR, CZ)
holder = sh.rounded_bar("holder", 0.16, 0.16, 0.9, m.steel, loc=(0, 0, 0))          # clamp at the needle tail
holder.parent = needle
thread = dr.glow_thread(m, points=190, thickness=0.05)
LOOSE = Vector((-2.6, FR, 1.4))


def arc_pt(th):
    a = math.radians(th)
    return Vector((R * math.cos(a), FR, CZ + R * math.sin(a)))


def update(scene_):
    f = scene_.frame_current
    t = f / c.FPS
    sweep = c.smooth(1.0, 4.6, t)
    tip = TIP0 + 245.0 * sweep
    needle.rotation_euler.y = -math.radians(tip - TIP0)
    needle.location = (0, FR, CZ)
    holder.location = arc_pt(tip - ARC) - needle.location if False else holder.location
    tail = tip - ARC
    pull = dr.back((t - 6.0) / 2.4, 1.2)                      # tighten: arc path -> shallow taut chord, lips close
    close = min(1.0, pull)
    path = [LOOSE] + ([arc_pt(th) for th in [180.0 + k * (tail - 180.0) / 28 for k in range(29)]] if tail > 180.0 else [arc_pt(tail)])
    if t > 4.6:                                               # needle pulled clear; the thread now runs entry -> under -> exit -> out
        entry, exitp = arc_pt(180.0), arc_pt(360.0)
        ang = [180.0 + 180.0 * k / 24 for k in range(25)]
        under = [Vector((R * math.cos(math.radians(a)) * (1 - 0.45 * close), FR, CZ + R * math.sin(math.radians(a)) * (1 - 0.30 * close))) for a in ang]
        out_end = Vector((2.6, FR, 1.0 - 0.7 * c.smooth(4.6, 6.0, t)))
        path = [LOOSE, entry + Vector((-0.3, 0, 0.2))] + under + [exitp + Vector((0.3, 0, 0.2)), out_end]
        needle.location = (0, FR, CZ + 30.0 * c.smooth(4.6, 5.2, t))
    dr.set_thread(thread, s.resample(path + [path[-1]], 190))
    W.set_gap(1.0 - 0.95 * close)
    p = c.smooth(0.0, T, t)
    dr.look(stage, (0.0, 0, -1.0), 15.5 - 4.0 * p, 10 + 14 * p, -26 + 52 * p)


stage.run(update, args, SLOT, "rig-02")
