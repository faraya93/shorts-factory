"""hielo 6 (cierre): a glass with a floating lid of ice; slow pull-back and orbit."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_glass as ig  # noqa: E402

S = sp.Shot(285, floor_z=0.0)
M = ig.palette(S)
ig.glass(S, M)
lid = S.cyl("lid", 4.6, 0.7, (0, 0, 9.1), M["ice"], axis="Z", verts=48)
for i, (x, y) in enumerate([(-1.6, 0.8), (1.4, -0.9)]):
    S.move(S.box(f"f{i}", (2.6, 2.6, 2.6), (x, y, 7.0), M["ice"], bevel=0.45, pop=(0.2 + 0.2 * i, 0.3)), [(0, (x, y, 6.6)), (S.T, (x, y, 6.6))])
S.cam([(0, (0, 0, 7), 34, 8, -25), (S.T, (0, 0, 8), 64, 12, 40)])
S.go()
