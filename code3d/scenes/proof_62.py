"""Block B5 asset seal still, electric-arc: a small arc between two points (two metal tips)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import arc_rig as ar  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402


import tape_rig as tr  # noqa: E402
S = sp.Shot(30, floor_z=-40.0)
metal = tr.plain("tips", "#9AA3AD", rough=0.3, metallic=0.9)
tr.cyl("tip_a", 0.5, 8.0, (-5.0, 0.0, 0.0), metal, axis="X")
tr.cyl("tip_b", 0.5, 8.0, (5.0, 0.0, 0.0), metal, axis="X")
ar.Arc((-1.2, 0.0, 0.0), (1.2, 0.0, 0.0), r=0.14, n=6, amp=1.3, branches=1, seed=9)
S.cam([(0.0, (0.0, 0.0, 0.0), 22.0, 6.0, 0.0), (S.T, (0.0, 0.0, 0.0), 22.0, 6.0, 0.0)])
rk.softboxes(0.3, centre=(0, -60, 80))
S.go()
