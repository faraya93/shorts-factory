"""termo2 1: see productions/mecanalia-es/009*/script.json (real thermos, transparent profile)."""
import math
import sys
from pathlib import Path
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import thermos_real as tr  # noqa: E402
from termo2_common import grow_ray, wisp_steam  # noqa: E402

S = sp.Shot(261, floor_z=0.0)
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
tc = S.t("espuma", default=5.8)
S.move(cap, [(0, (0, 0, tr.H + 3.2)), (1.0, (0, 0, tr.H + 3.2)), (1.6, (0, 0, tr.H + 3.2 + 14)), (2.4, (7, 0, tr.H + 3.2 + 18)), (T, (7, 0, tr.H + 3.2 + 18))])
S.spin(cap, [(0, (0, 0, 0)), (1.0, (0, 0, 0)), (2.4, (0.5, 0.4, 0.2))])
tv, w = wisp_steam(S, "steam", (12, 12, 26), (0, 0, tr.H + 14), density=3.2, warp=0.28, gain=0.7)   # curling, wispy steam: the thin emissive box measured p90 dE 6 on lime and a straight column read as a flashlight beam (2026-11-08)
tv.location = (0, 0, 300)
S.every_frame(lambda t: (setattr(tv, "location", (0, 0, tr.H + 12) if t > 1.2 else (0, 0, 300)), setattr(w, "default_value", t * 0.6)))
S.cam([(0, (0, 0, 15), 110, 10, -30), (2.5, (0, 0, 16), 86, 22, 0), (5.5, (0, 0, 18), 66, 6, 30), (T, (0, 0, 15), 60, 4, 55)])
S.go()
