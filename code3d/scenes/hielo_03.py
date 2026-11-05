"""hielo 3 (hunde): the cubes fall to the bottom and stack until the glass is full from below."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_glass as ig  # noqa: E402

S = sp.Shot(215, floor_z=0.0)
M = ig.palette(S)
ig.glass(S, M, pop=(0.05, 0.3))
pos = [(-1.4, -1.4), (1.4, -1.4), (-1.4, 1.4), (1.4, 1.4)]
t0 = S.t("cae", default=1.2)
n = 0
for layer in range(3):
    for j, (x, y) in enumerate(pos):
        z_final = 1.55 + layer * 2.7
        t_hit = t0 + 0.28 * n
        c = ig.cube(S, M, f"s{n}", (x, y, 24.0), rot=(0.1 * j, 0.0, 0.6 * j), pop=(max(0.1, t_hit - 1.3), 0.15))
        S.move(c, [(t_hit - 1.3, (x, y, 24.0)), (t_hit, (x, y, z_final))])
        n += 1
S.cam([(0, (0, 0, 14), 52, 6, -30), (t0 + 1.5, (0, 0, 9), 42, 8, 0), (S.T, (0, 0, 6), 36, 10, 24)])
S.go()
