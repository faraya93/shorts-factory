"""nube 1 (hook): a cloud sits on the left pan of a balance and tips it down; cars pile onto the right pan until it levels; counter 300."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import setpiece as sp  # noqa: E402
import cloud_rig as cr  # noqa: E402
import common as c  # noqa: E402

S = sp.Shot(244)
M = cr.palette(S)
t_cars, t_300 = S.t("común", default=5.4), S.t("trescientos", default=6.2)
H, L = 12.0, 6.5
S.box("post", (1.3, 1.3, H), (0, 0.6, H / 2), S.ink, bevel=0.3, pop=(0.05, 0.4))
S.box("base", (6.0, 3.0, 0.8), (0, 0.6, 0.4), S.ink, bevel=0.3, pop=(0.05, 0.4))
beam = S.box("beam", (2 * L + 1.4, 1.0, 0.9), (0, 0, H), M["board"], bevel=0.3, pop=(0.2, 0.4))
panL = S.cyl("panL", 4.6, 0.45, (-L, 0, 6), M["plate"], axis="Z", verts=64, bevel=0.1, pop=(0.3, 0.4))
panR = S.cyl("panR", 4.6, 0.45, (L, 0, 6), M["plate"], axis="Z", verts=64, bevel=0.1, pop=(0.3, 0.4))
rodL = S.cyl("rodL", 0.12, 1.0, (-L, 0, 9), S.ink, axis="Z", verts=12)
rodR = S.cyl("rodR", 0.12, 1.0, (L, 0, 9), S.ink, axis="Z", verts=12)
cloud = S.empty("cloudg", (-L, 0, 9))
for p in cr.puffs(S, M, (0, 0, 0), n=24, rx=3.6, ry=2.0, rz=2.0, seed=3, pop0=0.5, stagger=0.04, r=(0.9, 1.7)):
    p.parent = cloud
tpl = [cr.car_template(S, M, k, f"car{k}") for k in range(4)]
for t_ in tpl:
    t_.scale = (0.5, 0.5, 0.5)
    S.items[-1][1]["base"] = (0.5, 0.5, 0.5)
NCARS = 66
def cars_n(t):
    return max(0, min(NCARS, int((t - 1.6) ** 1.55 * 2.2))) if t > 1.6 else 0
def theta(t):
    n = cars_n(t)
    return -0.34 * (1.0 - min(1.0, n / 60.0)) + 0.02 * math.sin(3.0 * t) * (1.0 - min(1.0, (t - 6.0) / 1.0 if t > 6 else 0))
def balance(t):
    th = theta(t)
    beam.rotation_euler = (0, th, 0)
    zl, zr = H + L * math.sin(th), H - L * math.sin(th)
    xl, xr = -L * math.cos(th), L * math.cos(th)
    for pan, rod, x, z in ((panL, rodL, xl, zl), (panR, rodR, xr, zr)):
        pan.location = (x, 0, z - 4.2)
        rod.location = (x, 0, z - 2.1)
        rod.scale = (1, 1, 4.2)
    cloud.location = (xl, 0, zl - 4.0 + 1.9)
S.every_frame(balance)
def car(i, t):
    n = cars_n(t)
    if i >= n:
        return None
    th = theta(t)
    zr, xr = H - L * math.sin(th) - 4.2, L * math.cos(th)
    layer, idx = i // 6, i % 6
    gx, gy = (idx % 3 - 1) * 2.0, (idx // 3 - 0.5) * 1.3
    born = 1.6 + ((i / 2.2) ** (1 / 1.55))
    fall = max(0.0, 1.0 - (t - born) / 0.28)
    return (xr + gx, gy, zr + 0.25 + layer * 0.78 + 14.0 * fall ** 2), 1.0
for k in range(4):
    S.swarm(NCARS // 4 + 1, tpl[k], lambda i, t, k=k: car(i * 4 + k, t) if i * 4 + k < NCARS else None)
S.cam([(0, (0, 0, 9), 34, 10, -22), (3.0, (2.0, 0, 11), 40, 12, -6), (6.2, (3.0, 0, 14), 54, 12, 8), (S.T, (2.0, 0, 14), 62, 16, 4)])
S.go()
