"""inodoro scene 3 (sifon): the bowl rises and fills the hidden curved tube; the siphon pulls the bowl dry and carries the waste through the trap."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import toilet_rig as tl  # noqa: E402

args, production, stage, m, SLOT = tr.begin(254, floor_z=-1.2)
tl.cpu_draft(stage, args)
T = SLOT / c.FPS
K = tl.Toilet()


def update(scene_):
    t = scene_.frame_current / c.FPS
    bowl = tl.keys(t, [(0.0, 5.5), (0.3, 5.6), (1.3, 6.3), (4.3, 6.3), (6.2, 2.7), (6.4, 2.6)])
    tube = tl.keys(t, [(0.0, 5.6), (1.3, 6.3), (6.1, 6.3), (6.9, 2.5)])
    lo = tl.keys(t, [(0.0, 5.9), (3.9, 5.9), (5.2, -1.8)])
    hi = tl.keys(t, [(0.0, 5.9), (6.3, 5.9), (7.4, -1.8)])
    leg = (lo, hi) if t < 6.3 else (-1.8, hi)
    K.state(tank=9.2, bowl=bowl if t < 6.4 else 2.6, chan=1.0 if t < 3.0 else tl.keys(t, [(3.0, 1.0), (4.0, 0.0)]), hole=0.0, tube=tube, leg2=leg)
    s0 = tl.keys(t, [(0.0, 0.0), (4.3, 0.0), (7.5, 1.0)])
    s1 = max(0.0, s0 - 0.07)
    if t < 4.3:
        wx, wz = 3.7, bowl - 0.05 + 0.06 * math.sin(2.0 * t); w2x, w2z = 4.7, bowl - 0.08
    else:
        wx, wz = tl.Toilet.path_point(s0); w2x, w2z = tl.Toilet.path_point(s1) if s1 > 0 else (4.7, bowl - 0.08)
    K.put_waste(0, wx, wz, tumble=3.0 * s0)
    K.put_waste(1, w2x, w2z, tumble=-2.0 * s0)
    p = c.smooth(1.4, 3.4, t)
    tr.look(stage, (1.2 - 1.2 * p, 0, 6.0 - 1.2 * p), 27.0 - 6.0 * p, 6.0, -4.0 + 6.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "toilet-03")
