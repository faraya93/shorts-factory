"""hielo2 2 (nueve): a glass of real water freezes from the bottom up (the water material hands over to the ice material along a front) and the ice ends ~9 % above the mark;
the camera then pans to a second glass where real ice cubes rise and float: ice weighs less."""
import math
import sys
from pathlib import Path
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402

S = sp.Shot(213)
R_, H_, LV, BASE = 5.0, 12.5, 9.0, 1.1
XA, XB = -6.4, 6.4
G = rk.glass()
W = rk.water("clear_water", "#DFF3F6", density=0.02)
I = rk.ice("clear_ice", core=0.9)
# left: an ICE-CUBE TRAY, the one place everybody has seen water turn into ice: six cells brim-full of water; they freeze and the cubes stand ABOVE the rim (the 9 % growth, exaggerated so it reads)
tray_m = rk.wet_tissue("g_pin", "#3E6FA8", sss=0.0, rough=0.4, coat=0.3)
CW, WL, RIM, TH = 2.7, 0.3, 1.1, 0.4
cols, rows = 3, 2
TW, TD = cols * CW + (cols + 1) * WL, rows * CW + (rows + 1) * WL
S.box("tray_base", (TW, TD, TH), (XA, 0, TH / 2), tray_m, bevel=0.12)
for i in range(cols + 1):
    S.box(f"tray_wx{i}", (WL, TD, RIM), (XA - TW / 2 + WL / 2 + i * (CW + WL), 0, TH + RIM / 2), tray_m, bevel=0.08)
for j in range(rows + 1):
    S.box(f"tray_wy{j}", (TW, WL, RIM), (XA, -TD / 2 + WL / 2 + j * (CW + WL), TH + RIM / 2), tray_m, bevel=0.08)
t_a, t_b = S.t("congelarse", default=1.3), S.t("nueve", default=2.7)
k = 0
for i in range(cols):
    for j in range(rows):
        cx = XA - TW / 2 + WL + CW / 2 + i * (CW + WL)
        cy = -TD / 2 + WL + CW / 2 + j * (CW + WL)
        wo = S.box(f"cellw{k}", (CW - 0.1, CW - 0.1, RIM), (cx, cy, TH + RIM / 2 - 0.02), W, bevel=0.12)
        rk.noshadow(wo)
        ta = t_a + 0.18 * k
        S.move(wo, [(0, (cx, cy, TH + RIM / 2 - 0.02)), (ta, (cx, cy, TH + RIM / 2 - 0.02)), (ta + 0.01, (cx, cy, -90)), (S.T, (cx, cy, -90))])
        cube = rk.ice_cube(S, f"cellice{k}", I, size=(CW - 0.1, CW - 0.1, RIM), loc=(cx, cy, -90), rot=(0, 0, 0.05 * k), seed=k + 4, bevel=0.2, bw=0.15, disp=0.05)
        S.move(cube, [(0, (cx, cy, -90)), (ta, (cx, cy, -90)), (ta + 0.01, (cx, cy, TH + RIM / 2 - 0.02)), (S.T, (cx, cy, TH + RIM / 2 - 0.02))])
        S.size(cube, [(0, (1, 1, 1)), (ta + 0.01, (1, 1, 1)), (t_b + 0.3 + 0.1 * k, (1, 1, 1)), (t_b + 1.5 + 0.1 * k, (1, 1, 1.45))])
        k += 1
# second glass: real ice cubes rise and float ("pesa menos y sube")
G2, W2, I2 = rk.glass(), rk.water("clear_water", density=0.02), rk.ice("clear_ice", core=0.9)
rk.tumbler(S, "glass2", G2, W2, r=R_, h=H_, level=LV, loc=(XB, 0, 0))
t_up = S.t("pesa", default=5.2)
for i, (dx, dy, rot) in enumerate(((-2.3, -0.9, 0.4), (2.1, -0.4, 1.1), (-0.2, 2.1, 0.2))):
    c = rk.ice_cube(S, f"cube{i}", I2, size=2.5, loc=(XB + dx, dy, 2.6), rot=(0.3 * i, 0.2, rot), seed=i + 1)
    ta = t_up - 0.5 + 0.25 * i
    S.move(c, [(0, (XB + dx, dy, 90)), (ta - 0.1, (XB + dx, dy, 90)), (ta - 0.05, (XB + dx, dy, 2.6)), (ta + 0.2, (XB + dx, dy, 2.6)), (ta + 1.3, (XB + dx * 0.9, dy, 8.9))])
    S.every_frame(lambda t, o=c: None)
rk.softboxes(2.2, centre=(0, 0, 8))
S.cam([(0, (XA, 0, 3), 34, 34, -6), (3.4, (XA, 0, 3), 26, 22, 0), (5.2, (2.0, 0, 8), 40, 12, 0), (S.T, (3.0, 0, 8), 36, 14, 8)])
S.go()
