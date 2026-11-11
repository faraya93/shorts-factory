"""avion 0 (asset job still, not a video scene): the airplane-door hero alone: an airliner with its boarding door closed, no hand, seen from the nose side (neutral reading of assets/library/airplane-door)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import avion_rig as av  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(30, floor_z=-av.JET_R - 3.0)
m = av.Mats(S)
jet = av.airliner(S, m, loc=(0, 0, 0), pane="sky", door="sky", name="jet")
av.door_swing(jet, 0.0)
lift = av.lights(S)


def upd(t):
    av.look(S, (14.0, 0.0, 4.0), 330.0, 14.0, 30.0)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(40, -30, 30))
S.go()
