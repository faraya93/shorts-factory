"""chicle 1 (hook): see productions/mecanalia-es/014*/script.json. A chewed wad is pulled off a dark sole, its pink threads stretching; it snaps free and drops into the top of the tract; the camera pulls back to the whole x-ray tract. (Re-stage 2026-11-09, third staging: the gum stick in its wrapper read as a lipstick 55/40/40, the pink bubble as a lollipop or balloon 45/45/45; stretched threads are the other cue for chewed gum.)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import chicle_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(231, floor_z=-60.0)
cr.backing(S)
T = cr.tract(S, loc=(0.0, 0.0, 0.0))
mat = cr.gum_material(S)
cr.set_coat(mat, 0.55)
t_fall = S.t("chicle?", default=1.5) + 0.35
mouth = T.at(0.0)
SOLE_TOP = 40.0
sole = S.box("sole", (11.0, 4.0, 1.0), (-1.2, -9.0, SOLE_TOP - 0.5), S.hero("ink", "#1D1B2E", rough=0.6, coat=0.0), bevel=0.2)
blob = cr.gum_piece(S, mat, "gum_stuck", r=1.0, loc=(-1.2, -9.0, SOLE_TOP + 0.35), seed=5)
S.size(blob, [(0, (1.5, 1.2, 0.5)), (S.T, (1.5, 1.2, 0.5))])
start = (-1.2, -9.0, 45.0)
gum = cr.gum_piece(S, mat, "gum", r=1.1, loc=start, pop=(0.05, 0.2))
for j, dx in enumerate((-0.6, -0.2, 0.15, 0.55)):
    st = cr.strand(S, f"gum_thread{j}", (start[0] + dx, start[1] + 0.1 * j, start[2] - 0.7), (-1.2 + dx * 1.9, -9.0 - 0.1 * j, SOLE_TOP + 0.6), r=0.12, mat=mat)
    S.size(st, [(0, 1e-3), (0.15, 1.0), (t_fall - 0.02, 1.0), (t_fall + 0.08, 1e-3)])
S.move(gum, [(0, start), (t_fall, start), (t_fall + 0.7, (mouth[0] - 0.3, mouth[1] - 2.0, mouth[2] + 4.0)), (t_fall + 1.2, mouth), (t_fall + 3.0, T.at(0.06)), (S.T, T.at(0.09))])
S.spin(gum, [(0, (0, 0, 0)), (t_fall, (0.4, 0.3, 0.2)), (S.T, (6.0, 4.0, 3.0))])
rk.softboxes(0.7, centre=(0, -30, 30))
S.cam([(0, (-1.0, -9.0, 43.0), 20, 4, 12), (1.6, (-1.0, -8.0, 43.0), 23, 5, 6), (3.2, (-1.0, -5.0, 38.0), 36, 8, -4), (5.0, (0.0, -2.0, 33.0), 50, 12, 0), (S.T, (0.0, -1.0, 30.0), 62, 14, -8)])
S.go()
