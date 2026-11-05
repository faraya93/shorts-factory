"""dedos 6 (cierre): the wrinkled fingertips and a grooved tyre side by side; pull-back."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import grip_rig as gr  # noqa: E402

S = sp.Shot(300)
M = gr.palette(S)
hand = ar.load(S, "human-hand", loc=(-6.0, 0, 3.0), rot=(0, 0, math.radians(8)), k=100.0)
ar.retint(hand.objs[0], "#C98963", role="g_big", rough=0.55)
mat = hand.objs[0].data.materials[0]
ar.node(mat, "Bump").inputs["Distance"].default_value = 0.0055
ar.node(mat, "wrinkle_amount").outputs[0].default_value = 1.0
S.box("board", (80, 1.0, 60), (0, 14, 10), M["plate"], bevel=0.4)
tyre = gr.wheel(S, M, "tyre", 9.0, 6.5, 5.0, 3.5, grooved=True, pop=(S.t("llantas", default=3.0), 0.5))
S.spin(tyre, [(0, (0, 0, 0)), (S.T, (0, 2 * math.pi, 0))])
S.cam([(0, (-4, 0, 9), 36, 6, -10), (S.T * 0.6, (0, 0, 9), 48, 6, 4), (S.T, (0, 0, 10), 68, 6, 10)])
S.go()
