"""Block B5 proof 030-P3 (a still): the P2 section, acid drops entering the gel and fizzing, changing colour halfway down."""
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
acid = S.hero("small", "#C6E36B", rough=0.2)
fiz = S.glass("#FFFFFF", alpha=0.6, rough=0.1, name="fizz")
for i, x in enumerate((-4.5, -1.5, 1.8, 4.6)):
    S.ball(f"drop{i}", acid, 0.8, (sx + x, ctr[1] - 4.0, top + 1.8 - 1.1 * (i % 2)))
    S.ball(f"drop_mid{i}", S.hero("small", "#E9E58A", rough=0.2), 0.6, (sx + x * 0.9, ctr[1] - 4.0, top - 1.2 - 0.2 * i))
for i in range(10):
    S.ball(f"fizz{i}", fiz, 0.28, (sx - 5.0 + i * 1.1, ctr[1] - 4.0 - 3.2, top - 0.8 + 0.5 * (i % 3)))
S.cam([(0.0, (sx, ctr[1], sz), 34.0, 8.0, 0.0), (S.T, (sx, ctr[1], sz), 34.0, 8.0, 0.0)])
rk.softboxes(0.7, centre=(0, -30, 30))
S.go()
