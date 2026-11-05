"""Supporting props for 006 (dedos-arrugados-agua): fingertip cutaway, wheels (smooth / grooved), grip pads and wet marbles. Geometric props drawn with the set-piece kit;
the HERO of the video is the library hand (assets/library/human-hand)."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402

SKIN, BONE, VESSEL = "#C98963", "#7A6A78", "#D9534F"


def palette(S):
    return {"skin": S.hero("big", SKIN, rough=0.55), "bone": S.hero("small", BONE, rough=0.5), "vessel": S.hero("mark", VESSEL, rough=0.4),
            "tyre": S.hero("housing", "#2D2A2B", rough=0.7, coat=0.0), "groove": S.hero("rubber", "#0F0E14", rough=0.8, coat=0.0),
            "marble": S.hero("mark", "#7FD0E8", rough=0.08, coat=0.6), "water": S.glass("#7FD0E8", alpha=0.25), "plate": S.plate_mat(), "board": S.board_mat(),
            "pad": S.hero("big", "#C98963", rough=0.6)}


def wheel(S, M, name, x, z, r=4.0, w=3.0, grooved=False, **tk):
    """Wheel with its axis along y. Returns the root empty (spin it with S.spin on rotation y)."""
    root = S.empty(name, (x, 0, z), **tk)
    S.cyl(name + "_t", r, w, (0, 0, 0), M["tyre"], axis="Y", parent=root, verts=64, bevel=0.35)
    if grooved:
        for gy in (-0.8, 0.0, 0.8):
            S.cyl(f"{name}_g{gy}", r + 0.05, 0.28, (0, gy, 0), M["groove"], axis="Y", parent=root, verts=64)
    return root


def marble(S, M, name, loc, r=0.9, **tk):
    return S.ball(name, M["marble"], r, loc, **tk)
