"""corazon 3 (latido): each beat pushes a slug of fluid along a tube into a measuring jar whose level rises a little per beat (70 mL)."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import heart_rig as hr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(216)
M = hr.palette(S)
S.box("floor", (26.0, 10.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
heart = hr.pump_heart(S, M, (-6.5, 0, 4.4), scale=0.95, pop=0.2, t_beat=0.4)
S.cyl("jar", 2.0, 8.0, (6.0, 0, 4.0), M["glass"], axis="Z", verts=40, bevel=0.05, pop=(0.3, 0.45))
fl = S.cyl("jarf", 1.85, 1.0, (6.0, 0, 0.5), M["fluid"], axis="Z", verts=40, pop=(0.4, 0.3))
NB = 7
def level(t):
    n = max(0.0, (t - 0.9) / hr.BEAT)
    h = 0.4 + 0.62 * min(n, 9) + 0.0
    h = min(h, 7.2)
    fl.scale = (1.0, 1.0, h)
    fl.location = (6.0, 0, 0.1 + h / 2)
S.every_frame(level)
slug = S.ball("slug", M["fluid"], 0.55, (0, 0, 0), seg=14)
def slugs(i, t):
    t0 = 0.55 + hr.BEAT * i
    k = (t - t0) / 0.7
    if k < 0 or k > 1.0:
        return None
    x = -4.4 + 10.0 * k
    z = 8.4 + 1.4 * math.sin(math.pi * k) - 3.5 * k * k
    return (x, 0, z), 1.0
S.swarm(10, slug, slugs)
S.line("pipe", [(-4.6, 0, 8.4), (-2.0, 0, 9.8), (3.0, 0, 9.8), (5.0, 0, 8.6)], 0.14, S.accent, grow=(0.5, 1.4))
S.cam([(0, (0, 0, 5), 34, 10, -22), (2.0, (2, 0, 5), 26, 8, 0), (S.T, (3, 0, 5), 24, 10, 16)])
S.go()
