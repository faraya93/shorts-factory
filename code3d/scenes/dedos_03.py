"""dedos 3 (surcos): macro on the library hand's fingertips: smooth skin sinks and the grooves appear."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402

S = sp.Shot(160)
hand = ar.load(S, "human-hand", loc=(0, 0, 0), k=100.0)
ar.retint(hand.objs[0], "#C98963", role="g_big", rough=0.55)
mat = hand.objs[0].data.materials[0]
wr = ar.node(mat, "wrinkle_amount")
ar.node(mat, "Bump").inputs["Distance"].default_value = 0.0055
S.every_frame(lambda t: wr.outputs[0].__setattr__("default_value", sp.interp([(0.4, 0.0), (S.T - 0.6, 1.0)], t)))
S.box("plate", (60, 1.0, 60), (0, 14, 6), S.plate_mat(), bevel=0.4)
S.cam([(0, (0, 0, 5), 34, 8, -12), (S.T, (0, 0, 3.2), 16, 4, 6)])
S.go()
