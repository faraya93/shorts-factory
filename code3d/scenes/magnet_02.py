"""imanes scene 2 (no-todos-los-metales): a magnet sweeps a row; only the steel clip answers (the stainless bar barely tilts)."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(352, floor_z=-1.2)
T = SLOT / c.FPS
mats = mr.setup()
mag = mr.Magnet("M", mats)
mag.root.scale = (0.8,) * 3
clip = mr.make_clip("clip", mats["steel"], wire=0.1, scale=1.5)
can = mr.make_can("can", mats, -1.4, 1.7)
coin = mr.make_coin("coin", mats, 0.6, 1.0)
bar = mr.make_bar("bar", mats, 2.8, 0.35, length=1.8)
CX0 = -3.3
MZ = 4.7


def update(scene_):
    t = scene_.frame_current / c.FPS
    mr.pop(clip, t, 0.3); mr.pop(can, t, 0.6); mr.pop(coin, t, 0.9); mr.pop(bar, t, 1.2)
    # magnet x: parked over the clip, then sweeps right over the can, coin and the stainless bar
    mx = mr.lerp(CX0, 2.8, c.smooth(6.2, 10.4, t)) if t > 6.2 else CX0
    mz = MZ + 0.35 * math.sin(2.0 * t)
    mag.place(mx, mz)
    # clip: leaps up at "aceros" (4.6) and rides under the magnet
    j = c.smooth(4.5, 5.3, t)
    cz = mr.lerp(1.5, mz - 0.56 - 1.5 + 0.2, j)
    clip.location = (mr.lerp(CX0, mx, 1.0 if j >= 1.0 else j), 0.0, cz)
    # stainless bar: leans a little when the magnet is overhead, never lifts
    d = abs(mx - 2.8)
    lean = 0.12 * math.exp(-(d / 1.6) ** 2)
    bar.rotation_euler = (0.0, lean, 0.0)
    u = c.smooth(0, T, t)
    tr.look(stage, (0.0, 0, 3.0), 27.0 - 1.0 * u, 9.0, 6.0 - 12.0 * u)

stage.run(update, args, SLOT, "magnet-02")
