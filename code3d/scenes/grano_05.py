"""grano 5 (solterona): a row of popcorn pieces and one hard kernel with a cracked hull; its steam escapes and it stays hard."""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import corn_rig as cr  # noqa: E402

S = sp.Shot(180)
M = cr.palette(S)
random.seed(5)
col = ar.load(S, "popcorn", loc=(0, 0, 0), k=100.0)
pieces, box = cr.retint_popcorn(col)
ar.unparent(col.objs)
S.reg(box); S.size(box, [(0, 1e-4)])
S.size(box, [(0, 1e-4)])
for o in pieces[8:]:
    S.reg(o); S.size(o, [(0, 1e-4)])
xs = [-15, -9, 9, 15, -12, 12, 4.5, -4.5]
for i, o in enumerate(pieces[:8]):
    x = xs[i]
    z = 3.0 + (i % 2) * 0.2
    S.reg(o, loc=[(0, (x, (i % 3) * 1.5 - 1.5, z))], rot=[(0, (random.random() * 6, random.random() * 6, random.random() * 6))], sc=[(0, 2.6)], pop=(0.1 + 0.12 * i, 0.4))
k = cr.kernel(S, M, (0, 0, 4.5), r=3.6, pop=(0.3, 0.3))
crack = S.box("crack", (0.35, 0.3, 4.0), (-1.4, -2.1, 5.3), M["dark"], bevel=0.05, rot=(0, math.radians(25), 0), pop=(S.t("rota", default=1.2), 0.3))
steam = S.ball("steam", M["steam"], 0.6, (0, 0, 0))
t0 = S.t("escapa", default=3.0)
def wisp(i, t):
    a = t0 + i * 0.22
    u = (t - a) % 2.2 if t >= a else None
    if u is None:
        return None
    k_ = u / 2.2
    return ((-1.4 - 1.5 * k_ + 0.4 * math.sin(u * 5 + i), -2.6, 6.0 + 7.0 * k_), (0.5 + 0.8 * k_) * (1 - k_))
S.swarm(10, steam, wisp)
S.cam([(0, (-8, 0, 4.5), 46, 8, -22), (S.T * 0.6, (0, 0, 4.5), 38, 8, 0), (S.T, (2, 0, 4.5), 30, 8, 10)])
S.go()
