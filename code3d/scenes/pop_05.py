"""palomitas 5 (espuma): the soft starch swells with the steam into a white irregular foam that sets at once; steam puffs rise; orbit and pull-back."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import pop_rig as pr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(210)
M = pr.palette(S)
t_alm, t_exp, t_enf, t_esp = S.t("almidón,", default=0.3), S.t("expande", default=2.2), S.t("enfría", default=3.6), S.t("espuma.", default=5.6)
S.box("table", (26.0, 12.0, 0.8), (0, 0, -0.4), M["plate"], bevel=0.3, pop=(0.05, 0.4))
C = (0, 0, 5.0)
gel = pr.puff(S, M, "gel", mat=M["gel"])
d = next(dd for ob, dd in S.items if ob is gel); d["pop"] = None
foam = pr.puff(S, M, "foam")
S.every_frame(lambda t: None)
def gel_f(t):
    k = c.smooth(0.2, t_exp + 1.6, t)
    s = 0.35 + 2.3 * k + 0.12 * math.sin(14 * t) * k * (1 - c.smooth(t_enf, t_enf + 0.4, t))
    gel.location = (C[0], C[1], C[2] + 0.6 * k)
    gel.rotation_euler = (0, 0, 0.5 * t)
    g = (1.0 if t < t_enf else max(1e-4, 1 - c.smooth(t_enf, t_enf + 0.25, t)))
    gel.scale = tuple(max(1e-4, s * g) for _ in range(3))
    f = 0.0 if t < t_enf else c.smooth(t_enf, t_enf + 0.25, t)
    s2 = 0.35 + 2.3 * c.smooth(0.2, t_exp + 1.6, t)
    foam.location = gel.location
    foam.rotation_euler = gel.rotation_euler
    foam.scale = tuple(max(1e-4, s2 * f) for _ in range(3))
d1 = next(dd for ob, dd in S.items if ob is foam); d1["pop"] = None
d["manual"] = d1["manual"] = True
# freeze the registered tracks so only gel_f drives them
d["base"] = (1.0, 1.0, 1.0); d1["base"] = (1.0, 1.0, 1.0)
for dd in (d, d1):
    dd["sc"] = None
S.items = [(o, dd) for o, dd in S.items if o not in (gel, foam)]
S.every_frame(gel_f)
sh = S.box("shard", (0.7, 0.35, 0.55), (0, 0, 0), M["shard"], bevel=0.1)
rnd = random.Random(3)
sd = [(rnd.uniform(-5, 5), rnd.uniform(-2.5, 2.5), rnd.uniform(0, 6.3)) for _ in range(14)]
S.swarm(14, sh, lambda i, t: ((sd[i][0], sd[i][1], 0.4), 1.0, (0, 0, sd[i][2])))
st = S.ball("steam", M["steam"], 0.5, (0, 0, 0), seg=10)
S.swarm(26, st, lambda i, t: ((sd[i % 14][0] * 0.6 + 0.8 * math.sin(i + t), sd[i % 14][1], 1.0 + ((t * 0.7 + i * 0.17) % 1.0) * 7.0), 0.4 + 0.9 * math.sin(math.pi * ((t * 0.7 + i * 0.17) % 1.0))) if t > t_exp else None)
S.cam([(0, (0, 0, 5), 26, 10, -40), (t_exp, (0, 0, 5.5), 22, 8, 0), (t_enf, (0, 0, 6), 24, 14, 70), (S.T, (0, 0, 6), 34, 18, 150)])
S.go()
