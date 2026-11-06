"""latido2 2 (latido): the heart contracts and, through the tube, fills a small glass up to the 70 ml mark. Camera pushes into the heart then pans to the glass."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import bottle_real as bt  # noqa: E402
from latido2_common import heart, slugs  # noqa: E402

S = sp.Shot(180, floor_z=0.0)
H = heart(S, (-5, 0, 0))
G = rk.glass()
W = rk.water("clear_water", "#F6DADA", density=0.14, absorb="#FF4A55")
cup, liq = rk.tumbler(S, "cup", G, W, r=3.4, h=7.0, level=5.6, loc=(12, 0, 0), wall=0.25, base=0.8)
t0, t1 = S.t("empuja", default=0.6), S.t("setenta", default=2.8)
S.size(liq, [(0, (1, 1, 0.03)), (t0, (1, 1, 0.03)), (t1 + 0.3, (1, 1, 1.0))])
S.torus("mark", 3.45, 0.06, (12, 0, 5.6), S.ink)
pts = [(-3.4, 0.0, 11.8), (-3.0, 0.0, 16.5), (3.0, 0.0, 17.5), (12.0, 0.0, 14.5), (12.0, 0.0, 9.0)]
bt.tube_path(S, pts)
slugs(S, pts, 0.3, n=8, period=0.7, travel=1.1)
rk.softboxes(2.0, centre=(0, 0, 8))
S.cam([(0, (-5, 0, 9), 56, 6, -25), (1.5, (-5, 0, 9), 34, 4, -8), (3.2, (4, 0, 8), 40, 8, 10), (S.T, (10, 0, 6), 30, 10, 22)])
S.go()
