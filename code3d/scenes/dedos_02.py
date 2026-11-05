"""dedos 2 (orden): cutaway of a fingertip on a cream plate; a nerve signal runs down, the vessels tighten."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import grip_rig as gr  # noqa: E402

S = sp.Shot(260)
M = gr.palette(S)
S.box("plate", (22, 1.2, 26), (0, 1.8, 8), M["plate"], bevel=0.5)                       # cream cutaway plate behind
tip = S.box("tip", (8.4, 2.0, 15), (0, 0, 7.5), M["skin"], bevel=1.2, pop=(0.1, 0.4))     # cut face of the fingertip
S.ball("tipcap", M["skin"], 4.2, (0, 0, 0.6), shape=(1, 0.48, 1), pop=(0.1, 0.4))
S.box("bone", (3.2, 0.5, 9.5), (0, -1.1, 9.6), M["bone"], bevel=0.8, pop=(0.5, 0.4))
for sx in (-1, 1):
    v = S.cyl(f"vessel{sx}", 0.9, 13.5, (sx * 2.9, -1.15, 7.5), M["vessel"], axis="Z", verts=32, pop=(S.t("vasos", default=3.5) - 2.2, 0.4))
    S.size(v, [(0, (1, 1, 1)), (S.t("aprietan", default=6.5), (1, 1, 1)), (S.t("aprietan", default=6.5) + 1.2, (0.38, 0.38, 1))])
INK = S.hero("ink", "#1D1B2E", rough=0.5)
nerve = S.line("nerve", [(0, -1.2, 21), (0, -1.2, 14), (0, -1.2, 7), (0, -1.2, 2.5)], 0.3, INK, grow=(0.6, 2.2))
pulse = S.ball("pulse", INK, 1.2, (0, -1.5, 21), pop=(S.t("orden", default=3.0), 0.3))
t0 = S.t("orden", default=3.0)
S.move(pulse, [(t0, (0, -1.5, 21)), (t0 + 1.8, (0, -1.5, 2.5))])
S.gone(pulse, t0 + 1.8, 0.3)
S.cam([(0, (0, 0, 10), 56, 4, -8), (3.0, (0, 0, 9), 40, 2, 6), (6.0, (0, 0, 6), 24, 0, -4), (S.T, (0, 0, 5), 20, 0, 4)])
S.go()
