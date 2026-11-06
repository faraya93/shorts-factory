"""latido2 5 (dia): the wall becomes a tower of real bottles that rises above the heart; the camera climbs along it."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
from latido2_common import heart, bottle_field  # noqa: E402

S = sp.Shot(200, floor_z=0.0)
H = heart(S, (0, 0, 0))
items = []
LAYERS = 10
for k in range(LAYERS):
    for r in range(6):
        for c in range(8):
            items.append(((c - 3.5) * 7.2, 12.0 + r * 7.2, k * 18.5, 0.3 + 0.42 * k + 0.01 * (c + r), 0.3))
bottle_field(S, items)
rk.softboxes(2.0, centre=(0, 0, 90))
S.cam([(0, (0, 5, 10), 70, 8, -28), (S.T * 0.55, (0, 12, 80), 190, 10, -8), (S.T, (0, 12, 100), 250, 14, 18)])
S.go()
