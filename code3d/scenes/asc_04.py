"""asc 4 (salto): see productions/mecanalia-es/017*/script.json. A cut-away car (front open) in free fall down a very tall shaft: a phone floats up off the floor on 'salto' (a jump only drifts you up inside the falling car) while the landings stream past; the camera travels beside the car."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import asc_rig as ar  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import math  # noqa: E402

S = sp.Shot(292, floor_z=0.0)
H, Z0, G, T_R = 1400.0, 1360.0, 26.0, 0.3
m = ar.Mats(S)
sh = ar.shaft(S, H, m)
cab = ar.Cab(S, m, Z0, open_front=True)
XS = [-6.5, -3.9, -1.3, 1.3, 3.9, 6.5]
rp = ar.Ropes(S, cab, m, XS, Z0 + ar.ROOF_ABOVE, H)
ph = ar.phone(S, m)
ph.parent = cab.root
ph.scale = (1.3, 1.3, 1.3)
t_j = S.t("salto", default=1.8) + 0.1
lift = ar.lights(S)


def upd(t):
    z = ar.fall_z(t, T_R, Z0, G, 8.0)
    v = ar.fall_v(t, T_R, G, Z0, 8.0)
    cab.set_z(z)
    ar.gear_set(cab, 0.0)
    rp.set(t, cut=[-1.0] * 6)
    ar.gov_set(cab.gov, (Z0 - z) / ar.GOV_R, min(1.0, v / 110.0))
    k = ar.ease((t - t_j) / 3.8)
    ph.location = (-3.5 + 2.0 * k, -3.0, 8.9 + 13.5 * k)
    ph.rotation_euler = (0.35 * k, 0.5 * math.sin(1.2 * (t - t_j)) * k, 0.4 * k)
    rad = sp.interp([(0, 120.0), (3.0, 105.0), (6.5, 125.0), (S.T, 170.0)], t)
    el = sp.interp([(0, 4.0), (S.T, -3.0)], t)
    az = sp.interp([(0, -24.0), (4.5, 0.0), (S.T, 26.0)], t)
    ar.look(S, (0.0, 0.0, z + 17.0), rad, el, az)
    lift(z - 3.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -20, 30))
S.go()
