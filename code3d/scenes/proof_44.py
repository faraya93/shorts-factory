"""Block B5 proof 030-P4 (a still): the P2 section, surface cells darkened and peeling off, new rounded cells pushing up."""
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
parts, top = pk.wall_section(S, (sx, ctr[1] - 4.0, sz - 3.0), gel=False)
old = S.hero("big", "#5A3A44", rough=0.6)
new = S.hero("small", "#F29AB0", rough=0.4)
for i in range(7):
    x = sx - 5.4 + i * 1.8
    if i % 2 == 0:
        S.ball(f"old{i}", old, 0.8, (x, ctr[1] - 4.0, top + 1.5 + 0.6 * (i % 3)), shape=(1.0, 1.0, 0.75))
    S.ball(f"new{i}", new, 0.9, (x, ctr[1] - 4.0, top + 0.5), shape=(1.0, 1.4, 1.0))
S.cam([(0.0, (sx, ctr[1], sz), 34.0, 8.0, 0.0), (S.T, (sx, ctr[1], sz), 34.0, 8.0, 0.0)])
rk.softboxes(0.7, centre=(0, -30, 30))
S.go()
