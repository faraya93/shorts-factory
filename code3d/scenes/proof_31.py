"""Block B5 proof 027-P1 (a still): the globe on the stage, a single file of figures leaving the stage edge in the foreground and wrapping the globe as an accent band; mid pull-back."""
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
amat = tr.plain("band_accent", A, rough=0.4)
g = gr.Globe(radius=10.0, loc=(0.0, 18.0, 13.0))
g.root.rotation_euler = (math.radians(-12.0), 0.0, 0.0)
gr.Bands(g, amat, amat, n=1, radius=10.0, thick=0.9)
for i in range(10):                                                     # the single file: from the stage edge toward the globe, then up its band
    pk.person(S, m, f"p{i}", (-6.0 + 1.2 * i, -34.0 + 4.6 * i, 0.0), rot_z=math.radians(-4.0), shirt=A, k=2.6 - 0.12 * i)
S.cam([(0.0, (0.0, 4.0, 10.0), 105.0, 14.0, -8.0), (S.T, (0.0, 4.0, 10.0), 105.0, 14.0, -8.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
