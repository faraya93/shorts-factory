"""caca 4 (vida): see productions/mecanalia-es/016*/script.json. The mound becomes a hill on one end of a giant see-saw; two cars sit on the other end; the plank tips toward the hill; the camera cranes up to a high plan view. The toilet stays at the foot of the hill (context cue)."""
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import caca_rig as cr  # noqa: E402
import caca_set as cs  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(202, floor_z=0.0)
S.stage.cam.data.clip_end = 40000.0
S.stage.cam.data.lens = 28.0                                                   # wide: a 760 cm plank must fit a portrait frame
cs.widen_floor(8.0)
B = cr.bathroom(S)
B.root.location = (-250.0, -335.0, 0.0)
PIV = (0.0, -60.0, 78.0)
plank, fulc = cs.seesaw(S, PIV, length=760.0, width=460.0)
CA = cs.car(S, loc=(0, 0, 0))
CB = cs.car(S, loc=(0, 0, 0))
for car, x in ((CA, 195.0), (CB, 320.0)):
    car.root.parent = plank
    car.root.location = (x, 0.0, -15.8)
P = cs.LitePile(S, "units", cs.N_UNITS, cr.stool_material(S), seed=7)
A = {"centre": (-250.0, 0.0), "radius": 70.0, "height": 60.0}
Z = {"centre": (-245.0, 0.0), "radius": 185.0, "height": 170.0}
t0 = S.t("tres", default=0.4)
t1 = S.t("autos", default=5.0)
AMP = 7.0


def ang(t):
    return sp.interp([(0, AMP), (t0, AMP), (t1, -AMP), (S.T, -AMP)], t)


def upd(t):
    k = sp.interp([(t0, 0.0), (t1 - 0.4, 1.0)], t)
    loc = cs.lerp_mound(cs.N_UNITS, A, Z, k)
    loc[:, 2] += 8.0 + 4.0 * (1.0 - k)
    sz = np.full(cs.N_UNITS, 1.4 + (3.4 - 1.4) * k)
    a = ang(t)
    world = cs.rot_y(loc, a, (0.0, 0.0, 0.0))                                    # plank-local -> rotated about the fulcrum, then moved to the fulcrum
    world[:, 1] += PIV[1]
    world[:, 2] += PIV[2]
    P.set(world, sz)
    plank.rotation_euler = (0.0, math.radians(a), 0.0)


S.every_frame(upd)
rk.softboxes(0.8, centre=(0, -60, 120))
S.cam([(0, (-170.0, -80.0, 100.0), 520, 8, -20), (S.T * 0.5, (-20.0, -60.0, 120.0), 900, 24, -4), (S.T, (30.0, -60.0, 40.0), 1550, 64, 0)])
S.go()
