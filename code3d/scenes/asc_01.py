"""asc 1 (hook): see productions/mecanalia-es/017*/script.json. The belief: a car hangs by ONE rope in a tall shaft; the rope snaps on 'caerías' and the car drops floor by floor, the camera tracking it down to the pit."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import asc_rig as ar  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(257, floor_z=0.0)
H, Z0, FLOOR, G = 330.0, 215.0, 8.0, 92.0
m = ar.Mats(S)
sh = ar.shaft(S, H, m)
cab = ar.Cab(S, m, Z0)
rp = ar.Ropes(S, cab, m, [0.0], Z0 + ar.ROOF_ABOVE, H)
t_cut = S.t("caerías", default=3.8)
t_land = t_cut + math.sqrt(2 * (Z0 - FLOOR) / G)
lift = ar.lights(S)


def upd(t):
    z = ar.fall_z(t, t_cut, Z0, G, FLOOR)
    if t_cut - 0.35 < t < t_cut:
        z += 0.5 * math.sin(70.0 * t) * (t - (t_cut - 0.35)) / 0.35            # the rope strains before it goes
    p = sp.pulse(t, t_land, 0.35)
    cab.root.scale = (1 + 0.05 * p, 1 + 0.05 * p, 1 - 0.14 * p)
    cab.set_z(z)
    rp.set(t, cut=[t_cut])
    ar.gear_set(cab, 0.0)
    tz = z + 18.0
    rad = sp.interp([(0, 235.0), (t_cut, 215.0), (t_land, 170.0), (S.T, 160.0)], t)
    el = sp.interp([(0, 6.0), (t_cut, 4.0), (t_land, 0.0), (S.T, -2.0)], t)
    az = sp.interp([(0, -14.0), (t_cut, -8.0), (t_land, 6.0), (S.T, 10.0)], t)
    ar.look(S, (0.0, 0.0, tz), rad, el, az)
    lift(tz - 20.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -20, 30))
S.go()
