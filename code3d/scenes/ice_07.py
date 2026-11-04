"""hielo 7 (cierre): cups where most solids sink and only the ice floats; the cube shows its open lattice; the pull-back to two glasses; ENVIASELO."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_rig as ir  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(347)
M = ir.palette(S)
t_poc, t_cong, t_sig = S.t("pocas", default=2.8), S.t("congelarse.", default=4.9), S.t("Sígueme,", default=6.5)
S.box("plate", (22.0, 7.0, 0.6), (0, 0, -0.3), M["plate"], bevel=0.25, pop=(0.05, 0.4))
big_g, big_l, SURF = ir.cup(S, M, 0, r=3.4, h=8.6, level=6.2, liquid="water", name="main", pop=0.1)
cube = ir.ice_cube(S, M, "cube", 3.0, (0, 0, 12.0), pop=(0.5, 0.4))
S.move(cube, [(0.5, (0, 0, 12.0)), (1.3, (0, 0, SURF + 0.8)), (S.T, (0, 0, SURF + 0.8))])
S.every_frame(lambda t: setattr(cube, "rotation_euler", (0.05 * math.sin(3 * t), 0.07 * math.sin(2.6 * t), 0.0)))
# the others: lumps that sink in their own liquids (appear on "pocas")
for k, (x, liq, h) in enumerate(((-9.0, "oil", "lump"), (-5.0, "water", "lump"), (5.0, "oil", "ox"), (9.0, "water", "ox"))):
    ir.cup(S, M, x, r=1.8, h=5.4, level=3.9, liquid=liq, name=f"c{k}", pop=t_poc - 0.5 + 0.15 * k)
    o = S.box(f"lp{k}", (1.3, 1.3, 1.2), (x, 0, 9.0), M[h], bevel=0.25, pop=(t_poc + 0.2 + 0.15 * k, 0.3))
    S.move(o, [(t_poc + 0.2 + 0.15 * k, (x, 0, 9.0)), (t_poc + 0.8 + 0.15 * k, (x, 0, 4.2)), (t_poc + 1.6 + 0.15 * k, (x, 0, 1.0))])
# lattice inside the cube on "congelarse"
lat = [(x * 0.8, y * 0.8, z * 0.8) for x in (-1, 0, 1) for y in (-1, 0, 1) for z in (-1, 0, 1)]
for i, p in enumerate(lat):
    o = S.ball(f"lo{i}", M["ox"], 0.26, (0, 0, 0), seg=12, pop=(t_cong + 0.03 * i, 0.3))
    S.every_frame(lambda t, o=o, p=p: setattr(o, "location", (p[0], p[1] - 0.6, SURF + 0.8 + p[2])))
for a in range(0, 27):
    pass
S.every_frame(lambda t: None)
S.cam([(0, (0, 0, 6), 30, 12, -26), (t_poc, (0, 0, 5), 44, 8, -4), (t_cong - 0.5, (0, 0, 5), 26, 6, 8), (t_cong + 1.2, (0, -1, 7.0), 12, 4, 0), (t_sig, (0, 0, 6), 34, 10, -6), (S.T, (0, 0, 6), 46, 14, 8)])
S.go()
