"""grano 6 (cierre): the striped box fills and overflows with popcorn; wide pull-back."""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import corn_rig as cr  # noqa: E402

S = sp.Shot(310)
random.seed(11)
col = ar.load(S, "popcorn", loc=(0, 0, 0), k=150.0)
pieces, box = cr.retint_popcorn(col)
ar.unparent(col.objs)
S.reg(box, pop=(0.05, 0.5))
tl = S.t("llena", default=3.0)
ups = [random.uniform(0.0, 1.0) for _ in pieces]
for i, o in enumerate(pieces):
    home = tuple(o.location)
    S.reg(o, pop=(0.6 + 1.2 * ups[i], 0.35))
    if o.location.z > 24.0 and i % 2 == 0:                        # a third of the top pieces erupt and fall around the box
        out = (random.uniform(-14, 14), random.uniform(-6, 4), random.uniform(10, 24))
        t0 = 2.4 + 0.04 * i
        S.move(o, [(t0, home), (t0 + 0.6, (home[0] + out[0] * 0.5, home[1] + out[1] * 0.5, home[2] + 16)), (t0 + 1.6, (home[0] + out[0], home[1] + out[1], 2.0 + 0.2 * (i % 5)))])
S.spin(box, [(0, (0, 0, 0)), (S.T, (0, 0, 0))])
S.cam([(0, (0, 0, 16), 78, 8, -18), (3.0, (0, 0, 16), 88, 10, 0), (S.T, (0, 0, 16), 104, 8, 14)])
S.go()
