"""Block B5 proof 030-P2 (a still): the stomach in x-ray at left, a magnified wall section at right joined by a callout cone; layers and a thick translucent gel on the inner face."""
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
sx, sz = ctr[0] + 25.0, ctr[2] - 2.0
cone = S.cone("callout", 0.6, 7.0, 16.0, (ctr[0] + 13.0, ctr[1] - 4.0, sz), S.glass("#FFFFFF", alpha=0.25, rough=0.2, name="callout"), rot=(0, math.radians(90), 0))
parts, top = pk.wall_section(S, (sx, ctr[1] - 4.0, sz - 3.0), gel=True)
S.cam([(0.0, (ctr[0] + 12.0, ctr[1], sz), 62.0, 8.0, 0.0), (S.T, (ctr[0] + 12.0, ctr[1], sz), 62.0, 8.0, 0.0)])
rk.softboxes(0.7, centre=(0, -30, 30))
S.go()
