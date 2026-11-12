"""Block B5 proof 027-P4 (a still): one accent figure, twelve grey figures in a loose team formation around it, full bodies in frame."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import globe_rig as gr  # noqa: E402
import paper_rig as pr  # noqa: E402
import proof_kit as pk  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402


S = sp.Shot(30, floor_z=0.0)
m = pr.Mats(S)
A = pk.accent()
pk.person(S, m, "one", (0.0, 0.0, 0.0), shirt=A, k=3.0)
for i in range(12):
    a = i / 12 * 2 * math.pi
    pk.person(S, m, f"g{i}", (14.0 * math.cos(a) * (1.0 + 0.1 * (i % 3)), 10.0 + 11.0 * math.sin(a) * (1.0 + 0.1 * (i % 2)) , 0.0), rot_z=math.radians(180) + a * 0.3, shirt=pk.GREY, k=3.0)
S.cam([(0.0, (0.0, 8.0, 5.0), 84.0, 20.0, 0.0), (S.T, (0.0, 8.0, 5.0), 62.0, 20.0, 0.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
