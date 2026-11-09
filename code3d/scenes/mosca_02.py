"""mosca 2 (basura): see productions/mecanalia-es/015*/script.json. The fly walks across a banana peel in front of the trash bag; its feet pick up dark particles (clean to coated)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import mosca_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(246, floor_z=0.0)
mr.counter(S)
bag = mr.prop(S, "trash-bag", loc=(8, 30, 0), rot=(0, 0, 0.4), k=mr.K * 1.1)
peel = mr.prop(S, "banana", loc=(0, -2, 0), rot=(0, 0, math.pi / 2), k=mr.K * 1.7)
F = mr.fly(S, loc=(-12, -3, 6.2), yaw=0.0)
rk.softboxes(0.7, centre=(0, 0, 30))
tp, ta = S.t("pisa", default=5.0), S.t("almohadillas", default=3.0)
S.move(F.root, [(0, (-12, -3, 6.2)), (S.T * 0.55, (-1, -3, 6.2)), (S.T, (11, -3, 6.2))])
spots = [(-0.6, 0.5), (-0.2, 1.0), (0.2, 1.5), (0.6, 2.0), (1.0, 2.5), (1.4, 3.0)]
spk = []
for i, (u, _) in enumerate(spots):
    for leg in ("legA", "legB"):
        b = S.ball(f"grime_{leg}_{i}", S.hero("g_mark", "#4A2E14", rough=0.9, coat=0.0), 0.34, (0, 0, 0), seg=10)
        t0 = ta + 0.3 * i
        S.size(b, [(0, 1e-4), (t0, 1e-4), (t0 + 0.5, 1.0)])
        spk.append((b, leg, u))


def upd(t):
    mr.rub(F, 0.12, phase=t * 9.0)
    for b, leg, u in spk:
        tip = mr.tarsus(F, leg)
        sh = tuple(F.arm.matrix_world @ F.arm.pose.bones[leg].head)
        d = [(s - p) for s, p in zip(sh, tip)]
        n = math.sqrt(sum(x * x for x in d)) or 1.0
        b.location = tuple(p + x / n * (0.6 + 0.9 * (u + 0.6)) for p, x in zip(tip, d))


S.every_frame(upd)
S.cam([(0, (-11, -3, 5.5), 32, 6, 70), (S.T * 0.5, (-3, -3, 5.0), 24, 9, 32), (ta, (-2, -3, 5.0), 20, 7, 20), (S.T, (9, -3, 5.0), 30, 12, -22)])
S.go()
