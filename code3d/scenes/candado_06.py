"""candado 6 (giro): with the right key the cylinder turns and the shackle pops up."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import lock_rig as lr  # noqa: E402

S = sp.Shot(150, floor_z=0.0)
M = lr.palette(S)
root, body, sh = lr.padlock(S, M, (0, 0, 0))
k = lr.key(S, M, (0.0, -2.6, 4.9))
S.spin(k, [(0.0, (0, 0, 0)), (1.2, (0, 0, 0)), (2.0, (0, math.radians(90), 0))])
tg = S.t("gancho", default=2.4)
S.move(sh, [(0, (0, 0, 0)), (tg - 0.2, (0, 0, 0)), (tg + 0.5, (0, 0, 2.6))])
S.cam([(0, (0, 0, 7), 34, 4, -14), (S.T, (0, 0, 8), 40, 10, 24)])
S.go()
