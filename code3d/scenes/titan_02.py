"""titan 2 (diseño): see productions/mecanalia-es/026*/script.json. The liner opens lengthwise (the deck and deckhouse lift off, the near half of the hull swings away); fifteen walls rise one
after another from the stern and split the hull into sixteen compartments; at "cuatro" the four bow compartments take water, light up in the accent, and the ship still floats on the sea line.
The camera travels along the hull from the stern to the bow."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402

S = sp.Shot(306, floor_z=-40.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
panels = ti.Panels(S, m)
lift = ti.lights(S, ti.LIGHT_K)
t_dies, t_cuatro = S.t("dieciséis", 0, 3.6), S.t("cuatro", 0, 6.4)


def upd(t):
    o = sp.interp([(0.2, 0.0), (2.2, 1.0)], t)
    bulk = [sp.interp([(t_dies - 1.4 + 0.12 * i, 0.0), (t_dies - 0.9 + 0.12 * i, 1.0)], t) for i in range(ti.NB)]
    f4 = sp.interp([(t_cuatro, 0.0), (t_cuatro + 1.8, 0.92)], t)
    fill = [f4 if k >= ti.NC - 4 else 0.0 for k in range(ti.NC)]
    tints = {k: "accent" for k in range(ti.NC - 4, ti.NC)} if t > t_cuatro else {}
    dip = sp.interp([(t_cuatro, 0.0), (t_cuatro + 2.0, 1.0)], t)
    ship.update(open=o, bulk=bulk, fill=fill, pitch=0.03 * dip, drop=0.8 * dip, tints=tints, funnel=1.0)
    ship.glow(None)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (-46.0, 0.0, 2.0), 175.0, 22.0, 0.0), (S.T * 0.5, (0.0, 0.0, 2.0), 155.0, 28.0, -6.0), (S.T, (44.0, 0.0, 2.0), 140.0, 30.0, 4.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
