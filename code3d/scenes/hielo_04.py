"""hielo 4 (lago): a lake as a water box; ice rises from the bottom; the summer sun melts only a thin top layer."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import ice_glass as ig  # noqa: E402

S = sp.Shot(220, floor_z=0.0)
M = ig.palette(S)
L, D, Hh = 26.0, 10.0, 10.0
lake = S.box("lake", (L, D, Hh), (0, 0, Hh / 2), M["lake"], bevel=0.5, pop=(0.05, 0.4))
ice = S.box("lakeice", (L - 0.6, D - 0.6, Hh - 0.3), (0, 0, 0.15), M["ice_solid"], bevel=0.4, pop=(0.1, 0.1))
tf = 2.4
S.size(ice, [(0, (1, 1, 0.001)), (tf, (1, 1, 0.001)), (tf + 3.2, (1, 1, 0.82))])
S.move(ice, [(0, (0, 0, 0.2)), (tf, (0, 0, 0.2)), (tf + 3.2, (0, 0, 0.2 + (Hh - 0.3) * 0.41))])
ts = 5.4
sun = S.ball("sun", M["sun"], 2.6, (-8.0, 0, 26.0), pop=(ts, 0.4))
S.move(sun, [(ts, (-8.0, 0, 26.0)), (S.T, (8.0, 0, 26.0))])
melt = S.box("melt", (L - 0.6, D - 0.6, 0.8), (0, 0, Hh * 0.82 + 0.1), M["lake"], bevel=0.2, pop=(ts + 0.8, 0.4))
S.cam([(0, (0, 0, 5), 64, 10, -26), (tf + 2.0, (0, 0, 8), 72, 14, -8), (S.T, (0, 0, 10), 90, 16, 12)])
S.go()
