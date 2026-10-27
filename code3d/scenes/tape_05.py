"""huincha-de-medir scene 5 (B5 the motor): exploded housing. The flat spiral spring (gold) winds as the blade is pulled out and recoils on release;
the brake pad only presses the blade. Slot 432 frames (14.4 s)."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(432)
T = SLOT / c.FPS
A = tr.Tape(m, loc=(0, 0, 0), name="tape")
tr.table(m, x0=-6.0, x1=3.0)
spring_mat = m.spring.node_tree.nodes["Principled BSDF"]


def update(scene_):
    t = scene_.frame_current / c.FPS
    explode = c.smooth(0.2, 1.7, t)
    A.front_group.location = (-7.0 * explode, -2.5 * explode, 7.0 * explode)
    A.front_group.rotation_euler = (math.radians(-25) * explode, math.radians(15) * explode, math.radians(20) * explode)
    cassette = c.smooth(1.2, 2.4, t)
    A.spring_group.location.y = -1.9 * cassette
    # blade pulled (3.5-6.3), held, released and recoiling (7.3-9.4), pulled again (9.5-10.5), braked (11.0-13.4)
    d = 7.0 * c.smooth(3.5, 6.3, t)
    if t >= 7.3:
        d = 7.0 * (1 - tr.ease_out((t - 7.3) / 1.4))
    if t >= 9.5:
        d = 5.0 * c.smooth(9.5, 10.5, t)
    brake = c.smooth(11.0, 11.6, t) * (1 - c.smooth(13.4, 14.0, t))
    if t >= 13.4:
        d = 5.0 * (1 - tr.ease_out((t - 13.4) / 0.9))
    R = A.set_coil(d)
    A.spring_group.location.z = tr.MOUTH_Z + R
    tension = min(1.0, d / 7.0)
    A.spring_rebuild(twist_amount=-2 * math.pi * 1.3 * tension, scale=1.0)
    spring_mat.inputs["Emission Strength"].default_value = 0.5 + 3.2 * tension
    A.spring_group.rotation_euler.y = 0.0
    A.pad_pivot.location.z = tr.MOUTH_Z + 0.12 + 0.55 * (1 - brake) * 1.0 - 0.0
    A.place_blade(d, theta=None, cs=lambda s: 1.0)
    p = c.smooth(0, T, t)
    tr.look(stage, (0.5 - 1.5 * p, 0, -0.3), 21 - 4 * p, 9 + 6 * p, -14 + 30 * p)


stage.run(update, args, SLOT, "tape-05")
