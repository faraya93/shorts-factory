"""hielo2 2 (nueve): a glass of real water freezes from the bottom up (the water material hands over to the ice material along a front) and the ice ends ~9 % above the mark."""
import copy
import math
import sys
from pathlib import Path
import bpy
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402

S = sp.Shot(213)
R_, H_, LV, BASE = 5.0, 12.5, 9.0, 1.1
G = rk.glass()
W = rk.water("clear_water", "#DFF3F6", density=0.02, clip="above")
I = rk.ice("clear_ice", core=0.6, seed=3.0, clip="below")
glass, liquid = rk.tumbler(S, "glass", G, W, r=R_, h=H_, level=LV)
ice_o = liquid.copy()
ice_o.data = liquid.data.copy()
ice_o.data.materials.clear()
ice_o.data.materials.append(I)
bpy.context.scene.collection.objects.link(ice_o)
rk.noshadow(ice_o)
ice_o.scale = (0.99, 0.99, 1.0)                  # a hair smaller than the water so the two surfaces never coincide (a ray would skip the visible one)
S.reg(ice_o)
t_a, t_b = S.t("congelarse", default=1.3), S.t("nueve", default=2.7)
def front(t):
    f = sp.interp([(0, BASE), (t_a, BASE), (t_b + 0.3, LV + 0.8)], t)
    rk.set_front(W, f)
    rk.set_front(I, f)
S.every_frame(front)
S.size(ice_o, [(0, (1, 1, 1)), (t_b + 0.3, (1, 1, 1)), (t_b + 1.6, (1, 1, 1.09))])             # freezing expands ~9 %
S.torus("mark", R_ + 0.06, 0.05, (0, 0, LV), S.ink)                                                 # one thin mark: where the water stood
rk.softboxes(2.2, centre=(0, 0, 8))
S.cam([(0, (0, 0, 8), 34, 10, -22), (S.T * 0.5, (0, 0, 8), 28, 8, -6), (S.T, (0, 0, 9), 24, 8, 10)])
S.go()
