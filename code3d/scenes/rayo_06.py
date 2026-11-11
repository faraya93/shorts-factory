"""rayo 6 (consecuencia): see productions/mecanalia-es/020*/script.json. The convertible under the storm in a wide frame: a second bolt comes down toward the open car, its path turns error-red and runs through the open cabin to the seat, then the camera pushes in from above toward the seat; no harm is shown. (Reshape rung 1: the tight top-down framing read 'car with crash marks'; see notes.md.)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import rayo_rig as ry  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(182, floor_z=-0.6)
m = ry.Mats(S)
dashes = ry.road(S, m)
cl = ry.storm_cloud(S, m, centre=(0.0, 20.0, 96.0))
car = ry.car(S, m, "hero")
ry.set_roof(car, 1.0)
lift = ry.lights(S)
SEAT = (1.0, -3.0, 8.5)
t_a = 0.5
t_r = S.t("camino", default=3.5) - 0.5
ry.bolt(S, "bolt_first", (0.0, 4.0, 100.0), (SEAT[0], SEAT[1], SEAT[2] + 1.0), S.accent, t_a, t_a + 0.3, r=1.0, n=12, amp=8.0, seed=9, branches=5, t_off=t_r)
ry.bolt(S, "bolt_red", (0.0, 4.0, 100.0), (SEAT[0], SEAT[1], SEAT[2] + 1.0), S.error, t_r, t_r + 0.35, r=1.1, n=12, amp=8.0, seed=9, branches=5)
t_in = t_r + 1.2


def upd(t):
    ry.scroll_dashes(dashes, t, 0.0)
    k = ry.ease(sp.interp([(0, 0.0), (t_in, 0.0), (S.T, 1.0)], t))                      # wide while the bolt turns red, then the push in
    rad = 235.0 - 170.0 * k
    el = 3.0 + 62.0 * k
    tz = 52.0 - 43.0 * k
    az = sp.interp([(0, 10.0), (S.T, 4.0)], t)
    ry.look(S, (1.0 * k, -3.0 * k, tz), rad, el, az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
