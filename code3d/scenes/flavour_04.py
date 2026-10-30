"""palta scene 4: one cilantro sprig, two smell towers: one person gets soap (white foam tokens), the other a fresh lime signal."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import flavour_rig as fr  # noqa: E402
import magnet_rig as mr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(247, floor_z=-1.2)
T = SLOT / c.FPS
W = mk.Words(production, 4)
M = fr.mats()
mk.board(M, fr.Z0 + 0.3, h=11.4)
Z0 = fr.Z0
P = [fr.Person(i, M, None) for i in range(3)]
A = fr.Avocado(M)
A.root.scale = (1e-4,) * 3
cil = fr.cilantro(M)
cil.scale = (1e-4,) * 3
for p in P:
    p.set_gain((1.0, 1.0, 1.0))
for tok in P[0].streams[1].o:
    tok.data.materials[0] = M["foam"]
P[0].gauge.seg[1].data.materials[0] = M["foam"]
t_or, t_cil, t_soap, t_fresh = W.t("OR6A2,", default=2.8), W.t("cilantro", default=3.8), W.t("jabón", default=4.6), W.t("fresco", default=6.3)
ring = mr.ring(m, "ring", 1.0, 1.0, (0.0, -0.4, Z0 + 2.0))
ring.scale = (1e-4,) * 3
SM = (0.0, 1.0, 0.0)


def update(scene_):
    t = scene_.frame_current / c.FPS
    s = 1e-4 if t < t_cil - 0.3 else max(1e-4, tr.back((t - t_cil + 0.3) / 0.5))
    cil.scale = (s * 0.8,) * 3
    for i in (0, 2):
        p = P[i]
        t_on = t_soap if i == 0 else t_fresh
        h = p.play_ch(t, 1, t_on, T, a=(0.0, 1.6, 0.0), fill_dur=1.4)
        p.gauge.set([0.0, h, 0.0])
    tr.look(stage, (0.0, 0, Z0 + 1.6), 33.0 - 3.0 * c.smooth(0, T, t), 6.0, -4.0 + 8.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "flavour-04")
