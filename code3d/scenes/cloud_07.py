"""nube 7 (cierre): the cloud, a chimney's smoke crossed out; the cloud flattens into a hovering lake over a tiny person; ENVIASELO."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import cloud_rig as cr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(280)
M = cr.palette(S)
t_hum, t_lago, t_sob = S.t("humo", default=1.3), S.t("lago", default=2.7), S.t("sobre", default=3.8)
C = (0, 0, 12)
for p in cr.puffs(S, M, C, n=26, rx=5.0, ry=2.4, rz=2.4, seed=2, pop0=0.1, stagger=0.02, r=(1.1, 2.0)):
    S.gone(p, t_lago + 0.1, 0.8)
# chimney and its smoke, crossed out
S.box("chimney", (2.0, 2.0, 5.0), (-8.0, 0, 2.5), M["board"], bevel=0.3, pop=(t_hum - 0.3, 0.4))
smoke = S.ball("smk", M["smoke"], 0.9, (0, 0, 0), seg=14)
def smk(i, t):
    if t < t_hum or t > t_lago + 0.2:
        return None
    k = ((t - t_hum) * 0.4 + i / 10.0) % 1.0
    return (-8.0 + 1.5 * math.sin(k * 5 + i) * k, 0, 5.5 + 7.0 * k), 0.5 + 1.1 * k
S.swarm(10, smoke, smk)
for nm, a in (("xa", 1), ("xb", -1)):
    S.box(nm, (6.5, 0.4, 0.7), (-8.0, -1.8, 10.0), S.error, bevel=0.2, rot=(0, math.radians(45 * a), 0), pop=(t_hum + 0.1, 0.3))
    S.gone(S.items[-1][0], t_lago + 0.1, 0.4)
# lake over a person
lake = S.box("lake", (13.0, 5.0, 2.6), (0, 0, 12.0), M["drop"], bevel=0.5, pop=(t_lago + 0.2, 0.6))
S.every_frame(lambda t: setattr(lake, "location", (0, 0, 12.0 + 0.25 * math.sin(2.0 * t))))
for k in range(3):
    r = S.torus(f"rp{k}", 1.0, 0.07, (0, -2.3, 13.35), M["cloud"], rot=(0, 0, 0))
    a = t_lago + 0.9 + 0.5 * k
    S.size(r, [(a, 0.3), (a + 1.6, 3.2)]); S.pop(r, a, 0.05); S.gone(r, a + 1.1, 0.5)
S.box("ground", (24.0, 7.0, 0.5), (0, 0, -0.1), M["plate"], bevel=0.2, pop=(t_sob - 0.8, 0.5))
body = S.cyl("body", 0.7, 2.0, (0, 0, 1.4), M["cars"][1], axis="Z", verts=24, pop=(t_sob - 0.5, 0.4))
head = S.ball("head", M["cars"][0], 0.65, (0, 0, 3.0), pop=(t_sob - 0.4, 0.4))
S.move(head, [(0, (0, 0, 3.0)), (t_sob - 0.2, (0, 0, 3.0)), (t_sob + 0.8, (0.0, -0.3, 3.1))])
S.cam([(0, (0, 0, 10), 36, 8, -16), (t_hum, (-3, 0, 9), 34, 8, -8), (t_lago + 0.5, (0, 0, 8), 40, 6, 8), (t_sob + 1.0, (0, 0, 7), 34, 12, 24), (S.T, (0, 0, 7), 52, 18, -10)])
S.go()
