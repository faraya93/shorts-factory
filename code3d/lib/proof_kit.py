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


def wall_section(S, loc, gel=True, w=12.0, d=6.0):
    """Block B5 (030): a magnified slice of the stomach wall as stacked layers (muscle, connective, a cell row, an optional thick translucent gel on the inner face). Returns (parts, top z)."""
    import tape_rig as tr
    x, y, z = loc
    layers = [("#7A2E3A", 1.6), ("#B8506A", 1.2), ("#E58FA3", 0.9)]
    parts, zc = [], z
    for i, (hexc, h) in enumerate(layers):
        parts.append(tr.rbox(f"wall_l{i}", (w, d, h), (x, y, zc + h / 2), tr.plain(f"wall_l{i}", hexc, rough=0.5), bevel=0.15))
        zc += h
    if gel:
        gm = S.glass("#CFE9C9", alpha=0.45, rough=0.08, name="gel")
        parts.append(tr.rbox("wall_gel", (w, d, 2.4), (x, y, zc + 1.2), gm, bevel=0.3))
        zc += 2.4
    return parts, zc
