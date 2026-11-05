"""candado 7 (cierre): the open padlock closes again with a click; wide pull-back."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import lock_rig as lr  # noqa: E402

S = sp.Shot(305, floor_z=0.0)
M = lr.palette(S)
root, body, sh = lr.padlock(S, M, (0, 0, 0))
S.move(sh, [(0, (0, 0, 2.6)), (1.6, (0, 0, 2.6)), (2.1, (0, 0, 0))])
k = lr.key(S, M, (9.0, -3.0, 3.0), rot=(0, 0, 0)) if False else lr.key(S, M, (9.0, -3.0, 3.0))
S.spin(k, [(0, (0.0, 0.0, 0.6)), (S.T, (0.0, 0.0, 0.6))])
S.cam([(0, (0, 0, 8), 36, 8, -20), (S.T, (0, 0, 9), 84, 12, 20)])
S.go()
