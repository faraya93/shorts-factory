"""hielo 1 (vasos): the what-if teaser: a cube sinks in water; then a lump of oil sinks in its liquid, and the real ice cube pops back up and floats."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_rig as ir  # noqa: E402

S = sp.Shot(221)
M = ir.palette(S)
t_hun, t_flo, t_sol, t_hund = S.t("hunde", default=3.7), S.t("flota.", default=6.1), S.t("sólido", default=3.2), S.t("hundiera?", default=1.3)
XL, XR = -3.8, 3.8
S.box("plate", (17.0, 7.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
ir.cup(S, M, XL, liquid="oil", name="cupL", pop=0.2)
ir.cup(S, M, XR, liquid="water", name="cupR", pop=0.3)
SURF = 4.8
# right cube: drops, sinks (the what-if), then rises and floats on "flota"
cube = ir.ice_cube(S, M, "cube", 1.9, (XR, 0, 12), pop=(0.6, 0.4))
S.move(cube, [(0.6, (XR, 0, 12.0)), (t_hund - 0.3, (XR, 0, SURF + 1.2)), (t_hund + 0.5, (XR, 0, 1.2)), (t_hund + 0.7, (XR, 0, 1.15)), (4.8, (XR, 0, 1.15)), (t_flo - 0.7, (XR, 0, 1.2)), (t_flo + 0.1, (XR, 0.0, SURF + 0.45))])
S.every_frame(lambda t: setattr(cube, "rotation_euler", (0.0, 0.0, 0.0)) if t < t_flo else setattr(cube, "rotation_euler", (0.06 * math.sin(4 * t), 0.08 * math.sin(3.3 * t), 0)))
# left lump: falls on "hunde" and stays at the bottom
lump = S.box("lump", (2.0, 2.0, 1.8), (XL, 0, 12), M["lump"], bevel=0.35, pop=(t_sol - 0.6, 0.4))
S.move(lump, [(t_sol - 0.6, (XL, 0, 12.0)), (t_hun, (XL, 0, SURF + 1.3)), (t_hun + 1.0, (XL, 0, 1.3))])
for k in range(2):
    r = S.torus(f"rip{k}", 1.0, 0.06, (XL, 0, SURF), M["ice"], rot=(0, 0, 0))
    a = t_hun + 0.05 + 0.3 * k
    S.size(r, [(a, 0.3), (a + 1.0, 2.0)]); S.pop(r, a, 0.05); S.gone(r, a + 0.6, 0.4)
S.cam([(0, (0, 0, 5), 32, 14, -34), (2.4, (0, 0, 4.4), 25, 8, -8), (t_hun + 0.6, (-1.5, 0, 3.8), 20, 6, 14), (t_flo, (2.0, 0, 4.4), 20, 8, 4), (S.T, (0, 0, 4.8), 26, 14, -12)])
S.go()
