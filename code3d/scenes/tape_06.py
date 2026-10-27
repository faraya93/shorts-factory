"""huincha-de-medir scene 6 (B6 REFRAME, one image): the blade unfolds across a gap as a miniature bridge and carries a weight. Slot 196 frames (6.53 s)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(196)
T = SLOT / c.FPS
A = tr.Tape(m, loc=(0, 0, 0), name="tape")
tr.table(m, x0=-6.0, x1=3.0)
DMAX = 17.0
E = 2.1 + DMAX
pedestal_b = tr.rbox("pedestal_b", (6.0, 6.0, 3.2), (E - 3.0, 0, -1.65 - 1.6), m.block, bevel=0.3)
weight = tr.rbox("weight", (2.6, 2.6, 2.6), (8.2, 0, 6.0), m.block, bevel=0.35)


def update(scene_):
    t = scene_.frame_current / c.FPS
    d = DMAX * tr.ease_out((t - 2.6) / 1.6) if t > 2.6 else 0.0
    drop = tr.back((t - 4.5) / 0.8, 1.1)
    load = c.smooth(4.8, 5.4, t)
    amp = 0.34 * load
    D = max(d, 0.001)

    def th(s):
        u = (s - A.inner) / D
        return amp * 3.14159 / D * __import__("math").cos(3.14159 * min(1.0, max(0.0, u)))

    A.place_blade(d, theta=th, cs=lambda s: 1.0, hook_slide=1.0)
    zb = A.blade.z_at(A.inner + DMAX * 0.5) if d > 0.1 else -1.55
    weight.location = (8.2, 0, (zb + 1.33) + 6.0 * (1 - min(1.0, max(0.0, drop)))) if t > 4.3 else (8.2, 0, -500.0)
    A.blade.stress(2.4 * load, A.inner + 8.0, 4.0)
    p = c.smooth(0, T, t)
    tr.look(stage, (9.5, 0, -0.6), 40 - 3 * p, 10 + 5 * p, -40 + 20 * p)


stage.run(update, args, SLOT, "tape-06")
