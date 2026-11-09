"""mosca 3 (sensores): see productions/mecanalia-es/015*/script.json. Taste sensors glow on the fly's raised feet; grime covers and darkens them; the fly rubs and they relight."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import mosca_rig as mr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(340, floor_z=0.0)
mr.counter(S)
mr.plate(S, loc=(0, 0, 0))
F = mr.fly(S, loc=(0.0, -9.0, 2.2), yaw=-1.25)
rk.softboxes(0.7, centre=(0, 0, 30))
tens, tfro = S.t("ensucian", default=4.5), S.t("frota", default=7.5)
mr.rub(F, 1.0, 0.0)
tipA, tipB = mr.tarsus(F, "legA"), mr.tarsus(F, "legB")
mid = tuple((a + b) / 2 for a, b in zip(tipA, tipB))
glow, grime = [], []
for leg in ("legA", "legB"):
    for i in range(6):
        g = S.ball(f"sensor_{leg}_{i}", S.accent, 0.13, (0, 0, 0), seg=10)
        k = S.ball(f"coat_{leg}_{i}", S.hero("g_mark", "#4A2E14", rough=0.9, coat=0.0), 0.26, (0, 0, 0), seg=10)
        S.size(g, [(0, 1e-4), (0.6 + 0.12 * i, 1e-4), (1.0 + 0.12 * i, 1.0)])
        S.size(k, [(0, 1e-4), (tens + 0.1 * i, 1e-4), (tens + 0.5 + 0.1 * i, 1.0), (tfro, 1.0), (tfro + 0.5, 1e-4)])
        glow.append((g, leg, i))
        grime.append((k, leg, i))


def upd(t):
    mr.rub(F, 1.0, phase=max(0.0, t - tfro) * 14.0)
    for lst in (glow, grime):
        for o, leg, i in lst:
            tip = mr.tarsus(F, leg)
            sh = tuple(F.arm.matrix_world @ F.arm.pose.bones[leg].head)
            d = [(s - p) for s, p in zip(sh, tip)]
            n = math.sqrt(sum(x * x for x in d)) or 1.0
            o.location = tuple(p + x / n * (0.25 + 0.55 * i) for p, x in zip(tip, d))


S.every_frame(upd)
S.cam([(0, (mid[0] - 1, mid[1], mid[2]), 46, 10, 40), (tens, mid, 17, 14, 18), (tfro, mid, 13, 10, 8), (S.T, (mid[0], mid[1] + 2, mid[2] - 2), 60, 16, 24)])
S.go()
