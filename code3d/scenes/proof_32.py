"""Block B5 proof 027-P2 (a still): rows of grey figures behind a front row of accent-shirted figures, filling the stage, camera at head height."""
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
pk.crowd(S, m, rows=6, per_row=9, x0=-26.0, dx=6.4, y0=6.0, dy=6.5, shirt=pk.GREY, k=2.4, tag="g")
for i in range(7):
    pk.person(S, m, f"f{i}", (-19.0 + i * 6.4, -5.0, 0.0), rot_z=0.1 * (i % 3 - 1), shirt=A, k=2.4)
S.cam([(0.0, (0.0, 10.0, 4.0), 95.0, 6.0, 0.0), (S.T, (0.0, 10.0, 4.0), 95.0, 6.0, 0.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
