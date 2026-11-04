"""pieles-arrugadas 5 (agarre): two pinches try to hold a wet marble: the smooth pair loses it, the grooved pair lifts it; dry, both hold."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import wrinkle_rig as wr  # noqa: E402

S = sp.Shot(232)
M = wr.palette(S)
t_moj, t_est, t_rap, t_sec = S.t("mojado:", default=1.2), S.t("estudio,", default=2.1), S.t("rápido,", default=5.0), S.t("secos,", default=5.9)
S.box("tray", (15.0, 5.0, 0.7), (0, 0, 0.0), M["plate"], bevel=0.25, pop=(0.05, 0.4))
def pair(x0, grooved):
    mar = S.ball(f"m{x0}", M["marble"], 0.95, (x0, 0, 1.3), pop=(0.3, 0.4))
    shell = S.ball(f"w{x0}", M["water"], 1.12, (x0, 0, 1.3), pop=(t_moj, 0.35))
    S.gone(shell, t_sec, 0.3)
    fingers = []
    for side in (-1, 1):
        f = S.cyl(f"fg{x0}{side}", 0.62, 3.6, (0, 0, 0), M["skin"], axis="X", verts=32, pop=(0.4, 0.4))
        tip = S.ball(f"ft{x0}{side}", M["skin"], 0.62, (0, 0, 0), parent=f, seg=24)
        tip.location = (0, 0, -side * 1.8)
        if grooved:
            for k in range(4):
                r = S.torus(f"fr{x0}{side}{k}", 0.65, 0.07, (0, 0, -side * (0.5 + 0.45 * k)), M["skin_dk"], parent=f, rot=(0, 0, 0), pop=(t_est - 0.8 + 0.1 * k, 0.3))
        fingers.append((f, side))
    return mar, shell, fingers
mL, sL, fL = pair(-3.5, False)
mR, sR, fR = pair(3.5, True)
def fpos(f, side, x0, gap, z, ydrift=0.0):
    return (x0 + side * gap, ydrift, z)
# right lane: pinch at t_est, lift, hold; left lane: pinch, the marble pops out, it tries again
LIFT = [(0.4, 9.0), (2.0, 1.3), (2.6, 1.3), (3.6, 7.5), (t_sec + 0.2, 7.5), (t_sec + 0.8, 1.4), (6.6, 1.4), (7.3, 7.0), (S.T, 7.0)]
GAPR = [(0.4, 3.8), (1.9, 3.8), (2.4, 1.15), (t_sec + 0.1, 1.15), (t_sec + 0.5, 3.0), (6.4, 3.0), (6.9, 1.15), (S.T, 1.15)]
for f, side in fR:
    S.move(f, [(a, (3.5 + side * g, 0, z)) for (a, z), (_, g) in zip(LIFT[:len(GAPR)], GAPR)] if False else [(0.4, (3.5 + side * 3.8, 0, 9.0)), (1.9, (3.5 + side * 3.8, 0, 1.3)), (2.4, (3.5 + side * 1.15, 0, 1.3)),
                                                                                  (3.6, (3.5 + side * 1.15, 0, 7.5)), (t_sec + 0.1, (3.5 + side * 1.15, 0, 7.5)), (t_sec + 0.6, (3.5 + side * 1.15, 0, 1.3)), (6.6, (3.5 + side * 3.2, 0, 1.3)),
                                                                                  (6.9, (3.5 + side * 3.2, 0, 1.3)), (7.1, (3.5 + side * 1.15, 0, 1.3)), (S.T, (3.5 + side * 1.15, 0, 7.0))])
S.move(mR, [(2.0, (3.5, 0, 1.3)), (2.4, (3.5, 0, 1.3)), (3.6, (3.5, 0, 7.5)), (t_sec + 0.1, (3.5, 0, 7.5)), (t_sec + 0.6, (3.5, 0, 1.3)), (7.1, (3.5, 0, 1.3)), (S.T, (3.5, 0, 7.0))])
S.move(sR, [(2.0, (3.5, 0, 1.3)), (2.4, (3.5, 0, 1.3)), (3.6, (3.5, 0, 7.5))])
# left lane: smooth fingers pinch and lift, the marble squirts out and drops; again; then dry: it holds
for f, side in fL:
    S.move(f, [(0.4, (-3.5 + side * 3.8, 0, 9.0)), (1.9, (-3.5 + side * 3.8, 0, 1.3)), (2.4, (-3.5 + side * 1.15, 0, 1.3)), (3.0, (-3.5 + side * 1.15, 0, 4.2)), (3.4, (-3.5 + side * 2.4, 0, 4.4)),
                (4.4, (-3.5 + side * 1.15, 0, 1.3)), (4.8, (-3.5 + side * 1.15, 0, 3.6)), (5.2, (-3.5 + side * 2.6, 0, 4.0)), (t_sec + 0.9, (-3.5 + side * 3.2, 0, 1.3)), (6.9, (-3.5 + side * 3.2, 0, 1.3)),
                (7.1, (-3.5 + side * 1.15, 0, 1.3)), (S.T, (-3.5 + side * 1.15, 0, 7.0))])
mv = [(2.4, (-3.5, 0, 1.3)), (3.0, (-3.5, 0, 4.2)), (3.2, (-3.5, 0, 6.0)), (3.45, (-3.4, 1.2, 8.3)), (3.9, (-3.2, 2.6, 4.0)), (4.4, (-3.0, 3.0, 1.2)), (4.8, (-3.0, 2.0, 1.2)), (5.2, (-3.5, 0, 1.3)),
      (6.6, (-3.5, 0, 1.3)), (7.1, (-3.5, 0, 1.3)), (S.T, (-3.5, 0, 7.0))]
S.move(mL, mv)
S.move(sL, [(2.4, (-3.5, 0, 1.3))] + mv[1:6]); S.gone(sL, t_sec, 0.3)
S.cam([(0, (0, 0, 4.2), 30, 12, -26), (2.4, (0, 0, 4.2), 23, 8, 0), (5.0, (0, 0, 4.6), 23, 14, 14), (S.T, (0, 0, 4.8), 30, 22, -6)])
S.go()
