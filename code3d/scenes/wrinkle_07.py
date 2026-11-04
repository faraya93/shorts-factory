"""pieles-arrugadas 7 (cierre): the grooved fingertip turns into a tyre and back; pool, five raisin-fingers come up; ENVÍASELO tag in the cream space."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import wrinkle_rig as wr  # noqa: E402

S = sp.Shot(273)
M = wr.palette(S)
t_lla, t_act, t_pis, t_ded = S.t("llantas", default=1.9), S.t("activa.", default=3.2), S.t("piscina", default=6.8), S.t("dedos", default=7.5)
f = wr.Finger(S, M, 0.0, 14.0, "main", rings=6, pop=(0.1, 0.3))
S.move(f.root, [(0.1, (0, 0, 14.0)), (1.0, (0, 0, 4.2))])
f.show_rings(1.0, 0.12, 0.3)
S.gone(f.root, t_lla, 0.3)
# tyre: a cylinder with groove rings, rolls on a wet road
road = S.box("road", (16.0, 5.0, 0.5), (0, 0, -0.1), M["plate"], bevel=0.2, pop=(t_lla - 0.3, 0.4))
film = S.box("film", (15.0, 4.2, 0.2), (0, 0, 0.25), M["water"], bevel=0.08, pop=(t_lla - 0.2, 0.4))
tyre = S.cyl("tyre", 3.2, 2.6, (-6.0, 0, 3.4), S.ink, axis="Y", verts=64, bevel=0.35, pop=(t_lla, 0.35))
S.move(tyre, [(t_lla, (-6.0, 0, 3.4)), (t_act, (3.0, 0, 3.4))])
S.spin(tyre, [(t_lla, (0, 0, 0)), (t_act, (0, 4.5, 0))])
S.gone(tyre, t_act - 0.1, 0.3); S.gone(road, t_act + 0.2, 0.4); S.gone(film, t_act + 0.2, 0.4)
f2 = wr.Finger(S, M, 0.0, 4.2, "back", rings=6, pop=(t_act, 0.35))
f2.show_rings(t_act + 0.1, 0.05, 0.25)
# pool + five raisin-fingers
pool = wr.tank(S, M, w=15.0, d=4.4, h=3.6, pop=(t_pis, 0.5))
S.gone(f2.root, t_pis - 0.5, 0.4)
xs = (-5.2, -2.6, 0.0, 2.6, 5.2)
for i, x in enumerate(xs):
    g = wr.Finger(S, M, x, 1.2, f"raisin{i}", rings=6, pop=(t_ded + 0.12 * i, 0.3))
    S.move(g.root, [(t_ded + 0.12 * i, (x, 0, 0.6)), (t_ded + 0.12 * i + 0.7, (x, 0, 6.2 + 0.6 * (i % 2)))])
    g.show_rings(t_ded + 0.12 * i + 0.1, 0.03, 0.2)
S.cam([(0, (0, 0, 6), 36, 10, -18), (t_lla, (0, 0, 4.5), 26, 6, 8), (t_act + 0.5, (0, 0, 5), 30, 12, -6), (t_pis, (0, 0, 5.5), 40, 16, 6), (S.T, (0, 0, 6.5), 34, 10, -4)])
S.go()
