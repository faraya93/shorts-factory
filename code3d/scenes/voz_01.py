"""voz 1 (hook): see productions/mecanalia-es/018*/script.json. The belief staged as a contrast: the skull speaks and clean rings cross to the phone; then the phone hands back a jagged red zigzag at the skull, as if it deformed the voice."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import voz_rig as vr  # noqa: E402
from mathutils import Vector  # noqa: E402

S = sp.Shot(211, floor_z=0.0)
vr.stage_set(S)
spk = vr.load_skull(S)
ph = vr.Phone(S)
rings = vr.Pool(S, 7, "ring")
origin = spk.mouth() + Vector((1.5, 0.0, 0.0))
target = Vector(vr.PHONE) + Vector((-1.0, -0.4, 0.0))
stop = (target - origin).length - 1.0
emits = [0.4 + 0.55 * i for i in range(7)]
t_zig = S.t("celular", default=4.4) - 0.1
zig = vr.zigzag(S, (2.0, -13.0, 15.0), (-12.0, -3.0, 12.0), grow=(t_zig, t_zig + 1.2))


def upd(t):
    spk.pose(t, emits)
    arr = vr.air(rings, t, emits, tuple(origin), tuple(target), 11.0, stop=stop)
    ph.set_bars(t, arr, live=0.8)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 30))
S.cam([(0, (-9.0, -6.0, 12.0), 105, 5, 24), (3.5, (-9.0, -6.0, 12.0), 118, 6, 10), (S.T, (-7.0, -6.0, 12.0), 132, 8, -10)])
S.go()
