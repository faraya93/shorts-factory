"""oido 3 (palito): see productions/mecanalia-es/024*/script.json. The swab swings in from the camera side to the canal axis and goes in; its cotton skims the wax lining at the entrance
into a pile in front of the tip, then pushes the pile deeper while the skin bands keep sliding outward; the camera follows the tip."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import oido_rig as od  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(238, floor_z=-2.0 * od.KS)
m = od.Mats(S)
ear = od.Ear(S, m)
cv = od.Conveyor(S, m, nb=7, nf=6, nd=0 + 1)
sw = od.Swab(S, m)
lift = od.lights(S, od.LIGHT_K)
T_SCOOP = S.t("Saca", default=2.0)
T_PUSH = S.t("empuja", default=4.0)
OFFS = [(2.5, 1.5, 0.0), (4.5, 3.0, 3.0), (4.8, 2.0, -3.2), (7.0, 3.5, 0.5), (7.2, 2.0, 3.6), (7.4, 2.6, -3.4), (9.6, 3.0, 0.2), (9.9, 2.4, 2.6)]
pile = od.lumps(S, m, "wax_pile", [(0, 0, 0)] * len(OFFS), r=3.1)


def tip_x(t):
    return sp.interp([(0.0, 2.0), (T_SCOOP - 0.6, 8.0), (T_SCOOP + 1.2, 16.0), (T_PUSH, 18.0), (S.T - 0.4, 36.0)], t)


def upd(t):
    cv.update(t, 6.0, bands_on=1.0, flakes_on=1.0, dust_on=0.0)
    x = tip_x(t)
    k = sp.interp([(0.0, 0.0), (T_SCOOP - 0.6, 1.0)], t)                                     # 0 = coming from the camera side, 1 = along the canal axis
    sw.tip_at(x, sp.lerp(-20.0, 1.5, k), od.CZ + sp.lerp(2.0, 0.0, k), tilt=sp.lerp(1.75, 0.0, k), pitch=sp.lerp(0.1, 0.0, k))
    ear.lining.scale = (1e-4,) * 3 if x > 11.0 else (1.0, 1.0, 1.0)                       # the cotton has taken the lining along
    for o, (dx, dy, dz) in zip(pile, OFFS):
        d = next(dd for ob, dd in S.items if ob is o)
        on = 1.0 if x > 11.0 else 0.0
        grow = min(1.0, max(0.0, (x - 11.0) / 3.0)) * on
        d["sw"] = None if grow < 0.05 else (od.P(x + dx, dy, od.CZ + dz), grow)
    lift(0.0, 0.0)


for o, d in S.items:
    if o in pile:
        d["sw"] = None                                                                      # placed per frame by upd (the swarm branch of Shot._update)
S.every_frame(upd)
S.cam([(0.0, od.P(4, -4, 34), od.R(215), 12.0, -34.0), (S.T * 0.45, od.P(8, 0, 34), od.R(240), 10.0, -34.0), (S.T, od.P(26, 0, 34), od.R(190), 8.0, -16.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
