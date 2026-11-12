"""Block B5 proof 026-P1 (a still, not a video scene): the liner 3/4 from the bow, the iceberg ahead of it at the waterline."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402


S = sp.Shot(30, floor_z=-36.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
sea = ti.Sea(S, m)
berg = ti.Iceberg(S, m, loc=(ti.L / 2 + 38.0, -14.0, ti.SEA_Z), size=(26.0, 17.0, 24.0))
lift = ti.lights(S, ti.LIGHT_K)


def upd(t):
    ship.update(open=0.0, bulk=[0.0] * ti.NB, fill=[0.0] * ti.NC)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (32.0, -6.0, 8.0), 330.0, 14.0, -40.0), (S.T, (32.0, -6.0, 8.0), 330.0, 14.0, -40.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
