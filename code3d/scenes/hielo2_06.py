"""hielo2 6 (cierre): one image: a glass of water with a real ice lid floating on top, the camera pulling back."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402

S = sp.Shot(283)
G, W, I = rk.glass(), rk.water("clear_water", density=0.02), rk.ice("clear_ice", core=1.2, seed=2.0)
glass, liquid = rk.tumbler(S, "glass", G, W, r=5.0, h=12.5, level=9.0)
lid = rk.disc(S, "lid", 4.55, 1.9, (0, 0, 8.0), I)
tl = S.t("tapa", default=1.8) - 0.4
S.every_frame(lambda t: setattr(lid, "location", (0.0, 0.0, 8.0 + 0.06 * math.sin(t * 1.6)) if t >= tl else (0.0, 0.0, 80.0)))
rk.softboxes(2.2)
S.cam([(0, (0, 0, 8), 24, 20, -20), (S.T * 0.5, (0, 0, 7), 32, 14, -6), (S.T, (0, 0, 6.5), 44, 8, 12)])
S.go()
