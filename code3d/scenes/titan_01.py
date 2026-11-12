"""titan 1 (hook): see productions/mecanalia-es/026*/script.json. A liner afloat on a calm sea; the camera orbits from the stern toward the bow while an iceberg drifts in ahead of the bow
and the camera pushes toward it. The tag ¿AGUJERO? hangs over the bow."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402

S = sp.Shot(213, floor_z=-36.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
sea = ti.Sea(S, m)
berg = ti.Iceberg(S, m, loc=(150.0, -26.0, ti.SEA_Z), size=(24.0, 15.0, 22.0))
lift = ti.lights(S, ti.LIGHT_K)


def upd(t):
    ship.update(open=0.0, bulk=[0.0] * ti.NB, fill=[0.0] * ti.NC, pitch=0.0)
    berg.root.location = (sp.interp([(0.0, 150.0), (S.T, 96.0)], t), -26.0, ti.SEA_Z)
    ship.root.location = (0.0, 0.0, 0.25 * math.sin(2.2 * t))
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (-10.0, 0.0, 16.0), 300.0, 16.0, -22.0), (S.T * 0.55, (10.0, 0.0, 14.0), 270.0, 14.0, -34.0), (S.T, (84.0, -8.0, 12.0), 200.0, 12.0, -52.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
