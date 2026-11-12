"""Block B5 proof 026-P5 (a still): x-ray hull tilted bow-down 8 degrees, water pouring over the open top of the fifth wall into the sixth box; no tray in frame."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402


S = sp.Shot(30, floor_z=-40.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
panels = ti.Panels(S, m)
lift = ti.lights(S, ti.LIGHT_K)
K = ti.NC - 6                                                             # the wall between the fifth and the sixth box from the bow


def upd(t):
    fill = [1.0 if k > K else (0.25 if k == K else 0.0) for k in range(ti.NC)]
    ship.update(open=1.0, bulk=None, fill=fill, pitch=0.14, drop=2.0, spill={K: (1.0, 0.25)}, funnel=1.0)
    ship.glow(None)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (ti.BULK_X[K], 0.0, 2.0), 170.0, 24.0, -6.0), (S.T, (ti.BULK_X[K], 0.0, 2.0), 170.0, 24.0, -6.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
