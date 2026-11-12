"""Small helpers shared by the block B5 proof stills (code3d/scenes/proof_NN.py): a sealed-figure person with a chosen shirt, the identity accent, and a grey crowd. Runs inside Blender."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import looks  # noqa: E402
import paper_rig as pr  # noqa: E402

SKIN, PANTS, BOOTS = "#E8B89A", "#3A3F4B", "#2A2A30"
GREY, TAUPE = "#8C9096", "#B7A99A"


def accent() -> str:
    return (looks.current() or {}).get("accent", "#117A8B")


def person(S, m, name, loc, rot_z=0.0, shirt="#8C9096", k=2.4):
    return pr.figure(S, m, name, loc, rot_z=rot_z, cols=(SKIN, shirt, PANTS, BOOTS), k=k)


def crowd(S, m, rows, per_row, x0, dx, y0, dy, shirt=GREY, k=2.4, jitter=0.35, tag="c"):
    out = []
    for r in range(rows):
        for i in range(per_row):
            jx = math.sin(r * 12.9 + i * 7.3) * jitter * dx
            out.append(person(S, m, f"{tag}{r}_{i}", (x0 + i * dx + (0.5 * dx if r % 2 else 0.0) + jx, y0 + r * dy, 0.0), rot_z=math.sin(r * 3.1 + i) * 0.4, shirt=shirt, k=k))
    return out
