"""cepillo 3 (nube): see productions/mecanalia-es/012*/script.json. Reshape rung 2: the bowl water turns blue, so the droplets show; they climb to face height and speckle a white tile."""
import sys
from pathlib import Path

import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import cepillo_rig as cr  # noqa: E402
import common as c  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(292, floor_z=0.0)
COL = {"ceramic": "#F5F2EC", "seat": "#E9E2D6", "cup": "#E8B23A", "toothbrush": "#B8327E", "brush": "#2B3442"}
B = cr.bathroom(S, COL)
rk.softboxes(0.5, centre=(0, 0, 70))
W = cr.Water(S)
tc = S.t("color", default=3.2)
ts = S.t("subieron", default=6.4)
BLUE = "#1E46FF"
tile = S.box("white_tile", (74.0, 1.2, 74.0), (0.0, 34.0, 150.0), S.hero("g_board_tile", "#F7F6F2", rough=0.2, coat=0.5), bevel=0.3)
surf = next(n for n in W.obj.data.materials[0].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
floor_b = next(n for n in bpy.data.materials["clear_floor"].node_tree.nodes if n.type == "BSDF_PRINCIPLED")
pale, blue = np.array(c.linear("#E4F0F1")[:3]), np.array(c.linear(BLUE)[:3])
N = 2200
P = cr.Plume(N, seed=12, flat=0.7)
beads = cr.Beads(S, "plume", N, cr.bead_mat("clear_plume", BLUE, 0.2))
M = 260
rng = np.random.default_rng(4)
at = np.stack([rng.uniform(-35, 35, M), np.full(M, 33.3), rng.uniform(115, 185, M)], axis=1)
drop_r, drop_t = rng.uniform(0.5, 1.3, M), rng.uniform(0.0, 1.8, M)
stains = cr.Beads(S, "stains", M, cr.bead_mat("clear_stain", BLUE, 0.1))
stain_unit = stains.unit * np.array([1.0, 0.12, 1.0], dtype=np.float32)


def upd(t):
    k = sp.interp([(tc, 0.0), (tc + 0.5, 1.0)], t)
    rgb = pale + (blue - pale) * k
    floor_b.inputs["Base Color"].default_value = (*rgb, 1.0)
    floor_b.inputs["Emission Color"].default_value = (*rgb, 1.0)
    surf.inputs["Base Color"].default_value = (*(1.0 + (blue - 1.0) * 0.6 * k), 1.0)
    W.update(cr.turbulence(W.R, W.TH, t, 1.2))
    u = np.full(N, np.clip((t - tc + 0.1) / 3.4, 0.0, 1.0))
    p, on = P.rise(u)
    beads.set(p, P.size * 0.8 * on * float(t >= tc - 0.1))
    r = drop_r * np.clip((t - ts - drop_t) / 0.2, 0.0, 1.0)
    co = (at[:, None, :] + r[:, None, None] * stain_unit[None, :, :]).astype(np.float32)
    stains.obj.data.vertices.foreach_set("co", co.reshape(-1))
    stains.obj.data.update()


S.every_frame(upd)
S.cam([(0, (0, -11, 52), 165, 12, -8), (tc, (0, -11, 88), 250, 7, -2), (S.T, (0, -11, 118), 372, 5, 6)])
S.go()
