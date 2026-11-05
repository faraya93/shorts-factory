"""latido 3 (minuto): two and a half 2-litre bottles line up beside the heart (5 L in a minute)."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import bottle_rig as br  # noqa: E402

S = sp.Shot(160, floor_z=0.0)
M = br.palette(S)
HX = -6.0
heart = ar.load(S, "human-heart", loc=(HX, 0, 0), k=100.0)
h = heart.objs[0]
ar.retint(h, "#C8323C", role="g_big", rough=0.4)
base = tuple(h.scale)
def beat(t):
    s = 1.0 + 0.09 * br.beat_amount(t)
    h.scale = (base[0] * s, base[1] * s, base[2] * s)
S.every_frame(beat)

t5 = S.t("cinco", default=1.0)
xs = [3.0, 7.5, 12.0]
for i, x in enumerate(xs):
    b = br.bottle(S, M, f"b{i}", (x, 0, 0.0), pop=(t5 + 0.35 * i, 0.4))
    if i == 2:
        S.size(b, [(0, (1, 1, 0.5))])
S.cam([(0, (3, 0, 5), 62, 8, -14), (S.T, (3, 0, 5), 74, 10, 8)])
S.go()
