"""v4-code3d scene 3 (knots): thread lying across a closed cut ties into small neat knots, one after another.

Run: blender -b --python code3d/scenes/scene_03.py -- production=<dir> mode=draft|final [stills=..] [frames=a-b] [out=..]
Reuses the scene-2 library (skin halves, Thread, stage); new: the knot polyline (suture.knot_polyline).
"""

import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import stage as st  # noqa: E402
import suture as s  # noqa: E402

args = c.parse_args()
SLOT = int(args.get("slot", 133))                      # narration slot: 4.43 s
T = SLOT / c.FPS

stage = st.Stage(Path(args["production"]), args.get("mode", "draft"))
GAP = 0.03                                             # a closed cut: just a groove
s.skin_half(-1, GAP, 2.6, 5.0, stage.skin, stage.tissue)
s.skin_half(+1, GAP, 2.6, 5.0, stage.skin, stage.tissue)
s.wound_floor(GAP + 0.01, 5.0, -0.1, stage.tissue)

KNOTS = [  # (y position, form start, form end, tighten start, tighten end)  seconds
    (-0.40, 0.15, 1.10, 1.10, 1.85),
    (0.45, 1.50, 2.45, 2.45, 3.20),
]
threads = [s.Thread(stage.thread_mat, points=170, thickness=0.036) for _ in KNOTS]
BASE_Z = 0.045


def update(scene_):
    t = scene_.frame_current / c.FPS
    for th, (y, f0, f1, t0, t1) in zip(threads, KNOTS):
        th.set(s.knot_polyline(c.smooth(f0, f1, t), c.smooth(t0, t1, t), Vector((0.0, y, 0.0)), reach=1.15, base_z=BASE_Z))
    k = c.smooth(0.0, T, t)
    c.orbit(stage.cam, Vector((0.0, -0.55 + 1.1 * k, 0.1)), 4.4, 48.0, -8.0 + 14.0 * k)


stage.run(update, args, SLOT, "scene-03")
