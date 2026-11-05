"""dedos 5 (agarre): two pads carry a wet marble along a track: the smooth pad loses it, the grooved pad delivers it to the finish."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import grip_rig as gr  # noqa: E402

S = sp.Shot(240)
M = gr.palette(S)
S.box("board", (34, 1.0, 22), (0, 2.5, 6.5), M["plate"], bevel=0.4)
T = S.T
for z, name in ((11.0, "smooth"), (2.0, "grooved")):
    S.box("track_" + name, (28, 3.0, 0.6), (0, 0, z - 1.3), M["bone"], bevel=0.2)
fin = S.box("finish", (0.8, 3.0, 9.0), (13.5, 0, 6.0), M["bone"], bevel=0.2)
tw = S.t("mojados", default=1.0)
glow = S.hero("gold", "#FFF1B8", rough=0.4)
# pads
x0, x1 = -12.0, 11.5
ps = S.box("pad_smooth", (3.2, 2.2, 1.0), (x0, 0, 11.0), M["pad"], bevel=0.3, pop=(0.1, 0.4))
pg = S.box("pad_grooved", (3.2, 2.2, 1.0), (x0, 0, 2.0), M["pad"], bevel=0.3, pop=(0.2, 0.4))
for dx in (-0.9, 0, 0.9):
    S.box(f"rib{dx}", (0.3, 2.3, 0.35), (dx, 0, 0.45), M["groove"], bevel=0.05, parent=pg)
S.move(ps, [(0.5, (x0, 0, 11.0)), (T - 0.8, (x1, 0, 11.0))])
S.move(pg, [(0.5, (x0, 0, 2.0)), (T - 0.8, (x1, 0, 2.0))])
# marbles: smooth one slides off the pad at ~45% of the way and falls; grooved one stays on the pad to the end
ms = S.ball("m_smooth", M["marble"], 0.95, (x0, 0, 12.4), pop=(0.3, 0.3))
mg = S.ball("m_grooved", M["marble"], 0.95, (x0, 0, 3.4), pop=(0.4, 0.3))
tf = T * 0.5
S.move(ms, [(0.5, (x0, 0, 12.0)), (tf, (x0 + (x1 - x0) * (tf - 0.5) / (T - 1.3), 0, 12.0)), (tf + 0.6, (x0 + (x1 - x0) * (tf - 0.2) / (T - 1.3) + 1.0, 0, 3.6)), (tf + 1.0, (x0 + (x1 - x0) * (tf + 0.3) / (T - 1.3) + 1.8, 0, 6.2)), (T, (x0 + 14.0, 0, -4.0))])
S.move(mg, [(0.5, (x0, 0, 3.0)), (T - 0.8, (x1, 0, 3.0))])
# the finish lights up when the grooved pad arrives
S.size(fin, [(0, (1, 1, 1)), (T - 0.9, (1, 1, 1)), (T - 0.5, (1.0, 1.0, 1.0))])
S.cam([(0, (-8, 0, 7), 44, 4, -12), (T * 0.5, (0, 0, 7), 38, 4, 0), (T, (8, 0, 6), 34, 4, 10)])
S.go()
