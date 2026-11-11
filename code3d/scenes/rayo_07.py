"""rayo 7 (cierre): see productions/mecanalia-es/020*/script.json. The single reframe image: the roof slides back onto the car, a bolt hits it, the accent cage lights around the driver and the current runs around the shell into the road, while the camera pulls back to the whole car under the storm."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import rayo_rig as ry  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(413, floor_z=-0.6)
m = ry.Mats(S)
dashes = ry.road(S, m)
cl = ry.storm_cloud(S, m, centre=(0.0, 20.0, 56.0))
car = ry.car(S, m, "hero")
lift = ry.lights(S)
t_roof = 0.6
t_hit = S.t("techo", default=3.0)
ry.bolt(S, "bolt_final", (0.0, 4.0, 60.0), (0.0, 0.0, ry.ROOF_TOP + 0.3), S.accent, t_hit, t_hit + 0.25, r=0.55, n=11, amp=4.5, seed=3, branches=4)
ry.cage(S, S.accent, t_hit + 0.3, dt=1.2)
N = 30
src = S.ball("bead_src", S.accent, 0.55)
t_flow = t_hit + 1.6
PATH = lambda s: [(0.0, 0.0, ry.ROOF_TOP), (0.0, s * ry.CW, ry.ROOF_TOP), (0.0, s * ry.CW, ry.SILL), (0.0, s * (ry.CW + 2.5), 0.4)]


def bead(i, t):
    s = 1 if i % 2 else -1
    if t < t_flow:
        return None
    k = ((t - t_flow) * 0.55 + i / N) % 1.0
    pts = PATH(s)
    seg = k * (len(pts) - 1)
    j = min(int(seg), len(pts) - 2)
    f = seg - j
    p = tuple(a + (b - a) * f for a, b in zip(pts[j], pts[j + 1]))
    return ((p[0] + ((i * 7) % 11 - 5) * 1.6, p[1], p[2]), 1.0)


S.swarm(N, src, bead)


def upd(t):
    ry.scroll_dashes(dashes, t, 0.0)
    ry.set_roof(car, sp.interp([(t_roof, 1.0), (t_roof + 1.6, 0.0)], t))
    az = sp.interp([(0, 14.0), (S.T, -16.0)], t)
    rad = sp.interp([(0, 85.0), (t_hit, 100.0), (S.T, 235.0)], t)
    el = sp.interp([(0, 28.0), (t_hit, 12.0), (S.T, 9.0)], t)
    tz = sp.interp([(0, 12.0), (t_hit + 1.0, 18.0), (S.T, 32.0)], t)
    ry.look(S, (0.0, 0.0, tz), rad, el, az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
