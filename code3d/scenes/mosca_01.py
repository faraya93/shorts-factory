"""mosca 1 (hook): see productions/mecanalia-es/015*/script.json. A fly on the rim of a plate lifts its front legs and rubs them; on 'viene' the camera whips out of the kitchen."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import mosca_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(256, floor_z=0.0)
mr.counter(S)
mr.plate(S, loc=(0, 0, 0))
F = mr.fly(S, loc=(0.0, -12.0, 2.2), yaw=-1.25)
rk.softboxes(0.7, centre=(0, 0, 30))
tl, tv = S.t("lavan", default=3.0), S.t("viene", default=7.0)


def upd(t):
    a = c.smooth(0.5, 1.4, t)
    mr.rub(F, a, phase=max(0.0, t - 0.8) * 14.0)


S.every_frame(upd)
S.cam([(0, (-2, -12, 7.0), 26, 6, 28), (tl, (-1, -12, 7.0), 21, 12, 8), (tv, (0, -6, 6.0), 70, 20, -10), (S.T, (0, 20, 20), 330, 24, -30)])
S.go()
