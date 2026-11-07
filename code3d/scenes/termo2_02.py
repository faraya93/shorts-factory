"""termo2 2: see productions/mecanalia-es/009*/script.json (real thermos, transparent profile)."""
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


cap = tr.cap(S, CAPM, (0, 0, tr.H + 3.2))
# a cup of the same coffee beside the flask: a glossy dark surface with steam, so the liquid reads as coffee at a glance
import math as _m
CUP = rk.wet_tissue("g_pin", "#B8432F", sss=0.0, rough=0.3, coat=0.8)          # a red glazed mug: a pale mug blew out to a flat white icon in the blind reading
cup = rk.lathe("cup", [(0.0, 0.0), (2.0, 0.0), (2.5, 0.3), (3.0, 4.2), (3.1, 5.4), (2.85, 5.45), (2.7, 4.3), (2.3, 0.9), (0.0, 0.9)], CUP, loc=(11.5, -5.0, 0.0), seg=64)
S.reg(cup)
cof = rk.lathe("cup_coffee", [(0.0, 4.35), (2.72, 4.35), (2.72, 4.42), (0.0, 4.42)], rk.coffee("shell_y"), loc=(11.5, -5.0, 0.0), seg=64)
S.reg(cof)
hdl = S.torus("cup_handle", 1.4, 0.3, (11.5 + 3.4, -5.0, 3.1), CUP, rot=(_m.pi / 2, 0, 0))
sv, sw = rk.heat_volume(S, "cup_steam", (5, 5, 12), (11.5, -5.0, 11.0), "#FFFFFF", density=0.05, strength=0.05, scale=0.7)
S.every_frame(lambda t: setattr(sw, "default_value", t * 0.6))
t_cup = 3.0                                                     # the cup slides in AFTER the cut has shown the flask alone: the flask is named on its own frames, the coffee on the cup frames
for o, base in ((cup, (11.5, -5.0, 0.0)), (cof, (11.5, -5.0, 0.0)), (hdl, (11.5 + 3.4, -5.0, 3.1)), (sv, (11.5, -5.0, 11.0))):
    S.move(o, [(0, (base[0] + 60, base[1], base[2])), (t_cup, (base[0] + 60, base[1], base[2])), (t_cup + 0.55, base)])
tw = S.t("paredes", default=1.0)
def cut(t):
    tr.set_cut(P, sp.interp([(0, -9.0), (0.4, -9.0), (tw + 0.9, 0.25)], t))
S.every_frame(cut)
S.cam([(0, (3, 0, 13), 100, 16, -20), (tw, (3, 0, 13), 88, 12, -10), (T, (3, 0, 13), 76, 8, 8)])
S.go()
