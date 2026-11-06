"""termo2 5: see productions/mecanalia-es/009*/script.json (real thermos, transparent profile)."""
import math
import sys
from pathlib import Path
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import thermos_real as tr  # noqa: E402
from termo2_common import grow_ray, window  # noqa: E402

S = sp.Shot(140, floor_z=0.0)
P = tr.thermos(S)
window(P, 7.0, 20.0)
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
tr.set_cut(P, 0.25)
tm = S.t("rebota", default=2.4)
xw = tr.RI_O - tr.T2 - 0.1
for k in range(5):
    z = 9.5 + 2.4 * k
    a_ = ray(f"out{k}", (0.0, 0.0, z), (xw, 0.0, z), 0.09)                         # normal incidence on the mirror wall: the light returns along the same line
    S.fns.append(grow_ray(a_, (0.0, 0.0, z), (xw, 0.0, z), S.t("infrarroja", default=1.6) + 0.1 * k, tm + 0.1 * k))
    b_ = ray(f"back{k}", (xw, 0.0, z), (0.0, 0.0, z), 0.09)
    S.fns.append(grow_ray(b_, (xw, 0.0, z), (0.0, 0.0, z), tm + 0.1 * k, tm + 0.7 + 0.1 * k))
S.cam([(0, (0, 0, 15), 96, 6, -34), (tm, (1.0, 0, 15), 86, 4, 0), (T, (1.0, 0, 15), 78, 14, 30)])
S.go()
