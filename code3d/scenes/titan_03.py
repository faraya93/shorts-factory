"""titan 3 (choque): see productions/mecanalia-es/026*/script.json. The iceberg slides along the near bow plates and a row of narrow slits opens one after another at the waterline; the camera
follows the graze at water level, then the ship opens lengthwise and the camera rises to a near top-down view over the bow, where five compartments take water."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import titanic_rig as ti  # noqa: E402

S = sp.Shot(365, floor_z=-40.0)
m = ti.Mats(S)
ship = ti.Liner(S, m)
ship.add_slits(6)
sea = ti.Sea(S, m)
panels = ti.Panels(S, m)
berg = ti.Iceberg(S, m, loc=(100.0, -22.0, ti.SEA_Z), size=(20.0, 13.0, 17.0))
lift = ti.lights(S, ti.LIGHT_K)
T_OPEN = 7.3


def upd(t):
    o = sp.interp([(T_OPEN, 0.0), (T_OPEN + 2.2, 1.0)], t)
    ship.update(open=o, bulk=None, fill=[sp.interp([(T_OPEN + 1.0, 0.0), (T_OPEN + 3.2, 0.55)], t) if k >= ti.NC - 5 else 0.0 for k in range(ti.NC)],
                tints={k: "red" for k in range(ti.NC - 5, ti.NC)} if o > 0.2 else {})
    ship.glow(None)
    for o_s, x_s in ship.slits:                                       # each slit opens once the iceberg has slid past its place
        ti_s = (104.0 - x_s - 14.0) / (90.0 / (T_OPEN - 0.6))
        k_s = 0.0 if o > 0.03 else ti.ease((t - ti_s) / 0.35)
        o_s.scale = (max(ti.EPS, k_s),) * 3
    open_now = o > 0.02
    sea.slab.scale = (ti.EPS,) * 3 if open_now else (1.0, 1.0, 1.0)
    panels.show(open_now)
    bx = sp.interp([(0.0, 104.0), (T_OPEN - 0.6, 14.0)], t)
    berg.root.location = (bx, -22.0, ti.SEA_Z)
    berg.root.scale = (ti.EPS,) * 3 if open_now else (1.0, 1.0, 1.0)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (70.0, -6.0, 4.0), 215.0, 9.0, -40.0), (3.0, (52.0, -8.0, 4.0), 190.0, 9.0, -30.0), (T_OPEN - 0.4, (28.0, -9.0, 2.0), 165.0, 12.0, -18.0),
       (T_OPEN + 1.6, (30.0, 0.0, -5.0), 175.0, 40.0, -6.0), (S.T, (32.0, 0.0, -5.0), 160.0, 66.0, 0.0)])
rk.softboxes(0.7, centre=(0, -40, 60))
S.go()
