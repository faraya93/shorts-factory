"""mosca 4 (escupe): see productions/mecanalia-es/015*/script.json. The fly lands on a slice of bread, taps it with its feet, and a drop from its mouth melts a dark wet patch into the crumb."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import mosca_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(222, floor_z=0.0)
mr.counter(S)
mr.plate(S, loc=(0, 0, 0))
mr.prop(S, "bread-slice", loc=(0, 0, 0.8), rot=(0, 0, 0.3), k=mr.K * 1.5)
TOP = 0.8 + 2.4
F = mr.fly(S, loc=(0, 0, TOP), yaw=-1.25)
rk.softboxes(0.7, centre=(0, 0, 30))
tl, te = S.t("aterriza", default=0.5), S.t("escupe", default=4.2)
L = (-3.0, -2.0, TOP)
S.move(F.root, [(0, (-14, 12, 38)), (tl + 1.2, L), (S.T, L)])
S.spin(F.root, [(0, (0, 0, -0.6)), (tl + 1.2, (0, 0, -1.25)), (S.T, (0, 0, -1.25))])
F.root.location = L
import bpy  # noqa: E402
bpy.context.view_layer.update()
m = mr.mouth(F)
drop = S.ball("drop", S.glass("#CFE8F0", alpha=0.55, name="water"), 0.55, m, seg=16)
S.move(drop, [(0, m), (te, m), (te + 0.7, (m[0], m[1], TOP + 0.4))])
S.size(drop, [(0, 1e-4), (te - 0.3, 1e-4), (te, 1.0), (te + 0.75, 1.0), (te + 0.85, 1e-4)])
wet = S.ball("wet_patch", S.hero("rubber_k", "#8A6A43", rough=0.12, coat=0.9), 1.0, (m[0], m[1], TOP + 0.05), shape=(1.5, 1.2, 0.12), seg=20)
S.size(wet, [(0, 1e-4), (te + 0.7, 1e-4), (te + 2.4, 1.0)])


def upd(t):
    land = 1.0 if t > tl + 1.2 else 0.0
    mr.rub(F, 0.25 * land + 0.1, phase=t * 11.0)


S.every_frame(upd)
S.cam([(0, (-8, 6, 24), 60, 38, 30), (tl + 1.2, (-3, -2, TOP + 3), 26, 22, 20), (te, (m[0], m[1], TOP + 1), 14, 12, 6), (S.T, (m[0], m[1], TOP + 1), 18, 30, -14)])
S.go()
