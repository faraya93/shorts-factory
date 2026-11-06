"""latido2 4 (hora): a wall of 150 real bottles grows around the heart, wave by wave; the camera travels along the wall."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
from latido2_common import heart, bottle_field  # noqa: E402

S = sp.Shot(100, floor_z=0.0)
H = heart(S, (0, 0, 0))
t0 = S.t("ciento", default=1.0)
items = []
for r in range(10):
    for c in range(15):
        x, z = (c - 7) * 7.4, r * 18.5
        d = abs(c - 7) + r * 0.7
        items.append((x, 14.0, z, 0.2 + 0.12 * d, 0.35))
bottle_field(S, items)
rk.softboxes(2.0, centre=(0, 0, 40))
S.cam([(0, (0, 0, 10), 60, 6, -30), (S.T * 0.5, (-20, 0, 40), 120, 8, -8), (S.T, (30, 0, 50), 150, 10, 20)])
S.go()
