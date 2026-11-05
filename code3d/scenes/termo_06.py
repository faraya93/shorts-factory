"""termo 6 (tapa): the lid sits loose; heat rises out through the gap at the top; pull-back following the leak."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import flask_rig as fr  # noqa: E402

S = sp.Shot(157, floor_z=0.0)
M = fr.palette(S)
P = fr.section(S, M, lid=False)
lid = S.box("loose_lid", (2 * fr.HW - 0.4, 1.1, 2.6), (0, 0, 21.3), M["cap"], bevel=0.4)
S.move(lid, [(0, (0, 0, 21.3)), (1.0, (0, 0, 21.3)), (1.6, (2.5, 0, 24.5))])
S.spin(lid, [(0, (0, 0, 0)), (1.0, (0, 0, 0)), (1.6, (0, 0.5, 0))])
def leak(i, t):
    t0 = 1.0 + 0.1 * i
    u = (t - t0) / 2.4
    if u < 0 or u > 1.0:
        return None
    x = -3.0 + (i % 6) * 1.2
    return ((x + 1.8 * u * (1 if i % 2 else -1), -1.0, 12.0 + 22.0 * u), 1.0 - 0.3 * u)
fr.heat(S, M, 20, leak)
S.cam([(0, (0, 0, 14), 44, 2, -8), (S.T, (0, 0, 22), 80, 10, 8)])
S.go()
