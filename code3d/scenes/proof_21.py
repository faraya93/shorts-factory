"""Block B5 asset seal still, bird: perched on the middle wire, side view (two poles in frame)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import bird_rig as br  # noqa: E402
import proof_kit as pk  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import wire_rig as wr  # noqa: E402


S = sp.Shot(30, floor_z=wr.GROUND_Z)
p = S.p or {}
m = wr.Mats(pk.accent(), p.get("error", "#7A0019"))
wr.street(m, -90.0, 270.0, 90.0)
b = br.Bird(loc=(0.0, 0.0, 0.0), scale=1.0, rot_z=0.0)
S.cam([(0.0, (0.0, 0.0, 3.0), 42.0, 6.0, -10.0), (S.T, (0.0, 0.0, 3.0), 42.0, 6.0, -10.0)])
rk.softboxes(0.7, centre=(0, -60, 80))
S.go()
