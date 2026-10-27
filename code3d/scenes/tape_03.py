"""huincha-de-medir scene 3 (B3 STANDOUT): the blade extends across the stage (counter 0 -> 3.4 m is an Editor overlay locked to the same ease), then
at its limit the curve flattens at ONE point, kinks, and the whole blade collapses. Slot 299 frames (9.97 s)."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(299)
T = SLOT / c.FPS
A = tr.Tape(m, loc=(0, 0, 0), name="tape")
tr.table(m)
DMAX, SK = 20.0, A.S(11.5)


def update(scene_):
    t = scene_.frame_current / c.FPS
    d = DMAX * tr.ease_out((t - 0.3) / 3.3)
    flat = c.smooth(5.0, 6.9, t)
    kink = 1.25 * c.smooth(7.0, 7.9, t) + 0.65 * c.smooth(7.9, 9.2, t)
    sag = 0.55 * c.smooth(7.8, 9.6, t)

    def th(s):
        k = 0.5 * (1 + math.tanh((s - SK) / 0.25))
        g = min(1.0, max(0.0, (s - 3.0) / 14.0))
        return kink * k + sag * g * g * (3 - 2 * g) + 0.003 * max(0.0, s - A.inner)

    def cs(s):
        return 1 - 0.96 * flat * math.exp(-((s - SK) / 0.9) ** 2)

    A.place_blade(d, theta=th, cs=cs)
    A.blade.stress(5.0 * flat, SK, 0.9)
    follow = min(1.0, d / DMAX)
    p = c.smooth(7.0, 9.4, t)
    tr.look(stage, (10.0, 0, -2.6 - 0.8 * p), 62 - 6 * c.smooth(0, T, t), 5 + 3 * p, -12 + 8 * c.smooth(0, T, t))


stage.run(update, args, SLOT, "tape-03")
