"""huincha-de-medir scene 7 (B7 CTA backdrop): the blade recoils into the closed tape; slow orbit behind the Editor's phone mock. Slot 146 frames (4.87 s)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(146)
T = SLOT / c.FPS
A = tr.Tape(m, loc=(0, 0, 0), name="tape")
tr.table(m, x0=-6.0, x1=3.0)


def update(scene_):
    t = scene_.frame_current / c.FPS
    d = 7.0 * (1 - tr.ease_out((t - 0.35) / 1.0)) if t > 0.35 else 7.0
    A.place_blade(d, theta=lambda s: 0.01 * max(0.0, s - A.inner), cs=lambda s: 1.0, hook_slide=1.0 - c.smooth(1.2, 1.5, t))
    A.blade.stress(0.0)
    p = c.smooth(0, T, t)
    tr.look(stage, (3.0, 0, -1.2), 30 - 3 * p, 18 + 3 * p, -32 + 20 * p)


stage.run(update, args, SLOT, "tape-07")
