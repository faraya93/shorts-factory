"""Block B5 proof 027-P3 (a still): the globe with one accent band and twelve grey bands stacked outward, 3/4 view."""
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


S = sp.Shot(30, floor_z=-30.0)
m = pr.Mats(S)
A = pk.accent()
g = gr.Globe(radius=10.0, loc=(0.0, 0.0, 0.0))
g.root.rotation_euler = (math.radians(-12.0), 0.0, 0.0)
gr.Bands(g, tr.plain("band_accent", A, rough=0.4), tr.plain("band_grey", pk.GREY, rough=0.5), n=13, radius=10.0, gap=0.95, thick=0.4)
S.cam([(0.0, (0.0, 0.0, 0.0), 78.0, 18.0, -28.0), (S.T, (0.0, 0.0, 0.0), 78.0, 18.0, -28.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
