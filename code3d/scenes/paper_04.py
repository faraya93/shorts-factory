"""paper 4 (montana): a snow-capped massif behind the stack; the stack keeps growing and the camera climbs beside it, past the clouds at the mountain's waist, until the column stands above the summit."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import paper_rig as pr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(158, floor_z=-0.05)
m = pr.Mats(S)
pr.big(S)
mount = pr.mountain("mount", H=85.0, R=64.0, loc=(0.0, 150.0, 0.0))
col = pr.column(m, "stack", w=5.0, d=6.5, loc=(16.0, 20.0, 0.0), pitch=1.0)
cl = pr.clouds(S, m, 6, (0.0, 110.0, 38.0), (55.0, 24.0, 6.0), seed=7, name="cloud")
pr.sun(S, 2.4)
lift = pr.av.lights(S, 3.0)
t_a, t_b = S.t("veintisiete,", default=0.6), S.t("cima", default=1.8)


def upd(t):
    h = 6.0 + 96.0 * pr.smooth(t_a - 0.2, t_b + 1.2, t)
    pr.set_height(col, h)
    tz = 14.0 + h * 0.62
    rad = sp.interp([(0, 90.0), (S.T, 200.0)], t)
    pr.look(S, (4.0, 70.0, tz), rad, sp.interp([(0, 3.0), (S.T, 6.0)], t), sp.interp([(0, -30.0), (S.T, -10.0)], t))
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.4, centre=(0, -30, 60))
S.go()
