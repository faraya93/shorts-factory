"""rayo 2 (golpe): see productions/mecanalia-es/020*/script.json. The camera dives down the bolt to the roof: the bolt strikes, then the current sweeps over the shell as accent bars (roof, pillars, doors) while the driver inside stays dark."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import rayo_rig as ry  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(220, floor_z=-0.6)
m = ry.Mats(S)
dashes = ry.road(S, m)
cl = ry.storm_cloud(S, m, centre=(0.0, 20.0, 96.0))                                                      # high, so the bolt is a tall picture of its own
car = ry.car(S, m, "hero")
lift = ry.lights(S)
t_hit = S.t("cae", default=1.0)
ry.bolt(S, "bolt_main", (0.0, 4.0, 100.0), (0.0, 0.0, ry.ROOF_TOP + 0.3), S.accent, t_hit, t_hit + 0.3, r=1.0, n=12, amp=8.0, seed=3, branches=5, t_off=t_hit + 4.5)
ry.cage(S, S.accent, t_hit + 0.4, dt=1.4)
flash = S.ball("flash", S.accent, 3.0, (0.0, 0.0, ry.ROOF_TOP + 1.5))
S.pop(flash, t_hit + 0.25, 0.25)
S.gone(flash, t_hit + 0.9, 0.3)


def upd(t):
    ry.scroll_dashes(dashes, t, 0.0)
    az = sp.interp([(0, 8.0), (t_hit + 1.0, 12.0), (S.T, 38.0)], t)
    rad = sp.interp([(0, 240.0), (t_hit + 1.0, 230.0), (t_hit + 2.6, 80.0), (S.T, 78.0)], t)           # wide while the bolt is the picture (the car is small below it), then the dive to the roof
    el = sp.interp([(0, 3.0), (t_hit + 1.0, 3.0), (t_hit + 2.6, 14.0), (S.T, 9.0)], t)
    tz = sp.interp([(0, 52.0), (t_hit + 1.0, 52.0), (t_hit + 2.6, 20.0), (S.T, 12.0)], t)
    ry.look(S, (0.0, 0.0, tz), rad, el, az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
