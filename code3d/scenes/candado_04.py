"""candado 4 (llave): the right key slides in and lifts every pin pair so all cuts meet the shear line."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import lock_rig as lr  # noqa: E402

S = sp.Shot(200, floor_z=0.0)
M = lr.palette(S)
cut = lr.Cut(S, M, show_key=True)
t0 = 0.8
cut.X = lambda t: -30.0 + 30.0 * sp.interp([(t0, 0.0), (t0 + 3.6, 1.0)], t)
S.pop(cut.line, t0 + 3.4, 0.3)
S.cam([(0, (0, 0, 11), 56, 2, -10), (S.T, (0, 0, 10.5), 36, 0, 6)])
S.go()
