"""v4-code3d scene 4 (absorbable): a layered skin cross-section; a thread loop inside the dermis dissolves while the
layers stay whole. The camera travels down through the layers from the top skin to the deepest one.

Run: blender -b --python code3d/scenes/scene_04.py -- production=<dir> mode=draft|final [stills=..] [frames=a-b] [out=..]
Reuses stage, box, Thread; the dissolve is the thread's visible arc length shrinking to nothing.
"""

import math
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import stage as st  # noqa: E402
import suture as s  # noqa: E402

args = c.parse_args()
SLOT = int(args.get("slot", 164))                      # narration slot: 5.47 s
T = SLOT / c.FPS

stage = st.Stage(Path(args["production"]), args.get("mode", "draft"))
W, D, FRONT = 3.4, 2.4, -1.2                           # block width (x), depth (y), cross-section plane (front face y)
dermis = c.principled("dermis", stage.pal["shaded skin"], roughness=0.6, subsurface=0.1)
fascia = c.principled("fascia", stage.pal["steel grey"], roughness=0.55)
LAYERS = [("epidermis", 0.0, -0.28, stage.skin), ("dermis", -0.28, -0.85, dermis),
          ("fascia", -0.85, -1.2, fascia), ("muscle", -1.2, -1.95, stage.tissue)]
for name, z1, z0, mat in LAYERS:
    s.box(name, -W / 2, W / 2, FRONT, FRONT + D, z0, z1, mat, bevel=0.025)

loop = s.Thread(stage.thread_mat, points=90, thickness=0.045)
LOOP_Z, LOOP_R = -0.56, 0.34                           # a suture loop sitting in the dermis, on the cut face


def update(scene_):
    t = scene_.frame_current / c.FPS
    gone = c.smooth(1.0, 4.3, t)                       # 0 intact -> 1 completely dissolved
    visible = 1.0 - gone
    n = max(2, int(64 * visible))
    r = LOOP_R * (0.4 + 0.6 * visible)                 # it also shrinks as it dissolves
    start = 0.6 * math.pi * gone                       # the arc is eaten from one end
    arc = [Vector((r * math.cos(start + 2 * math.pi * visible * i / (n - 1) + 0.5), FRONT - 0.005,
                   LOOP_Z + r * math.sin(start + 2 * math.pi * visible * i / (n - 1) + 0.5))) for i in range(n)]
    loop.obj.hide_render = visible < 0.03
    loop.set(arc)
    k = c.smooth(0.0, T, t)                            # camera: down through the layers
    c.orbit(stage.cam, Vector((0.0, FRONT, 0.0 - 1.5 * k)), 4.6 - 1.0 * k, 8.0, -10.0 + 14.0 * k)


stage.run(update, args, SLOT, "scene-04")
