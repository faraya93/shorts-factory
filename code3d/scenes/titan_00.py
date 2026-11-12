"""titan 0 (asset job still, not a video scene): the liner alone, afloat on a calm sea, three-quarter view from ahead of the bow, no iceberg (neutral reading of assets/library/ocean-liner)."""
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
lift = ti.lights(S, ti.LIGHT_K)


def upd(t):
    ship.update(open=0.0, bulk=[0.0] * ti.NB, fill=[0.0] * ti.NC)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (0.0, 0.0, 14.0), 300.0, 15.0, -30.0), (S.T, (0.0, 0.0, 14.0), 300.0, 15.0, -30.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
