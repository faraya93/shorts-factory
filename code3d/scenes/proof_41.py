"""Block B5 proof 030-P1 (a still): inside the stomach, a pink-brown meat chunk in glowing acid, its surface frayed into strands."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import chicle_rig as cr  # noqa: E402
import proof_kit as pk  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402


S = sp.Shot(30, floor_z=-60.0)
cr.backing(S)
T = cr.tract(S, loc=(0.0, 0.0, 0.0))
ctr = T.at(cr.frac_of(6))
meat = S.hero("big", "#B8605A", rough=0.55, coat=0.1)
chunk = cr.gum_piece(S, meat, "meat", r=3.2, loc=(ctr[0], ctr[1] - 3.0, ctr[2]))
fray = [cr.strand(S, f"fray{i}", (ctr[0] + 2.6 * math.cos(a), ctr[1] - 3.0, ctr[2] + 1.2 * math.sin(a)), (ctr[0] + 4.6 * math.cos(a), ctr[1] - 3.0, ctr[2] - 3.4), r=0.18, mat=meat)
        for i, a in enumerate((0.3, 1.1, 2.0, 2.9, 3.8, 4.7, 5.6))]
pool = cr.acid(S, (ctr[0], ctr[1] - 3.0, ctr[2] - 3.4), (7.0, 4.0, 2.6))
glow = S.emit("#D7F25A", 1.4, name="acid_glow")
S.ball("acid_core", glow, 1.0, (ctr[0], ctr[1] - 3.0, ctr[2] - 3.6), shape=(5.4, 2.4, 1.0))
S.cam([(0.0, ctr, 34.0, 6.0, 0.0), (S.T, ctr, 34.0, 6.0, 0.0)])
rk.softboxes(0.7, centre=(0, -30, 30))
S.go()
