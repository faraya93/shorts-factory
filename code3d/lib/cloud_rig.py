"""Rig for 007 (nube-cuantos-autos-pesa): palette, a cloud built from spheres, one-mesh toy cars, point clouds, a wireframe cube."""
import math
import random
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

CLOUD, DROP, CAR_COLOURS, SMOKE = "#FFFFFF", "#1E4DB0", ("#F2C94C", "#6C4FD6", "#E6E6EA", "#2F9E8F"), "#4A4F57"


def palette(S):
    return {"cloud": S.hero("big", CLOUD, rough=0.9, coat=0.0), "drop": S.glass("#5468E0", alpha=0.7, rough=0.05), "drop_solid": S.hero("small", DROP, rough=0.15, coat=0.4),
            "smoke": S.hero("rubber", SMOKE, rough=0.9, coat=0.0), "wheel": S.hero("ink", "#202020", rough=0.6), "glass": S.glass("#FFFFFF", alpha=0.14, rough=0.1, name="foam"),
            "cars": [S.hero(r, h, rough=0.35, coat=0.4) for r, h in zip(("housing", "mark", "blade", "small"), CAR_COLOURS)], "plate": S.plate_mat(), "board": S.board_mat()}


def blob_points(n, rx, ry, rz, seed=1, flat_bottom=True):
    rnd = random.Random(seed)
    out = []
    while len(out) < n:
        x, y, z = rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)
        if x * x + y * y + z * z <= 1.0:
            if flat_bottom and z < -0.45:
                z = -0.45 + (z + 0.45) * 0.2
            out.append((x * rx, y * ry, z * rz))
    return out


def puffs(S, M, c, n=26, rx=5.5, ry=2.6, rz=3.0, seed=2, pop0=0.1, stagger=0.03, r=(1.1, 2.1)):
    """A cumulus: spheres in a flat-bottomed blob around c; returns the list (each popped in staggered from pop0)."""
    rnd = random.Random(seed + 7)
    out = []
    for i, (x, y, z) in enumerate(blob_points(n, rx, ry, rz, seed)):
        out.append(S.ball(f"puff{i}", M["cloud"], rnd.uniform(*r), (c[0] + x, c[1] + y, c[2] + z), seg=20, pop=(pop0 + stagger * i, 0.45)))
    return out


def car_template(S, M, k, name="car"):
    """Toy car as ONE mesh (body + cabin + 4 wheels), joined, nose along +x, 3.6 long; k picks the colour."""
    mat = M["cars"][k % len(M["cars"])]
    parts = [tr.rbox(name + "_b", (3.6, 1.8, 0.9), (0, 0, 0.75), mat, bevel=0.25), tr.rbox(name + "_c", (2.0, 1.6, 0.8), (-0.2, 0, 1.5), mat, bevel=0.25)]
    for sx in (-1.1, 1.1):
        for sy in (-0.95, 0.95):
            parts.append(tr.cyl(f"{name}_w", 0.42, 0.35, (sx, sy, 0.42), M["wheel"], axis="Y", verts=20))
    bpy.ops.object.select_all(action="DESELECT")
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = name
    return S.reg(o)


def cube_frame(S, mat, c, side, r=0.09, grow=(0.0, 1.0)):
    """Twelve edge tubes of a cube centred on c (drawn together, as one growing outline)."""
    h = side / 2
    P = [(sx, sy, sz) for sx in (-h, h) for sy in (-h, h) for sz in (-h, h)]
    edges = [(a, b) for i, a in enumerate(P) for b in P[i + 1:] if sum(abs(u - v) > 1e-6 for u, v in zip(a, b)) == 1]
    return [S.line("edge", [(c[0] + a[0], c[1] + a[1], c[2] + a[2]), (c[0] + b[0], c[1] + b[1], c[2] + b[2])], r, mat, grow=grow, smooth=False) for a, b in edges]
