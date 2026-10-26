"""Bold cartoon primitives (run inside Blender): the shared construction vocabulary for drawn scenes.
Everything is a simple convex-ish shape so the toon outline inks cleanly: rounded bars, rings, cone needles, ellipsoids,
and extruded 2D outlines (for jagged or irregular silhouettes). Callers pass toon materials (toon.make_material)."""

import math

import bmesh
import bpy
from mathutils import Vector


def _finish(obj, material, smooth=True):
    if smooth:
        for poly in obj.data.polygons:
            poly.use_smooth = True
    obj.data.materials.append(material)
    return obj


def ellipsoid(name, rx, ry, rz, material, loc=(0, 0, 0), segments=64, rings=32):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=segments, ring_count=rings, location=loc)
    obj = bpy.context.object
    obj.name, obj.scale = name, (rx, ry, rz)
    bpy.ops.object.transform_apply(scale=True)
    return _finish(obj, material)


def rounded_bar(name, hx, hy, hz, material, loc=(0, 0, 0), rot=(0, 0, 0), bevel_frac=0.95):
    """A stadium-shaped bar: a box with a near-full bevel (rounded ends, clean convex outline). Half sizes."""
    bpy.ops.mesh.primitive_cube_add(size=2, location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name, obj.scale = name, (hx, hy, hz)
    bpy.ops.object.transform_apply(scale=True)
    mod = obj.modifiers.new("round", "BEVEL")
    mod.width, mod.segments, mod.limit_method = min(hx, hy, hz) * bevel_frac, 10, "NONE"
    return _finish(obj, material)


def ring(name, major, minor, material, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=48, minor_segments=18,
                                     location=loc, rotation=rot)
    obj = bpy.context.object
    obj.name = name
    return _finish(obj, material)


def cone_needle(name, p0: Vector, p1: Vector, r_tail, r_tip, material):
    """A chunky straight needle from tail p0 to tip p1 (a tapered cone, rounded tail)."""
    d = p1 - p0
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=r_tail, radius2=r_tip, depth=d.length, location=(p0 + p1) / 2)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    return _finish(obj, material)


def extruded_polygon(name, pts2d, depth, material, loc=(0, 0, 0), bevel=0.12):
    """A flat shape (any outline, concave allowed) extruded `depth` along +z, round-bevelled. Bottom at z = 0."""
    bm = bmesh.new()
    verts = [bm.verts.new((x, y, 0.0)) for x, y in pts2d]
    face = bm.faces.new(verts)
    ext = bmesh.ops.extrude_face_region(bm, geom=[face])
    for v in [g for g in ext["geom"] if isinstance(g, bmesh.types.BMVert)]:
        v.co.z += depth
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = loc
    bpy.context.scene.collection.objects.link(obj)
    mod = obj.modifiers.new("round", "BEVEL")
    mod.width, mod.segments, mod.limit_method, mod.angle_limit = bevel, 5, "ANGLE", math.radians(35)
    return _finish(obj, material)


def bar_between(name, p0: Vector, p1: Vector, radius: float, material):
    """A chunky rounded bar from p0 to p1 (cartoon limbs, tweezer arms, pincers)."""
    d = p1 - p0
    return rounded_bar(name, radius, d.length / 2, radius, material, loc=(p0 + p1) / 2,
                       rot=d.to_track_quat("Y", "Z").to_euler())
