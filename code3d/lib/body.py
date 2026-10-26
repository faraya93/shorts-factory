"""Stylized body parts for code3d scenes (runs inside Blender).

Forearm: a tapered tube of skin over a red tissue core, with a lens-shaped lengthwise SLIT whose opening angle is
animated (the mesh is rebuilt each frame). Skin outside, tissue inside, a peach rim along the edge (Solidify with
material offsets). Axes: the arm runs along y, the slit is on top (+z).
"""

import math

import bmesh
import bpy


class Forearm:
    NY, NA = 70, 64

    def __init__(self, stage, length=7.0, r_wrist=0.75, r_elbow=1.0, slit_center=0.3, slit_half_len=2.0):
        self.length, self.r_wrist, self.r_elbow = length, r_wrist, r_elbow
        self.yc, self.h = slit_center, slit_half_len
        self.y0 = -length / 2
        rim = stage.thread_mat.copy()
        rim.name = "rim"
        rim.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = stage.skin.node_tree.nodes[
            next(n.name for n in stage.skin.node_tree.nodes if n.type == "GROUP")].inputs["Diffuse Color"].default_value
        rim.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.5
        self.mesh = bpy.data.meshes.new("forearm")
        self.obj = bpy.data.objects.new("forearm", self.mesh)
        bpy.context.scene.collection.objects.link(self.obj)
        for m in (stage.skin, stage.tissue, rim):
            self.mesh.materials.append(m)
        solid = self.obj.modifiers.new("solidify", "SOLIDIFY")
        solid.thickness, solid.offset = 0.07, -1.0
        solid.material_offset, solid.material_offset_rim = 1, 2
        # tissue core just inside the shell, plus rounded ends (wrist palm, elbow) in skin
        self.core = self._tube("core", stage.tissue, shrink=0.075)
        self._cap(stage.skin, self.y0, self.r_wrist, (1.0, 0.7, 1.0))             # rounded wrist end
        self._cap(stage.skin, -self.y0, self.r_elbow, (1.0, 0.7, 1.0))            # rounded elbow end

    def radius(self, y):
        return self.r_wrist + (self.r_elbow - self.r_wrist) * (y - self.y0) / self.length

    def _tube(self, name, material, shrink):
        bm = bmesh.new()
        rings = []
        for i in range(self.NY + 1):
            y = self.y0 + self.length * i / self.NY
            r = self.radius(y) - shrink
            rings.append([bm.verts.new((r * math.sin(2 * math.pi * j / self.NA), y, r * math.cos(2 * math.pi * j / self.NA)))
                          for j in range(self.NA)])
        for i in range(self.NY):
            for j in range(self.NA):
                bm.faces.new((rings[i][j], rings[i][(j + 1) % self.NA], rings[i + 1][(j + 1) % self.NA], rings[i + 1][j]))
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        mesh = bpy.data.meshes.new(name)
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        for p in mesh.polygons:
            p.use_smooth = True
        mesh.materials.append(material)
        return obj

    def _cap(self, material, y, radius, scale):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, y, 0), segments=48, ring_count=24)
        obj = bpy.context.object
        obj.scale = scale
        bpy.ops.object.shade_smooth()
        obj.data.materials.append(material)

    def lens(self, y):
        k = 1 - ((y - self.yc) / self.h) ** 2
        return max(0.0, k) ** 0.6

    def rebuild(self, slit_deg: float) -> None:
        """Rebuild the shell with the slit opened to `slit_deg` degrees at its widest point."""
        bm = bmesh.new()
        closed = slit_deg < 0.4
        rings = []
        for i in range(self.NY + 1):
            y = self.y0 + self.length * i / self.NY
            r = self.radius(y)
            half = math.radians(slit_deg) / 2 * self.lens(y)
            if closed:
                angles = [2 * math.pi * j / self.NA for j in range(self.NA)]
            else:
                angles = [half + (2 * math.pi - 2 * half) * j / self.NA for j in range(self.NA + 1)]
            rings.append([bm.verts.new((r * math.sin(a), y, r * math.cos(a))) for a in angles])
        n = len(rings[0])
        for i in range(self.NY):
            for j in range(n if closed else n - 1):
                bm.faces.new((rings[i][j], rings[i][(j + 1) % n], rings[i + 1][(j + 1) % n], rings[i + 1][j]))
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)   # weld the seam wherever the slit has zero width
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(self.mesh)
        bm.free()
        for p in self.mesh.polygons:
            p.use_smooth = True
