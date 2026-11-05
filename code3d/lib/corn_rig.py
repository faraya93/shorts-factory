"""Supporting props for 011 (palomitas): the unpopped kernel, its layered cutaway and steam, plus the retint of the library popcorn asset.
The HERO of the video is the library asset 'popcorn' (assets/library/popcorn)."""
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import asset_rig as ar  # noqa: E402
import common as c  # noqa: E402

HULL, STARCH, DROP, CREAM, INK = "#D9831A", "#E8B845", "#4FB3FF", "#F7E7C2", "#1D1B2E"


def palette(S):
    return {"hull": S.hero("big", HULL, rough=0.45), "starch": S.hero("small", STARCH, rough=0.6), "drop": S.glass(DROP, alpha=0.8, rough=0.05),
            "steam": S.hero("foam", "#FFFFFF", rough=0.9, coat=0.0, alpha=0.7), "plate": S.plate_mat(), "dark": S.hero("rubber", "#5A3A10", rough=0.8, coat=0.0),
            "ink": S.hero("ink", INK, rough=0.5), "shard": S.hero("big", HULL, rough=0.5)}


def kernel(S, M, loc, r=4.0, name="kernel", **tk):
    """Whole kernel: a rounded teardrop (flattened ellipsoid + a small dark tip)."""
    root = S.empty(name, loc, **tk)
    S.ball(name + "_b", M["hull"], r, (0, 0, r * 0.18), shape=(0.80, 0.55, 0.82), parent=root, seg=32)
    S.cone(name + "_c", r * 0.10, r * 0.62, r * 1.05, (0, 0, -r * 0.62), M["hull"], parent=root, verts=32)
    S.ball(name + "_tip", M["dark"], r * 0.14, (0, 0, -r * 1.12), shape=(1, 1, 1.2), parent=root, seg=12)
    return root


def retint_popcorn(col):
    """Pieces cream, box stripes ink/cream (the stage colour must not swallow the source red)."""
    pieces = [o for o in col.objs if o.name.startswith("popcorn_")]
    mat = None
    for o in pieces:
        if mat is None:
            mat = o.data.materials[0]
            ar.retint(mat, CREAM, role="g_big", rough=0.75)
        else:
            o.data.materials.clear(); o.data.materials.append(mat)
    box = next(o for o in col.objs if o.name == "box")
    m = box.data.materials[0]
    nt = m.node_tree
    bs = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"); tex = next(n for n in nt.nodes if n.type == "TEX_IMAGE")
    ramp = nt.nodes.new("ShaderNodeValToRGB"); bw = nt.nodes.new("ShaderNodeRGBToBW")
    ramp.color_ramp.elements[0].position = 0.25; ramp.color_ramp.elements[0].color = c.linear(INK)
    ramp.color_ramp.elements[1].position = 0.45; ramp.color_ramp.elements[1].color = c.linear("#FFF3E0")
    nt.links.new(tex.outputs["Color"], bw.inputs["Color"]); nt.links.new(bw.outputs["Val"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], bs.inputs["Base Color"])
    m.name = "g_pin"
    return pieces, box


def cutaway(S, M, x=0.0, z=9.0, r=7.5, t_on=0.1):
    """Layered section of the kernel facing the camera: hull ring, starch, water drop. Returns (hull, starch, drop)."""
    S.box("plate", (30, 1.0, 30), (x, 2.2, z + 2), M["plate"], bevel=0.5)
    hull = S.cyl("c_hull", r, 1.2, (x, 0.0, z), M["hull"], axis="Y", verts=64, pop=(t_on, 0.4))
    S.size(hull, [(0, (0.78, 1, 1.0))])
    st = S.cyl("c_starch", r * 0.86, 1.2, (x, -0.5, z), M["starch"], axis="Y", verts=64, pop=(t_on + 0.1, 0.4))
    S.size(st, [(0, (0.78, 1, 1.0))])
    dr = S.ball("c_drop", M["drop"], 1.5, (x, -1.2, z - 1.0), pop=(t_on + 0.3, 0.4))
    return hull, st, dr
