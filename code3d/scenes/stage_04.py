"""v6-staged scene 4 (the dissolving thread): the laces are chains of glossy black beads that shrink from the top down and float
away as glass bubbles while the boot stays closed. Slot 164 frames (5.47 s). The camera rises and orbits the whole time."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import boot_world as bw  # noqa: E402
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402

args, production, stage, m, SLOT = bw.begin(164)
T, ROWS = SLOT / c.FPS, bw.ROWS
panel = bw.build_boot(m)
fl = bw.Flaps(m)
g = fl.set(0.4, 0.03)
RISE = Vector((0.0, math.sin(bw.PITCH), math.cos(bw.PITCH)))              # world "up" in panel coordinates
beads, bubbles = [], []
for strand, sides in enumerate(([-1, 1, -1, 1, -1], [1, -1, 1, -1, 1])):
    path = [bw.lift(bw.eyelet_at(sd, i, g)) for i, sd in enumerate(sides)]
    pts = []
    for a, b in zip(path, path[1:]):
        n = int((b - a).length / 0.46)
        pts += [a.lerp(b, k / n) for k in range(n)]
    pts.append(path[-1])
    for i, p in enumerate(pts):
        gi = 1.0 - i / len(pts)                                           # 0 at the top (dissolves first), 1 at the bottom
        bead = sh.ellipsoid("bead", 0.27, 0.27, 0.27, m.cord, loc=p, segments=32, rings=16)
        beads.append((bead, gi, p))
        if i % 3 == 0:
            bub = sh.ellipsoid("bubble", 1.0, 1.0, 1.0, m.bubble, loc=(0, 0, -500), segments=32, rings=16)
            bubbles.append((bub, gi, p, i))
bw.adopt(panel)


def update(scene_):
    t = scene_.frame_current / c.FPS
    front = 1.45 * c.smooth(0.3, T - 0.5, t)
    for bead, gi, p in beads:
        s_ = 1.0 - min(1.0, max(0.0, (front - gi) / 0.4))
        s_ = s_ * (1 + 0.22 * math.sin(math.pi * min(1.0, max(0.0, (front - gi) / 0.12))) * (1 if s_ > 0 else 0))   # a small swell before it shrinks
        bead.scale = (s_, s_, s_)
        lw.show(bead, s_ >= 0.08)
    for bub, gi, p, i in bubbles:
        a = min(1.0, max(0.0, (front - gi - 0.12) / 0.75))
        size = (0.35 + 0.35 * ((i * 5) % 7) / 6) * c.smooth(0.0, 0.18, a) * (1 - c.smooth(0.85, 1.0, a))
        bub.scale = (size, size, size)
        drift = Vector((0.9 * math.sin(i + 3 * a), 0.0, 0.0))
        bub.location = (p + RISE * (6.5 * a * (1 + 0.25 * (i % 4))) + drift + Vector((0, 0, 0.6))) if size >= 0.05 else Vector((0, 0, -500))
    p_ = c.smooth(0.0, T, t)
    bw.look(stage, bw.to_world((0, 1.0, 0.3)) + Vector((0, 0, 1.4)), 34.0 - 5.0 * p_, 34 + 12 * p_, -20 + 40 * p_)


stage.run(update, args, SLOT, "stage-04")
