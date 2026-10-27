"""huincha-de-medir scene 4 (B4 the end hook): macro of the loose hook sliding exactly its own thickness on its slotted rivets; pushed against a wall
(measure inside) and hooked over an edge (measure outside), the zero tick (gold cursor) reads the same. Slot 373 frames (12.43 s)."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(373)
T = SLOT / c.FPS
HT, LB = tr.Hook.HT, 10.0
X0 = HT                                                   # the zero tick / contact plane (absolute x)
blade = tr.Blade(m.blade.copy(), "macro_blade")
hook = tr.Hook(m)
wall = tr.rbox("wall", (8.0, 6.0, 4.2), (X0 + 4.0, 0, -0.9), m.block, bevel=0.15)                # to the right of X0, taller than the lip
obj = tr.rbox("object", (8.0, 5.0, 3.0), (X0 - 4.0, 0, -1.56), m.block, bevel=0.15)              # left of X0, top at z = -0.06
cursor = tr.cyl("zero_cursor", 0.05, 2.5, (X0, 0, 0.32), m.gold, axis="Y", verts=16)
glow = tr.rbox("slot_glow", (0.5, 1.9, 0.04), (-0.8, 0, 0.3), m.gold_dim, bevel=0.01)


def update(scene_):
    t = scene_.frame_current / c.FPS
    ox, slide, lift = 0.0, 0.5, 0.0
    if t < 3.0:                                           # loose: the hook rattles
        slide = 0.5 + 0.5 * math.sin(2 * math.pi * 1.1 * max(0.0, t - 0.4)) * c.smooth(0.3, 0.9, t)
    elif t < 6.0:                                         # it moves exactly its own thickness (slow)
        slide = 0.5 + 0.5 * math.sin(math.pi * (c.smooth(3.2, 5.2, t) - 0.5)) if t < 5.2 else 1.0
        slide = c.smooth(3.2, 5.2, t)
    else:
        slide = 1.0
    if t >= 6.2:                                          # PUSH (inside): the blade comes from the left against the wall
        ox = -1.2 + 1.2 * c.smooth(6.4, 7.5, t)
        slide = min(1.0, max(0.0, -ox / HT))
    if t >= 7.6:                                          # swap: the blade lifts, the wall sinks, the object rises, then PULL (outside)
        w = c.smooth(7.6, 8.4, t)
        lift = 1.5 * math.sin(math.pi * w)
        ox = 0.9 * c.smooth(7.7, 8.3, t) if t < 8.4 else 0.9 - 0.9 * c.smooth(8.5, 9.3, t)
        slide = 0.0 if t < 8.5 else min(1.0, max(0.0, (X0 - ox) / HT)) if ox < X0 else 0.0
    wall.location.z = -0.9 - 5.0 * (1 - c.smooth(6.0, 6.5, t)) - 5.0 * c.smooth(7.7, 8.3, t)
    obj.location.z = -1.56 - 5.0 * (1 - c.smooth(7.9, 8.5, t))
    wall.location.x = X0 + 4.0
    blade.set(LB, None, None, origin=(ox - LB + 0.0 * 1.0, 0, lift))
    hook.place(blade.end_frame, slide)
    cur = c.smooth(6.6, 7.0, t) * 1.0
    cursor.scale = (1.0, 1.0, max(0.001, cur))
    glow.location.z = 0.3 if t > 10.1 else -500
    az = -38 - 14 * c.smooth(0, T, t)
    tr.look(stage, (-0.8, 0, -0.5), 19.0 - 3.0 * c.smooth(2.5, 6.5, t), 22 - 5 * c.smooth(0, T, t), az)


stage.run(update, args, SLOT, "tape-04")
