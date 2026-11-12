"""Rig of the earth-globe asset (block B5, 2026-11-11; serves production 027): a stylised planet Earth built from code (own work, route code-primitive): an icosphere whose vertex colours put
blue oceans, green-and-tan continents and white polar caps on it (continents from layered noise, so the outline is irregular), a thin translucent atmosphere shell, and an optional band stack
(`Bands`) that wraps the globe as the unit's rings of people. Runs inside Blender. Scene units are centimetres of a toy scale (the globe is 20 across at radius 10 unless told otherwise)."""
import math
import sys
from pathlib import Path

import bmesh
import bpy
import mathutils
from mathutils import noise

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tape_rig as tr  # noqa: E402

OCEAN, LAND, DRY, ICE = (0.10, 0.34, 0.66), (0.28, 0.62, 0.30), (0.78, 0.68, 0.42), (0.95, 0.97, 1.0)


def _land(p) -> float:
    """> 0 on land: two noise octaves over the unit sphere, shifted so about a third of the planet is land."""
    return noise.noise((p.x * 1.5 + 3.1, p.y * 1.5 - 1.7, p.z * 1.5 + 0.4)) * 0.8 + noise.noise((p.x * 3.4, p.y * 3.4 + 5.0, p.z * 3.4 - 2.0)) * 0.35 - 0.08


class Globe:
    """The planet: root empty at `loc`, `spin` rotates it about its axis (z)."""

    def __init__(self, name="globe", radius=10.0, loc=(0.0, 0.0, 0.0), atmosphere=True):
        self.root = tr.empty(f"{name}_root", loc)
        self.spin_empty = tr.empty(f"{name}_spin", (0, 0, 0), parent=self.root)
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=5, radius=radius)
        layer = bm.loops.layers.color.new("Col")
        for f in bm.faces:
            ctr = f.calc_center_median().normalized()
            h = _land(ctr)
            if abs(ctr.z) > 0.86 + 0.04 * noise.noise((ctr.x * 4.0, ctr.y * 4.0, 1.0)):
                col = ICE
            elif h > 0.0:
                col = DRY if h > 0.34 and abs(ctr.z) < 0.55 else LAND
            else:
                col = OCEAN
            for lp in f.loops:
                lp[layer] = (*col, 1.0)
        me = bpy.data.meshes.new(f"{name}_mesh")
        bm.to_mesh(me)
        bm.free()
        for p in me.polygons:
            p.use_smooth = False
        self.obj = bpy.data.objects.new(f"{name}_body", me)
        bpy.context.scene.collection.objects.link(self.obj)
        self.obj.parent = self.spin_empty
        mat = bpy.data.materials.new(f"{name}_mat")
        mat.use_nodes = True
        nt = mat.node_tree
        bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        attr = nt.nodes.new("ShaderNodeVertexColor")
        attr.layer_name = "Col"
        nt.links.new(attr.outputs["Color"], bsdf.inputs["Base Color"])
        bsdf.inputs["Roughness"].default_value = 0.55
        me.materials.append(mat)
        if atmosphere:
            amat = tr.plain(f"{name}_air", "#9CCBFF", rough=0.2)
            bsdf2 = next(n for n in amat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
            bsdf2.inputs["Alpha"].default_value = 0.16
            amat.surface_render_method = "BLENDED"
            bpy.ops.mesh.primitive_uv_sphere_add(radius=radius * 1.06, segments=48, ring_count=24, location=(0, 0, 0))
            a = bpy.context.object
            a.name = f"{name}_air"
            for p in a.data.polygons:
                p.use_smooth = True
            a.data.materials.append(amat)
            a.parent = self.root

    def spin(self, angle: float) -> None:
        self.spin_empty.rotation_euler = (0.0, 0.0, angle)


class Bands:
    """A stack of thin rings (tori) around the globe: band 0 is the accent one, the rest grey, each a little further out."""

    def __init__(self, globe: "Globe", accent_mat, grey_mat, n=13, radius=10.0, gap=0.9, thick=0.45):
        self.rings = []
        for i in range(n):
            r = radius * 1.12 + gap * i
            bpy.ops.mesh.primitive_torus_add(major_radius=r, minor_radius=thick, major_segments=96, minor_segments=8, location=(0, 0, 0), rotation=(math.radians(72), 0, 0))
            o = bpy.context.object
            o.name = f"band_{i}"
            o.data.materials.append(accent_mat if i == 0 else grey_mat)
            o.parent = globe.root
            self.rings.append(o)
