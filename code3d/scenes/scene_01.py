"""v4-code3d scene 1 (hook): a smooth forearm opens into a clean gap; the camera starts wide and travels toward the cut.

Run: blender -b --python code3d/scenes/scene_01.py -- production=<dir> mode=draft|final [stills=..] [frames=a-b] [out=..]
New library object: body.Forearm (slit tube). Everything else comes from the shared stage.
"""

import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import body  # noqa: E402
import common as c  # noqa: E402
import stage as st  # noqa: E402

args = c.parse_args()
SLOT = int(args.get("slot", 242))                      # narration slot: 8.07 s
T = SLOT / c.FPS

stage = st.Stage(Path(args["production"]), args.get("mode", "draft"))
arm = body.Forearm(stage)


def update(scene_):
    t = scene_.frame_current / c.FPS
    arm.rebuild(0.0 + 55.0 * c.smooth(1.4, 6.0, t))    # intact skin, then the slit opens
    k = c.smooth(0.3, T - 0.3, t)                      # camera: wide on the whole arm -> close on the cut
    c.orbit(stage.cam, Vector((0.0, -1.2 + 1.5 * k, 0.1)), 12.0 - 6.0 * k, 62.0 - 6.0 * k, -6.0 + 10.0 * k)


stage.run(update, args, SLOT, "scene-01")
