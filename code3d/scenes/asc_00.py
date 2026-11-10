"""asc 0 (asset still, not a video scene): the closed car hanging on one rope in its shaft, for the asset's own blind naming (docs/current/specs/asset-system.md step 12)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import asc_rig as ar  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(30, floor_z=0.0)
H, Z0 = 330.0, 215.0
m = ar.Mats(S)
ar.shaft(S, H, m)
cab = ar.Cab(S, m, Z0)
rp = ar.Ropes(S, cab, m, [0.0], Z0 + ar.ROOF_ABOVE, H)
lift = ar.lights(S)


def upd(t):
    ar.gear_set(cab, 0.0)
    rp.set(t)
    ar.look(S, (0.0, 0.0, Z0 + 20.0), 215.0, 5.0, -10.0)
    lift(Z0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -20, 30))
S.go()
