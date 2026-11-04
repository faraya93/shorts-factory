"""corazon 2 (puno): a fist and the pump side by side, the same size; the pump beats and every beat sends out a ring."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import heart_rig as hr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(206)
M = hr.palette(S)
t_pun, t_cien = S.t("puño,", default=2.3), S.t("cien", default=3.4)
S.box("floor", (26.0, 10.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
fist = S.empty("fist", (-5.0, 0, 4.0), pop=(0.2, 0.45))
S.box("palm", (4.6, 3.6, 3.4), (0, 0, 0), M["skin"], bevel=0.9, parent=fist)
for k in range(4):
    S.box(f"fing{k}", (1.0, 1.0, 1.2), (-1.5 + k * 1.0, -1.9, 0.9), M["skin"], bevel=0.35, parent=fist)
S.box("thumb", (1.0, 2.8, 1.0), (2.0, -1.4, -0.2), M["skin"], bevel=0.35, parent=fist, rot=(0, 0, math.radians(20)))
S.move(fist, [(0, (-5.0, 0, 4.0)), (t_pun - 0.4, (-5.0, 0, 4.0)), (t_pun + 0.6, (-5.0, 0, 4.0))])
heart = hr.pump_heart(S, M, (5.0, 0, 4.4), scale=1.0, pop=0.8, t_beat=1.0)
S.every_frame(lambda t: setattr(fist, "rotation_euler", (0, 0, 0.1 * math.sin(1.5 * t))))
N = 9
def ring(i, t):
    t0 = 1.0 + hr.BEAT * i + 0.05
    if t < t0:
        return None
    k = (t - t0) / 1.8
    if k > 1.0:
        return None
    return (5.0, -0.6, 4.4), 0.6 + 7.0 * k
rg = S.torus("ring", 1.0, 0.07, (0, 0, 0), S.accent, rot=(math.pi / 2, 0, 0))
S.swarm(N, rg, ring)
S.cam([(0, (0, 0, 5), 34, 10, -24), (t_pun, (-1, 0, 4.4), 24, 6, 0), (t_cien, (2, 0, 4.4), 22, 8, 18), (S.T, (0, 0, 4.4), 30, 14, -10)])
S.go()
