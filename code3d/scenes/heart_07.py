"""corazon 7 (cierre): a person lies on a sofa doing nothing while the pump keeps beating and filling bottles beside them; wide orbit."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import heart_rig as hr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(296)
M = hr.palette(S)
t_cor, t_bom, t_sig = S.t("corazón", default=0.7), S.t("bomba", default=2.9), S.t("Sígueme,", default=5.4)
S.box("floor", (34.0, 12.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
# sofa + person
S.box("seat", (8.0, 3.4, 1.6), (-6.0, 0, 0.8), M["board"], bevel=0.4, pop=(0.1, 0.45))
S.box("back", (8.0, 0.9, 3.2), (-6.0, 1.3, 2.4), M["board"], bevel=0.4, pop=(0.15, 0.45))
S.box("arm", (1.1, 3.4, 2.6), (-9.5, 0, 1.6), M["board"], bevel=0.4, pop=(0.2, 0.45))
body = S.cyl("body", 0.85, 4.2, (-6.0, -0.1, 2.5), M["shirt"], axis="X", verts=28, pop=(0.5, 0.4))
head = S.ball("head", M["skin"], 0.85, (-3.6, -0.1, 2.6), pop=(0.5, 0.4))
S.cyl("legs", 0.7, 3.0, (-8.6, -0.1, 2.4), M["shirt"], axis="X", verts=24, pop=(0.5, 0.4))
S.every_frame(lambda t: setattr(head, "location", (-3.6, -0.1, 2.6 + 0.04 * math.sin(2.0 * t))))
heart = hr.pump_heart(S, M, (2.0, 0, 5.0), scale=0.9, pop=t_cor, t_beat=t_cor + 0.2, amp=0.12)
tpl = hr.bottle(S, M, "bt")
def bots(i, t):
    t0 = t_bom + 0.35 * i
    if t < t0:
        return None
    return (7.0 + (i % 5) * 2.4, -2.5 + (i // 5) * 2.6, 0.0), min(1.0, (t - t0) / 0.3)
S.swarm(15, tpl, bots)
S.line("feed", [(3.4, 0, 3.2), (5.0, 0, 1.2), (14.0, -1.0, 0.8)], 0.15, S.accent, grow=(t_bom, t_bom + 1.0))
S.cam([(0, (-3, 0, 4), 34, 10, -26), (t_cor, (-2, 0, 4), 26, 8, -6), (t_bom, (1, 0, 4), 32, 10, 12), (t_sig, (2, 0, 4), 44, 16, -8), (S.T, (2, 0, 4), 50, 22, 8)])
S.go()
