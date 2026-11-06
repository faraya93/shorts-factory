"""termo2 3: see productions/mecanalia-es/009*/script.json (real thermos, transparent profile)."""
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

S = sp.Shot(155, floor_z=0.0)
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


G2 = rk.water('clear_water', '#EAF6F3')
AIR = rk.droplet(S, 'air_tpl', G2, 0.2, (0, 0, 0))
cap = tr.cap(S, CAPM)
tr.set_cut(P, 0.25)
t1, t2, t3 = S.t("tocando", default=2.1), S.t("aire", default=3.4), S.t("luz", default=4.3)
S.every_frame(lambda t: setattr(P["hot"], "default_value", 3.0 * sp.interp([(t1 - 0.2, 0.0), (t1 + 1.0, 1.0)], t)))
gx = (tr.RI_O + tr.RO - tr.T) / 2
def air(i, t):
    if t < t2 - 0.3:
        return None
    a = i * 2.399 + t * 2.0
    z = 5 + (i * 3.1) % 18 + 2.0 * math.sin(t * 3 + i)
    ang = ((i * 0.83) % 2.6) - 1.3                      # spread over the front of the gap
    return ((3.35 * math.sin(ang), -3.35 * math.cos(ang), z + (t - t2) * 1.2), 1.0)
S.swarm(26, AIR, air)
rays = []
for k in range(5):
    z = 8 + 3 * k
    r_ = ray(f"r{k}", (1.0, 0.0, z), (tr.RO - tr.T - 0.1, 0.0, z), 0.07)
    S.fns.append(grow_ray(r_, (1.0, 0.0, z), (tr.RO - tr.T - 0.1, 0.0, z), t3 + 0.1 * k, t3 + 0.6 + 0.1 * k))
S.cam([(0, (0, 0, 14), 60, 4, -14), (t2, (2, 0, 13), 44, 2, 0), (t3 + 0.5, (3, 0, 12), 34, 8, 10), (T, (4, 0, 12), 38, 12, 22)])
S.go()
