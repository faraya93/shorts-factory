"""rayo 3 (neumaticos): see productions/mecanalia-es/020*/script.json. A close frame on the front tyre, the camera climbs the whole bolt up to the cloud base (the sky it crossed), then comes back down to a wide frame holding the whole bolt: it does not stop at the car, an arc leaps from the rim over the rubber to the wet road. (Reshape rung 2: the tight wheel framings read only 'car'; see notes.md.)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import rayo_rig as ry  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(251, floor_z=-0.6)
m = ry.Mats(S)
dashes = ry.road(S, m)
cl = ry.storm_cloud(S, m, centre=(0.0, 20.0, 96.0))
car = ry.car(S, m, "hero")
lift = ry.lights(S)
ry.bolt(S, "bolt_sky", (0.0, 4.0, 100.0), (0.0, 0.0, ry.ROOF_TOP + 0.3), S.accent, 0.0, 0.05, r=1.0, n=12, amp=8.0, seed=3, branches=5)
t_arc = S.t("salta", default=5.6) - 0.6
ry.bolt(S, "arc_wheel", (-12.9, -9.6, 3.7), (-3.0, -16.0, 0.3), S.accent, t_arc, t_arc + 0.25, r=0.7, n=8, amp=2.2, seed=5, branches=4)
spark = S.ball("spark_pop", S.accent, 1.2, (-3.0, -16.0, 0.6))
S.pop(spark, t_arc + 0.25, 0.2)
glow = S.cyl("road_glow", 4.0, 0.12, (-3.0, -16.0, 0.08), S.accent)                           # a flat pool of accent where the arc lands
S.pop(glow, t_arc + 0.3, 0.3)
t_up, t_top, t_down = 0.6, 3.4, 4.8


def upd(t):
    ry.scroll_dashes(dashes, t, 0.0)
    k = ry.ease(sp.interp([(0, 0.0), (t_up, 0.0), (t_top, 1.0), (t_down, 1.0), (t_down + 1.0, 0.0), (S.T, 0.0)], t))
    c = ry.ease(sp.interp([(t_down - 0.4, 0.0), (t_down + 1.2, 1.0)], t))                   # settle on a wide frame that holds the whole bolt and the arc
    tx = (-13.0 + 13.0 * k) * (1 - c) + (-4.0) * c
    ty = -4.0 * (1 - c) - 6.0 * c
    tz = (4.0 + 48.0 * k) * (1 - c) + 40.0 * c
    rad = (62.0 + 170.0 * k) * (1 - c) + 215.0 * c
    el = (6.0 + 8.0 * k) * (1 - c) + 3.0 * c
    az = sp.interp([(0, 2.0), (t_top, 16.0), (S.T, 6.0)], t)
    ry.look(S, (tx, ty, tz), rad, el, az)
    lift(tx, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
