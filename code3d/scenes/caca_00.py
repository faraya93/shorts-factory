"""caca 0 (asset still, not a video scene): the stool unit alone on the stage, for the asset's own blind naming (docs/current/specs/asset-system.md step 12)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caca_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(30, floor_z=0.0)
mat = cr.stool_material(S)
P = cr.Pile(S, "units", 1, mat, seed=4, flat="upright")
P.set([(0.0, 0.0, 0.0)], [1.4])
rk.softboxes(0.7, centre=(0, -20, 20))
S.cam([(0, (0.0, 0.0, 5.0), 60, 14, -12), (S.T, (0.0, 0.0, 5.0), 60, 14, -12)])
S.go()
