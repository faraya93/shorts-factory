"""palomitas 7 (cierre): a kernel with a lit fuse pops into popcorn (steam puffs, shards); popcorn rains into a bucket; wide pull-back."""
import math
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import pop_rig as pr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(300)
M = pr.palette(S)
t_exp, t_vap, t_sig = S.t("explosivo", default=3.0), S.t("vapor.", default=3.6), S.t("Sígueme,", default=4.9)
TB = t_vap
S.box("table", (44.0, 20.0, 0.8), (0, 0, -0.4), M["plate"], bevel=0.3, pop=(0.05, 0.4))
k = S.ball("kern", M["kernel"], 1.0, (-4.0, 0, 3.4), shape=(2.4, 2.0, 3.1), pop=(0.2, 0.45), seg=36)
S.gone(k, TB, 0.05)
S.every_frame(lambda t: setattr(k, "location", (-4.0 + 0.16 * math.sin(50 * t) * c.smooth(TB - 1.0, TB, t) * (1 if t < TB else 0), 0, 3.4)))
S.line("fuse", [(-4.0, 0, 6.4), (-3.2, 0, 8.4), (-4.4, 0, 10.2)], 0.15, S.ink, grow=(0.8, 1.6), smooth=True)
spark = S.ball("spark", S.accent, 0.4, (-4.4, 0, 10.2), pop=(1.7, 0.2))
S.move(spark, [(1.7, (-4.4, 0, 10.2)), (TB - 0.05, (-4.0, 0, 6.5))]); S.gone(spark, TB - 0.1, 0.1)
fl = S.ball("flash", S.accent, 1.0, (-4.0, 0, 3.4), seg=24)
S.size(fl, [(TB, 1e-3), (TB + 0.1, 6.0), (TB + 0.6, 7.0)]); S.pop(fl, TB, 0.05); S.gone(fl, TB + 0.08, 0.3)
big = pr.puff(S, M, "big")
S.move(big, [(0, (-4.0, 0, 3.4))])
d = next(dd for ob, dd in S.items if ob is big); d["pop"] = None
S.items = [(o, dd) for o, dd in S.items if o is not big]
def bigf(t):
    s = 1e-4 if t < TB else 0.9 + 1.8 * c.smooth(TB, TB + 0.5, t)
    big.location = (-4.0, 0, 3.4 + 1.0 * c.smooth(TB, TB + 0.5, t))
    big.rotation_euler = (0, 0, 0.7 * t)
    big.scale = (max(1e-4, s),) * 3
S.every_frame(bigf)
st = S.ball("puff", M["steam"], 1.2, (0, 0, 0), seg=14)
rnd = random.Random(4)
dr = [(rnd.uniform(-1, 1), rnd.uniform(-0.6, 0.2), rnd.uniform(0, 1)) for _ in range(14)]
S.swarm(14, st, lambda i, t: ((-4.0 + dr[i][0] * (2.0 + 7.0 * (t - TB)), -1.0, 3.4 + dr[i][2] * (2.0 + 5.0 * (t - TB))), min(2.2, 0.4 + 2.0 * (t - TB))) if TB < t < TB + 1.6 else None)
sh = S.box("shard", (0.7, 0.35, 0.55), (0, 0, 0), M["shard"], bevel=0.1)
S.swarm(10, sh, lambda i, t: ((-4.0 + dr[i][0] * (3.0 + 8.0 * (t - TB)), dr[i][1] * 3, max(0.4, 3.4 + dr[i][2] * 5 - 2.0 * (t - TB) ** 2)), 1.0, (t * 5, t * 4, i)) if t > TB else None)
# the bucket (a cone with a rim) on the right and popcorn raining into it
S.cone("bucket", 3.4, 4.6, 5.0, (8.0, 0, 2.5), M["board"], pop=(TB + 0.2, 0.5))
S.torus("brim", 4.6, 0.35, (8.0, 0, 5.0), M["board"], pop=(TB + 0.2, 0.5))
pf = pr.puff(S, M, "rain")
N = 36
def rain(i, t):
    t0 = TB + 0.6 + 0.12 * i
    if t < t0:
        return None
    k = (t - t0) / 0.8
    fx = 8.0 + 2.6 * math.cos(i * 2.399) * (0.4 + 0.6 * (i % 5) / 5) * 1.0
    fy = 1.6 * math.sin(i * 2.399)
    fz = 5.4 + 1.1 * (i // 6) * 0.9 * 0.9
    z = fz + max(0.0, 1.0 - k) ** 2 * 14.0
    return (fx, fy, z), 0.7, (0, 0, i)
S.swarm(N, pf, rain)
S.cam([(0, (-3, 0, 5), 30, 10, -22), (TB - 0.4, (-4, 0, 4), 22, 6, 0), (TB + 1.0, (0, 0, 5), 34, 10, 10), (t_sig, (3, 0, 5), 40, 14, -6), (S.T, (2, 0, 5), 56, 22, 8)])
S.go()
