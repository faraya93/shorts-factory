"""latido2 1 (hook): a beating heart; a clear tube carries a red slug to a real PET bottle that starts to fill. Camera orbits from the heart to the bottle."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import bottle_real as bt  # noqa: E402
from latido2_common import heart, slugs  # noqa: E402

S = sp.Shot(255, floor_z=0.0)
H = heart(S, (0, 0, 0))
BX = 13.0
B = bt.parts(S, (BX, 0, 0))
S.size(B["liquid"], [(0, (1, 1, 0.03)), (2.0, (1, 1, 0.03)), (S.T, (1, 1, 0.42))])
S.size(B["liquid"], [(0, (1, 1, 0.03)), (2.0, (1, 1, 0.03)), (S.T, (1, 1, 0.42))])
pts = [(1.6, 0.0, 11.8), (2.2, 0.0, 16.5), (6.0, 0.0, 20.5), (BX, 0.0, 21.5), (BX, 0.0, 18.5)]
bt.tube_path(S, pts)
slugs(S, pts, 0.8)
rk.softboxes(2.0, centre=(0, 0, 8))
S.cam([(0, (0, 0, 9), 62, 8, -48), (S.T * 0.5, (5, 0, 9), 56, 10, -10), (S.T, (11, 0, 9), 50, 12, 24)])
S.go()
