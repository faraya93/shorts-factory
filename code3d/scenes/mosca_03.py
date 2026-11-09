"""mosca 3 (sensores): see productions/mecanalia-es/015*/script.json. Taste sensors glow on the fly's raised feet; grime covers and darkens them; the fly rubs and they relight (audit rung 2 staging: lit feet, no x-ray)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import mosca_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(340, floor_z=0.0)
mr.counter(S)
mr.plate(S, loc=(0, 0, 0))
F = mr.fly(S, loc=(0.0, -9.0, 2.2), yaw=-1.25)
rk.softboxes(0.7, centre=(0, 0, 30))
tens, tfro = S.t("ensucian", default=4.5), S.t("frota", default=7.5)
mr.rub(F, 1.0, 0.0)
tipA, tipB = mr.tarsus(F, "legA"), mr.tarsus(F, "legB")
mid = tuple((a + b) / 2 for a, b in zip(tipA, tipB))
shA = tuple(F.arm.matrix_world @ F.arm.pose.bones["legA"].head)
leg = tuple(t + 0.45 * (s - t) for t, s in zip(tipA, shA))                    # the middle of one front leg: the macro target (rung 1 re-stage: the leg fills the frame, in profile)


def upd(t):
    mr.rub(F, 1.0, phase=max(0.0, t - tfro) * 14.0)
    coat = c.smooth(tens, tens + 0.8, t) * (1.0 - c.smooth(tfro, tfro + 0.6, t))
    mr.feet(F, coat=coat, glow=c.smooth(0.5, 1.6, t))


S.every_frame(upd)
ctr = (mid[0] - 1.0, mid[1] + 1.0, 6.5)                                         # the whole fly: the feet are lit and coated on a fly the readers can name
S.cam([(0, ctr, 44, 8, 40), (2.2, ctr, 25, 8, 28), (tens, ctr, 23, 10, 18), (tfro, ctr, 22, 8, 8), (S.T, ctr, 60, 14, 30)])
S.go()
