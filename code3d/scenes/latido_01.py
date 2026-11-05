"""latido 1 (hook): the library heart beats alone; a first bottle appears beside it."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import bottle_rig as br  # noqa: E402

S = sp.Shot(280, floor_z=0.0)
M = br.palette(S)
heart = ar.load(S, "human-heart", loc=(-3.0, 0, 0), k=100.0)
h = heart.objs[0]
ar.retint(h, "#C8323C", role="g_big", rough=0.4)
nodes = h.data.materials[0].node_tree.nodes
for n in nodes:
    if n.type == "TEX_IMAGE":                       # keep the vessel texture but flatten it into the red (clean model look, no tissue detail)
        pass
base = tuple(h.scale)
def beat(t):
    s = 1.0 + 0.09 * br.beat_amount(t)
    h.scale = (base[0] * s, base[1] * s, base[2] * s)
S.every_frame(beat)
S.spin(heart.root, [(0, (0, 0, math.radians(-25))), (S.T, (0, 0, math.radians(35)))])
b = br.bottle(S, M, "bottle", (8.0, 0, 0.0), pop=(S.t("botellas", default=1.5), 0.45))
S.cam([(0, (0, 0, 6), 54, 8, -22), (S.T, (0, 0, 6), 46, 10, 22)])
S.go()
