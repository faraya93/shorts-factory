"""hielo 1 (flota): three ice cubes float in a glass of water, each with its top above the surface; slow orbit."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_glass as ig  # noqa: E402

S = sp.Shot(240, floor_z=0.0)
M = ig.palette(S)
ig.glass(S, M, pop=(0.05, 0.4))
cubes = []
for i, (x, y, rz) in enumerate([(-1.6, 0.8, 0.3), (1.4, -0.9, 0.9), (0.3, 1.8, 1.4)]):
    c = ig.cube(S, M, f"c{i}", (x, y, 9.2), rot=(0.05 * i, 0.04, rz), pop=(0.3 + 0.25 * i, 0.4))
    cubes.append((c, x, y))
def float_(t):
    for i, (c, x, y) in enumerate(cubes):
        c.location.z = 8.45 + ig.bob(t, i)
S.every_frame(float_)
S.cam([(0, (0, 0, 7), 52, 8, -40), (S.T * 0.5, (0, 0, 7), 44, 12, 10), (S.T, (0, 0, 7), 40, 10, 50)])
S.go()
