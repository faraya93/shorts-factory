"""v5-drawn scene 4 (the thread dissolving): the lace is a chain of beads that shrink from the top down and float away as outline
bubbles while the flaps stay shut. Slot 164 frames (5.47 s)."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402

args, production, stage, m, SLOT = lw.begin(164)
T, ROWS = SLOT / c.FPS, lw.ROWS
g = lw.gap_fn(0.3, 0.07)
lw.flaps(m, 0.3, 0.07)
lw.eyelets(m, ROWS, g)
beads, bubbles = [], []
for strand in (0, 1):                                                        # the same X lacing, made of beads
    path = [Vector((e.x, e.y, 0.6)) for e in (lw.eyelet((-1 if (i + strand) % 2 == 0 else 1), ROWS[i], g) for i in range(5))]
    pts = []
    for a, b in zip(path, path[1:]):
        L = (b - a).length
        pts += [a.lerp(b, k * 0.28 / L) for k in range(int(L / 0.28))]
    for i, p in enumerate(pts):
        gi = 1.0 - i / len(pts)                                              # 0 at the top (dissolves first), 1 at the bottom
        bead = sh.ellipsoid("bead", 0.2, 0.2, 0.2, m.cord, loc=p, segments=24, rings=12)
        beads.append((bead, gi))
        if i % 3 == 0:
            bubbles.append((sh.ring("bubble", 0.3, 0.055, m.steel, loc=(0, 0, -5)), gi, p, i))


def update(scene_):
    t = scene_.frame_current / c.FPS
    front = 1.45 * c.smooth(0.4, T - 0.4, t)                                 # the dissolving front sweeps from the top down
    for bead, gi in beads:
        s_ = 1.0 - min(1.0, max(0.0, (front - gi) / 0.42))
        bead.scale = (s_, s_, s_)
        bead.hide_render = s_ < 0.1
    for ring, gi, p, i in bubbles:                                           # what dissolved floats up as an outline bubble
        a = min(1.0, max(0.0, (front - gi - 0.17) / 0.7))
        size = c.smooth(0.0, 0.2, a) * (1 - c.smooth(0.8, 1.0, a)) * (0.55 + 0.45 * ((i * 5) % 7) / 6)
        ring.hide_render = size < 0.06
        ring.scale = (size, size, size)
        ring.location = (p.x * 0.5 + 0.5 * math.sin(i), p.y + 0.9 * a * (1 + 0.3 * (i % 4)), 0.9 + 3.0 * a)
    k = c.smooth(0.0, T, t)
    lw.look(stage, (0, 1.2, 1.0), 22.0 - 1.5 * k, 66)


lw.finish(stage, args, SLOT, update, "lace-04")
