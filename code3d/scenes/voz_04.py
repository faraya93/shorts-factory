"""voz 4 (giro, the turn): see productions/mecanalia-es/018*/script.json. A second skull enters as a listener facing the first, the phone between them. The glow stays inside the speaker; only air rings reach the listener and the phone."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import voz_rig as vr  # noqa: E402
from mathutils import Vector  # noqa: E402

S = sp.Shot(250, floor_z=0.0)
vr.stage_set(S)
spk = vr.load_skull(S)
t_pop = S.t("demás", default=3.2) + 0.1
lis = vr.clone_skull(S, spk, pop=(t_pop, 0.5))
ph = vr.Phone(S, scale=0.62)                                                    # rung 1 (2026-11-10): smaller, so the skulls are what a reader names in the wide frame
ph.set_dot(1.0)
t_air = S.t("aire", default=5.9) - 0.7
bone = vr.Pool(S, 8, "bone", parent=spk.root, minor=0.03)
ear = vr.Pool(S, 3, "ear", parent=spk.root, minor=0.1)
ear_l = vr.Pool(S, 5, "ear", parent=lis.root, minor=0.1)
r_ph = vr.Pool(S, 5, "ring")
r_li = vr.Pool(S, 5, "ring")
b_emits = [0.2 + 0.6 * i for i in range(8)]
e_emits = [0.4, 1.2, 2.0]
a_emits = [t_air + 0.4 * i for i in range(5)]
origin = spk.mouth() + Vector((1.5, 0.0, 0.0))
t_ph = Vector(ph.loc) + Vector((-0.7, -0.3, 0.0))
t_li = lis.mouth() + Vector((-1.0, 0.0, 0.0))
SPEED = 14.0
l_arr = [te + ((t_li - origin).length - 1.0) / SPEED + 0.1 for te in a_emits]


def upd(t):
    spk.glow(sp.interp([(5.0, 1.0), (5.9, 0.0)], t))
    spk.pose(t, b_emits)
    vr.climb(bone, t, b_emits)
    vr.ear_pulse(ear, t, e_emits, side=-1)
    arr = vr.air(r_ph, t, a_emits, tuple(origin), tuple(t_ph), SPEED, stop=(t_ph - origin).length - 1.0)
    vr.air(r_li, t, a_emits, tuple(origin), tuple(t_li), SPEED, stop=(t_li - origin).length - 1.0)
    vr.ear_pulse(ear_l, t, l_arr, side=1, dur=0.9)
    ph.set_bars(t, arr, live=1.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 30))
S.cam([(0, (-18.0, -7.0, 12.0), 55, 2, 10), (2.0, (-17.0, -5.0, 12.0), 72, 5, 14), (3.4, (2.0, -6.0, 10.0), 135, 8, 18), (S.T, (2.0, -6.0, 10.0), 142, 12, 8)])
S.go()
