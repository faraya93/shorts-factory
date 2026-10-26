"""v6-staged scene 3 (tying off): the laced boot's loose cord ends rise and cross into a knot (a small squash on the pull), and a
big glossy black bow pops open on the boot. Slot 133 frames (4.43 s). The camera orbits and pushes in."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import boot_world as bw  # noqa: E402
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = bw.begin(133)
T, ROWS = SLOT / c.FPS, bw.ROWS
panel = bw.build_boot(m)
fl = bw.Flaps(m)
g = fl.set(0.4, 0.03)
KNOT = Vector((0.0, ROWS[-1] + 1.35, 1.15))
paths = [[bw.lift(bw.eyelet_at(sd, i, g)) for i, sd in enumerate(sides)] for sides in ([-1, 1, -1, 1, -1], [1, -1, 1, -1, 1])]
strands = [s.Thread(m.cord, points=170, thickness=0.24) for _ in paths]
stops = [sh.ellipsoid("stopper", 0.5, 0.5, 0.42, m.cord, loc=bw.lift(bw.eyelet_at(sd, 0, g)) + Vector((0, 0, 0.05))) for sd in (-1, 1)]
knot = sh.ellipsoid("knot", 1.0, 1.0, 1.0, m.cord, loc=KNOT)
bow = []
for side in (-1, 1):
    a, b, rot = 1.35, 0.75, math.radians(24) * side
    cx, cy = side * 1.5, KNOT.y + 0.35
    loop = [Vector((cx + a * math.cos(th) * math.cos(rot) - b * math.sin(th) * math.sin(rot),
                    cy + a * math.cos(th) * math.sin(rot) + b * math.sin(th) * math.cos(rot), KNOT.z + 0.2 + 0.15 * math.sin(th)))
            for th in [i * 2 * math.pi / 40 for i in range(41)]]
    tail = lw.chaikin([KNOT + Vector((0, -0.1, -0.1)), Vector((side * 0.6, KNOT.y - 1.3, 1.0)), Vector((side * 1.7, KNOT.y - 2.7, 0.9))], 3)
    bow.append((s.Thread(m.cord, points=150, thickness=0.3), loop, s.Thread(m.cord, points=70, thickness=0.3), tail))
bw.adopt(panel)


def update(scene_):
    t = scene_.frame_current / c.FPS
    end = bw.back((t - 0.1) / 1.0, 1.3)
    for thread, path in zip(strands, paths):                               # the loose ends rise and cross into the knot
        tip = path[-1].lerp(KNOT, min(end, 1.0)) + Vector((0, 0, 0.25 * math.sin(math.pi * min(1.0, end))))
        pts = []
        for a_, b_ in zip(path + [tip], path[1:] + [tip]):
            pts += lw.arch(a_, b_, 0.07)[:-1]
        thread.set(pts + [tip])
    squash = 1 - 0.12 * math.sin(math.pi * c.smooth(0.9, 1.4, t))           # anticipation: the knot squeezes before it pops
    kscale = bw.back((t - 1.0) / 0.7, 2.0) * squash
    knot.scale = (0.5 * kscale, 0.46 * kscale, 0.42 * kscale)
    lw.show(knot, kscale >= 0.02)
    loop_s = bw.back((t - 1.6) / 1.1, 2.4)
    tail_f = c.smooth(2.3, 3.4, t)
    for loop_t, loop, tail_t, tail in bow:
        lw.show(loop_t.obj, loop_s >= 0.03)
        lw.show(tail_t.obj, loop_s >= 0.03)
        loop_t.set([KNOT + (p - KNOT) * max(loop_s, 0.02) for p in loop])
        tail_t.set(tail[:max(2, int(len(tail) * tail_f))])
    fl.set(0.4 - 0.12 * c.smooth(0.2, 1.1, t), 0.03)                         # the pull pinches the flaps a touch more
    p = c.smooth(0.0, T, t)
    bw.look(stage, bw.to_world((0, 1.5, 0.3)) + Vector((0, 0, 0.6)), 34.0 - 6.0 * p, 40 + 4 * p, 18 - 44 * p)


stage.run(update, args, SLOT, "stage-03")
