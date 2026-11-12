"""Block B5 proof 026-P7 (a still): a tilted ice-cube tray alone, water spilling from cell to cell."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402


import math

import tape_rig as tr  # noqa: E402

S = sp.Shot(30, floor_z=-1.2)
m = ti.Mats(S)
root = tr.empty("tray_root", (0.0, 0.0, 6.0))
tr_mat = tr.plain("tray_plastic", "#D9E3EA", rough=0.4)
tr.rbox("tray_base", (30.0, 12.0, 1.2), (0.0, 0.0, 0.0), tr_mat, bevel=0.3, parent=root)
tr.rbox("tray_wall_b", (30.0, 0.8, 3.4), (0.0, 6.0, 1.8), tr_mat, bevel=0.2, parent=root)
tr.rbox("tray_wall_f", (30.0, 0.8, 3.4), (0.0, -6.0, 1.8), tr_mat, bevel=0.2, parent=root)
for i in range(7):
    tr.rbox(f"tray_div{i}", (0.8, 12.0, 3.4), (-15.0 + i * 5.0, 0.0, 1.8), tr_mat, bevel=0.2, parent=root)
tr.rbox("tray_div_mid", (30.0, 0.8, 3.0), (0.0, 0.0, 1.6), tr_mat, bevel=0.2, parent=root)
for i in range(6):                                                         # water in the lower cells, a sheet over the lip on the low side
    for j in (-3.0, 3.0):
        tr.rbox(f"tray_w{i}{int(j)}", (3.8, 4.8, 0.5 + 2.4 * (i / 5.0)), (-12.5 + i * 5.0, j, 0.9 + 0.25 + 1.2 * (i / 5.0)), m.water, bevel=0.1, parent=root)
tr.rbox("tray_spill", (0.8, 11.0, 7.0), (14.6, 0.0, -2.0), m.spill, bevel=0.1, parent=root)
root.rotation_euler = (0.0, math.radians(18.0), 0.0)
lift = ti.lights(S, ti.LIGHT_K)
S.cam([(0.0, (0.0, 0.0, 6.0), 70.0, 28.0, -20.0), (S.T, (0.0, 0.0, 6.0), 70.0, 28.0, -20.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
