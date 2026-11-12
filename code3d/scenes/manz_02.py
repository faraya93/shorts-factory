"""manz 2 (amigdalina): see productions/mecanalia-es/025*/script.json. The opened apple (cut faces to the camera); the camera pushes into the left half's core, where one seed sits in its cavity
standing tip up; its shell parts to a slit and the teal kernel glows inside it. Ladder rung 4 (context staging): the seed is read inside the apple's core, not on its own (rung 1 wide with the
halves behind it and rung 2 upright and alone both read as a chocolate egg or clam)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import manz_rig as mz  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

S = sp.Shot(198, floor_z=-1.0)
m = mz.Mats(S)
fr = mz.Fruit(S, m, skip=(("L", 0),))
K_IN = 1.25
sd = mz.Seed(S, m, L=mz.SEED_L * K_IN, W=mz.SEED_W * K_IN)
tr.rbox("plinth_plate", (170, 90, 2.0), (0, 0, -1.0), m.plate, bevel=0.6)
lift = mz.lights(S, mz.LIGHT_K)
T_OPEN = S.t("amigdalina,", default=3.0)
CAV = (-27.9, -0.9, 24.5)                                                          # the left half's first cavity (world), cut face toward the camera


def upd(t):
    fr.split(1.0)
    gap = sp.interp([(T_OPEN, 0.0), (T_OPEN + 1.0, 0.9)], t)
    kern = sp.interp([(T_OPEN, 0.0), (T_OPEN + 0.6, 1.0)], t)
    sd.set(CAV, (0.0, -math.pi / 2, 0.0), gap=gap, k=1.0, kernel=kern)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (0, 0, 32), 270, 12.0, 0.0), (S.T * 0.4, (-27, -1, 26), 120, 8.0, 0.0), (S.T * 0.75, (-26.5, -1, 25), 64, 5.0, 2.0), (S.T, (-26.5, -1, 25), 56, 4.0, 4.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
