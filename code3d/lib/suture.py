"""Reusable code3d objects for the suturing scenes (runs inside Blender): skin halves, wound floor, curved needle, thread.

Axes: x across the cut, y along the cut, z up (skin surface at z = 0). The needle turns about a circle centre in the
x-z plane, exactly as a real curved needle is driven through tissue.
"""

import math

import bmesh
import bpy
from mathutils import Vector

SKIN_LAYER = 0.12      # thin skin layer on top of the tissue block: shows as a peach rim around the cut
SLAB_DEPTH = 1.0


def box(name, x0, x1, y0, y1, z0, z1, material, bevel=0.03, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=2)
    obj = bpy.context.object
    obj.name = name
    obj.scale = ((x1 - x0) / 2, (y1 - y0) / 2, (z1 - z0) / 2)
    obj.location = ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        mod = obj.modifiers.new("bevel", "BEVEL")
        mod.width, mod.segments = bevel, 3
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def skin_half(side: int, gap_half: float, width: float, length: float, skin_mat, tissue_mat):
    """One side of the cut (side = -1 left, +1 right): an empty carrying a skin layer over a tissue block."""
    root = bpy.data.objects.new(f"half_{'L' if side < 0 else 'R'}", None)
    bpy.context.scene.collection.objects.link(root)
    x0, x1 = sorted((side * gap_half, side * (gap_half + width)))
    y0, y1 = -length / 2, length / 2
    box("skin", x0, x1, y0, y1, -SKIN_LAYER, 0.0, skin_mat, bevel=0.03, parent=root)
    box("tissue", x0, x1, y0, y1, -SLAB_DEPTH, -SKIN_LAYER, tissue_mat, bevel=0.02, parent=root)
    return root


def wound_floor(gap_half: float, length: float, floor_z: float, tissue_mat):
    return box("wound_floor", -gap_half, gap_half, -length / 2, length / 2, -SLAB_DEPTH, floor_z, tissue_mat, bevel=0)


def curved_needle(radius: float, center_z: float, tip_deg: float, arc_deg: float, r_tail: float, r_tip: float, material):
    """A tapered tube along an arc of the circle (centre (0, 0, center_z), x-z plane). Its origin is the circle
    centre, so rotating the object about y turns the needle through the skin."""
    steps, sides = 64, 14
    bm = bmesh.new()
    rings = []
    for i in range(steps + 1):
        s = i / steps                                  # 0 = tail ... 1 = tip
        a = math.radians(tip_deg - arc_deg * (1 - s))
        radial = Vector((math.cos(a), 0, math.sin(a)))
        center = radial * radius
        r = r_tip + (r_tail - r_tip) * (1 - s) ** 1.4
        ring = []
        for j in range(sides):
            phi = 2 * math.pi * j / sides
            ring.append(bm.verts.new(center + r * (math.cos(phi) * radial + math.sin(phi) * Vector((0, 1, 0)))))
        rings.append(ring)
    for i in range(steps):
        for j in range(sides):
            bm.faces.new((rings[i][j], rings[i][(j + 1) % sides], rings[i + 1][(j + 1) % sides], rings[i + 1][j]))
    bm.faces.new(rings[0][::-1])                       # flat tail end
    bm.faces.new(rings[-1])                            # sharp tip end
    mesh = bpy.data.meshes.new("needle")
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("needle", mesh)
    obj.location = (0, 0, center_z)
    bpy.context.scene.collection.objects.link(obj)
    for poly in mesh.polygons:
        poly.use_smooth = True
    mesh.materials.append(material)
    return obj


def arc_points(cx, cz, radius, a0_deg, a1_deg, step_deg=3.0, y=0.0):
    n = max(1, int(abs(a1_deg - a0_deg) / step_deg))
    return [Vector((cx + radius * math.cos(math.radians(a0_deg + (a1_deg - a0_deg) * i / n)), y,
                    cz + radius * math.sin(math.radians(a0_deg + (a1_deg - a0_deg) * i / n)))) for i in range(n + 1)]


def resample(poly: list, n: int) -> list:
    """Evenly spaced n points along a polyline (so the thread keeps a constant point count while it changes)."""
    if len(poly) == 1:
        return poly * n
    lengths = [0.0]
    for a, b in zip(poly, poly[1:]):
        lengths.append(lengths[-1] + (b - a).length)
    total = lengths[-1] or 1e-9
    out, k = [], 0
    for i in range(n):
        d = total * i / (n - 1)
        while k < len(poly) - 2 and lengths[k + 1] < d:
            k += 1
        seg = (lengths[k + 1] - lengths[k]) or 1e-9
        out.append(poly[k].lerp(poly[k + 1], min(1.0, max(0.0, (d - lengths[k]) / seg))))
    return out


class Thread:
    """A thin tube whose polyline is rewritten every frame (frame handler), at a constant point count."""

    def __init__(self, material, points: int = 120, thickness: float = 0.02):
        self.n = points
        data = bpy.data.curves.new("thread", "CURVE")
        data.dimensions = "3D"
        data.bevel_depth = thickness
        data.bevel_resolution = 3
        data.use_fill_caps = True
        spline = data.splines.new("POLY")
        spline.points.add(points - 1)
        self.spline = spline
        self.obj = bpy.data.objects.new("thread", data)
        data.materials.append(material)
        bpy.context.scene.collection.objects.link(self.obj)

    def set(self, polyline: list) -> None:
        for point, v in zip(self.spline.points, resample(polyline, self.n)):
            point.co = (v.x, v.y, v.z, 1.0)


def knot_polyline(form: float, tight: float, center: Vector, reach: float, base_z: float, scale_loose: float = 0.30,
                  scale_tight: float = 0.085, m: int = 160) -> list:
    """A thread along x through `center` that ties an overhand (trefoil) knot.
    form 0 -> straight thread, 1 -> knot at the loose scale; tight 0 -> loose, 1 -> small tight knot.
    The strands are identical in both shapes; only the middle section is flattened onto the thread line (form 0)
    or traces the trefoil (form 1), so the blend never kinks."""
    scale = scale_loose + (scale_tight - scale_loose) * tight
    x_end = 2.16 * scale                                # the trefoil's end points, shifted so they sit on y = 0
    out = []
    for i in range(m):
        u = i / (m - 1)
        if u < 0.25:                                    # left strand into the knot
            p = Vector((-reach, 0.0, 0.0)).lerp(Vector((-x_end, 0.0, 0.0)), u / 0.25)
        elif u > 0.75:                                  # right strand out of the knot
            p = Vector((x_end, 0.0, 0.0)).lerp(Vector((reach, 0.0, 0.0)), (u - 0.75) / 0.25)
        else:
            w = (u - 0.25) / 0.5
            flat = Vector((-x_end + 2 * x_end * w, 0.0, 0.0))
            ang = (2 * math.pi - 0.5) - w * (2 * math.pi - 1.0)
            # the trefoil's ends sit at z = +/-0.9975 (before the 0.7 factor): remove that ramp so both ends land on the
            # skin, and add a small arch so the whole knot stays above it
            z = 0.7 * (-math.sin(3 * ang) - 0.9975 * (1 - 2 * w)) + 0.9 * math.sin(math.pi * w)
            knot = Vector((math.sin(ang) + 2 * math.sin(2 * ang), math.cos(ang) - 2 * math.cos(2 * ang) + 0.2, z)) * scale
            p = flat.lerp(knot, form)
        out.append(Vector((center.x + p.x, center.y + p.y, base_z + p.z)))
    return out
