"""v7-drawn scene 4 (absorbable thread): inside the cutaway a pale thread (a chain of beads) sits in the wound among small
yellow-green cells; the thread breaks into particles from the middle and vanishes; tweezers come toward the empty path and
withdraw. Slot 164 frames (5.47 s)."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import dark_rig as dr  # noqa: E402
import shapes as sh  # noqa: E402

args, production, stage, m, SLOT = dr.begin(164)
T = SLOT / c.FPS
W = dr.Wound(m)
W.set_gap(1.0)
FR = dr.FRONT
N = 26
beads = [sh.ellipsoid("bead", 0.11, 0.11, 0.11, m.thread, loc=(0.0, FR + 0.05, -0.15 - 1.0 * i / (N - 1)), segments=16, rings=8) for i in range(N)]
cells = []
for i in range(34):
    ang = i * 2.399
    cells.append((sh.ellipsoid("cell", 0.07, 0.07, 0.07, m.cells, loc=(0, FR, -0.6), segments=12, rings=6), ang, 0.55 + 0.35 * ((i * 7) % 5) / 4, -0.2 - 0.95 * ((i * 3) % N) / N))
tw_root, tw_piv = dr.tweezers(m)


def update(scene_):
    t = scene_.frame_current / c.FPS
    front = 1.2 * c.smooth(1.4, 3.6, t)                          # the dissolve front spreads from the middle outwards
    for i, b in enumerate(beads):
        d = abs(i - (N - 1) / 2) / ((N - 1) / 2)
        sc = 1.0 - min(1.0, max(0.0, (front - d * 0.9) / 0.3))
        b.scale = (sc, sc, sc)
        dr.show(b, sc > 0.08)
    gather = c.smooth(0.2, 1.8, t)
    for cell, ang, rad, z in cells:
        r = (rad * 1.3) * (1 - gather) + 0.28 * gather
        cell.location = (math.cos(ang + 2.0 * t) * r * 0.9, FR + 0.02, z + 0.04 * math.sin(3 * t + ang))
    tw_root.location = (1.8 - 1.1 * c.smooth(3.4, 4.4, t) + 1.0 * c.smooth(4.4, 5.2, t), FR - 0.1, -1.1 + 0.2 * c.smooth(3.4, 4.4, t))
    for pivot, sign in tw_piv:
        pivot.rotation_euler.y = sign * 0.10
    k = c.smooth(0.0, T, t)
    dr.look(stage, (0.0, 0, -0.8), 14.0 - 4.5 * k, 9 + 6 * k, 10 - 22 * k)


stage.run(update, args, SLOT, "rig-04")
