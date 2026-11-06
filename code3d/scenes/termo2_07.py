"""termo2 7: see productions/mecanalia-es/009*/script.json (real thermos, transparent profile)."""
import math
import sys
from pathlib import Path
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import thermos_real as tr  # noqa: E402
from termo2_common import grow_ray  # noqa: E402

S = sp.Shot(293, floor_z=0.0)
P = tr.thermos(S)
CAPM = rk.wet_tissue("rubber_k", "#2B2B33", sss=0.0, rough=0.5, coat=0.1)
rk.softboxes(2.0, centre=(0, 0, 14))
tr.front_light(2.5)
GOLD = rk.emissive("ray", "#FFD36B", 9.0)
T = S.T


def ray(name, p0, p1, r=0.07):
    o = rk.ray(S, name, p0, p1, r, GOLD)
    S.items[:] = [it for it in S.items if it[0] is not o]
    return o


def swirl(i, t, z0, z1, rad, spd):
    a = i * 2.399 + t * spd
    return (rad * math.cos(a), rad * math.sin(a), z0 + (z1 - z0) * ((i * 0.37 + t * 0.15) % 1.0))


cap = tr.cap(S, CAPM)
tc = S.t("vacío", default=2.6)
def cut(t):
    tr.set_cut(P, sp.interp([(0, 0.25), (tc, 0.25), (tc + 0.8, -9.0)], t))
S.every_frame(cut)
S.every_frame(lambda t: setattr(P["hot"], "default_value", 0.0))
S.cam([(0, (0, 0, 15), 40, 8, -26), (T * 0.5, (0, 0, 15), 60, 10, -4), (T, (0, 0, 15), 88, 6, 16)])
S.go()
