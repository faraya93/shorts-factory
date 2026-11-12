"""manz 4 (rota, the turn): see productions/mecanalia-es/025*/script.json. Two pads close on a seed lying on the plinth; at "rompe" its shell cracks open and the teal kernel bursts out as a
cloud of beads; the pads draw back."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import manz_rig as mz  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

S = sp.Shot(208, floor_z=-1.0)
m = mz.Mats(S)
sd = mz.Seed(S, m)
tr.rbox("plinth_plate", (170, 90, 2.0), (0, 0, -1.0), m.plate, bevel=0.6)
padL = S.box("pad_L", (10, 24, 22), (0, 0, 0), m.pad, bevel=1.4)
padR = S.box("pad_R", (10, 24, 22), (0, 0, 0), m.pad, bevel=1.4)
cl, dirs = mz.cloud(S, m, 34, r=1.1)
lift = mz.lights(S, mz.LIGHT_K)
T_CRACK = S.t("rompe", default=3.0)
SEED_Z = 5.6


def pads_x(t):
    return sp.interp([(0.3, 34.0), (T_CRACK - 0.1, 17.0), (T_CRACK + 1.2, 34.0)], t)


def upd(t):
    px = pads_x(t)
    for o, sgn in ((padL, -1.0), (padR, 1.0)):
        d = next(dd for ob, dd in S.items if ob is o)
        d["sw"] = ((sgn * px, 0.0, 11.0), 1.0)
    gap = sp.interp([(T_CRACK - 0.1, 0.0), (T_CRACK + 0.5, 9.0)], t)
    kern = sp.interp([(T_CRACK - 0.1, 1.0), (T_CRACK + 1.6, 0.45)], t) if t > T_CRACK - 0.1 else 0.0
    shake = 0.5 * math.sin(t * 50.0) * sp.interp([(T_CRACK - 0.9, 0.0), (T_CRACK - 0.1, 1.0), (T_CRACK, 0.0)], t)
    sd.set((shake, 0.0, SEED_Z + 0.5 * gap), (0.0, 0.0, 0.0), gap=gap, kernel=kern)
    u = max(0.0, t - T_CRACK)
    for i, (o, v) in enumerate(zip(cl, dirs)):
        d = next(dd for ob, dd in S.items if ob is o)
        if u <= 0.0:
            d["sw"] = None
            continue
        r = 48.0 * (1.0 - math.exp(-1.6 * u))
        d["sw"] = ((v.x * r, v.y * r * 0.6, SEED_Z + 8.0 + v.z * r), max(0.2, 1.0 - 0.18 * u))
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (0, 0, 8), 190, 9.0, -12.0), (T_CRACK, (0, 0, 9), 140, 8.0, 8.0), (S.T, (0, 0, 26), 250, 14.0, 0.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
