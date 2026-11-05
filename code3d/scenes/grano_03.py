"""grano 3 (presión): heat turns the drop into steam that fills the kernel and squeezes the hull; the whole kernel shakes harder and harder."""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import corn_rig as cr  # noqa: E402

S = sp.Shot(210)
M = cr.palette(S)
random.seed(4)
hull, st, dr = cr.cutaway(S, M, 0, 9.0, 7.2, t_on=0.05)
t_h = S.t("hierve", default=2.0)
S.size(dr, [(t_h, 1.0), (t_h + 1.4, 0.0001)])
rnd = [(random.uniform(-3.2, 3.2), random.uniform(-4.5, 4.0)) for _ in range(26)]
steam = S.ball("steam", M["steam"], 0.85, (0, 0, 0))
def puff(i, t):
    a = t_h + 0.05 * i
    if t < a:
        return None
    k = min(1.0, (t - a) / 0.9)
    x, z = rnd[i]
    return ((x * k, -1.4, 8.0 + z * k), 0.4 + 1.5 * k)
S.swarm(26, steam, puff)
# hull: squeezed: grows a little and vibrates with growing amplitude
def shake(t):
    amp = 0.0 if t < t_h else min(1.0, (t - t_h) / 4.0)
    dx = amp * 0.35 * math.sin(t * 60.0)
    for o in (hull, st):
        o.location.x = dx
    hull.scale = (0.78 * (1 + 0.10 * amp) * hull.scale[0] / max(hull.scale[0], 1e-9) if False else hull.scale[0], hull.scale[1], hull.scale[2])
S.every_frame(shake)
S.size(hull, [(0, (0.78, 1, 1.0)), (S.T, (0.86, 1, 1.07))])
S.size(st, [(0, (0.78, 1, 1.0)), (S.T, (0.84, 1, 1.04))])
# hot pan glow under the section
glow = S.cyl("pan", 9.0, 0.6, (0, 0.0, -5.0), S.hero("accent", "#FFA45C", rough=0.5), axis="Z", verts=64)
S.cam([(0, (0, 0, 8), 40, 0, 0), (S.T, (0, 0, 8), 30, 0, 0)])
S.go()
