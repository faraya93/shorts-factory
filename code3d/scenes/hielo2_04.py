"""hielo2 4 (lago): a lake in cross-section (glass box of real water). If ice sank, real ice would pile up from the bottom; the summer sun only melts the top layer."""
import math
import sys
from pathlib import Path
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402

S = sp.Shot(217)
TW, TD, TH, WL = 22.0, 7.5, 12.0, 0.45
G, W, I = rk.glass(), rk.water("clear_water", "#DFF3F6", density=0.03), rk.ice("clear_ice", core=0.9)
rk.noshadow(S.box("tank_floor", (TW, TD, WL), (0, 0, WL / 2), G, bevel=0.1))
for nm, size, loc in (("wl", (WL, TD, TH), (-TW / 2 + WL / 2, 0, TH / 2)), ("wr", (WL, TD, TH), (TW / 2 - WL / 2, 0, TH / 2)),
                      ("wf", (TW, WL, TH), (0, -TD / 2 + WL / 2, TH / 2)), ("wb", (TW, WL, TH), (0, TD / 2 - WL / 2, TH / 2))):
    rk.noshadow(S.box("tank_" + nm, size, loc, G, bevel=0.1))
rk.contact_shadow(S, (0, 0, 0), 17, 0.5, squash=(1.0, 0.6))
WIDTH = (TW - 2 * WL - 0.3, TD - 2 * WL - 0.3, TH - WL - 1.0)
rk.noshadow(S.box("lake_water", WIDTH, (0, 0, WL + WIDTH[2] / 2 + 0.02), W, bevel=0.2))
CS = 3.0
cols, rows, layers = 6, 2, 3
t_in = S.t("congelaría", default=2.2)
t_sun = S.t("sol", default=4.0)
cubes = []
n = 0
for k in range(layers):
    for r_ in range(rows):
        for c_ in range(cols):
            x = (c_ - (cols - 1) / 2) * (CS + 0.05) + (0.3 if r_ else -0.3) * (k % 2 + 0.2)
            y = (r_ - (rows - 1) / 2) * (CS + 0.1)
            z = WL + 0.05 + CS / 2 + k * (CS + 0.04)
            ta = 0.6 + n * 0.075
            cube = rk.ice_cube(S, f"cube{n}", I, size=CS, loc=(x, y, z), rot=(0.1 * n, 0.07 * n, 0.3 * n), seed=n + 1, bw=0.12, disp=0.05)
            S.move(cube, [(0, (x, y, 90)), (ta, (x, y, 90)), (ta + 0.02, (x, y, 30)), (ta + 0.55, (x, y, z + 1.0)), (ta + 0.8, (x, y, z))])
            if k == layers - 1:                                                            # the top layer melts under the summer sun
                S.size(cube, [(0, (1, 1, 1)), (t_sun + 0.6, (1, 1, 1)), (t_sun + 2.2, (0.82, 0.82, 0.4))])
            cubes.append(cube)
            n += 1
sun_m = rk.emissive("sun", "#FFD27A", 14.0)
sun = S.ball("sun", sun_m, 2.0, (-9, -4, 24), pop=(t_sun - 0.2, 0.4))
sun.visible_shadow = False
rk.softboxes(1.8, centre=(0, 0, 6))
S.cam([(0, (0, 0, 7), 46, 8, -14), (S.T * 0.5, (0, 0, 7), 38, 14, 0), (S.T, (0, 0, 7), 34, 22, 10)])
S.go()
