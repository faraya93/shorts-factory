"""v7-drawn scene 1 (hook = CONTRAST + the gap): two identical wound blocks on the dark stage. A straight needle and the curved
needle try to pass through both lips; the straight one tears out through the base (red), the curved one arcs under the wound
and exits the far lip trailing a gold thread. The camera pushes into the right block; the lips then spring toward each other
and fall back (they cannot close alone). Slot 268 frames (8.93 s)."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import dark_rig as dr  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = dr.begin(268)
T = SLOT / c.FPS
AX, BX = -2.15, 2.15
A, B = dr.Wound(m, (AX, 0, 0)), dr.Wound(m, (BX, 0, 0))

# straight needle over block A's left half (entry x = -1.0 from A's centre), tip pointing down
needle_s = dr.straight_needle(m)
tear = sh.rounded_bar("tear", 0.07, 0.03, 0.5, m.red, loc=(0, 0, 0))
# curved needle on block B, circle centre at B's surface centre, drawn in front of the cut face
R, CZ = 1.55, 0.0
needle_c, TIP0, ARC = dr.curved_needle(m, R, CZ, 105.0, 150.0)
needle_c.location = (BX, dr.FRONT, CZ)
thread = dr.glow_thread(m, points=170)
LOOSE = Vector((BX - 2.1, dr.FRONT, 1.0))


def arc_pt(theta_deg):
    a = math.radians(theta_deg)
    return Vector((BX + R * math.cos(a), dr.FRONT, CZ + R * math.sin(a)))


def update(scene_):
    f = scene_.frame_current
    t = f / c.FPS
    # --- straight needle: hover, plunge straight down through the left half, jam out through the base
    drop = c.smooth(0.7, 1.7, t)
    tip_z = 2.3 - 7.0 * drop                         # from above the surface to below the block (base at z = -3.9)
    sx = AX - 1.0
    needle_s.location = (sx, dr.FRONT, tip_z)
    tear_len = max(0.001, min(3.9, 0.3 - tip_z))
    tear.scale = (1, 1, tear_len / 0.5 * 0.5)
    tear.location = (sx + 0.02, dr.FRONT - 0.03, -tear_len / 2 + 0.0)
    dr.show(tear, tip_z < 0.0)
    # --- curved needle: swings along its arc under the wound and out of the right lip
    sweep = c.smooth(0.9, 2.6, t)
    tip = TIP0 + 245.0 * sweep
    needle_c.rotation_euler.y = -math.radians(tip - TIP0)
    tail = tip - ARC
    path = [LOOSE]
    if tail > 180.0:
        path += [arc_pt(th) for th in [180.0 + k * (tail - 180.0) / 24 for k in range(25)]]
    else:
        path += [arc_pt(tail)]
    dr.set_thread(thread, s.resample(path + [path[-1]], 170))
    # --- the lips of block B: at rest, then they try to close and fall back ("no cierran solos")
    g = 1.0 - 0.55 * math.sin(math.pi * c.smooth(6.9, 7.9, t)) * (1 if t > 6.9 else 0)
    A.set_gap(1.0)
    B.set_gap(g)
    # --- camera: wide on both blocks, then a push-in on block B, with a slow orbit
    p = c.smooth(2.4, 5.0, t)
    drift = c.smooth(0.0, T, t)
    tx = BX * p
    dr.look(stage, (tx, 0, -1.4), 25.0 - 12.5 * p - 0.8 * drift, 11 + 4 * drift, -6 + 10 * drift)
    stage.track("blockA", (AX, dr.FRONT, -1.4), f)
    stage.track("blockB", (BX, dr.FRONT, -1.4), f)
    stage.track("woundB", (BX, dr.FRONT, -0.4), f)
    stage.track("straight_tip", (sx, dr.FRONT, tip_z), f)
    stage.track("lipsB", (BX, dr.FRONT, 0.0), f)


stage.run(update, args, SLOT, "rig-01")
