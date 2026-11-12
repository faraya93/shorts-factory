"""titan 5 (final): see productions/mecanalia-es/026*/script.json. Compartment after compartment fills, the bow drops further and the hull slides below the sea line (the sea closes over the
hole in the front panels). The camera pulls back sideways from the hull to the open sea and settles low."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402

S = sp.Shot(309, floor_z=-40.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
panels = ti.Panels(S, m)
lift = ti.lights(S, ti.LIGHT_K)


def upd(t):
    fill = [sp.interp([(0.2 + 0.14 * (ti.NC - 1 - k), 0.0 if k < ti.NC - 5 else 1.0), (1.4 + 0.2 * (ti.NC - 1 - k), 1.0)], t) for k in range(ti.NC)]
    pitch = sp.interp([(0.0, 0.14), (3.0, 0.24), (8.2, 0.62)], t)
    drop = sp.interp([(0.0, 3.0), (4.0, 7.0), (S.T, 52.0)], t)
    ship.update(open=1.0, fill=fill, pitch=pitch, drop=drop)
    ship.glow(None)
    panels.fill(sp.interp([(4.6, 0.0), (4.8, 1.0)], t))
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (26.0, 0.0, -4.0), 190.0, 16.0, -4.0), (4.0, (4.0, 0.0, -10.0), 280.0, 13.0, -10.0), (S.T, (0.0, 0.0, -22.0), 400.0, 8.0, -14.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
