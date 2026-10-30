"""alcohol scene 2: the three factory settings (REWARD, BRAKE, STRESS) move to different starting positions on each machine."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import loop_rig as lr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(267, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 2)
M = lr.mats()
mk.board(M, lr.Z0, w=11.6, h=11.4)
A = lr.Machine(0, m, M)
B = lr.Machine(1, m, M)
Z0 = lr.Z0
ks = [W.t("recompensa,", default=4.7), W.t("freno", default=5.7), W.t("estrés.", default=7.5)]
t_dos = W.t("máquinas", default=0.6)
pa = lr.phase(lambda x: 0.12, 0)


def update(scene_):
    t = scene_.frame_current / c.FPS
    for mc in (A, B):
        s = [0.5 + (lr.SETTINGS[mc.idx][k] - 0.5) * c.smooth(ks[k] - 0.2, ks[k] + 0.9, t) for k in range(3)]
        mc.set_sliders(s)
        lr.run_tokens(mc.full, lr.phase(lambda x: 0.12, t), t, 0.0, amount=0.5)
    p = c.smooth(0, T, t)
    tr.look(stage, (0.5 + 1.8 * p, 0, Z0), 32.0 - 6.0 * p, 6.0, -4.0 + 8.0 * p)

stage.run(update, args, SLOT, "loop-02")
