"""grano 1 (hook): one kernel, and the false belief (air) against the truth (water); a popped piece appears beside it."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import corn_rig as cr  # noqa: E402

S = sp.Shot(270, plinth=False)
M = cr.palette(S)
k = cr.kernel(S, M, (-4.2, 0, 5.0), r=4.2, pop=(0.1, 0.4))
S.spin(k, [(0, (0, 0, 0)), (S.T, (0, 0, math.radians(200)))])
col = ar.load(S, "popcorn", loc=(0, 0, 0), k=100.0)
pieces, box = cr.retint_popcorn(col)
ar.unparent(col.objs)
p = pieces[0]
S.reg(box); S.size(box, [(0, 1e-4)])
for o in pieces[1:]:
    S.reg(o); S.size(o, [(0, 1e-4)])
S.reg(p, loc=[(0, (4.6, 0, 4.2))], rot=[(0, (0.3, 0.2, 0.0)), (S.T, (0.3, 0.2, 2.0))], sc=[(0, 3.2)], pop=(S.t("aire", default=3.0), 0.5))
S.cam([(0, (0, 0, 4.8), 58, 8, -28), (4.0, (0, 0, 4.8), 50, 12, 4), (S.T, (0, 0, 4.8), 46, 10, 28)])
S.go()
