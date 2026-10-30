"""palta scene 7 (closing): the same avocado, three columns, three signals; the C2 tag sits below."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import flavour_rig as fr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(386, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 7)
M = fr.mats()
mk.board(M, fr.Z0 + 0.3, h=11.4)
Z0 = fr.Z0
P = [fr.Person(i, M, None) for i in range(3)]
A = fr.Avocado(M)
t_end = W.t("envíaselo", default=T - 3.0)


def update(scene_):
    t = scene_.frame_current / c.FPS
    for p in P:
        p.play(t, 0.2, T, fill_dur=1.5)
    s = tr.back(min(1.0, max(0.0, (t - t_end + 0.1) / 0.5))) if t > t_end - 0.1 else 1.0
    A.root.scale = (A.size * (1.0 + 0.12 * (s - 1.0 if t > t_end - 0.1 else 0.0)),) * 3
    p_ = c.smooth(0, T, t)
    tr.look(stage, (0.0, 0, Z0 + 0.3), 34.0 + 6.0 * p_, 6.0, -4.0 + 8.0 * p_)

stage.run(update, args, SLOT, "flavour-07")
