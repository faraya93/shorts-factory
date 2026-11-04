"""Rig for 008 (hielo-que-pasaria-si-se-hundiera): palette, glass cups, ice, a fish, a lattice of water molecules."""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402

ICE, WATER, OIL, LUMP, FISH, OXY, HYD = "#68B8EA", "#8FD3F5", "#F2A63B", "#FFE9B0", "#FF7A8A", "#FF5A5F", "#FFFFFF"


def palette(S):
    return {"ice": S.glass(ICE, alpha=0.96, rough=0.15), "water": S.glass(WATER, alpha=0.5, rough=0.06), "oil": S.hero("housing", OIL, rough=0.2, coat=0.0, alpha=0.62),
            "lump": S.hero("blade", LUMP, rough=0.5), "fish": S.hero("mark", FISH, rough=0.4, coat=0.3), "ox": S.hero("small", OXY, rough=0.35, coat=0.3),
            "hy": S.hero("rubber", HYD, rough=0.4), "glass": S.glass("#FFFFFF", alpha=0.2, rough=0.05, name="foam"), "plate": S.plate_mat(), "board": S.board_mat()}


def cup(S, M, x, r=2.6, h=6.5, level=4.6, liquid="water", y=0.0, pop=0.2, name="cup"):
    """Glass cylinder standing on z=0 with a liquid inside; returns (glass, liquid, surface_z)."""
    g = S.cyl(name, r, h, (x, y, h / 2), M["glass"], axis="Z", verts=48, bevel=0.05, pop=(pop, 0.45))
    lq = S.cyl(name + "_lq", r - 0.12, level, (x, y, level / 2 + 0.2), M[liquid], axis="Z", verts=48, pop=(pop + 0.1, 0.45))
    return g, lq, level + 0.2


def ice_cube(S, M, name, size, loc, **tk):
    return S.box(name, (size, size, size), loc, M["ice"], bevel=size * 0.12, **tk)


class Fish:
    def __init__(self, S, M, name, color_mat=None, scale=1.0, **tk):
        self.root = S.empty(name, (0, 0, 0), **tk)
        S.ball(name + "_b", color_mat or M["fish"], 0.8 * scale, (0, 0, 0), shape=(1.7, 0.7, 0.9), parent=self.root, seg=20)
        S.cone(name + "_t", 0.7 * scale, 0.05 * scale, 1.0 * scale, (-1.55 * scale, 0, 0), color_mat or M["fish"], rot=(0, math.radians(-90), 0), parent=self.root, verts=16)
        S.ball(name + "_e", M["hy"], 0.16 * scale, (0.9 * scale, -0.5 * scale, 0.2 * scale), parent=self.root, seg=10)

    def swim(self, S, path_fn):
        def upd(t):
            x, y, z, ang = path_fn(t)
            self.root.location = (x, y, z)
            self.root.rotation_euler = (0, 0, ang)
        S.every_frame(upd)


def lattice_points(nx=4, nz=3, ny=3, sx=1.25, sy=1.05, sz=1.15, z0=0.8):
    return [(( i - (nx - 1) / 2) * sx, (j - (ny - 1) / 2) * sy, z0 + k * sz + (0.35 if (i + j) % 2 else 0.0)) for i in range(nx) for j in range(ny) for k in range(nz)]
