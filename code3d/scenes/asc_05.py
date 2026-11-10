"""asc 5 (colchon): see productions/mecanalia-es/017*/script.json. The turn. The camera starts low on the pit buffer ('abajo hay un amortiguador'), cranes up the whole tall shaft to the car, the ropes go on 'chocó', and the car falls the full height and lands on the buffer's cap plate, which sinks into its sleeve and stops it on 'sobrevivió'."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import asc_rig as ar  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(339, floor_z=0.0)
H, Z0 = 790.0, 700.0
m = ar.Mats(S)
sh = ar.shaft(S, H, m)
buf = ar.Buffer(S, m)
cab = ar.Cab(S, m, Z0)
XS = [-6.5, -3.9, -1.3, 1.3, 3.9, 6.5]
rp = ar.Ropes(S, cab, m, XS, Z0 + ar.ROOF_ABOVE, H)
t_c = S.t("chocó", default=6.1)
t_hit = S.t("sobrevivió", default=9.8) + 0.1
ZC = buf.top0
G = 2.0 * (Z0 - ZC) / (t_hit - t_c) ** 2
t_up = 3.4
t_top = 5.4
cuts = [t_c + 0.06 * i for i in range(6)]
lift = ar.lights(S)


def base_z(t):
    if t <= t_c:
        return Z0, 0.0
    if t < t_hit:
        return Z0 - 0.5 * G * (t - t_c) ** 2, G * (t - t_c)
    k = min(1.0, (t - t_hit) / 0.45)
    s = buf.STROKE * (1.0 - (1.0 - k) ** 2)
    return ZC - s, 0.0


def upd(t):
    z, v = base_z(t)
    cab.set_z(z)
    buf.set(max(0.0, ZC - z))
    ar.gear_set(cab, 0.0)
    rp.set(t, cut=cuts)
    ar.gov_set(cab.gov, (Z0 - z) / ar.GOV_R, min(1.0, v / 110.0))
    if t < t_top:
        tz = sp.interp([(0, 52.0), (t_up, 56.0), (t_top, Z0 + 20.0)], t)
        rad = sp.interp([(0, 120.0), (t_up, 150.0), (t_up + 1.6, 260.0), (t_top, 250.0)], t)
    else:
        tz = z + 18.0
        rad = sp.interp([(t_top, 250.0), (t_hit, 150.0), (S.T, 130.0)], t)
    el = sp.interp([(0, 9.0), (t_up, 7.0), (t_top, 2.0), (t_hit, 0.0), (S.T, 3.0)], t)
    az = sp.interp([(0, -22.0), (t_up, -14.0), (t_top, 0.0), (t_hit, 12.0), (S.T, 18.0)], t)
    shake = sp.pulse(t, t_hit, 0.5, 1.2)
    ar.look(S, (0.0, 0.0, tz - shake), rad, el, az)
    lift(tz - 20.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -20, 30))
S.go()
