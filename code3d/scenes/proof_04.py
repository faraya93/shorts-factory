"""Block B5 proof 026-P4 (a still): x-ray hull, the first five bow boxes filled with blue water, the slits open at the waterline, bow dipped 3 degrees."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402


S = sp.Shot(30, floor_z=-40.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
ship.add_slits(6)
panels = ti.Panels(S, m)
lift = ti.lights(S, ti.LIGHT_K)


def upd(t):
    ship.update(open=1.0, bulk=None, fill=[0.9 if k >= ti.NC - 5 else 0.0 for k in range(ti.NC)], pitch=0.052, drop=0.8, tints={k: "red" for k in range(ti.NC - 5, ti.NC)}, funnel=1.0)
    ship.glow(None)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (6.0, 0.0, 2.0), 300.0, 22.0, -4.0), (S.T, (6.0, 0.0, 2.0), 300.0, 22.0, -4.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
