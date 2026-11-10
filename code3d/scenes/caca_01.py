"""caca 1 (hook): see productions/mecanalia-es/016*/script.json. An empty kitchen scale beside the toilet; one stylised stool unit drops onto its platter; the camera orbits in low."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caca_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(294, floor_z=0.0)
B = cr.bathroom(S)
sx, sy = cr.SCALE_AT
cr.bathroom_scale(S)
mat = cr.stool_material(S)
P = cr.Pile(S, "units", 1, mat, seed=4, flat="upright")
t0 = S.t("caca", default=0.9) + 0.2
land = (sx, sy, 5.4)


def upd(t):
    k = sp.interp([(t0, 0.0), (t0 + 0.45, 1.0)], t)
    z = land[2] + (1.0 - k) * 38.0
    sz = 1.0 if t >= t0 else 1e-4
    P.set([(land[0], land[1], z)], [0.95 * sz])


S.every_frame(upd)
rk.softboxes(0.7, centre=(30, -20, 30))
S.cam([(0, (16.0, -16.0, 34.0), 185, 9, -14), (t0, (26.0, -22.0, 22.0), 130, 9, -8), (S.T, (30.0, -28.0, 14.0), 95, 12, 6)])
S.go()
