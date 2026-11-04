"""palomitas 2 (grano): the kernel turns transparent: the water drop, the starch core and the hard shell; orbit and push-in."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import pop_rig as pr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(197)
M = pr.palette(S)
t_got, t_alm, t_cas = S.t("gotita", default=1.3), S.t("almidón", default=2.8), S.t("cáscara", default=3.7)
S.box("table", (24.0, 12.0, 0.8), (0, 0, -0.4), M["plate"], bevel=0.3, pop=(0.05, 0.4))
C = (0, 0, 6.2)
L = pr.kernel_layers(S, M, C, big=3.2, t_xray=t_got - 0.3)
d = next(dd for ob, dd in S.items if ob is L["drop"]); d["base"] = (1.9, 1.9, 1.9)
S.every_frame(lambda t: (setattr(L["kern"], "rotation_euler", (0, 0, 0.5 * t)), setattr(L["shell"], "rotation_euler", (0, 0, 0.5 * t))))
S.torus("ringc", 3.9, 0.07, (0, -1.5, 6.2), S.accent, rot=(math.pi / 2, 0, 0), pop=(t_cas, 0.4))
S.cam([(0, (0, 0, 6.2), 34, 12, -34), (t_got, (0, 0, 6.2), 24, 8, -10), (t_alm, (0, 0, 6.0), 18, 8, 12), (S.T, (0, 0, 6.2), 22, 10, 38)])
S.go()
