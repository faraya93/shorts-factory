"""Block B5 proof 028-P5 (a still): the bird in its wings-spread state, scaled large, on a pole crossarm, one wingtip on the wire, a red path through wing and body into the pole."""
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
b = br.Bird(loc=(0.0, 0.0, -1.5), scale=2.4, rot_z=math.radians(-90.0))
b.wings(1.0, flap=math.radians(8.0))
wr.dotted(m, [(0.0, 12.0, 6.0), (0.0, 4.0, 8.0), (0.0, 0.0, 6.0), (0.0, 0.0, -2.0), (0.0, 0.0, -30.0)], n=30, r=0.5)
S.cam([(0.0, (0.0, 0.0, 4.0), 90.0, 4.0, -12.0), (S.T, (0.0, 0.0, 4.0), 90.0, 4.0, -12.0)])
rk.softboxes(0.7, centre=(0, -60, 80))
S.go()
