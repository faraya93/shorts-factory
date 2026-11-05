"""Props for 008 (hielo-que-pasaria-si-se-hundiera): a glass of water and ice cubes, as alpha-blended translucent solids (no refraction).
The hero (ice cube + glass) is the code-primitive library entry 'ice-cube'."""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402

ICE, WATER = "#CFEFFF", "#4FB3E8"


def palette(S):
    return {"ice": S.hero("big", ICE, rough=0.12, coat=0.5, alpha=0.7), "water": S.glass(WATER, alpha=0.42, rough=0.05),
            "lake": S.glass("#1565C0", alpha=0.32, rough=0.05, name="lake_w"), "ice_solid": S.hero("big", "#E8F8FF", rough=0.2, coat=0.4, alpha=0.93), "glass": S.glass("#EAF7FF", alpha=0.16, rough=0.02, name="glass_w"), "rim": S.hero("mark", "#FFFFFF", rough=0.2), "sun": S.hero("accent", "#FFD66B", rough=0.5),
            "line": S.hero("ink", "#1D1B2E", rough=0.5), "plate": S.plate_mat()}


def glass(S, M, r=5.0, h=12.0, level=9.0, x=0.0, pop=None):
    g = S.cyl("glass", r, h, (x, 0, h / 2), M["glass"], axis="Z", verts=48, bevel=0.15, pop=pop)
    w = S.cyl("water", r - 0.35, level, (x, 0, level / 2 + 0.2), M["water"], axis="Z", verts=48, pop=pop)
    rim = S.torus("rim", r, 0.14, (x, 0, h), M["rim"], pop=pop)
    return g, w, rim


def cube(S, M, name, loc, size=2.6, rot=(0, 0, 0), **tk):
    return S.box(name, (size, size, size), loc, M["ice"], bevel=0.45, rot=rot, **tk)


def bob(t, i, amp=0.18):
    return amp * math.sin(t * 2.0 + i * 1.7)
