"""palta scene 3: personal sensor gains: the taste tower grows or shrinks per person (TAS2R38); supertaster ring."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import flavour_rig as fr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(392, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 3)
M = fr.mats()
mk.board(M, fr.Z0 + 0.3, h=11.4)
Z0 = fr.Z0
P = [fr.Person(i, M, None) for i in range(3)]
A = fr.Avocado(M)
for p in P:
    p.set_gain((1.0, 1.0, 1.0))
t_var, t_hit, t_super = W.t("TAS2R38", default=3.6), W.t("hacen", default=4.8), W.t("supercatadores", default=10.0)
ring = mr.ring(m, "ring", 1.0, 1.0, (fr.COLS[0] - 1.15, -0.4, Z0 + 2.2))
TARGET = fr.GAINS
BITTER = (0.7, 0.0, 0.0)


def update(scene_):
    t = scene_.frame_current / c.FPS
    k = c.smooth(t_var, t_var + 1.2, t)
    for i, p in enumerate(P):
        g = [1.0 + (TARGET[i][0] - 1.0) * k, 1.0, 1.0]
        p.set_gain(g)
        h = p.play_ch(t, 0, t_hit, T, a=BITTER)
        p.gauge.set([h, 0.0, 0.0])
    s = 1e-4 if t < t_super else 0.75 * min(1.0, (t - t_super) / 0.4)
    ring.scale = (s, 1.0, s)
    tr.look(stage, (0.0, 0, Z0 + 0.3), 33.0, 6.0, -3.0 + 6.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "flavour-03")
