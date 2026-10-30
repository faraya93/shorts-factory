"""imanes scene 5 (polos): opposite poles snap together; the same poles push apart."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(276, floor_z=-1.2)
T = SLOT / c.FPS
mats = mr.setup()
A = mr.Magnet("A", mats, thick=1.8); B = mr.Magnet("B", mats, thick=1.8)
for g in (A, B):
    g.root.scale = (0.6,) * 3
AX, Z = -1.5, 0.62
CONTACT = AX + 1.75 * 2 * 0.5 + 1.75 - 0.0   # A right end + half length of B


def update(scene_):
    t = scene_.frame_current / c.FPS
    A.place(AX, Z)
    right_end = AX + 1.5
    near = right_end + 1.5
    x = 2.9
    z = Z
    rot = 0.0
    if t < 1.9:
        x = 2.9
    elif t < 2.9:                                     # opposite poles: accelerate together
        k = (t - 1.9) / 1.0
        x = mr.lerp(2.9, near, k * k)
    elif t < 3.0:
        x = near
    if t >= 3.0 and t < 4.6:                          # lift, flip about the vertical axis, hold apart
        k = c.smooth(3.0, 4.3, t)
        x = mr.lerp(near, 2.9, k)
        z = Z + 1.2 * math.sin(math.pi * k)
        rot = math.pi * k
    elif t >= 4.6:
        rot = math.pi
        if t < 5.0:
            x = 2.9
        elif t < 6.9:                                 # brought close by the same pole: slows against the resistance
            k = c.smooth(5.0, 6.9, t)
            x = mr.lerp(2.9, near + 0.55, k)
        else:                                         # and is thrown back
            k = c.smooth(7.0, 7.9, t)
            x = mr.lerp(near + 0.55, 2.9, k)
    B.place(x, z, rot_z=rot)
    a_kick = 0.0
    if t >= 6.9 and t < 7.9:
        a_kick = -0.45 * math.sin(math.pi * (t - 6.9))
    A.place(AX + a_kick, Z)
    u = c.smooth(0, T, t)
    tr.look(stage, (0.0, 0, 1.9), 18.5 - 0.8 * u, 10.0, -7.0 + 12.0 * u)

stage.run(update, args, SLOT, "magnet-05")
