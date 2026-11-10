"""voz 3 (hueso): see productions/mecanalia-es/018*/script.json. The camera leaves the phone and goes into the skull: the bone lights up in the accent, rings climb it from the jaw, and a pulse reaches the ear canal directly."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import voz_rig as vr  # noqa: E402

S = sp.Shot(277, floor_z=0.0)
vr.stage_set(S)
spk = vr.load_skull(S)
ph = vr.Phone(S)
ph.set_dot(1.0)
t_v = S.t("vibrar", default=3.6)
t_e = S.t("oído", default=6.7) - 0.1
bone = vr.Pool(S, 6, "bone", parent=spk.root, minor=0.03)
ear = vr.Pool(S, 5, "ear", parent=spk.root, minor=0.1)
b_emits = [t_v + 0.6 * i for i in range(6)]
e_emits = [t_e + 0.5 * i for i in range(5)]


def upd(t):
    spk.glow(sp.interp([(t_v - 0.3, 0.0), (t_v + 0.8, 1.0)], t))
    spk.pose(t, b_emits)
    vr.climb(bone, t, b_emits)
    vr.ear_pulse(ear, t, e_emits, side=-1)
    ph.set_bars(t, [], live=0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 30))
S.cam([(0, (-8.0, -8.0, 10.0), 115, 6, -14), (2.4, (-17.0, -4.0, 12.0), 88, 6, 12), (5.0, (-18.0, -6.0, 12.0), 65, 4, 16), (S.T, (-18.0, -7.0, 12.0), 55, 2, 10)])
S.go()
