"""corazon 1 (botellas): the pump beats and fills one bottle; the camera pulls back as thousands of full bottles pop in, in rows."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import heart_rig as hr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(204)
M = hr.palette(S)
t_ref, t_san, t_mil = S.t("refresco", default=2.3), S.t("sangre", default=3.4), S.t("mil.", default=5.6)
S.box("floor", (60.0, 24.0, 0.6), (8, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
heart = hr.pump_heart(S, M, (-8.0, 0, 5.2), scale=1.0, pop=0.2)
# hero bottle: glass + rising fluid, fed by a tube from the heart
S.cyl("hg", 0.95, 3.0, (0, 0, 1.5), M["glass"], axis="Z", verts=24, bevel=0.1, pop=(t_ref - 0.3, 0.4))
S.cyl("hn", 0.38, 0.9, (0, 0, 3.4), M["glass"], axis="Z", verts=16, pop=(t_ref - 0.3, 0.4))
fl = S.cyl("hf", 0.82, 2.3, (0, 0, 0.3), M["fluid"], axis="Z", verts=24, pop=(t_ref - 0.2, 0.3))
S.every_frame(lambda t: (setattr(fl, "scale", (1, 1, max(1e-3, 0.95 * c.smooth(t_san - 0.2, t_san + 2.0, t)))), setattr(fl, "location", (0, 0, 0.25 + 1.15 * max(1e-3, 0.95 * c.smooth(t_san - 0.2, t_san + 2.0, t))))))
S.line("tube", [(-5.6, 0, 8.2), (-3.0, 0, 9.2), (0.0, 0, 8.0), (0.0, 0, 5.2)], 0.22, S.accent, grow=(t_san - 0.4, t_san + 0.6))
tpl = hr.bottle(S, M, "bt")
NX, NY = 22, 8
cells = [(i, j) for i in range(NX) for j in range(NY)]
cells.sort(key=lambda ij: math.hypot(ij[0] - 6, (ij[1] - 3.5) * 2.0))
def bot(i, t):
    a, b = cells[i]
    born = t_mil - 0.3 + 0.012 * i
    if t < born:
        return None
    k = min(1.0, (t - born) / 0.35)
    return (2.6 + a * 2.2, 1.6 + b * 2.2, 0.0), k
S.swarm(NX * NY, tpl, bot)
S.cam([(0, (-4, 0, 5), 34, 10, -20), (t_ref, (-4, 0, 5), 28, 8, -6), (t_san + 1.5, (-3, 0, 4.5), 26, 10, 8), (t_mil, (4, 4, 4), 32, 22, 14), (S.T, (14, 6, 2), 56, 34, 22)])
S.go()
