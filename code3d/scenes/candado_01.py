"""candado 1 (hook): a padlock on the stage, its key comes in and meets the keyhole."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import lock_rig as lr  # noqa: E402

S = sp.Shot(305, floor_z=0.0)
M = lr.palette(S)
root, body, sh = lr.padlock(S, M, (0, 0, 0))
k = lr.key(S, M, (6.0, -20.0, 5.2), pop=(0.3, 0.4))
S.move(k, [(0.3, (7.0, -22.0, 7.0)), (3.5, (3.0, -12.0, 5.8)), (6.5, (0.0, -3.0, 4.9)), (S.T, (0.0, -2.6, 4.9))])
S.spin(k, [(0.3, (0.0, 0.0, 0.5)), (6.5, (0.0, 0.0, 0.0))])
S.cam([(0, (0, 0, 7), 52, 8, -35), (S.T * 0.55, (0, 0, 7), 44, 10, -5), (S.T, (0, 0, 6.5), 34, 6, 14)])
S.go()
