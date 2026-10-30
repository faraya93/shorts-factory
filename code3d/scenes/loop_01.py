"""alcohol scene 1 (hook): two identical machines get the same bottle; one completes a lap and stops, the other keeps going."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import loop_rig as lr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(215, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 1)
M = lr.mats()
mk.board(M, lr.Z0, w=11.6, h=11.4)
A = lr.Machine(0, m, M)
B = lr.Machine(1, m, M)
Z0 = lr.Z0
t_pop, t_run, t_stop, t_urge = W.t("persona", default=0.6), W.t("tomarse", default=1.2), W.t("parar,", default=2.2) + 0.9, W.t("pensando", default=5.2)


def update(scene_):
    t = scene_.frame_current / c.FPS
    for mc in (A, B):
        mk.pop(mc.bottle, t, t_pop - 0.2)
    pa = max(0.0, (t - t_run) * 0.22)
    lr.run_tokens(A.full, pa, t, t_run, amount=1.0 if t < t_stop else 0.0)
    pb = lr.phase(lambda x: 0.22 + 0.25 * c.smooth(t_urge, t_urge + 1.5, x), max(0.0, t - t_run))
    lr.run_tokens(B.full, pb, t, t_run)
    B.cue_all(1.0 if t > t_urge else 0.0)
    tr.look(stage, (0.0, 0, Z0), 32.0 - 1.5 * c.smooth(0, T, t), 6.0, -5.0 + 10.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "loop-01")
