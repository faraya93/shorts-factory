"""Block B5 asset seal still, bird: flying, wings spread (the same asset, three-quarter view from below)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import bird_rig as br  # noqa: E402
import proof_kit as pk  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import wire_rig as wr  # noqa: E402


S = sp.Shot(30, floor_z=-40.0)
b = br.Bird(loc=(0.0, 0.0, 0.0), scale=1.0, rot_z=math.radians(15.0))
b.wings(1.0, flap=math.radians(14.0))
b.root.location = (0.0, 0.0, 4.0)
S.cam([(0.0, (0.0, 0.0, 6.0), 64.0, 10.0, -34.0), (S.T, (0.0, 0.0, 6.0), 64.0, 10.0, -34.0)])
rk.softboxes(0.7, centre=(0, -60, 80))
S.go()
