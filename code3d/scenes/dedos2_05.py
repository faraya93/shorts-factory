"""dedos2 5 (agarre): one pair of real fingertips and a wet stone. Smooth tips lose it and it falls; the tips wrinkle and lift it; the stone dries and the smooth tips hold it too."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import real_kit as rk  # noqa: E402
import finger_rig as fr  # noqa: E402

S = sp.Shot(243)
skin = rk.wet_tissue("g_big", "#C98963", sss=0.35, rough=0.5, coat=0.2)
W = rk.water("clear_water", "#E4F5F4")
R, T = fr.R_DEFAULT, S.T
t_arr = S.t("arrugados", default=2.0)
t_dry = S.t("secos", default=5.2)
SR, ZS = 3.0, 5.0                                                      # stone radius, resting height of the stone's centre
GX = SR * 0.84 + R * 0.92                                              # finger centre distance from the axis while pinching
ZF = ZS - R * 0.95                                                     # finger tip height so the pad's widest part meets the stone
fl = fr.Fingertip(S, skin, "L", L=26.0, loc=(-9.0, 0, ZF + 6))
fr_ = fr.Fingertip(S, skin, "R", L=26.0, loc=(9.0, 0, ZF + 6))
fr_.obj.rotation_euler = (0, 0, math.pi)                              # right finger: pad faces -x
LIFT = 7.0
t_slip, t_fall = 1.9, 2.5
keys_z = [(0, ZF + 6), (0.9, ZF + 6), (1.2, ZF), (1.5, ZF), (t_slip, ZF + 2.2), (t_fall - 0.2, ZF + 3.0),            # smooth tips: pinch, lift a little, the stone slips out
          (t_fall + 0.3, ZF + 6), (t_fall + 0.9, ZF + 6), (t_fall + 1.4, ZF), (3.9, ZF), (4.8, ZF + LIFT), (T, ZF + LIFT)]   # the tips wrinkle on the way, pinch again, lift and hold
keys_xl = [(0, -9.0), (0.9, -9.0), (1.2, -GX), (t_fall - 0.2, -GX - 0.2), (t_fall + 0.3, -9.0), (t_fall + 0.9, -9.0), (t_fall + 1.4, -GX), (T, -GX)]
S.move(fl.obj, [(t, (x, 0, z)) for (t, z), x in zip(keys_z, [-9.0, -9.0, -GX, -GX, -GX, -GX - 0.2, -9.0, -9.0, -GX, -GX, -GX, -GX])])
S.move(fr_.obj, [(t, (-x, 0, z)) for (t, z), x in zip(keys_z, [-9.0, -9.0, -GX, -GX, -GX, -GX - 0.2, -9.0, -9.0, -GX, -GX, -GX, -GX])])
S.every_frame(lambda t: [f.set_wrinkle(sp.interp([(0, 0.0), (t_fall + 0.1, 0.0), (t_fall + 1.3, 1.0), (t_dry, 1.0), (t_dry + 1.0, 0.0)], t)) for f in (fl, fr_)])
wet = rk.wet_tissue("g_pin", "#F2B3C3", sss=0.35, rough=0.25, coat=1.0)        # a bar of soap: pale pink, glossy and wet
wb = next(n for n in wet.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
foam_m = rk.wet_tissue("g_mark", "#FFFFFF", sss=0.2, rough=0.6, coat=0.3)
import random


def soap(name, loc, seed, **tk):
    root = S.empty(name, loc, **tk)
    bar = S.box(name + "_bar", (SW, 6.4, 8.4), (0, 0, 0), wet, bevel=1.0, parent=root)
    rng = random.Random(seed)
    for i in range(9):                                                   # suds clinging to the top and sides
        r_ = rng.uniform(0.35, 0.8)
        f = S.ball(f"{name}_foam{i}", foam_m, r_, (rng.uniform(-SW / 2, SW / 2), rng.uniform(-3.0, 3.0), 4.1 + rng.uniform(-0.2, 0.3)), parent=root)
        S.gone(f, t_dry - 0.3, 0.3)
    return root


SW = 2 * (SR * 0.84)
sA = soap("soapA", (0, 0, ZS), 5, pop=(0.15, 0.3))
S.move(sA, [(0.15, (0, 0, ZS)), (1.4, (0, 0, ZS)), (t_slip, (0, 0, ZS + 2.2)), (t_slip + 0.25, (0, 0, ZS + 2.6)), (t_slip + 0.7, (0.4, 0, ZS - 4)), (t_fall + 0.1, (0.8, 0, ZS - 24))])
S.spin(sA, [(0, (0, 0, 0)), (t_slip, (0, 0, 0)), (t_fall, (1.2, 0.5, 0.7))])
S.gone(sA, t_fall + 0.1, 0.1)
sB = soap("soapB", (0, 0, ZS), 2, pop=(t_fall + 0.6, 0.25))
S.move(sB, [(t_fall + 0.6, (0, 0, ZS)), (3.9, (0, 0, ZS)), (4.8, (0, 0, ZS + LIFT)), (T, (0, 0, ZS + LIFT))])
def dry_out(t):
    k = sp.interp([(0, 0.0), (t_dry, 0.0), (t_dry + 0.7, 1.0)], t)
    wb.inputs["Coat Weight"].default_value = 1.0 - k
    wb.inputs["Roughness"].default_value = 0.25 + 0.5 * k
S.every_frame(dry_out)
for i in range(6):                                                    # drops thrown off by the slipping stone
    ang = 0.7 + i * 0.75
    d = rk.droplet(S, f"fly{i}", W, 0.22 + 0.04 * (i % 3), (0, 0, ZS), pop=(t_slip + 0.05 * i, 0.12))
    S.move(d, [(t_slip + 0.05 * i, (math.cos(ang) * 2.0, 0.2, ZS + 0.5)), (t_slip + 0.5 + 0.05 * i, (math.cos(ang) * 5.5, 1.2, ZS + 0.5 + math.sin(ang) * 3.0)), (t_slip + 1.2 + 0.05 * i, (math.cos(ang) * 8.0, 2.4, ZS - 9.0))])
    S.gone(d, t_slip + 1.2 + 0.05 * i, 0.15)
rk.softboxes(3.0, centre=(0, 0, 6), sides=False)
S.cam([(0, (0, 0, 6.0), 46, 3, -4), (T * 0.5, (0, 0, 7.0), 42, 3, 2), (T, (0, 0, 9.5), 44, 3, 6)])
S.go()
