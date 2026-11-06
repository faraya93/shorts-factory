"""termo2 4: see productions/mecanalia-es/009*/script.json (real thermos, transparent profile)."""
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

S = sp.Shot(146, floor_z=0.0)
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


G2 = rk.water('clear_water', '#EAF6F3')
AIR = rk.droplet(S, 'air_tpl', G2, 0.32, (0, 0, 0))
cap = tr.cap(S, CAPM)
tr.set_cut(P, 0.25)
ts = S.t("sin", default=0.3)
tp = S.t("sirve:", default=2.8)
S.every_frame(lambda t: setattr(P["hot"], "default_value", 3.0 * (1.0 - sp.interp([(ts + 0.3, 0.0), (tp + 0.6, 0.85)], t))))
gx = (tr.RI_O + tr.RO - tr.T) / 2
def air(i, t):
    u = (t - (ts + 0.1 + 0.03 * i)) / 1.4
    base_z = 5 + (i * 3.1) % 18
    if u < 0:
        return ((3.35 * math.sin(((i * 0.83) % 2.6) - 1.3), -3.35 * math.cos(((i * 0.83) % 2.6) - 1.3), base_z), 1.0)
    z = base_z + u * 30.0
    if z > 29.0:
        return None
    return ((3.35 * math.sin(((i * 0.83) % 2.6) - 1.3), -3.35 * math.cos(((i * 0.83) % 2.6) - 1.3), z), 1.0)
S.swarm(26, AIR, air)
S.cam([(0, (0, 0, 15), 96, 6, -30), (2.0, (0, 0, 15), 86, 5, -6), (T, (0, 0, 15), 78, 8, 24)])
S.go()
