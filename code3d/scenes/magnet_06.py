"""imanes scene 6 (cortar-un-iman): a blade cuts the bar in half; the halves part, then both turn out to carry two poles."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(262, floor_z=-1.2)
T = SLOT / c.FPS
mats = mr.setup()
mag = mr.Magnet("M", mats, thick=1.8)
mag.root.scale = (0.75,) * 3
blade = tr.rbox("cutter", (0.14, 1.9, 3.4), (0.0, 0.0, 6.0), mats["ink"], bevel=0.04)
Z = 0.78
state = {"cut": None}


def update(scene_):
    t = scene_.frame_current / c.FPS
    d = c.smooth(1.2, 1.9, t) - c.smooth(2.0, 2.7, t)
    blade.location = (0.0, 0.0, mr.lerp(6.0, 1.0, d))
    bs = 1.0 if t < 2.8 else 1e-4
    blade.scale = (bs, bs, bs)
    gap = 1.6 * c.smooth(2.3, 3.4, t)
    mag.split(gap)
    cut = t >= 3.9
    mag.set_halves_cut(cut)
    pulse = 1.0 + 0.25 * math.sin(math.pi * (t - 3.9) / 0.5) if 3.9 <= t < 4.4 else 1.0
    mag.blocks[1].scale = mag.blocks[2].scale = (1.0, pulse, pulse)
    mag.place(0.0, Z)
    u = c.smooth(0, T, t)
    tr.look(stage, (0.0, 0, 1.9), 16.0 - 1.0 * u, 10.0, -6.0 + 12.0 * u)

stage.run(update, args, SLOT, "magnet-06")
