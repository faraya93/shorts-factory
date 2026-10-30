"""alcohol scene 7 (closing): both machines run; recovery with support slows machine B and lightens its tracks; the C2 tag sits below."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import loop_rig as lr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(440, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 7)
M = lr.mats()
mk.board(M, lr.Z0, w=11.6, h=11.4)
A = lr.Machine(0, m, M)
B = lr.Machine(1, m, M)
Z0 = lr.Z0
t_rec, t_apo = W.t("recuperación", default=7.3), W.t("apoyo", default=8.6)
ring = mr.ring(m, "help", 1.0, 1.0, (lr.SLIDER_X[1], -0.8, B.cz))
ring.scale = (1e-4,) * 3
B.set_sliders(lr.SETTINGS[1])


def update(scene_):
    t = scene_.frame_current / c.FPS
    ka = c.smooth(t_apo, t_apo + 2.0, t)
    B.track_depth(0.8 * (1 - ka))
    sp = 0.3 - 0.18 * ka
    lr.run_tokens(A.full, lr.phase(lambda x: 0.12, t), t, 0.0, amount=0.5)
    lr.run_tokens(B.full, lr.phase(lambda x: 0.3 - 0.18 * c.smooth(t_apo, t_apo + 2.0, x), t), t, 0.0)
    s = 1e-4 if t < t_apo - 0.3 else 1.1 * min(1.0, (t - t_apo + 0.3) / 0.5)
    ring.scale = (s, 1.0, s)
    B.set_sliders((lr.SETTINGS[1][0], lr.SETTINGS[1][1] + 0.22 * ka, lr.SETTINGS[1][2] - 0.2 * ka))
    p = c.smooth(0, T, t)
    tr.look(stage, (0.3, 0, Z0), 31.0 + 5.0 * p, 6.0, -4.0 + 8.0 * p)

stage.run(update, args, SLOT, "loop-07")
