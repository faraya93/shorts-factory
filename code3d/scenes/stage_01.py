"""v6-staged scene 1 (the hook): the glossy boot stands unlaced; the flaps squeeze together (anticipation), spring wide open and
settle, and the two loose cords swing from the top eyelets (follow-through). The camera pushes in on the gap and orbits the
whole time. Slot 242 frames (8.07 s)."""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import boot_world as bw  # noqa: E402
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import suture as s  # noqa: E402

args, production, stage, m, SLOT = bw.begin(242)
T = SLOT / c.FPS
panel = bw.build_boot(m)
fl = bw.Flaps(m)
cords = {side: s.Thread(m.cord, points=90, thickness=0.24) for side in (-1, 1)}
bw.adopt(panel)


def update(scene_):
    t = scene_.frame_current / c.FPS
    squeeze = c.smooth(0.0, 0.9, t) * (1 - c.smooth(0.9, 1.0, t))
    spring = bw.back((t - 0.95) / 1.5, 2.4)
    open_ = spring + 0.04 * math.sin(2 * math.pi * 0.35 * t) * c.smooth(2.5, 3.5, t)
    g0 = 0.85 - 0.5 * squeeze + 1.65 * open_
    g = fl.set(g0, 0.05, tilt=math.radians(11) * open_)
    for side in (-1, 1):
        sway = 0.55 * math.sin(2 * math.pi * 0.9 * (t - 1.2) + side) * math.exp(-0.5 * max(0.0, t - 1.2)) * c.smooth(0.9, 1.4, t)
        p0 = bw.lift(bw.eyelet_at(side, 4, g, math.radians(11) * open_))
        pts = [p0, p0 + Vector((side * 0.7, 0.6, 0.3)), p0 + Vector((side * (1.4 + sway), -0.9, 0.0)),
               p0 + Vector((side * (1.5 + 1.4 * sway), -3.0, -0.2))]
        cords[side].set([v for a, b in zip(pts, pts[1:]) for v in lw.arch(a, b, 0.06)[:-1]] + [pts[-1]])
    p = c.smooth(0.0, T, t)
    bw.look(stage, bw.to_world((0, 0.4 * p, 0.2)) + Vector((0, 0, 0.8)), 38.0 - 14.0 * p, 36 + 5 * p, -22 + 36 * p)


stage.run(update, args, SLOT, "stage-01")
