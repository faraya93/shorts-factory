"""inodoro scene 1 (hook): the cutaway toilet; a waste form pops in on "caca"; the siphon is marked on "sifón"."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import toilet_rig as tl  # noqa: E402

args, production, stage, m, SLOT = tr.begin(199, floor_z=-1.2)
tl.cpu_draft(stage, args)
T = SLOT / c.FPS
K = tl.Toilet()
ring1 = tl.ring(m, "siphon_ring", (-1.3, -1.0, 3.6), 1e-4, 1e-4)


def update(scene_):
    t = scene_.frame_current / c.FPS
    K.state()
    s = tr.back((t - 0.7) / 0.4) if t > 0.7 else 1e-4
    K.put_waste(0, 3.7, 4.55 + 0.08 * math.sin(2.0 * t), s=s)
    K.put_waste(1, 4.7, 4.52 + 0.06 * math.sin(2.4 * t + 1.0), s=s)
    k = tr.back((t - 4.7) / 0.5) if t > 4.7 else 0.0
    ring1.scale = (max(1e-4, 2.6 * k), 1.0, max(1e-4, 3.9 * k))
    u = c.smooth(0, T, t)
    p = c.smooth(3.6, 6.2, t)
    tr.look(stage, (0.8 - 1.6 * p, 0, 7.4 - 2.8 * p), 36.0 - 13.0 * p, 6.0, -8.0 + 10.0 * u)

stage.run(update, args, SLOT, "toilet-01")
