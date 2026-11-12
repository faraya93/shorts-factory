"""titan 4 (desborde, the turn): see productions/mecanalia-es/026*/script.json. The hull is open lengthwise with its five bow compartments taking water; the bow dips; the walls do not reach the
top, so the water climbs and spills over each wall into the next compartment, aft, one after another; the open wall tops light up in the accent at "arriba". The camera rides high over the
bow and travels toward the stern with the spill."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402

S = sp.Shot(308, floor_z=-40.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
panels = ti.Panels(S, m)
lift = ti.lights(S, ti.LIGHT_K)
T_UP = S.t("arriba", 0, 3.6)
Q0, DQ = 3.6, 1.15                          # the first spill starts here; each next wall follows after DQ seconds


def upd(t):
    full = sp.interp([(0.2, 0.55), (3.0, 1.0)], t)
    fill = [full if k >= ti.NC - 5 else 0.0 for k in range(ti.NC)]
    spill = {}
    for q in range(5):
        j = ti.NC - 6 - q                    # the wall between compartment j and j + 1; the water pours into compartment j
        ts = Q0 + DQ * q
        rf = sp.interp([(ts + 0.4, 0.0), (ts + 1.6, 1.0)], t)
        fill[j] = rf
        amt = min(1.0, max(0.0, (t - ts) / 0.4)) * (1.0 - sp.interp([(ts + 1.4, 0.0), (ts + 1.9, 1.0)], t))
        spill[j] = (amt, rf)
    pitch = sp.interp([(0.0, 0.02), (4.0, 0.14)], t)
    ship.update(open=1.0, fill=fill, pitch=pitch, drop=sp.interp([(0.0, 0.5), (S.T, 3.0)], t), spill=spill, tints={k: "red" for k in range(ti.NC - 5, ti.NC)})
    ship.glow([sp.interp([(T_UP + 0.1 * (ti.NB - 1 - i), 0.0), (T_UP + 0.1 * (ti.NB - 1 - i) + 0.4, 1.0)], t) if i >= ti.NC - 8 else 0.0 for i in range(ti.NB)])
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (42.0, 0.0, -4.0), 130.0, 44.0, -10.0), (4.0, (28.0, 0.0, -4.0), 115.0, 50.0, -4.0), (S.T, (-6.0, 0.0, -4.0), 140.0, 40.0, 8.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
