"""asc 3 (frenos): see productions/mecanalia-es/017*/script.json. Every rope is cut on 'todos'; the car accelerates, the landings stream past faster and faster, then on 'agarra' the rails light up around the car's base and the car stops dead. The camera starts wide, orbits down with the car and settles on its base, where the rails are gripped."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import asc_rig as ar  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(294, floor_z=0.0)
H, Z0, G = 500.0, 415.0, 14.0
m = ar.Mats(S)
sh = ar.shaft(S, H, m)
cab = ar.Cab(S, m, Z0)
XS = [-6.5, -3.9, -1.3, 1.3, 3.9, 6.5]
rp = ar.Ropes(S, cab, m, XS, Z0 + ar.ROOF_ABOVE, H)
t_c = S.t("todos", default=1.0)
t_e = S.t("agarra", default=6.2) + 0.05
D = 0.9
v_e = G * (t_e - t_c)
z_e = Z0 - 0.5 * G * (t_e - t_c) ** 2
cuts = [t_c + 0.07 * i for i in range(6)]
lift = ar.lights(S)


def zv(t):
    if t <= t_c:
        return Z0, 0.0
    if t <= t_e:
        return Z0 - 0.5 * G * (t - t_c) ** 2, G * (t - t_c)
    dt = min(t - t_e, D)
    a = v_e / D
    z = z_e - v_e * dt + 0.5 * a * dt * dt
    v = v_e * (1.0 - dt / D)
    return z, v


def upd(t):
    z, v = zv(t)
    z -= sp.pulse(t, t_e + D, 0.5, 0.7)
    cab.set_z(z)
    ar.gear_set(cab, (t - t_e) / 0.35)
    rp.set(t, cut=cuts)
    ar.gov_set(cab.gov, (Z0 - z) / ar.GOV_R, min(1.0, v / 70.0))
    tx = sp.interp([(0, 0.0), (2.6, 0.0), (4.2, 10.0), (5.3, 10.0), (6.3, 0.0), (S.T, 0.0)], t)
    off = sp.interp([(0, 15.0), (4.2, 10.0), (6.0, 4.0), (S.T, 12.0)], t)
    rad = sp.interp([(0, 235.0), (2.6, 215.0), (4.2, 130.0), (5.3, 125.0), (6.3, 175.0), (7.6, 190.0), (S.T, 200.0)], t)
    el = sp.interp([(0, 3.0), (4.2, 1.0), (6.0, 1.0), (S.T, 3.0)], t)
    az = sp.interp([(0, -8.0), (2.6, -8.0), (4.2, -22.0), (5.3, -22.0), (6.3, 6.0), (S.T, 12.0)], t)
    ar.look(S, (tx, 0.0, z + off), rad, el, az)
    lift(z + off - 20.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -20, 30))
S.go()
