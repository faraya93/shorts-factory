"""mosca 2 (basura): see productions/mecanalia-es/015*/script.json. The fly walks across a banana peel in front of the trash bag; its feet pick up grime (clean to coated)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
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
PATH = [(0, (-12, -3, 6.2)), (S.T * 0.55, (-1, -3, 6.2)), (S.T, (11, -3, 6.2))]
S.move(F.root, PATH)


def body(t):
    """The walking fly's body centre at time t: the camera follows the whole fly (leg-only macros were never named as a leg by the readers; the coated feet carry the beat)."""
    p = sp.interp(PATH, t)
    return (p[0] + 1.5, p[1], p[2] + 3.0)


def upd(t):
    mr.rub(F, 0.12, phase=t * 9.0)
    mr.feet(F, coat=c.smooth(2.2, tp + 0.6, t))


S.every_frame(upd)
S.cam([(0, (4, 14, 22), 175, 18, -16), (1.8, (2, 4, 12), 60, 12, 20), (ta - 1.0, body(ta - 1.0), 24, 8, 58), (ta + 1.0, body(ta + 1.0), 20, 6, 48), (S.T * 0.85, body(S.T * 0.85), 24, 10, 22), (S.T, (9, -3, 5.0), 34, 12, -22)])
S.go()
