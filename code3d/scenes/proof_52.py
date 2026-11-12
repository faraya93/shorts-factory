"""Block B5 proof 028-P2 and W1 (a still): low along the wire, accent pulses inside a translucent jacket racing toward the camera, poles receding. W1 renders this same frame at the final profile."""
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
wr.street(m, -60.0, 700.0, 90.0, core=True)
wr.beads(m, (60.0, 20.0, -20.0))
S.cam([(0.0, (-40.0, 0.0, 0.0), 120.0, 2.0, 86.0), (S.T, (-40.0, 0.0, 0.0), 120.0, 2.0, 86.0)])
rk.softboxes(0.7, centre=(0, -60, 80))
S.go()
