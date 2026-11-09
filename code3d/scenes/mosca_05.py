"""mosca 5 (giro): see productions/mecanalia-es/015*/script.json. The mouth sucks up the melted patch (it shrinks under the bobbing head; audit rung 2, the built labellum read badly in draft), then the camera drops to the feet and the trash particles sit on the bread."""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import mosca_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(300, floor_z=0.0)
mr.counter(S)
mr.plate(S, loc=(0, 0, 0))
mr.prop(S, "bread-slice", loc=(0, 0, 0.8), rot=(0, 0, 0.3), k=mr.K * 1.5)
TOP = 0.8 + 2.4
L = (-3.0, -2.0, TOP)
F = mr.fly(S, loc=L, yaw=-1.25)
rk.softboxes(0.7, centre=(0, 0, 30))
ts, tp = S.t("sorbe", default=0.6), S.t("patas", default=6.5)
bpy.context.view_layer.update()
m = mr.mouth(F)
wet = S.ball("wet_patch", S.hero("rubber_k", "#8A6A43", rough=0.12, coat=0.9), 1.0, (m[0], m[1], TOP + 0.05), shape=(1.5, 1.2, 0.12), seg=20)
S.size(wet, [(0, 1.0), (ts + 0.3, 1.0), (tp - 1.0, 1e-4)])
S.move(F.root, [(0, L), (ts, L), (ts + 0.3, (L[0], L[1], L[2] - 0.4)), (ts + 0.8, (L[0], L[1], L[2] - 0.1)), (ts + 1.3, (L[0], L[1], L[2] - 0.4)), (ts + 1.8, (L[0], L[1], L[2] - 0.1)),
                  (ts + 2.3, (L[0], L[1], L[2] - 0.4)), (tp - 1.0, (L[0], L[1], L[2] - 0.1)), (S.T, L)])
for i in range(10):
    b = S.ball(f"grime_{i}", S.hero("g_mark", "#4A2E14", rough=0.9, coat=0.0), 0.22, (m[0] + 2.2 * math.cos(i * 1.3), m[1] + 1.8 * math.sin(i * 1.3), TOP + 0.15), seg=14)
    S.size(b, [(0, 1e-4), (tp + 0.1 * i, 1e-4), (tp + 0.1 * i + 0.5, 1.0)])


def upd(t):
    mr.rub(F, 0.0, 0.0)
    mr.feet(F, coat=1.0)


S.every_frame(upd)
S.cam([(0, (m[0], m[1], TOP + 1.5), 12, 14, 10), (ts + 1.0, (m[0], m[1], TOP + 1.2), 10, 18, -8), (tp, (m[0] + 1, m[1], TOP + 1.0), 16, 12, 30), (S.T, (m[0] + 2, m[1] + 1, TOP + 1.0), 22, 28, 60)])
S.go()
