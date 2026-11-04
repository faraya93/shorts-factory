"""pieles-arrugadas 4 (canales): a smooth pad and a grooved pad press a water film; the grooves channel the water out; a tyre rolls past."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import wrinkle_rig as wr  # noqa: E402
import common as c  # noqa: E402

random.seed(4)
S = sp.Shot(183)
M = wr.palette(S)
t_can, t_lla, t_des = S.t("canales,", default=1.2), S.t("llanta,", default=2.9), S.t("desvían", default=3.5)
S.box("plate", (15.0, 8.0, 0.6), (0, 0, 0.0), M["plate"], bevel=0.2, pop=(0.05, 0.4))
S.box("film", (14.0, 7.0, 0.3), (0, 0, 0.45), M["water"], bevel=0.1, pop=(0.2, 0.4))
XL, XR = -3.6, 3.6
HZ = 2.6
# left: smooth pad; right: grooved pad (comb of ridges hanging under a block)
smooth = S.box("padL", (4.4, 4.4, 1.5), (XL, 0, 6.5), M["skin"], bevel=0.45, pop=(0.4, 0.4))
S.move(smooth, [(0.5, (XL, 0, 9.0)), (1.5, (XL, 0, 1.55)), (2.4, (XL, 0, 1.45)), (S.T, (XL, 0, 1.5))])
S.every_frame(lambda t: setattr(smooth, "rotation_euler", (0, 0, 0.06 * math.sin(7 * t) * c.smooth(2.4, 3.0, t))))
padR = S.box("padR", (4.4, 4.4, 1.5), (XR, 0, 6.5), M["skin"], bevel=0.45, pop=(0.4, 0.4))
S.move(padR, [(0.5, (XR, 0, 9.0)), (1.5, (XR, 0, 1.75)), (2.4, (XR, 0, 1.65)), (S.T, (XR, 0, 1.7))])
teeth = [S.box(f"tooth{i}", (0.42, 4.4, 0.7), (XR - 1.8 + i * 0.6, 0, 0), M["skin_dk"], bevel=0.12, parent=padR, pop=(0.4, 0.4)) for i in range(7)]
for o in teeth:
    o.location = (o.location[0] - XR, 0, -1.0)
# droplets: left squirt randomly and slowly; right run in lines through the channels toward the camera
dr = S.ball("drop", M["water"], 0.42, (0, 0, 0))
rnd = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(0.0, 1.0)) for _ in range(26)]
def drops(i, t):
    t0 = 1.5
    if t < t0:
        return None
    if i < 12:                                                        # left pad: few, random, short
        a, b, ph = rnd[i]
        k = ((t - t0) * 0.5 + ph) % 1.0
        return (XL + a * (2.3 + 1.4 * k), b * (2.3 + 1.4 * k), 0.9 + 0.5 * math.sin(math.pi * k)), 0.8 * (1 - 0.5 * k)
    j = i - 12
    lane = j % 7
    k = ((t - t0) * 0.75 + j * 0.37) % 1.0
    return (XR - 1.8 + lane * 0.6, 2.2 + 3.2 * k, 0.75 + 0.3 * math.sin(math.pi * k)), 0.8 * (1 - 0.3 * k)
S.swarm(26, dr, drops)
# tyre rolling past behind
wheel = S.cyl("wheel", 3.6, 2.8, (14, 6.5, 3.6), S.ink, axis="Y", verts=64, bevel=0.3)
grv = [S.torus(f"g{i}", 3.02, 0.12, (14, 6.5, 3.6), M["board"], rot=(math.pi / 2, 0, 0), parent=None) for i in range(1)]
S.move(wheel, [(t_lla - 0.2, (11.0, 6.5, 3.6)), (t_lla + 3.0, (-11.0, 6.5, 3.6))])
S.spin(wheel, [(t_lla - 0.2, (0, 0, 0)), (t_lla + 3.0, (0, 7.3, 0))])
S.cam([(0, (0, 0, 3), 30, 24, -30), (2.0, (0, 0, 2.6), 24, 14, -8), (4.0, (0, 1.0, 3.0), 26, 30, 14), (S.T, (0, 0, 3.0), 28, 62, 20)])
S.go()
