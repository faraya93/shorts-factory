"""chicle 2 (esofago): see productions/mecanalia-es/014*/script.json. A wave of muscle (a squeeze ring) travels down the oesophagus behind the gum and pushes it along; the camera follows it down."""
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import chicle_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(166, floor_z=-60.0)
cr.backing(S)
T = cr.tract(S, loc=(0.0, 0.0, 0.0))
mat = cr.gum_material(S)
cr.set_coat(mat, 0.55)
gum = cr.gum_piece(S, mat, "gum", r=0.55, loc=T.at(0.0))
ring = cr.ring(S, "ring", S.accent, 0.95, 0.3, T.at(0.0))
rk.softboxes(0.7, centre=(0, -30, 30))
s_end = cr.S_STOMACH_IN
t0, t1 = 0.4, S.T - 0.5


def sg(t):
    k = sp.interp([(t0, 0.0), (t1, 1.0)], t)
    return s_end * k


def upd(t):
    s = sg(t)
    gum.location = T.at(s)
    gum.rotation_euler = (s * 40.0, s * 25.0, 0.0)
    sr = max(0.0, s - 0.03)
    ring.location = T.at(sr)
    ring.rotation_euler = cr.aim(cr.tangent(T, sr))


S.every_frame(upd)
keys = []
for i, t in enumerate([0.0, 1.5, 3.0, 4.4, S.T]):
    p = T.at(sg(t) + (0.015 if i else 0.0))
    keys.append((t, p, 16 if i < 4 else 20, 8, 28 - 14 * i))
S.cam(keys)
S.go()
