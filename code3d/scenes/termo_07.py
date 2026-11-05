"""termo 7 (cierre): the cap closes; no steam; wide pull-back."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import flask_rig as fr  # noqa: E402

S = sp.Shot(285, floor_z=0.0)
M = fr.palette(S)
body, cap = fr.flask(S, M, (0, 0, 0))
S.move(cap, [(0, (0, 0, fr.CAP_UP)), (0.9, (0, 0, fr.CAP_Z))])
S.cam([(0, (0, 0, 17), 74, 8, -25), (S.T, (0, 0, 18), 130, 10, 22)])
S.go()
