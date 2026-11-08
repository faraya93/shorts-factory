"""Rebuild the bristles of the toothbrush-in-cup asset as dense tufts of real tubes (hair particles bake badly through the source's Array modifier and do not survive the x100 rig scale).
    .venv/bin/python tools/blender_run.py -- -b assets/library/toothbrush-in-cup/toothbrush-in-cup.blend --python assets/library/toothbrush-in-cup/build.py
Head frame from PCA of the top of each handle; the tufts stand on the face the source's hairs pointed to."""
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy
import mathutils as M
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "factory"))
import asset_library as al  # noqa: E402

HEAD_LEN = 0.034
ROWS, COLS = 4, 10
TUBE_R, BRISTLE_LEN = 0.00085, 0.011
SIDES = 8
PACK = [(0.0, 0.0)]                                                            # one chunky column per tuft (doctrine: simplified heroes); thin packed tubes kept tripping coplanar QA
BRISTLE_HEX = (0.86, 0.87, 0.88, 1)


def bristle_material():
    m = bpy.data.materials.get("bristle") or bpy.data.materials.new("bristle")
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = BRISTLE_HEX
    b.inputs["Roughness"].default_value = 0.42
    return m


def strip_hair(ob):
    """Drop every face of the slot the hair bake added (the last slot) and return the old hair's centroid."""
    me, mi = ob.data, len(ob.data.materials) - 1
    bm = bmesh.new()
    bm.from_mesh(me)
    faces = [f for f in bm.faces if f.material_index == mi]
    pts = [v.co.copy() for f in faces for v in f.verts]
    bmesh.ops.delete(bm, geom=faces, context="FACES")
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context="VERTS")
    bm.to_mesh(me)
    bm.free()
    me.materials.pop(index=mi)
    return sum(pts, M.Vector()) / len(pts)


def dedupe(ob):
    """The source handle stacks copies of its own surface (mesh QA: 34k coplanar pairs in 6.5k faces): weld and keep one face per vertex set."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    before = len(bm.faces)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=3.5e-4)
    names = [m.name if m else "" for m in ob.data.materials]
    decals = [i for i, n in enumerate(names) if n in ("text", "Material.005")]     # printed label and stripe sit coplanar on the handle; also removes any brand print
    bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in decals], context="FACES")
    seen, dup = set(), []
    for f in bm.faces:
        key = frozenset(v.index for v in f.verts)
        if key in seen:
            dup.append(f)
        seen.add(key)
    bmesh.ops.delete(bm, geom=dup, context="FACES")
    bm.to_mesh(ob.data)
    bm.free()
    ob.data.update()
    print(f"dedupe {ob.name}: {before} -> {len(ob.data.polygons)} faces")


def head_frame(ob, hair_c):
    co = np.array([v.co[:] for v in ob.data.vertices])
    axis = co[co[:, 2] > co[:, 2].min() + 0.05]
    u, s, vh = np.linalg.svd(axis - axis.mean(0), full_matrices=False)
    long_ = M.Vector(vh[0])
    if long_.z < 0:
        long_ = -long_
    end = max((M.Vector(p) for p in co), key=lambda p: p.dot(long_))
    d = np.array(long_[:])
    t = (co @ d)
    head = co[t > t.max() - HEAD_LEN]
    c = M.Vector(head.mean(0))
    u, s, vh = np.linalg.svd(head - head.mean(0), full_matrices=False)
    width = M.Vector(vh[1]).normalized()
    thick = long_.cross(width).normalized()
    if (hair_c - c).dot(thick) < 0:
        thick = -thick
    half_w = float(np.abs((head - head.mean(0)) @ np.array(width[:])).max())
    half_t = float(np.abs((head - head.mean(0)) @ np.array(thick[:])).max())
    return c, end, long_, width, thick, half_w, half_t


def tube(vs, fs, a, b, r, roll):
    d = (b - a).normalized()
    u = d.orthogonal().normalized()
    v = d.cross(u)
    u, v = u * math.cos(roll) + v * math.sin(roll), v * math.cos(roll) - u * math.sin(roll)     # no two neighbouring tubes share a face plane (QA: coplanar pairs)
    n = len(vs)
    for p, rr in ((a, r), (b, r * 0.82)):
        for k in range(SIDES):
            t = k * 2 * math.pi / SIDES
            vs.append(p + (u * math.cos(t) + v * math.sin(t)) * rr)
    for k in range(SIDES):
        fs.append((n + k, n + (k + 1) % SIDES, n + SIDES + (k + 1) % SIDES, n + SIDES + k))
    fs.append(tuple(n + SIDES + k for k in range(SIDES)))


def add_bristles(ob, rng):
    hair_c = strip_hair(ob)
    dedupe(ob)
    c, end, long_, width, thick, half_w, half_t = head_frame(ob, hair_c)
    me = ob.data
    mat = bristle_material()
    me.materials.append(mat)
    mi = len(me.materials) - 1
    span = HEAD_LEN * 0.82
    vs, fs = [], []
    base = end - long_ * (HEAD_LEN * 0.5 + 0.001)
    for i in range(COLS):
        along = (i + 0.5) / COLS - 0.5
        for j in range(ROWS):
            across = (j + 0.5) / ROWS - 0.5
            root = base + long_ * (along * span) + width * (across * half_w * 1.6) + thick * (half_t * 0.75)
            for q, a in PACK:                                                  # hex-packed, splaying outward: tubes of a tuft never touch (QA: intersecting coplanar pairs)
                offs = long_ * (q * math.cos(a)) + width * (q * math.sin(a))
                tip = thick * BRISTLE_LEN * rng.uniform(0.96, 1.04) + offs * 0.1
                tube(vs, fs, root + offs, root + offs + tip, TUBE_R, rng.uniform(0, math.pi / 2))
    bm = bmesh.new()
    bm.from_mesh(me)
    nv = [bm.verts.new(v) for v in vs]
    bm.verts.ensure_lookup_table()
    for f in fs:
        face = bm.faces.new([nv[i] for i in f])
        face.material_index = mi
        face.smooth = True
    bm.to_mesh(me)
    bm.free()
    me.update()


def replicate(col):
    """brush_b welds clean (mesh QA 0 pairs; a and c keep residual stacked layers): the other two are copies of it, turned about the cup's axis."""
    cup = col.objects["cup"]
    cx = sum((cup.matrix_world @ M.Vector(c)).x for c in cup.bound_box) / 8
    cy = sum((cup.matrix_world @ M.Vector(c)).y for c in cup.bound_box) / 8
    src = col.objects["brush_b"]
    for name, deg in (("brush_a", 118.0), ("brush_c", -125.0)):
        me = src.data.copy()
        me.name = name
        me.transform(M.Matrix.Translation((cx, cy, 0)) @ M.Matrix.Rotation(math.radians(deg), 4, "Z") @ M.Matrix.Translation((-cx, -cy, 0)))
        me.update()
        col.objects[name].data = me


def main():
    rng = random.Random(12)
    col = bpy.data.collections["asset"]
    for ob in col.objects:
        if ob.name.startswith("brush_"):
            add_bristles(ob, rng)
    replicate(col)
    print(al.save_collection("toothbrush-in-cup", "asset"))


main()
