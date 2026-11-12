"""Block B5 proof 026-P6 (a still): wide, the liner bow-under at 20 degrees, stern rising, half below the sea slab."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402


S = sp.Shot(30, floor_z=-60.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
sea = ti.Sea(S, m)
lift = ti.lights(S, ti.LIGHT_K)


def upd(t):
    ship.update(open=0.0, bulk=[0.0] * ti.NB, fill=[0.0] * ti.NC, pitch=0.35, drop=14.0, funnel=1.0)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (0.0, 0.0, 6.0), 380.0, 8.0, -10.0), (S.T, (0.0, 0.0, 6.0), 380.0, 8.0, -10.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
