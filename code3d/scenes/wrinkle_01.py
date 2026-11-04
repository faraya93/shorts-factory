"""pieles-arrugadas 1 (hook): a sponge swells in the water, the finger in the same water does not; a red X over the false belief."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import wrinkle_rig as wr  # noqa: E402

S = sp.Shot(210)
M = wr.palette(S)
SURF = 7.0
wr.tank(S, M, pop=(0.1, 0.5))
# the contrast: sponge (left) vs finger (right)
sponge = S.box("sponge", (3.0, 2.4, 2.2), (-3.2, 0, 15.0), M["sponge"], bevel=0.5, pop=(0.2, 0.4))
S.move(sponge, [(0.2, (-3.2, 0, 15.0)), (1.5, (-3.2, 0, 8.6)), (2.1, (-3.2, 0, 7.4)), (6.5, (-3.2, 0, 7.2))])
S.size(sponge, [(0, (1, 1, 1)), (2.8, (1, 1, 1)), (4.9, (1.55, 1.35, 1.5))])
fg = wr.Finger(S, M, 3.4, 15.0, "fing", rings=5, pop=(0.3, 0.4))
S.move(fg.root, [(0.2, (3.4, 0, 15.0)), (1.5, (3.4, 0, 6.0)), (2.1, (3.4, 0, 4.4))])
wr.ripples(S, M, -3.2, SURF, 1.6, n=2)
wr.ripples(S, M, 3.4, SURF, 1.6, n=2)
# red X over the "se hincha" idea, on the word "no"
xa = S.box("xa", (3.4, 0.35, 0.45), (-3.2, -2.2, 12.0), S.error, bevel=0.15, rot=(0, math.radians(45), 0), pop=(S.t("no", default=5.5), 0.3))
xb = S.box("xb", (3.4, 0.35, 0.45), (-3.2, -2.2, 12.0), S.error, bevel=0.15, rot=(0, math.radians(-45), 0), pop=(S.t("no", default=5.5) + 0.08, 0.3))
S.cam([(0, (0, 0, 9), 40, 22, -30), (2.5, (0, 0, 8.4), 34, 12, -10), (5.0, (-1.0, 0, 9.0), 27, 8, 12), (S.T, (0.5, 0, 9.4), 30, 10, 26)])
S.go()
