"""latido 4 (hora): a wall of 150 bottles builds up behind the heart (300 L in an hour); pull-back."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import bottle_rig as br  # noqa: E402

S = sp.Shot(140, floor_z=0.0)
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
COLS, ROWS = 15, 10
ts = S.t("trescientos", default=0.8)
def cell(i, t):
    c, r = i % COLS, i // COLS
    a = ts + 0.012 * i + 0.2 * r
    if t < a:
        return None
    k = min(1.0, (t - a) / 0.25)
    return (((c - (COLS - 1) / 2) * 1.9, 5.5, r * 4.4), 0.5 * k)
S.swarm(COLS * ROWS, tpl, cell)
S.cam([(0, (0, 0, 6), 46, 6, -10), (S.T, (0, 0, 20), 118, 4, 6)])
S.go()
