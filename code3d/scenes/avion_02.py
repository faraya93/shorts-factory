"""avion 2 (tapon): see productions/mecanalia-es/019*/script.json. The cabin seen down its aisle, the door at the far end wider than its hole and held against the frame stops (accent): it slides inward toward the camera, turns edge-on, and only then goes out through the hole like a plug."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import avion_rig as av  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(212, floor_z=av.FLOOR_Z - 4.0)
m = av.Mats(S)
ai = av.aisle(S, m, door=True, passengers=((-8, -14, 1), (8, 24, 2), (-24, 14, 0)))
lift = av.lights(S)
w = S.t("moverse", default=4.2)
t_in, t_turn, t_out, t_end = w - 0.2, w + 0.9, S.t("tapón", default=5.8) - 0.7, S.t("tapón", default=5.8) + 0.8


def upd(t):
    av.door_plug(ai, t, t_in, t_turn, t_out, t_end)
    rad = sp.interp([(0, 150.0), (3.0, 108.0), (S.T, 100.0)], t)
    az = sp.interp([(0, -97.0), (S.T, -84.0)], t)
    av.look(S, (40.0, 0.0, 6.0), rad, 5.0, az)
    lift(40.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(10, 0, 40))
S.go()
