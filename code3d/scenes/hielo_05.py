"""hielo 5 (tapa): the stacked cubes rise back to the surface and a lid of ice closes over the water."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_glass as ig  # noqa: E402

S = sp.Shot(210, floor_z=0.0)
M = ig.palette(S)
ig.glass(S, M)
pos = [(-1.4, -1.4), (1.4, -1.4), (-1.4, 1.4), (1.4, 1.4)]
tr = S.t("bloques", default=3.5)
n = 0
cubes = []
for layer in range(3):
    for j, (x, y) in enumerate(pos):
        zf = 1.55 + layer * 2.7
        c = ig.cube(S, M, f"s{n}", (x, y, zf), rot=(0.1 * j, 0.0, 0.6 * j))
        z_top = 8.5 + 0.0 * layer
        S.move(c, [(0, (x, y, zf)), (0.4 + 0.1 * n, (x, y, zf)), (0.4 + 0.1 * n + 1.6, (x * 1.6 + 0.0, y * 1.6, z_top + (0.05 * layer)))])
        n += 1
lid = S.cyl("lid", 4.6, 0.7, (0, 0, 9.1), M["ice"], axis="Z", verts=48, pop=(tr, 0.4))
S.cam([(0, (0, 0, 6), 40, 6, -20), (S.T, (0, 0, 7), 34, 14, 22)])
S.go()
