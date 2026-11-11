"""rayo 4 (jaula): see productions/mecanalia-es/020*/script.json. The camera orbits the car once: its shell turns into a cage of accent bars around the seated driver, and beads of current run over the roof and down both flanks into the road."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import rayo_rig as ry  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(190, floor_z=-0.6)
m = ry.Mats(S)
dashes = ry.road(S, m)
car = ry.car(S, m, "hero")
lift = ry.lights(S)
t_c = S.t("carrocería", default=1.2)
ry.cage(S, S.accent, t_c, dt=1.3)
N = 30
src = S.ball("bead_src", S.accent, 0.55)
t_flow = t_c + 1.4
PATH = lambda s: [(0.0, 0.0, ry.ROOF_TOP), (0.0, s * ry.CW, ry.ROOF_TOP), (0.0, s * ry.CW, ry.SILL), (0.0, s * (ry.CW + 2.5), 0.4)]


def bead(i, t):
    s = 1 if i % 2 else -1
    k = ((t - t_flow) * 0.55 + i / N) % 1.0
    if t < t_flow:
        return None
    pts = PATH(s)
    seg = k * (len(pts) - 1)
    j = min(int(seg), len(pts) - 2)
    f = seg - j
    p = tuple(a + (b - a) * f for a, b in zip(pts[j], pts[j + 1]))
    x_off = ((i * 7) % 11 - 5) * 1.6
    return ((p[0] + x_off, p[1], p[2]), 1.0)


S.swarm(N, src, bead)


def upd(t):
    ry.scroll_dashes(dashes, t, 0.0)
    az = sp.interp([(0, 0.0), (S.T, 340.0)], t)
    rad = sp.interp([(0, 125.0), (S.T, 140.0)], t)
    el = sp.interp([(0, 10.0), (S.T, 22.0)], t)
    ry.look(S, (0.0, 0.0, 11.0), rad, el, az)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
