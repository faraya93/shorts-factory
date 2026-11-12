"""Block B5 proof 026-P3 (a still): low camera along the starboard bow, the iceberg face pressed to the plates, a row of bright slits behind the contact point."""
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
sea = ti.Sea(S, m)
berg = ti.Iceberg(S, m, loc=(16.0, -22.0, ti.SEA_Z), size=(20.0, 13.0, 17.0))
lift = ti.lights(S, ti.LIGHT_K)


def upd(t):
    ship.update(open=0.0, bulk=None, fill=[0.0] * ti.NC)
    ship.slit_state(1.0)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (30.0, -9.0, 2.0), 175.0, 10.0, -20.0), (S.T, (30.0, -9.0, 2.0), 175.0, 10.0, -20.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
