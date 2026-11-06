"""hielo2 5 (tapa): two lakes side by side. Real world: a raft of ice floats on liquid water. If ice sank: the lake is packed with ice down to the bottom."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402

S = sp.Shot(206)
TW, TD, TH, WL = 11.0, 7.0, 10.5, 0.4
G, W, I = rk.glass(), rk.water("clear_water", "#DFF3F6", density=0.03), rk.ice("clear_ice", core=0.9)
WIN = (TW - 2 * WL - 0.3, TD - 2 * WL - 0.3, TH - WL - 1.0)
def tank(x):
    rk.noshadow(S.box(f"floor{x}", (TW, TD, WL), (x, 0, WL / 2), G, bevel=0.1))
    for nm, size, loc in (("l", (WL, TD, TH), (x - TW / 2 + WL / 2, 0, TH / 2)), ("r", (WL, TD, TH), (x + TW / 2 - WL / 2, 0, TH / 2)),
                          ("f", (TW, WL, TH), (x, -TD / 2 + WL / 2, TH / 2)), ("b", (TW, WL, TH), (x, TD / 2 - WL / 2, TH / 2))):
        rk.noshadow(S.box(f"w{nm}{x}", size, loc, G, bevel=0.1))
    rk.contact_shadow(S, (x, 0, 0), 9, 0.5, squash=(1.0, 0.7))
    rk.noshadow(S.box(f"water{x}", WIN, (x, 0, WL + WIN[2] / 2 + 0.02), W, bevel=0.2))
XL, XR = -7.2, 7.2
tank(XL)
tank(XR)
CS = 2.9
top = WL + WIN[2]
n = 0
for i, (dx, dy) in enumerate(((-2.7, -0.9), (0.2, 0.7), (2.8, -0.6))):                  # the real lake: a few cubes floating at the surface (about 9 % above it)
    c = rk.ice_cube(S, f"raft{i}", I, size=CS, loc=(XL + dx, dy, top - CS * 0.45), rot=(0.1 * i, 0.2, 0.5 * i), seed=20 + i, bw=0.12, disp=0.05)
    S.every_frame(lambda t, o=c, dx=dx, dy=dy, i=i: setattr(o, "location", (XL + dx + 0.08 * math.sin(t + i), dy, top - CS * 0.45 + 0.07 * math.sin(t * 1.7 + i))))
t_b = S.t("bloques", default=4.2)
for k in range(3):                                                                       # the changed world: the lake is packed with sunk ice, layer by layer
    for r_ in range(2):
        for c_ in range(3):
            x = XR + (c_ - 1) * (CS + 0.05) + (0.25 if r_ else -0.25) * (k % 2 + 0.3)
            y = (r_ - 0.5) * (CS + 0.1)
            z = WL + 0.05 + CS / 2 + k * (CS + 0.04)
            ta = 2.4 + n * 0.12
            c = rk.ice_cube(S, f"pile{n}", I, size=CS, loc=(x, y, z), rot=(0.1 * n, 0.08 * n, 0.3 * n), seed=40 + n, bw=0.12, disp=0.05)
            S.move(c, [(0, (x, y, 90)), (ta, (x, y, 90)), (ta + 0.02, (x, y, 30)), (ta + 0.5, (x, y, z + 1.0)), (ta + 0.75, (x, y, z))])
            n += 1
rk.softboxes(1.8, centre=(0, 0, 6))
S.cam([(0, (XL, 0, 6), 30, 10, -12), (2.6, (0, 0, 6), 40, 12, 0), (S.T, (0, 0, 6), 46, 16, 8)])
S.go()
