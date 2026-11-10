"""chicle 7 (cierre): see productions/mecanalia-es/014*/script.json. One image: the gum passes through the whole tract once more as a passenger, its route drawn behind it, while the camera pulls back to the whole body and the wrapper."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import chicle_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(312, floor_z=-60.0)
cr.backing(S)
T = cr.tract(S, loc=(0.0, 0.0, 0.0))
mat = cr.gum_material(S)
cr.set_coat(mat, 0.0)
gum = cr.gum_piece(S, mat, "gum", r=0.7, loc=T.at(0.0))
t0, t1 = 0.3, 8.6
route = cr.route_line(S, T, 0.0, 1.0, S.accent, r=0.2, n=90, grow=(t0, t1))
rk.softboxes(0.7, centre=(0, -30, 30))


def sg(t):
    k = sp.interp([(t0, 0.0), (t1, 1.0)], t)
    return 0.985 * k


def upd(t):
    s = sg(t)
    gum.location = T.at(s)
    gum.rotation_euler = (s * 30.0, s * 20.0, s * 8.0)


S.every_frame(upd)
S.cam([(0, T.at(0.02), 20, 8, 20), (2.0, T.at(sg(2.0)), 22, 10, 5), (5.0, T.at(sg(5.0)), 38, 12, -10), (8.0, (0, 0, 24), 80, 14, 6), (S.T, (6, 0, 23), 92, 14, 0)])
S.go()
