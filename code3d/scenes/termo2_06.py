"""termo2 6: see productions/mecanalia-es/009*/script.json (real thermos, transparent profile)."""
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

S = sp.Shot(139, floor_z=0.0)
P = tr.thermos(S)
window(P, 6.0, 21.5)
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
tl = S.t("tapa:", default=1.4)
S.move(cap, [(0, (0, 0, tr.H + 3.2)), (tl, (0, 0, tr.H + 3.2)), (tl + 0.8, (5, 0, tr.H + 10)), (T, (5, 0, tr.H + 10))])
tr.set_cut(P, 0.25)
S.every_frame(lambda t: setattr(P["hot"], "default_value", 0.0))
pv, pw = rk.heat_volume(S, "plume", (9, 9, 30), (0, 0, 300), "#FF7A2A", density=0.01, strength=1.2, scale=0.5)
S.every_frame(lambda t: (setattr(pv, "location", (0, 0, tr.H + 14) if t > tl + 0.2 else (0, 0, 300)), setattr(pw, "default_value", t * 0.7)))
S.cam([(0, (0, 0, 14), 96, 4, -20), (tl, (0, 0, 18), 88, 14, -8), (T, (0, 0, 22), 96, 20, 16)])
S.go()
