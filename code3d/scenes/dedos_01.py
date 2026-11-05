"""dedos 1 (hook, contrast): the library hand dips into water; only the fingertips wrinkle, the forearm stays smooth."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402

S = sp.Shot(260)
skin = S.hero("big", "#C98963", rough=0.55)
water = S.glass("#7FD0E8", alpha=0.22)
hand = ar.load(S, "human-hand", loc=(0, 0, 40), k=100.0)
ar.retint(hand.objs[0], "#C98963", role="g_big", rough=0.55)
wr = ar.node(hand.objs[0].data.materials[0], "wrinkle_amount")
S.move(hand.root, [(0.3, (0, 0, 44)), (2.0, (0, 0, 2.0)), (S.T, (0, 0, 2.0))])
tank = S.box("tank", (20, 12, 15.5), (0, 0, 7.2), water, bevel=0.6)
S.every_frame(lambda t: wr.outputs[0].__setattr__("default_value", sp.interp([(0, 0.0), (3.0, 0.0), (6.0, 1.0)], t)))
S.cam([(0, (0, 0, 9), 62, 12, -20), (4, (0, 0, 9), 52, 8, 5), (S.T, (0, 0, 9), 46, 6, 25)])
S.go()
