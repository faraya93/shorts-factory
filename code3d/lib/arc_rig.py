"""Rig of the electric-arc asset (block B5, 2026-11-11; the arc job of the second-opinion report P8): a jagged emissive electric arc built from code (own work, route code-primitive). `arc()` draws
one main path between two points as a jittered polyline with a hot white-blue core and a thicker translucent halo in the identity accent, with optional side branches (`branches`), a `spark()` for a tiny
one with a flash disc at the contact, and `Arc.flicker(t)` that re-seeds the jitter at a given rate. No fire (the fire route is unmeasured). Runs inside Blender.
Units are the toy centimetres of the scene; r is the core tube radius."""
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tape_rig as tr  # noqa: E402

CORE_HEX, HALO_HEX = "#F2FBFF", "#7FD8EA"


def _path(p0, p1, n, amp, rnd):
    a, b = Vector(p0), Vector(p1)
    axis = (b - a)
    ln = axis.length
    d = axis.normalized()
    side = d.cross(Vector((0, 1, 0)) if abs(d.y) < 0.9 else Vector((1, 0, 0))).normalized()
    up = d.cross(side).normalized()
    pts = [a]
    for i in range(1, n):
        k = i / n
        pts.append(a + axis * k + side * rnd.uniform(-amp, amp) * ln * 0.1 + up * rnd.uniform(-amp, amp) * ln * 0.1)
    pts.append(b)
    return pts


def _curve(name, pts, r, mat, parent):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth, cu.bevel_resolution = r, 2
    sp = cu.splines.new("POLY")
    sp.points.add(len(pts) - 1)
    for p, v in zip(sp.points, pts):
        p.co = (v.x, v.y, v.z, 1.0)
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    cu.materials.append(mat)
    o.parent = parent
    return o


class Arc:
    def __init__(self, p0, p1, name="arc", r=0.3, n=9, amp=1.0, branches=0, seed=4, halo_hex=HALO_HEX):
        self.root = tr.empty(f"{name}_root")
        self.core = tr.gold_emit(f"{name}_core", CORE_HEX, 9.0)
        self.halo = halo_material(f"{name}_halo", halo_hex, 2.5, 0.32)
        self.args = (Vector(p0), Vector(p1), name, r, n, amp, branches)
        self.parts = []
        self.flicker(seed)

    def flicker(self, seed: int) -> None:
        """Re-draw the jitter from `seed` (call with a new integer every few frames for the flicker)."""
        for o in self.parts:
            bpy.data.objects.remove(o, do_unlink=True)
        self.parts = []
        p0, p1, name, r, n, amp, branches = self.args
        rnd = random.Random(seed)
        main = _path(p0, p1, n, amp, rnd)
        self.parts += [_curve(f"{name}_halo", main, r * 2.6, self.halo, self.root), _curve(f"{name}_core", main, r, self.core, self.root)]
        for j in range(branches):
            i = rnd.randint(2, max(2, len(main) - 3))
            tip = main[i] + (Vector((rnd.uniform(-1, 1), rnd.uniform(-0.4, 0.4), rnd.uniform(-1, 1))).normalized() * (p1 - p0).length * rnd.uniform(0.25, 0.4))
            bp = _path(main[i], tip, 4, amp, rnd)
            self.parts += [_curve(f"{name}_bhalo{j}", bp, r * 1.8, self.halo, self.root), _curve(f"{name}_bcore{j}", bp, r * 0.55, self.core, self.root)]


def spark(loc, name="spark", r=0.2, size=1.4, seed=2):
    """A single small spark: a short arc with a flash disc at its start."""
    a = Vector(loc)
    arc = Arc(a, a + Vector((0.0, 0.0, size)), name=name, r=r, n=4, amp=1.2, branches=1, seed=seed)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 2.4, segments=16, ring_count=8, location=a)
    o = bpy.context.object
    o.name = f"{name}_flash"
    o.data.materials.append(arc.core)
    o.parent = arc.root
    return arc


def halo_material(name, hex_color, strength=2.0, alpha=0.35):
    """Emission mixed with transparency: the halo must let the white core inside it show."""
    import common as c
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    em, tp, mix, out = (nt.nodes.new(t) for t in ("ShaderNodeEmission", "ShaderNodeBsdfTransparent", "ShaderNodeMixShader", "ShaderNodeOutputMaterial"))
    em.inputs["Color"].default_value = c.linear(hex_color)
    em.inputs["Strength"].default_value = strength
    mix.inputs["Fac"].default_value = alpha
    nt.links.new(tp.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    m.surface_render_method = "BLENDED"
    return m
