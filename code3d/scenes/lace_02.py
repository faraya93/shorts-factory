"""v5-drawn scene 2 (the hero): a chunky needle threaded with the lace folded double slides through the eyelet rings of BOTH flaps,
pulling the lace through; then the lace tightens and the V-shaped gap closes. Slot 367 frames (12.23 s)."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = lw.begin(367)
T, ROWS, HX, HY = SLOT / c.FPS, lw.ROWS, 1.5, 4.7
Y_N, LN = ROWS[3], 6.4                                                      # the needle works on the 4th row; needle length

flap = {side: sh.rounded_bar(f"flap_{side}", HX, HY, 0.35, m.skin) for side in (-1, 1)}
tongue = sh.rounded_bar("tongue", 1.3, HY + 0.55, 0.2, m.red, loc=(0, 0.35, -0.32))
rings = {(side, i): sh.ring("eyelet", 0.3, 0.1, m.steel) for side in (-1, 1) for i in range(5)}
needle = sh.cone_needle("needle", Vector((-LN, 0, 0)), Vector((0, 0, 0)), 0.2, 0.03, m.needle)   # origin at the middle; tip at +LN/2
eye = sh.ring("eye", 0.27, 0.085, m.needle)
lace = [s.Thread(m.cord, points=170, thickness=0.13) for _ in (0, 1)]


def update(scene_):
    t = scene_.frame_current / c.FPS
    close = c.smooth(6.3, 10.0, t)
    g0, k = 1.15 - 0.8 * close, 0.19 - 0.14 * close                         # the V-shaped gap closes as the lace is pulled
    g = lw.gap_fn(g0, k)
    phi = math.atan(k / 2)
    for side in (-1, 1):
        flap[side].location = (side * (g0 / 2 + HX), 0, 0)
        flap[side].rotation_euler.z = -side * phi
        for i, y in enumerate(ROWS):
            rings[(side, i)].location = lw.eyelet(side, y, g)
    tongue.scale.x = ((g0 + abs(k) * HY) / 2 + 0.05) / 1.3

    tip_x = -2.6 + 12.2 * c.smooth(1.0, 6.3, t)                             # the needle slides right through BOTH rings
    needle.location = (tip_x - LN / 2, Y_N, 0.4)
    eye_p = Vector((tip_x - LN - 0.36, Y_N, 0.4))
    eye.location = eye_p
    lift = lambda v, z=0.62: Vector((v.x, v.y, z))
    e = lambda side, i: lw.eyelet(side, ROWS[i], g)
    ring_l, ring_r, E = e(-1, 3), e(1, 3), Vector((eye_p.x, Y_N, 0.5))
    if E.x < ring_l.x - 0.35:
        tail = [E]                                                          # the doubled lace still ends in the eye
    elif E.x < ring_r.x - 0.35:
        tail = [lift(ring_l), E]                                            # ... now through the left ring
    else:
        tail = [lift(ring_l), lift(ring_r), E]                              # ... and through the right ring too
    slack = 0.35 * (1 - c.smooth(6.3, 9.0, t))
    for thread, base in zip(lace, ([lift(e(-1, 0)), lift(e(1, 1)), lift(e(-1, 2))], [lift(e(1, 0)), lift(e(-1, 1)), lift(e(1, 2))])):
        pts, path = [], base + tail
        for a, b in zip(path, path[1:]):
            pts += lw.arch(a, b, 0.07 + slack)[:-1]
        thread.set(pts + [path[-1]])
    lw.look(stage, (0, 0.3, 0.2), 19.5, 74)


lw.finish(stage, args, SLOT, update, "lace-02")
