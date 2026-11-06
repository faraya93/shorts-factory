"""latido2 3 (minuto): three real bottles fill one after another (two and a half); the camera pulls back and rises."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import bottle_real as bt  # noqa: E402
from latido2_common import heart, slugs  # noqa: E402

S = sp.Shot(165, floor_z=0.0)
H = heart(S, (-8, 0, 0))
xs = (6.0, 16.0, 26.0)
ts = (S.t("cinco", default=1.4), S.t("dos", default=2.3), S.t("media", default=3.0))
ends = (2.4, 3.5, 4.6)
fills = (1.0, 1.0, 0.5)
for k, x in enumerate(xs):
    B = bt.parts(S, (x, 0, 0))
    S.size(B["liquid"], [(0, (1, 1, 0.03)), (ts[k] - 0.4, (1, 1, 0.03)), (ends[k], (1, 1, fills[k]))])
    pts = [(-6.4 + 1.0, 0.0, 11.8), (-6.0, 0.0, 17 + 2 * k), (x - 2, 0.0, 22 + 2 * k), (x, 0.0, 21.5), (x, 0.0, 18.5)]
    bt.tube_path(S, pts, 0.28)
    slugs(S, pts, ts[k] - 0.6, n=5, period=0.5, travel=0.9, r=0.3)
rk.softboxes(2.0, centre=(0, 0, 8))
S.cam([(0, (4, 0, 9), 50, 8, -16), (2.5, (8, 0, 11), 66, 14, -4), (S.T, (10, 0, 14), 86, 24, 10)])
S.go()
