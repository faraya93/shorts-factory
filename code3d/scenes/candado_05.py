"""candado 5 (casi): an almost identical key: one tooth is a little low, one pin stays under the shear line and blocks."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import lock_rig as lr  # noqa: E402

S = sp.Shot(165, floor_z=0.0)
M = lr.palette(S)
cut = lr.Cut(S, M, wrong=3, show_key=True)
cut.X = lambda t: -30.0 + 30.0 * sp.interp([(0.3, 0.0), (2.6, 1.0)], t)
S.pop(cut.line, 2.4, 0.3)
bad = S.torus("badring", 1.8, 0.14, (3.0, -1.4, 9.2), S.error, rot=(math.pi / 2, 0, 0), pop=(S.t("pino", default=3.0), 0.3))
S.cam([(0, (0, 0, 10.5), 52, 2, -10), (2.8, (2, 0, 10), 40, 0, 4), (S.T, (3, 0, 9.5), 22, 0, 6)])
S.go()
