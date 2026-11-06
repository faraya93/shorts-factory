"""dedos2 6 (cierre): one image: the wrinkled fingertip with water running sideways along its grooves (real droplets), the camera pulling back."""
import math
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import finger_rig as fr  # noqa: E402

S = sp.Shot(292)
skin = rk.wet_tissue("g_big", "#C98963", sss=0.35, rough=0.5, coat=0.22)
W = rk.water("clear_water", "#E4F5F4")
F = fr.Fingertip(S, skin, "tip", L=34.0, loc=(0, 0, 0))
F.set_wrinkle(0.0)
t1 = S.t("empapada", default=1.0)
S.every_frame(lambda t: F.set_wrinkle(sp.interp([(0, 1.0), (S.T, 1.0)], t)))
S.spin(F.obj, [(0, (0, 0, math.radians(-36))), (S.T, (0, 0, math.radians(18)))])
R = F.R
tf = S.t("canales", default=1.9)
for k in range(7):                                                              # a bead in each groove, travelling around the pad and falling off at the side
    zc = F.wl * (k + 0.5) + 0.55
    zc = min(zc, 7.0)
    d = rk.droplet(S, f"bead{k}", W, 0.26 + 0.03 * (k % 3), (R, 0, zc), pop=(tf + 0.12 * k, 0.2))
    S.every_frame(lambda t, d=d, k=k, zc=zc: setattr(d, "location", (
        (R * 1.03) * math.cos(sp.interp([(tf, 0.35), (tf + 3.6, -1.0)], t) + 0.15 * k), (R * fr.FLAT * 1.03) * math.sin(sp.interp([(tf, 0.35), (tf + 3.6, -1.0)], t) + 0.15 * k), zc)))
rk.softboxes(4.0, centre=(0, 0, 4))
S.cam([(0, (0, 0, 2.6), 15, 4, -30), (S.T * 0.5, (0, 0, 3.4), 22, 2, -12), (S.T, (0, 0, 4.2), 36, 4, 8)])
S.go()
