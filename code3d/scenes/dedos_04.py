"""dedos 4 (canales): a smooth wheel aquaplanes on a water film; a grooved wheel pushes the water out through its grooves."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import grip_rig as gr  # noqa: E402

S = sp.Shot(210)
M = gr.palette(S)
S.box("road", (34, 14, 1.2), (0, 0, -0.6), M["plate"], bevel=0.3)
film = S.box("film", (32, 12, 0.5), (0, 0, 0.25), M["water"], bevel=0.2)
R = 4.0
tc = S.t("canales", default=1.0)
# smooth wheel (back lane), grooved wheel (front lane): rolling in +x, camera tracks along
ws = gr.wheel(S, M, "w_smooth", -12.0, R + 0.9, R, 3.0, grooved=False, pop=(0.1, 0.4))
wg = gr.wheel(S, M, "w_groove", -12.0, R + 0.0, R, 3.0, grooved=True, pop=(0.2, 0.4))
ws.location.y = 3.4; wg.location.y = -3.4
S.move(ws, [(0.0, (-12.0, 3.4, R + 0.9)), (S.T, (10.0, 3.4, R + 0.9))])
S.move(wg, [(0.0, (-12.0, -3.4, R)), (S.T, (10.0, -3.4, R))])
S.spin(ws, [(0.0, (0, 0, 0)), (S.T, (0, 4.0 * math.pi, 0))])       # spins fast, lifted on the water
S.spin(wg, [(0.0, (0, 0, 0)), (S.T, (0, 22.0 / R * math.pi, 0))])  # rolls: arc length = distance
# spray: droplets leave the grooved wheel sideways along the grooves
def spray(i, t):
    t0 = 1.4 + i * 0.07
    if t < t0 or t > t0 + 1.0:
        return None
    k = (t - t0) / 1.0
    x0 = -12.0 + 22.0 * (t0 / S.T)
    side = -1 if i % 2 else 1
    return ((x0 - 2.0 * k, -3.4 + side * (2.2 + 4.5 * k), 0.8 + 3.0 * k * (1 - k)), 0.5 + 0.3 * (1 - k))
drop = S.ball("drop", M["marble"], 0.45, (0, 0, 0))
S.swarm(18, drop, spray)
S.cam([(0, (-6, 0, 3), 62, 12, -48), (3.0, (-1, 0, 3), 52, 10, -28), (5.0, (0, 0, 2), 52, 50, -10), (S.T, (3, 0, 2), 52, 68, 0)])
S.go()
