"""pieles-arrugadas 3 (surcos): the smooth skin sheet loses volume, sinks and folds into long grooves; grazing camera sweep."""
import math
import sys
import numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import wrinkle_rig as wr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(178)
M = wr.palette(S)
t_vol, t_jal, t_pli = S.t("volumen", default=2.2), S.t("jala", default=2.8), S.t("surcos.", default=4.5)
S.box("flesh", (12.6, 10.6, 4.6), (0, 0, 2.5), M["skin_dk"], bevel=0.35, pop=(0.1, 0.45))
hf = S.heightfield("skin", M["skin"], size=(12.0, 10.0), n=(150, 125), loc=(0, 0, 5.0))
for k, z in enumerate((1.4, 3.2)):
    S.cyl(f"v{k}", 0.55, 12.8, (0, -5.35, z), M["vessel"], axis="X", verts=24, pop=(0.5 + 0.2 * k, 0.4))
def surface(t):
    base = -0.9 * c.smooth(t_vol - 0.2, t_jal + 0.8, t)
    amp = 1.15 * c.smooth(t_jal, t_pli + 0.6, t)
    X, Y = hf.X, hf.Y
    ph = 2 * math.pi * (X + 0.55 * np.sin(Y * 0.55)) / 1.15
    ridges = amp * np.sin(ph) * (0.75 + 0.25 * np.cos(Y * 0.4))
    return base + ridges - 0.1 * amp
S.every_frame(lambda t: hf.update(surface(t)))
S.cam([(0, (0, 0, 4), 34, 58, -40), (2.5, (0, 0, 4.2), 27, 46, -20), (S.T, (0.5, 0, 4.0), 22, 34, 25)])
S.go()
