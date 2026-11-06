"""dedos2 3 (surcos): macro of a real fingertip: smooth, then the pulp loses volume and the pad folds into grooves (real mesh deformation, wet subsurface skin)."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import finger_rig as fr  # noqa: E402

S = sp.Shot(154)
skin = rk.wet_tissue("g_big", "#C98963", sss=0.35, rough=0.5, coat=0.22)
F = fr.Fingertip(S, skin, "tip", loc=(0, 0, 0))
t1, t2 = S.t("jala", default=2.2), S.t("surcos", default=3.7)
S.every_frame(lambda t: F.set_wrinkle(sp.interp([(0, 0.0), (t1 - 0.2, 0.0), (t2 + 0.5, 1.0)], t)))
S.spin(F.obj, [(0, (0, 0, math.radians(-28))), (S.T, (0, 0, math.radians(30)))])
rk.softboxes(4.5, centre=(0, 0, 4))
S.cam([(0, (0, 0, 3.4), 24, 8, -40), (S.T * 0.6, (0, 0, 2.8), 17, -4, 6), (S.T, (0, 0, 2.4), 13.5, -10, 38)])
S.go()
