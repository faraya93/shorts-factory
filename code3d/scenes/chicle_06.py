"""chicle 6 (giro): see productions/mecanalia-es/014*/script.json. The turn: gum pieces keep arriving one after another along the large intestine and pile up, each still a chewed piece, until the colon is plugged; a row of gum sticks stands beside the body, one for every piece (rung 1 re-stage 2026-11-09: the merged smooth ball read as a brain / tumour, 35/35/25)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import chicle_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(242, floor_z=-60.0)
cr.backing(S)
T = cr.tract(S, loc=(0.0, 0.0, 0.0))
mat = cr.gum_material(S)
cr.set_coat(mat, 0.25)
s_in = cr.frac_of(13)
s_c = cr.frac_of(16)                                                           # where the pile forms: the ascending colon
B = T.at(s_c)
N = 12
pieces = [cr.gum_piece(S, mat, f"gum{i}", r=0.55, loc=T.at(s_in), seed=3 + i, pop=(0.2 + 0.5 * i, 0.25)) for i in range(N)]
BUB = {2: 0.55, 6: 0.5, 10: 0.6}                                                  # pieces that carry a small bubble (the cue for gum, as in scene 1)
bubs = {}
for i, kk in BUB.items():
    ta = 0.2 + 0.5 * i + 1.1
    b = cr.bubble(S, f"gum_bubble{i}", 1.0, T.at(s_in))
    S.size(b, [(0, 1e-3), (ta, 1e-3), (ta + 0.8, kk)])
    bubs[i] = b
rk.softboxes(0.7, centre=(0, -30, 30))


def upd(t):
    for i, g in enumerate(pieces):
        ta = 0.2 + 0.5 * i
        k = sp.interp([(ta, 0.0), (ta + 1.1, 1.0)], t)
        a = T.at(s_in + (s_c - s_in) * k)
        rest = (B[0] + 0.3 * math.sin(i * 2.1), B[1] + 0.25 * math.cos(i * 1.7), B[2] - 1.0 + 0.36 * i)
        p = tuple(a[j] + (rest[j] - a[j]) * (k ** 3) for j in range(3))
        g.location = p
        g.rotation_euler = (i + 0.3 * t, 0.5 * i, 0.4 * t)
    for i, b in bubs.items():
        g = pieces[i]
        b.location = (g.location[0] + 0.55, g.location[1] - 0.7, g.location[2] + 0.2)


S.every_frame(upd)
S.cam([(0, (B[0] + 4.0, B[1], B[2] - 4.0), 36, 6, 16), (3.0, (B[0] + 2.0, B[1], B[2] - 2.0), 33, 6, 6), (S.T - 2.0, (B[0] + 2.0, B[1], B[2] - 1.5), 30, 8, -4), (S.T, (B[0] + 2.0, B[1], B[2] - 1.5), 28, 8, -10)])
S.go()
