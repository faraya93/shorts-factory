"""hielo2 3 (hunde): imagine the ice sank: six real cubes fall through the water of a glass and stack from the bottom up."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402

S = sp.Shot(213)
G, W, I = rk.glass(), rk.water("clear_water", density=0.02), rk.ice("clear_ice", core=0.9)
glass, liquid = rk.tumbler(S, "glass", G, W, r=5.0, h=12.5, level=9.0)
SZ = 2.5
rest = [(-1.3, -0.3, 2.45), (1.3, 0.4, 2.45), (-1.2, 0.5, 4.95), (1.25, -0.4, 4.95), (-0.9, -0.2, 7.4), (1.0, 0.35, 7.4)]
t0 = S.t("cubo", default=1.4)
for i, (x, y, z) in enumerate(rest):
    ta = t0 + 0.95 * i
    c = rk.ice_cube(S, f"cube{i}", I, size=SZ, loc=(x, y, 22), rot=(0.4 * i, 0.3, 0.5 + i), seed=i + 1)
    S.move(c, [(0, (x, y, 80)), (ta - 0.25, (x, y, 80)), (ta - 0.2, (x, y, 22)), (ta + 0.35, (x * 0.9, y, 10.0)), (ta + 0.75, (x, y, z + 0.5)), (ta + 0.95, (x, y, z))])
    S.spin(c, [(0, (0.4 * i, 0.3, 0.5 + i)), (ta - 0.2, (0.4 * i, 0.3, 0.5 + i)), (ta + 0.95, (0.1 * i, 0.05, 0.2 * i))])
rk.softboxes(2.2)
S.cam([(0, (0, 0, 9), 36, 12, -26), (S.T * 0.55, (0, 0, 7), 30, 10, 4), (S.T, (0, 0, 6), 27, 14, 22)])
S.go()
