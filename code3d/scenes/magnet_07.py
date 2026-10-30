"""imanes scene 7 (cta): the field, the clip it takes, the small magnet it rejects, and the filings it organises."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(356, floor_z=-1.2)
T = SLOT / c.FPS
mats = mr.setup()
Z0 = 6.2
mr.board(mats, Z0 + 0.3)
mag = mr.Magnet("M", mats)
mag.place(0.0, Z0)
fil = mr.Filings(mats, y=0.6)
fil.obj.location = (0.0, 0.0, Z0)
clip = mr.make_clip("clip", mats["steel"], wire=0.1, scale=1.3)
small = mr.Magnet("S", mats, length=2.0)
small.root.scale = (0.8,) * 3
glue = tr.empty("glue_root", (-3.9, -1.0, Z0 + 0.4))
tr.cyl("glue_body", 0.8, 2.2, (0, 0, 0), mats["s"], axis="Z", parent=glue, verts=48, bevel=0.1)
tr.cyl("glue_cap", 0.35, 0.9, (0, 0, 1.45), mats["n"], axis="Z", parent=glue, verts=32, bevel=0.05)
tr.cyl("glue_band", 0.82, 0.5, (0, 0, 0.1), mats["ink"], axis="Z", parent=glue, verts=48, bevel=0.03)


def update(scene_):
    t = scene_.frame_current / c.FPS
    g = mr.pop(glue, t, 0.7) if t < 2.4 else 1e-4
    glue.scale = (g, g, g)
    vis = c.smooth(2.6, 3.2, t)
    u = c.smooth(2.7, 3.7, t)
    if t > 4.85:
        u = 1.0 - c.smooth(4.85, 5.1, t) + c.smooth(5.1, 6.3, t)
        u = min(1.0, max(0.0, u)) if t < 5.1 else c.smooth(5.1, 6.3, t)
    fil.set(u, visible=max(1e-3, vis))
    # atrae (3.8): the clip drifts in from the right and sticks to the S end
    a = c.smooth(3.8, 4.4, t)
    clip.location = (mr.lerp(4.0, 3.1, a), -1.0, Z0 + mr.lerp(2.6, 0.0, a))
    clip.rotation_euler = (0.0, 0.0, mr.lerp(0.5, math.pi / 2, a))
    # rechaza (4.4): a small magnet is brought up to the N end and thrown back
    k = c.smooth(4.3, 4.9, t) - c.smooth(5.0, 5.6, t)
    small.place(mr.lerp(-5.5, -3.7, k), Z0, rot_z=math.pi)
    u2 = c.smooth(0, T, t)
    tr.look(stage, (0.0, 0, Z0 + 0.2), 27.0 + 3.0 * u2, 6.0, -5.0 + 10.0 * u2)

stage.run(update, args, SLOT, "magnet-07")
