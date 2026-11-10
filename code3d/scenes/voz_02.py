"""voz 2 (aire): see productions/mecanalia-es/018*/script.json. The zigzag unspools; the same clean rings leave the mouth, cross the air and reach the phone, whose screen wakes (record dot and level bars)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import voz_rig as vr  # noqa: E402
from mathutils import Vector  # noqa: E402

S = sp.Shot(279, floor_z=0.0)
vr.stage_set(S)
spk = vr.load_skull(S)
ph = vr.Phone(S)
rings = vr.Pool(S, 9, "ring")
origin = spk.mouth() + Vector((1.5, 0.0, 0.0))
target = Vector(vr.PHONE) + Vector((-1.0, -0.4, 0.0))
stop = (target - origin).length - 1.0
t0 = S.t("sonido", default=2.6) + 0.1
emits = [t0 + 0.55 * i for i in range(9)]
zig = vr.zigzag(S, (2.0, -13.0, 15.0), (-12.0, -3.0, 12.0))


def upd(t):
    vr.unspool(zig, (t - 0.4) / 1.0)
    spk.pose(t, emits)
    arr = vr.air(rings, t, emits, tuple(origin), tuple(target), 11.0, stop=stop)
    ph.set_dot((t - arr[0]) / 0.3)
    ph.set_bars(t, arr, live=1.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 30))
S.cam([(0, (2.0, -10.0, 12.0), 68, 5, 16), (2.6, (-8.0, -4.0, 9.0), 85, 5, 8), (5.0, (-4.0, -9.0, 11.0), 85, 6, 14), (7.0, (4.0, -13.0, 12.0), 58, 5, -8), (S.T, (5.0, -13.0, 12.0), 50, 4, -26)])
S.go()
