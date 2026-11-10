"""chicle 3 (estomago): see productions/mecanalia-es/014*/script.json. The gum lands in the stomach acid among bread pieces that dissolve; its pale sugar coat washes off and the deeper pink rubbery core stays whole."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import chicle_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(333, floor_z=-60.0)
cr.backing(S)
T = cr.tract(S, loc=(0.0, 0.0, 0.0))
mat = cr.gum_material(S)
cr.set_coat(mat, 0.55)
C = (3.8, 0.0, 22.5)                                                           # stomach centre (scene cm)
gum = cr.gum_piece(S, mat, "gum", r=1.3, loc=T.at(cr.S_STOMACH_IN))
pool = cr.acid(S, (C[0], C[1], C[2] - 2.2), (3.0, 2.0, 1.2))
S.size(pool, [(0, 1e-3), (S.t("ácido", default=1.4), 1e-3), (S.t("ácido", default=1.4) + 1.2, 1.0)])
bread = []
for i, (dx, dy, dz, rz) in enumerate([(-1.6, -0.4, 0.9, 0.5), (1.2, 0.5, 1.2, 2.1), (0.2, -1.0, 1.5, 4.0)]):
    h = cr.food(S, "bread-slice", (C[0] + dx, C[1] + dy, C[2] - 2.2 + dz), 20.0, rot=(0.6, 0.2, rz))
    bread.append((h, (dx, dy, dz)))
rk.softboxes(0.7, centre=(0, -30, 30))
t_in, t_az, t_go = 0.1, S.t("azúcar", default=3.9), S.t("goma", default=6.7)
t_dis = S.t("deshace", default=1.9)
for j, (h, off) in enumerate(bread):
    S.size(h.root, [(0, 1.0), (t_dis + 0.2 * j, 1.0), (t_dis + 1.8 + 0.2 * j, 1e-3)])


def upd(t):
    k = sp.interp([(t_in, 0.0), (t_in + 1.5, 1.0)], t)
    entry = T.at(cr.S_STOMACH_IN)
    rest = (C[0] + 0.3 * math.sin(t * 1.3), C[1] + 0.2 * math.cos(t * 1.1), C[2] - 1.6 + 0.25 * math.sin(t * 2.0))
    gum.location = tuple(entry[i] + (rest[i] - entry[i]) * k for i in range(3))
    gum.rotation_euler = (0.3 * t, 0.2 * t, 0.5 * t)
    cr.set_coat(mat, sp.interp([(t_az, 0.55), (t_az + 2.2, 0.0)], t))


S.every_frame(upd)
S.cam([(0, (3.0, 0, 30), 30, 6, 10), (2.0, (C[0], 0, 23), 24, 8, 25), (6.0, (C[0], 0, 22), 20, 10, 60), (S.T, (C[0], 0, 22), 22, 12, 95)])
S.go()
