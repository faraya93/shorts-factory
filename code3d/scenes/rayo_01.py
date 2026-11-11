"""rayo 1 (hook): see productions/mecanalia-es/020*/script.json. A car drives along a wet road (the dashes scroll under it) beneath an ink storm cloud that flickers as charge gathers; the camera tracks alongside and drifts out."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import rayo_rig as ry  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(207, floor_z=-0.6)
m = ry.Mats(S)
dashes = ry.road(S, m)
cl = ry.storm_cloud(S, m, centre=(0.0, 20.0, 52.0))
car = ry.car(S, m, "hero")
lift = ry.lights(S)
glow = S.ball("charge", S.accent, 3.0, (0, 14.0, 47.0))
S.size(glow, [(0, 0.2), (2.0, 0.8), (4.0, 1.6), (S.T, 2.6)])
flick = [S.ball(f"flick{i}", S.accent, 1.8, (x, 10.0, 49.0 - 3 * (i % 2))) for i, x in enumerate((-30, -14, 18, 34))]
for i, f in enumerate(flick):
    S.pop(f, 1.0 + 1.3 * i, 0.3)
    S.gone(f, 1.0 + 1.3 * i + 0.5, 0.2)


def upd(t):
    ry.scroll_dashes(dashes, t, 70.0)
    car.root.rotation_euler = (0.0, 0.0, -math.pi / 2 + 0.004 * math.sin(7.0 * t))        # a little road shake
    az = sp.interp([(0, 12.0), (S.T, -14.0)], t)
    rad = sp.interp([(0, 105.0), (3.0, 115.0), (S.T, 150.0)], t)
    el = sp.interp([(0, 6.0), (S.T, 14.0)], t)
    tz = sp.interp([(0, 20.0), (S.T, 30.0)], t)
    ry.look(S, (0.0, 0.0, tz), rad, el, az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
