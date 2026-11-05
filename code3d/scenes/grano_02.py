"""grano 2 (gota): the kernel is cut open: hull, starch and a drop of water inside."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import corn_rig as cr  # noqa: E402

S = sp.Shot(210)
M = cr.palette(S)
k = cr.kernel(S, M, (0, 0, 9.0), r=7.0, pop=(0.05, 0.3))
S.spin(k, [(0, (0, 0, 0)), (1.2, (0, 0, 0.9))])
S.gone(k, 1.1, 0.35)
hull, st, dr = cr.cutaway(S, M, 0, 9.0, 7.2, t_on=1.2)
S.move(dr, [(0, (0, -1.2, 8.0)), (S.T, (0, -1.2, 8.0))])
S.size(dr, [(S.t("gotita", default=2.5), 1.0), (S.t("gotita", default=2.5) + 0.4, 1.35), (S.t("gotita", default=2.5) + 0.8, 1.0)])
S.cam([(0, (0, 0, 9), 62, 6, -20), (1.5, (0, 0, 9), 56, 2, -4), (S.T, (0, 0, 8.5), 38, 0, 4)])
S.go()
