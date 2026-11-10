"""chicle 5 (salida): see productions/mecanalia-es/014*/script.json. The camera pulls back to reveal the whole coiled tract while the gum races through the intestine to the end."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import chicle_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(222, floor_z=-60.0)
cr.backing(S)
T = cr.tract(S, loc=(0.0, 0.0, 0.0))
mat = cr.gum_material(S)
cr.set_coat(mat, 0.0)
gum = cr.gum_piece(S, mat, "gum", r=0.75, loc=T.at(cr.S_PYLORUS))
rk.softboxes(0.7, centre=(0, -30, 30))
t0, t1 = 0.2, 5.0
s_a, s_b = cr.S_PYLORUS + 0.02, 0.985


def upd(t):
    k = sp.interp([(t0, 0.0), (t1, 1.0)], t)
    k = k * k * 0.35 + k * 0.65                                                  # speeds up through the coils
    gum.location = T.at(s_a + (s_b - s_a) * k)
    gum.rotation_euler = (k * 14.0, k * 9.0, k * 6.0)


S.every_frame(upd)
mid = T.at(0.62)
S.cam([(0, (mid[0], mid[1], mid[2]), 26, 8, 8), (3.0, (0, 0, 28), 62, 12, 14), (S.T, (0, 0, 23), 80, 14, -10)])
S.go()
