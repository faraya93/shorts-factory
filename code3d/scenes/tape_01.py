"""huincha-de-medir scene 1 (B1 HOOK, contrast on one stage): two tapes extend their blades side by side over the table edge; the FLAT
blade flops almost at once, the CURVED blade keeps going. Slot 180 frames (6.0 s)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(180)
T = SLOT / c.FPS
ZA, ZB = -4.4, 3.4
A = tr.Tape(m, loc=(0, 0, ZA), name="flat")
B = tr.Tape(m, loc=(0, 0, ZB), name="curved")
tr.table(m, z_top=ZA + tr.MOUTH_Z - 0.45)
tr.table(m, z_top=ZB + tr.MOUTH_Z - 0.45)
DMAX = 9.0


def update(scene_):
    t = scene_.frame_current / c.FPS
    d = DMAX * tr.ease_out((t - 0.15) / 2.5)
    flop = c.smooth(0.25, 1.4, t)

    def th_flat(s):
        k = min(1.0, max(0.0, (s - A.S(0.9)) / 2.4))
        return 1.5 * flop * k * k * (3 - 2 * k)

    A.place_blade(d, theta=th_flat, cs=lambda s: 0.0)
    B.place_blade(d, theta=lambda s: 0.012 * max(0.0, s - B.inner), cs=lambda s: 1.0)
    B.blade.stress(0.9 * c.smooth(2.0, 3.2, t), B.S(6.0), 6.0)
    A.blade.stress(0.0)
    p = c.smooth(0, T, t)
    tr.look(stage, (4.2, 0, -1.4), 44 - 7 * p, 7 + 3 * p, -16 + 9 * p)


stage.run(update, args, SLOT, "tape-01")
