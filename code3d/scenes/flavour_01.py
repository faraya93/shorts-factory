"""palta scene 1 (hook): one avocado half feeds three columns; each column shows a different signal."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import flavour_rig as fr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(234, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 1)
M = fr.mats()
mk.board(M, fr.Z0 + 0.3, h=11.4)
Z0 = fr.Z0
P = [fr.Person(i, M, None) for i in range(3)]
A = fr.Avocado(M)
tp = W.t("palta", default=1.0) - 0.25
ton = {1: W.t("cremosa", default=1.5), 0: W.t("incomible", default=3.0), 2: W.t("Cambia", default=5.0)}


def update(scene_):
    t = scene_.frame_current / c.FPS
    A.pop(t, tp)
    for i in range(3):
        P[i].play(t, ton[i], T, fill_dur=2.2)
    tr.look(stage, (0.0, 0, Z0 + 0.3), 36.0 - 2.0 * c.smooth(0, T, t), 6.0, -5.0 + 10.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "flavour-01")
