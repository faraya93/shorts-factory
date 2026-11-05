"""latido 2 (latido): the heart contracts and a small glass fills with one beat's worth (70 ml)."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import bottle_rig as br  # noqa: E402

S = sp.Shot(210, floor_z=0.0)
M = br.palette(S)
HX = -3.0
heart = ar.load(S, "human-heart", loc=(HX, 0, 0), k=100.0)
h = heart.objs[0]
ar.retint(h, "#C8323C", role="g_big", rough=0.4)
base = tuple(h.scale)
def beat(t):
    s = 1.0 + 0.09 * br.beat_amount(t)
    h.scale = (base[0] * s, base[1] * s, base[2] * s)
S.every_frame(beat)

glass = S.cyl("glass", 2.0, 5.0, (9.0, 0, 2.5), M["glass"], axis="Z", verts=40, bevel=0.2, pop=(0.3, 0.4))
liq = S.cyl("liquid", 1.8, 4.2, (9.0, 0, 2.2), M["blood"], axis="Z", verts=40, pop=(0.4, 0.2))
S.size(liq, [(0, (1, 1, 0.02)), (S.t("setenta", default=2.5), (1, 1, 0.02)), (S.t("setenta", default=2.5) + 0.6, (1, 1, 1.0))])
S.move(liq, [(0, (9.0, 0, 0.3)), (S.t("setenta", default=2.5), (9.0, 0, 0.3)), (S.t("setenta", default=2.5) + 0.6, (9.0, 0, 2.2))])
S.cam([(0, (3, 0, 6), 66, 8, -14), (S.T, (3, 0, 5), 48, 6, 8)])
S.go()
