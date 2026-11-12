"""titan 6 (cierre, the reframe): see productions/mecanalia-es/026*/script.json. One image: the flooded, bow-down hull on the sea line with every wall top lighting up in the accent, one after
another from the bow to the stern, while the camera pulls back and rises to the whole hull."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402

S = sp.Shot(295, floor_z=-40.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
panels = ti.Panels(S, m)
lift = ti.lights(S, ti.LIGHT_K)
T_PAR = S.t("paredes", 0, 1.6)


def upd(t):
    ship.update(open=1.0, fill=[1.0] * ti.NC, pitch=0.2, drop=6.0)
    ship.glow([sp.interp([(T_PAR + 0.22 * (ti.NB - 1 - i), 0.0), (T_PAR + 0.22 * (ti.NB - 1 - i) + 0.5, 1.0)], t) for i in range(ti.NB)])
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (46.0, 0.0, -4.0), 150.0, 30.0, -8.0), (S.T * 0.55, (20.0, 0.0, -4.0), 230.0, 34.0, -4.0), (S.T, (0.0, 0.0, -4.0), 310.0, 36.0, 4.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
