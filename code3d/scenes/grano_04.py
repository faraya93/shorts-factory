"""grano 4 (estallido): the kernel gives way and becomes a popcorn piece (library asset), with shards flying; the camera pulls back hard."""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import corn_rig as cr  # noqa: E402

S = sp.Shot(200)
M = cr.palette(S)
random.seed(8)
tp = S.t("pum", default=1.5)
k = cr.kernel(S, M, (0, 0, 5.0), r=4.0, pop=(0.05, 0.3))
def tremble(t):
    amp = min(1.0, t / max(tp, 0.1))
    k.location.x = amp * 0.25 * math.sin(t * 75.0)
S.every_frame(tremble)
S.gone(k, tp, 0.05)
col = ar.load(S, "popcorn", loc=(0, 0, 0), k=100.0)
pieces, box = cr.retint_popcorn(col)
ar.unparent(col.objs)
S.reg(box); S.size(box, [(0, 1e-4)])
big = pieces[0]
for o in pieces[1:]:
    S.reg(o); S.size(o, [(0, 1e-4)])
S.reg(big, loc=[(0, (0, 0, 6.0))], rot=[(0, (0.3, 0.2, 0.0)), (S.T, (0.3, 0.2, 1.4))], sc=[(0, 4.2)], pop=(tp, 0.35))
shard = S.ball("shard", M["shard"], 0.5, (0, 0, 0))
dirs = [(random.uniform(-1, 1), random.uniform(-0.3, 0.6), random.uniform(0.2, 1.2)) for _ in range(18)]
def fly(i, t):
    if t < tp or t > tp + 1.0:
        return None
    u = t - tp
    d = dirs[i]
    return ((d[0] * 14 * u, d[1] * 14 * u, 5.0 + d[2] * 12 * u - 9 * u * u), 1.0 - u)
S.swarm(18, shard, fly)
S.cam([(0, (0, 0, 5), 34, 4, -10), (tp - 0.1, (0, 0, 5), 30, 4, -4), (tp + 1.2, (0, 0, 6), 58, 14, 14), (S.T, (0, 0, 6), 62, 12, 22)])
S.go()
