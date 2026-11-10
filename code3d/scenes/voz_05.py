"""voz 5 (cierre): see productions/mecanalia-es/018*/script.json. The reframe as one image: a single wave of air crosses the whole row (speaker, phone, listener) and every receiver lights at once; the camera pulls back and up."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import voz_rig as vr  # noqa: E402
from mathutils import Vector  # noqa: E402

S = sp.Shot(281, floor_z=0.0)
vr.stage_set(S)
spk = vr.load_skull(S)
lis = vr.clone_skull(S, spk)
ph = vr.Phone(S, loc=(3.0, 11.0, 12.0), yaw=math.radians(-38.0), scale=0.55)    # rung 1 (2026-11-10): behind the row, small, so the skulls dominate (centred in front it was named first, 55/80/85)
ph.set_dot(1.0)
t_w = S.t("única", default=2.4) + 0.1
emits = [t_w + 0.5 * i for i in range(9)]
r_ph = vr.Pool(S, 0, "ring")                                                    # rung 1 (2026-11-10): no ring stream to the phone here (the clump of rings read as a key, 55/45/60); its meter still answers each arrival
r_li = vr.Pool(S, 9, "ring", minor=0.14)
ear_l = vr.Pool(S, 9, "ear", parent=lis.root, minor=0.1)
origin = spk.mouth() + Vector((1.5, 0.0, 0.0))
t_ph = Vector(ph.loc) + Vector((-0.7, -0.3, 0.0))
t_li = lis.mouth() + Vector((-1.0, 0.0, 0.0))
SPEED = 14.0
l_arr = [te + ((t_li - origin).length - 1.0) / SPEED + 0.1 for te in emits]


def upd(t):
    spk.pose(t, emits)
    arr = vr.air(r_ph, t, emits, tuple(origin), tuple(t_ph), SPEED, stop=(t_ph - origin).length - 1.0)
    vr.air(r_li, t, emits, tuple(origin), tuple(t_li), SPEED, r0=4.5, grow=0.3, stop=(t_li - origin).length - 1.0)      # one wide wave across the row
    vr.ear_pulse(ear_l, t, l_arr, side=1, dur=0.9)
    ph.set_bars(t, arr, live=1.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 30))
S.cam([(0, (2.0, -6.0, 10.0), 140, 6, 12), (4.0, (2.0, -4.0, 10.0), 158, 12, 22), (S.T, (2.0, -2.0, 14.0), 195, 22, 16)])
S.go()
