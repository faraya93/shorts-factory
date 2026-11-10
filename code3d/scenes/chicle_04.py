"""chicle 4 (intestino): see productions/mecanalia-es/014*/script.json. The stomach churns (squash and stretch); the gum and three whole corn kernels are pushed out through the exit into the small intestine side by side; the camera travels along."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import chicle_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(217, floor_z=-60.0)
cr.backing(S)
T = cr.tract(S, loc=(0.0, 0.0, 0.0))
mat = cr.gum_material(S)
cr.set_coat(mat, 0.0)
kmat = S.hero("big", "#F2BE2B", rough=0.55, coat=0.05)                          # corn yellow (011's orange egg read as a bean among the pink)
s0, s1 = cr.frac_of(6), 0.46
gum = cr.gum_piece(S, mat, "gum", r=0.7, loc=T.at(s0))
tm, tk = S.t("amasa", default=2.4), S.t("granos", default=4.5)
kern = [cr.kernel(S, kmat, f"kernel{i}", r=0.5, loc=T.at(s0), pop=(tk + 0.3 * i, 0.3)) for i in range(4)]
rk.softboxes(0.7, centre=(0, -30, 30))
S.size(T.hero.root, [(0, (1, 1, 1)), (tm - 0.3, (1, 1, 1)), (tm, (1.05, 1.0, 0.94)), (tm + 0.4, (0.96, 1.0, 1.05)), (tm + 0.8, (1.05, 1.0, 0.94)), (tm + 1.2, (0.97, 1.0, 1.04)), (tm + 1.7, (1, 1, 1))])
t_go, t_end = tm + 0.8, S.T - 0.4


def sgum(t):
    k = sp.interp([(t_go, 0.0), (t_end, 1.0)], t)
    return s0 + (s1 - s0) * k


def upd(t):
    s = sgum(t)
    bob = 0.25 * math.sin(t * 2.0) if t < t_go else 0.0
    p = T.at(s)
    gum.location = (p[0], p[1], p[2] + bob)
    gum.rotation_euler = (0.4 * t, 0.3 * t, 0.2 * t)
    for i, kn in enumerate(kern):
        q = T.at(max(s0, s + 0.012 * (i - 1.5)))
        kn.location = (q[0] + (1.4 if i % 2 else -1.4), q[1] - 0.8, q[2] + 0.4 * (i - 1.5))
        kn.rotation_euler = (0.0, 0.0, 0.5 * math.sin(t + i) + 0.6 * (i - 1.5))


S.every_frame(upd)
keys = []
for i, t in enumerate([0.0, 2.2, 4.0, 5.8, S.T]):
    p = T.at(sgum(t))
    keys.append((t, (p[0], p[1], p[2] + 1.0), 26 if i < 2 else 15, 8, -28 + 20 * i))
S.cam(keys)
S.go()
