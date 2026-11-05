"""hielo 2 (nueve): a block of water freezes and grows 9 % above the marked level."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_glass as ig  # noqa: E402

S = sp.Shot(215, floor_z=0.0)
M = ig.palette(S)
tn = S.t("nueve", default=2.0)
S.box("plate", (24, 1.0, 22), (0, 4.0, 9), M["line"], bevel=0.4)
wb = S.box("wblock", (7, 7, 10), (0, 0, 5.0), M["water"], bevel=0.5, pop=(0.1, 0.4))
S.gone(wb, tn - 0.4, 0.3)
ib = S.box("iblock", (7, 7, 10), (0, 0, 5.0), M["ice"], bevel=0.5, pop=(tn - 0.4, 0.3))
S.size(ib, [(0, (1, 1, 1.0)), (tn, (1, 1, 1.0)), (tn + 1.6, (1.0, 1.0, 1.09))])
S.move(ib, [(0, (0, 0, 5.0)), (tn, (0, 0, 5.0)), (tn + 1.6, (0, 0, 5.45))])
line = S.box("mark", (12, 0.3, 0.35), (0, -3.8, 10.0), M["line"], bevel=0.05, pop=(0.6, 0.3))
S.cam([(0, (0, 0, 6), 46, 4, -30), (tn, (0, 0, 8), 36, 2, -10), (S.T, (0, 0, 9.5), 24, 0, 8)])
S.go()
