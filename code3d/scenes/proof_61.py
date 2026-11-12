"""Block B5 asset seal still, electric-arc: the full branching bolt across the frame."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import arc_rig as ar  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402


S = sp.Shot(30, floor_z=-40.0)
ar.Arc((0.0, 0.0, 22.0), (3.0, 0.0, -14.0), r=0.7, n=11, amp=1.1, branches=3, seed=5)
S.cam([(0.0, (0.0, 0.0, 4.0), 58.0, 4.0, 0.0), (S.T, (0.0, 0.0, 4.0), 58.0, 4.0, 0.0)])
rk.softboxes(0.3, centre=(0, -60, 80))
S.go()
