"""pieles-arrugadas 2 (orden): cutaway of the fingertip pad: a nerve signal runs down, the vessels (tubes) tighten and fewer beads flow."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import wrinkle_rig as wr  # noqa: E402

S = sp.Shot(195)
M = wr.palette(S)
t_ord, t_vas, t_apr = S.t("orden,", default=3.0), S.t("vasos", default=3.8), S.t("aprietan.", default=5.1)
S.box("plate", (10.0, 0.8, 12.5), (0, 0.7, 6.4), M["plate"], bevel=0.3, pop=(0.1, 0.45))
S.box("skin", (10.0, 1.0, 2.2), (0, -0.05, 11.9), M["skin"], bevel=0.3, pop=(0.4, 0.45))
vz = [9.0, 6.9, 4.8]
vess = [S.cyl(f"vessel{i}", 0.6, 9.4, (0, -0.05, z), M["vessel"], axis="X", verts=32, pop=(0.7 + 0.15 * i, 0.4)) for i, z in enumerate(vz)]
for v in vess:
    S.size(v, [(t_apr - 0.3, (1, 1, 1)), (t_apr + 0.9, (0.45, 0.45, 1.0))])
bead = S.ball("bead", M["bead"], 0.42, (0, -0.1, 0))
def flow(i, t):
    lane, k = i % 3, i // 3
    if t < 1.2:
        return None
    squeezed = t > t_apr
    if squeezed and k >= 3:
        return None
    sp_ = 0.22 if not squeezed else 0.12
    x = -4.4 + 8.8 * ((t * sp_ + k / 6.0 + lane * 0.13) % 1.0)
    r = 1.0 if not squeezed else 0.55
    return (x, -0.1, vz[lane]), r
S.swarm(18, bead, flow)
nerve = S.line("nerve", [(-3.6, -0.3, 18.0), (-3.6, -0.3, 13.5), (-3.6, -0.3, 10.5), (-3.6, -0.3, 8.2)], 0.22, S.accent, grow=(0.9, 2.0), smooth=False)
pulse = S.ball("pulse", S.accent, 0.6, (-3.6, -0.4, 18.0))
for j, a in enumerate((t_ord - 0.3, t_ord + 0.5, t_ord + 1.2)):
    pj = S.ball(f"pulse{j}", S.accent, 0.6, (-3.6, -0.4, 18.0), pop=(a, 0.15))
    S.move(pj, [(a, (-3.6, -0.4, 18.0)), (a + 0.55, (-3.6, -0.4, 8.4))])
    S.gone(pj, a + 0.5, 0.2)
S.move(pulse, [(0, (-3.6, -0.4, 18.0))]); S.gone(pulse, 0.0, 0.01)
S.cam([(0, (0, 0, 10), 44, 10, -24), (3.0, (-1.0, 0, 9.0), 30, 6, -8), (S.T, (0.5, 0, 7.5), 21, 4, 10)])
S.go()
