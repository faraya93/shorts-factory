"""v5-drawn scene 3 (tying off): the criss-cross lace runs to the top, the strands knot, and a bold bow pops open. Slot 133 frames (4.43 s)."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = lw.begin(133)
T, ROWS = SLOT / c.FPS, lw.ROWS
g = lw.gap_fn(0.3, 0.07)
lw.flaps(m, 0.3, 0.07)
lw.eyelets(m, ROWS, g)
KNOT = Vector((0.0, ROWS[-1] + 1.2, 0.78))
zl = 0.62
lift = lambda v: Vector((v.x, v.y, zl))
paths = [[lift(lw.eyelet(-1 if i % 2 == 0 else 1, ROWS[i], g)) for i in range(5)],
         [lift(lw.eyelet(1 if i % 2 == 0 else -1, ROWS[i], g)) for i in range(5)]]
strands = [s.Thread(m.cord, points=150, thickness=0.13) for _ in paths]
knot = sh.ellipsoid("knot", 1.0, 1.0, 1.0, m.cord, loc=KNOT)
bow = []
for side in (-1, 1):
    a, b, rot = 1.05, 0.55, math.radians(24) * side
    cx, cy = side * 1.15, KNOT.y + 0.28
    loop = [Vector((cx + a * math.cos(th) * math.cos(rot) - b * math.sin(th) * math.sin(rot),
                    cy + a * math.cos(th) * math.sin(rot) + b * math.sin(th) * math.cos(rot), 0.95 + 0.12 * math.sin(th)))
            for th in [i * 2 * math.pi / 40 for i in range(41)]]
    tail = lw.chaikin([KNOT + Vector((0, -0.1, -0.1)), Vector((side * 0.45, KNOT.y - 1.0, 0.8)), Vector((side * 1.35, KNOT.y - 2.1, 0.7))], 3)
    bow.append((s.Thread(m.cord, points=150, thickness=0.17), loop, s.Thread(m.cord, points=70, thickness=0.17), tail))


def update(scene_):
    t = scene_.frame_current / c.FPS
    end = c.smooth(0.2, 1.2, t)
    for thread, path in zip(strands, paths):                                # the strands run up and into the knot
        pts = []
        for a, b in zip(path + [path[-1].lerp(KNOT, end)], path[1:] + [path[-1].lerp(KNOT, end)]):
            pts += lw.arch(a, b, 0.07)[:-1]
        thread.set(pts + [path[-1].lerp(KNOT, end)])
    kscale = lw.pop((t - 1.0) / 0.9)
    knot.scale = (0.36 * kscale, 0.34 * kscale, 0.3 * kscale)
    lw.show(knot, kscale >= 0.02)
    loop_s = lw.pop((t - 1.7) / 1.4)
    tail_f = c.smooth(2.5, 3.6, t)
    for loop_t, loop, tail_t, tail in bow:
        lw.show(loop_t.obj, loop_s >= 0.03)
        lw.show(tail_t.obj, loop_s >= 0.03)
        loop_t.set([KNOT + (p - KNOT) * max(loop_s, 0.02) for p in loop])
        tail_t.set(tail[:max(2, int(len(tail) * tail_f))])
    k = c.smooth(0.0, T, t)
    lw.look(stage, (0, 0.6, 0.2), 22.0 - 2.0 * k, 74)


lw.finish(stage, args, SLOT, update, "lace-03")
