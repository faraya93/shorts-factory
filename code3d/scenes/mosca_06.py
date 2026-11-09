"""mosca 6 (cierre): see productions/mecanalia-es/015*/script.json. The fly takes off from the plate, its route draws back from the plate to the trash bag, and the camera pulls out of the kitchen."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import mosca_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(318, floor_z=0.0)
mr.counter(S)
mr.plate(S, loc=(0, 0, 0))
mr.prop(S, "bread-slice", loc=(0, 0, 0.8), rot=(0, 0, 0.3), k=mr.K * 1.5)
TOP = 0.8 + 2.4
BAG = (110.0, 95.0, 0.0)
mr.prop(S, "trash-bag", loc=BAG, rot=(0, 0, 0.4), k=mr.K * 1.1)
L = (-3.0, -2.0, TOP)
F = mr.fly(S, loc=L, yaw=-1.25)
rk.softboxes(0.7, centre=(40, 40, 30))
tc, te = S.t("catadora", default=3.0), S.t("envíaselo", default=6.5)
S.move(F.root, [(0, L), (tc, L), (tc + 1.2, (L[0] + 4, L[1] + 8, L[2] + 12)), (S.T, (BAG[0] * 0.6, BAG[1] * 0.6, 40))])
S.spin(F.root, [(0, (0, 0, -1.25)), (tc, (0, 0, -1.25)), (S.T, (0, 0, 0.9))])
pts = [(L[0], L[1], 1.2), (30, 25, 1.2), (70, 40, 1.2), (BAG[0] - 18, BAG[1] - 14, 1.2)]
S.line("route", pts, 0.6, S.accent, grow=(tc + 0.8, te + 1.5))


def upd(t):
    a = 1.0 - min(1.0, max(0.0, (t - tc) / 0.8))
    mr.rub(F, 0.8 * a, phase=t * 14.0)


S.every_frame(upd)
S.cam([(0, (-3, -2, TOP + 2), 28, 14, 20), (tc, (-2, -2, TOP + 4), 55, 22, 10), (te, (30, 25, 10), 190, 28, -10), (S.T, (55, 45, 12), 400, 32, -26)])
S.go()
