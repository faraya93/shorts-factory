"""hielo 3 (cubos): the imagined version: cubes fall to the bottom of a glass one after another and pile up to the top."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_rig as ir  # noqa: E402

S = sp.Shot(179)
M = ir.palette(S)
t_cub, t_fon, t_api = S.t("cubo", default=1.8), S.t("fondo,", default=2.3), S.t("apila", default=3.7)
S.box("plate", (8.0, 5.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
H = 10.5
ir.cup(S, M, 0, r=2.7, h=H, level=H - 1.6, liquid="water", name="tall", pop=0.1)
tpl = ir.ice_cube(S, M, "tc", 1.6, (0, 0, 20))
N = 10
def cube(i, t):
    t0 = 1.0 + 0.36 * i
    if t < t0:
        return None
    layer, side = i // 2, i % 2
    zf = 0.35 + 0.8 + layer * 1.62
    xf = (-0.85 if side == 0 else 0.85) + 0.1 * math.sin(i * 2.1)
    k = (t - t0) / 0.9
    z = zf + max(0.0, 1.0 - k) ** 2 * (H + 6 - zf)
    if k > 1.0:
        z = zf + 0.08 * max(0.0, 1.0 - (k - 1.0) * 3) * math.sin(14 * (k - 1.0))
    return (xf, 0.0, z), 1.0, (0.0, 0.0, 0.25 * math.sin(i) * max(0.0, 1.0 - k))
S.swarm(N, tpl, cube)
S.cam([(0, (0, 0, 7), 40, 12, -26), (2.0, (0, 0, 6), 26, 8, 0), (4.0, (0, 0, 3.0), 22, 6, 18), (S.T, (0, 0, 5.0), 26, 10, 24)])
S.go()
