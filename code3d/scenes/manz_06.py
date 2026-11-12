"""manz 6 (cierre): see productions/mecanalia-es/025*/script.json. The reframe image: the whole apple beside one enlarged seed whose shell, parted with the teal kernel glowing in the seam,
latches shut at "cápsula"; the camera eases back."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import manz_rig as mz  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

S = sp.Shot(281, floor_z=-1.0)
m = mz.Mats(S)
fr = mz.Fruit(S, m, seeds=False)
sd = mz.Seed(S, m)
tr.rbox("plinth_plate", (190, 100, 2.0), (0, 0, -1.0), m.plate, bevel=0.6)
lift = mz.lights(S, mz.LIGHT_K)
T_LATCH = S.t("cápsula", default=2.0)


def upd(t):
    fr.whole_only((-27.0, 0.0, 0.0), (0, 0, 0.45))
    gap = sp.interp([(0.0, 3.5), (T_LATCH - 0.3, 3.5), (T_LATCH + 0.3, 0.0)], t)
    bump = 0.8 * sp.pulse(t, T_LATCH + 0.25, 0.5)
    sd.set((25.0, -5.0, 5.6 + 0.5 * gap + bump), (0.0, 0.0, math.pi - 0.35), gap=gap, kernel=1.0 if gap > 0.05 else 0.0)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (0, 0, 24), 250, 12.0, -14.0), (S.T, (0, 0, 26), 310, 14.0, 8.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
