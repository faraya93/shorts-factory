"""dedos2 1 (contraste): the library hand dips into a glass tray of real water (refraction); only the fingertips wrinkle, the forearm above the water stays smooth."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import real_kit as rk  # noqa: E402

S = sp.Shot(260)
G, W = rk.glass(), rk.water("clear_water", "#E4F5F4", density=0.012)
hand = ar.load(S, "human-hand", loc=(0, 0, 44), k=100.0)
ar.retint(hand.objs[0], "#C98963", role="g_big", rough=0.55)
wr = ar.node(hand.objs[0].data.materials[0], "wrinkle_amount")
S.move(hand.root, [(0.3, (0, 0, 44)), (2.0, (0, 0, 2.0)), (S.T, (0, 0, 2.0))])
TW, TD, TH, WALL, LV = 34.0, 22.0, 13.0, 0.5, 10.5
rk.noshadow(S.box("tray_floor", (TW, TD, WALL), (0, 0, WALL / 2), G, bevel=0.1))
rk.contact_shadow(S, (0, 0, 0), 24, 0.55, squash=(1.0, 0.75))
for nm, size, loc in (("wl", (WALL, TD, TH), (-TW / 2 + WALL / 2, 0, TH / 2)), ("wr", (WALL, TD, TH), (TW / 2 - WALL / 2, 0, TH / 2)),
                      ("wf", (TW, WALL, TH), (0, -TD / 2 + WALL / 2, TH / 2)), ("wb", (TW, WALL, TH), (0, TD / 2 - WALL / 2, TH / 2))):
    rk.noshadow(S.box("tray_" + nm, size, loc, G, bevel=0.1))
rk.noshadow(S.box("tray_water", (TW - 2 * WALL - 0.1, TD - 2 * WALL - 0.1, LV - WALL), (0, 0, WALL + (LV - WALL) / 2 + 0.02), W, bevel=0.2))
S.every_frame(lambda t: wr.outputs[0].__setattr__("default_value", sp.interp([(0, 0.0), (3.0, 0.0), (7.0, 1.0)], t)))
rk.softboxes(4.0, centre=(0, 0, 10))
S.cam([(0, (0, 0, 11), 66, 12, -28), (4, (0, 0, 10), 56, 8, 4), (S.T, (0, 0, 10), 50, 6, 26)])
S.go()
