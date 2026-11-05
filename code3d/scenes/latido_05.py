"""latido 5 (día): 3600 bottles stack into a building-sized block (7200 L in a day); very wide pull-back."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import bottle_rig as br  # noqa: E402

S = sp.Shot(240, floor_z=0.0)
M = br.palette(S)
HX = 0.0
heart = ar.load(S, "human-heart", loc=(HX, 0, 0), k=100.0)
h = heart.objs[0]
ar.retint(h, "#C8323C", role="g_big", rough=0.4)
base = tuple(h.scale)
def beat(t):
    s = 1.0 + 0.09 * br.beat_amount(t)
    h.scale = (base[0] * s, base[1] * s, base[2] * s)
S.every_frame(beat)

tpl = br.bottle(S, M, "tpl", (0, 0, 0))
W, D, H = 20, 12, 15
td = S.t("siete", default=1.0)
def cell(i, t):
    c, d, r = i % W, (i // W) % D, i // (W * D)
    a = td + 0.35 * r + 0.004 * (i % (W * D))
    if t < a:
        return None
    k = min(1.0, (t - a) / 0.2)
    return (((c - (W - 1) / 2) * 1.0 * 1.5, 8.0 + d * 1.3 * 1.5, r * 2.6), 0.3 * k)
S.swarm(W * D * H, tpl, cell)
S.cam([(0, (0, 4, 8), 70, 6, -10), (S.T * 0.5, (0, 8, 22), 130, 8, 4), (S.T, (0, 8, 30), 190, 8, 12)])
S.go()
