"""imanes scene 1 (hook-contraste): magnet, clip and can; the clip jumps to the magnet, the can does not."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(288, floor_z=-1.2)
T = SLOT / c.FPS
mats = mr.setup()
mag = mr.Magnet("M", mats)
mag.root.scale = (0.6,) * 3
clip = mr.make_clip("clip", mats["steel"], wire=0.1, scale=1.3)
can = mr.make_can("can", mats, 2.85, 1.45, r=0.8, h=2.9)
MX0, MZ = -2.0, 0.35


def update(scene_):
    t = scene_.frame_current / c.FPS
    mr.pop(clip, t, 1.15); mr.pop(can, t, 2.3)
    hop = c.smooth(6.3, 7.1, t)
    x = mr.lerp(1.05, 0.08, hop)
    clip.location = (x, 0.0, 1.3 + 0.5 * math.sin(math.pi * hop))
    clip.rotation_euler = (0.0, 0.25 * math.sin(math.pi * hop) , 0.0)
    slide = c.smooth(7.7, 8.8, t)
    mx = MX0 + 1.0 * slide
    mag.place(mx, MZ)
    if hop >= 1.0:
        clip.location = (x + (mx - MX0), 0.0, 1.3)
    can.rotation_euler = (0, 0, 0.0)
    u = c.smooth(0, T, t)
    tr.look(stage, (0.0, 0, 2.3), 19.5 - 0.8 * u, 13.0, -10.0 + 14.0 * u)

stage.run(update, args, SLOT, "magnet-01")
