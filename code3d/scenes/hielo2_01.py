"""hielo2 1 (flota): a glass of water with three real ice cubes floating, slow orbit. Transparent profile: glass, water and ice are refracting materials."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402

S = sp.Shot(210)
G, W, I = rk.glass(), rk.water("clear_water", density=0.02), rk.ice("clear_ice", core=0.9)
glass, liquid = rk.tumbler(S, "glass", G, W, r=5.0, h=12.5, level=9.4)
cubes = []
for i, (x, y, rot) in enumerate(((-2.3, -0.9, 0.4), (2.1, -0.4, 1.1), (-0.2, 2.1, 0.2))):
    cubes.append(rk.ice_cube(S, f"cube{i}", I, size=2.5, loc=(x, y, 8.9), rot=(0.3 * i, 0.2, rot), seed=i + 1))
    S.every_frame(lambda t, o=cubes[-1], i=i, x=x, y=y: setattr(o, "location", (x + 0.12 * math.sin(t * 1.3 + i), y + 0.1 * math.cos(t * 1.1 + i),       # cubes drop in from above (a volume object cannot be scaled to zero: openvdb aborts), then bob
              8.55 + 0.1 * math.sin(t * 2.0 + i * 1.7) + (90.0 if t < 0.15 + 0.2 * i else 14.0 * max(0.0, (0.15 + 0.2 * i + 0.45 - t) / 0.45) ** 2))))
rk.softboxes(2.0)
S.cam([(0, (0, 0, 7), 34, 14, -24), (S.T, (0, 0, 7), 30, 18, 26)])
S.go()
