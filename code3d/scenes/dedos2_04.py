"""dedos2 4 (canales): two fingertips on a wet glass pane. The smooth one rides on a film of water (a gap under it); the wrinkled one presses and the water leaves through its grooves."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import finger_rig as fr  # noqa: E402

S = sp.Shot(174)
skin = rk.wet_tissue("g_big", "#C98963", sss=0.35, rough=0.5, coat=0.22)
G, W = rk.glass(), rk.water("clear_water", "#E4F5F4")
rk.noshadow(S.box("pane", (40, 14, 1.4), (0, 0, -0.7), G, bevel=0.15))
rk.contact_shadow(S, (0, 0, -1.4), 22, 0.45)
R, th = fr.R_DEFAULT, math.radians(78)
X0 = 3.4
tc = S.t("canales", default=1.0)
fL = fr.Fingertip(S, skin, "fL", L=7.0, loc=(-X0, 0, R + 0.5))
fR = fr.Fingertip(S, skin, "fR", L=7.0, loc=(X0, 0, R + 1.8))
fL.obj.rotation_euler = (0, th, math.pi)
fR.obj.rotation_euler = (0, th, 0)
fR.set_wrinkle(1.0)
xc = R * math.sin(th)                                                         # where the lowest point of the pad lies along the shaft
film = rk.droplet(S, "film", W, 1.0, (-X0 - xc, 0, 0.2), sc=[(0, (2.9, 1.9, 0.2))])
film2 = rk.droplet(S, "film2", W, 1.0, (X0 + xc, 0, 0.2), sc=[(0, (2.9, 1.9, 0.2)), (tc + 0.5, (2.9, 1.9, 0.2)), (tc + 1.8, (1.6, 1.0, 0.03))])
S.move(fL.obj, [(0, (-X0, 0, R + 0.5)), (S.T, (-X0 - 1.5, 0, R + 0.5))])                       # the smooth tip rides on the film, drifting sideways
S.move(film, [(0, (-X0 - xc, 0, 0.2)), (S.T, (-X0 - xc - 1.5, 0, 0.2))])
S.move(fR.obj, [(0, (X0, 0, R + 1.8)), (tc + 0.3, (X0, 0, R + 1.8)), (tc + 1.7, (X0, 0, R + 0.03)), (S.T, (X0, 0, R + 0.03))])
for i in range(8):                                                             # the water leaves through the grooves (sideways, out of the contact patch)
    sg = 1 if i % 2 else -1
    r_ = 0.34 + 0.05 * (i % 3)
    a, b = X0 + xc - 1.2 + 0.35 * i, X0 + xc - 1.2 + 0.2 * i
    d = rk.droplet(S, f"drop{i}", W, r_, (a, sg * 0.4, r_), pop=(tc + 1.0 + 0.09 * i, 0.2))
    S.move(d, [(tc + 1.0 + 0.09 * i, (a, sg * 0.4, r_)), (tc + 2.1 + 0.09 * i, (b, sg * 3.4, r_)), (S.T, (b + 0.3, sg * 4.6, r_))])
import random
rng = random.Random(4)
for i in range(26):                                                         # the pane is wet all over: many beads of different sizes
    rk.droplet(S, f"bead{i}", W, rng.uniform(0.18, 0.55), (rng.uniform(-17, 17), rng.uniform(-5.5, 5.5), 0.1)).scale = (1, 1, 0.55)
rk.softboxes(3.0, centre=(0, 0, 4), sides=False)
S.cam([(0, (0, 0, 3.0), 52, 22, -16), (S.T * 0.55, (0, 0, 2.6), 45, 18, -4), (S.T, (2, 0, 2.4), 40, 14, 10)])
S.go()
