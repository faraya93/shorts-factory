"""paper 1 (hook): see productions/mecanalia-es/021*/script.json. A single white sheet lies on the ground with the Moon low on the horizon; the camera pushes in low from the Moon to the sheet, which folds in half once."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import paper_rig as pr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(261, floor_z=-0.05)
m = pr.Mats(S)
pr.big(S)
sheet = pr.Sheet(m, "sheet", loc=(0.0, 0.0, 0.0))
moon = pr.moon(S, "moon", R=26.0, loc=(0.0, 270.0, 46.0))
lift = pr.av.lights(S, 1.6)
t_fold = S.t("menos.", default=7.4)


def upd(t):
    sheet.fold(pr.smooth(t_fold - 1.4, t_fold - 0.2, t))
    tgt = sp.interp([(0, (0.0, 90.0, 30.0)), (4.2, (0.0, 20.0, 12.0)), (S.T, (4.0, 0.0, 2.0))], t)
    rad = sp.interp([(0, 190.0), (4.2, 80.0), (S.T, 54.0)], t)
    el = sp.interp([(0, 2.0), (4.2, 8.0), (S.T, 32.0)], t)
    az = sp.interp([(0, 8.0), (S.T, -14.0)], t)
    pr.look(S, tgt, rad, el, az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -20, 30))
S.go()
