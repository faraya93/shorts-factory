"""Street environment of production 028 (why birds can stand on power lines), block B5 proofs: poles with crossarms and insulators receding along x, three wires (the middle one at y = 0, z = 0),
translucent wire jackets with a copper core, accent current beads, and dotted current paths. Runs inside Blender. Units are the toy centimetres of bird_rig (the perched bird is about 7 long)."""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tape_rig as tr  # noqa: E402

WIRE_Y = (-6.0, 0.0, 6.0)
GROUND_Z = -70.0


class Mats:
    def __init__(self, accent_hex, error_hex):
        self.pole = tr.plain("pole_wood", "#8A6A4A", rough=0.7)
        self.arm = tr.plain("pole_arm", "#6E5238", rough=0.7)
        self.ins = tr.plain("insulator", "#D9DEE3", rough=0.3)
        self.jacket = tr.plain("wire_jacket", "#4B4F57", rough=0.4)
        self.copper = tr.plain("wire_copper", "#C9773F", rough=0.3, metallic=0.8)
        self.glass = tr.plain("wire_clear", "#B8C4D0", rough=0.1)
        bsdf = next(n for n in self.glass.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        bsdf.inputs["Alpha"].default_value = 0.28
        self.glass.surface_render_method = "BLENDED"
        self.bead = tr.gold_emit("current_bead", accent_hex, 7.0)
        self.red = tr.gold_emit("current_red", error_hex, 6.0)


def pole(m, x, name="pole", height=None):
    top = -1.5
    h = (height or 68.0)
    tr.cyl(f"{name}{x:.0f}_mast", 1.1, h, (x, 0.0, top - h / 2), m.pole, axis="Z", verts=20)
    tr.rbox(f"{name}{x:.0f}_arm", (2.0, 22.0, 1.4), (x, 0.0, top), m.arm, bevel=0.2)
    for y in WIRE_Y:
        tr.cyl(f"{name}{x:.0f}_ins{y:.0f}", 0.6, 1.5, (x, y, top + 0.9), m.ins, axis="Z", verts=14)


def wires(m, x0, x1, jacket=None, core=False):
    """The three wires between x0 and x1 (a jacket, optionally clear over a copper core so the current beads inside it can be seen)."""
    out = []
    for y in WIRE_Y:
        if core:
            tr.cyl(f"wire_core{y:.0f}", 0.28, x1 - x0, ((x0 + x1) / 2, y, 0.0), m.copper, axis="X", verts=12)
            out.append(tr.cyl(f"wire_clear{y:.0f}", 0.7, x1 - x0, ((x0 + x1) / 2, y, 0.0), m.glass, axis="X", verts=16))
        else:
            out.append(tr.cyl(f"wire_jacket{y:.0f}", 0.5, x1 - x0, ((x0 + x1) / 2, y, 0.0), jacket or m.jacket, axis="X", verts=16))
    return out


def street(m, x0=-200.0, x1=520.0, step=90.0, core=False):
    x = x0
    while x <= x1:
        pole(m, x)
        x += step
    return wires(m, x0, x1, core=core)


def beads(m, xs, y=0.0, r=0.62):
    out = []
    for i, x in enumerate(xs):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=16, ring_count=8, location=(x, y, 0.0))
        o = bpy.context.object
        o.name = f"bead_{i}"
        o.data.materials.append(m.bead)
        out.append(o)
    return out


def dotted(m, pts, n=26, r=0.28, name="dot"):
    """Small red emissive beads along the polyline pts (a dotted current path)."""
    segs = list(zip(pts[:-1], pts[1:]))
    lens = [math.dist(a, b) for a, b in segs]
    total = sum(lens)
    out = []
    for i in range(n):
        d = total * i / (n - 1)
        for (a, b), ln in zip(segs, lens):
            if d <= ln + 1e-6:
                k = d / ln if ln else 0.0
                p = tuple(a[j] + (b[j] - a[j]) * k for j in range(3))
                break
            d -= ln
        bpy.ops.mesh.primitive_uv_sphere_add(radius=r, segments=12, ring_count=6, location=p)
        o = bpy.context.object
        o.name = f"{name}_{i}"
        o.data.materials.append(m.red)
        out.append(o)
    return out
