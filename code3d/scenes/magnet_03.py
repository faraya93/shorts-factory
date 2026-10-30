"""imanes scene 3 (campo-invisible): rings hint at the field, iron filings are scattered and then organise along the field lines."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(290, floor_z=-1.2)
T = SLOT / c.FPS
mats = mr.setup()
Z0 = 6.0
mr.board(mats, Z0 + 0.3)
mag = mr.Magnet("M", mats)
mag.place(0.0, Z0)
fil = mr.Filings(mats, y=0.6)
fil.obj.location = (0.0, 0.0, Z0)
rings = [mr.ring(m, f"ring{i}", 1.0, 1.0, (0.0, 0.0, Z0)) for i in range(3)]


def update(scene_):
    t = scene_.frame_current / c.FPS
    for i, r in enumerate(rings):
        k = (t - (1.5 + 0.45 * i)) / 1.6
        s = 1e-4 if (k < 0 or k > 1) else (1.2 + 3.6 * k)
        r.scale = (s * 1.0, 1.0, s * 0.8)
    vis = c.smooth(4.1, 5.0, t)
    u = c.smooth(6.0, 8.6, t)
    fil.set(u, visible=max(1e-3, vis))
    z = 1.0 - c.smooth(0, T, t)
    tr.look(stage, (0.0, 0, Z0 + 0.4), 27.0 - 1.5 * c.smooth(0, T, t), 6.0, -6.0 + 12.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "magnet-03")
