"""Fingertip rig for 006 (dedos-arrugados-agua, every-element remake 2026-11-05). Runs inside Blender.

Fingertip(S, ...)       a full fingertip (tip at z=0, finger rising along +z, pad facing local +x). Real geometry that WRINKLES: `set_wrinkle(a)` (0 smooth .. 1 wrinkled) rewrites the
                        vertices with numpy: the pad side folds into transverse ridges and grooves, the whole tip loses a little volume. Skin is a subsurface wet-tissue material
                        (no skin texture, no pores, no blood on screen).
fingertip_section(...)  the same finger cut along its axis (half revolved, planar cut faces): skin shell, pulp, bone as separate solids, with a vessel tree and a nerve on the cut face.
Units: BU = 1 cm of a macro-scaled finger (R about 2.4)."""
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import real_kit as rk  # noqa: E402

R_DEFAULT, L_DEFAULT = 2.4, 14.0
FLAT = 0.84                      # cross-section: finger is a little flatter than it is wide (y/x)


def _profile_arc(R, z0=0.0, n=22):
    """(r, z) points of a hemispherical tip from the pole (0, z0) to the equator (R, z0 + R)."""
    return [(R * math.sin(math.pi / 2 * k / n), z0 + R * (1 - math.cos(math.pi / 2 * k / n))) for k in range(n + 1)]


class Fingertip:
    def __init__(self, S, mat, name="finger", R=R_DEFAULT, L=L_DEFAULT, seg=112, rings_shaft=48, loc=(0, 0, 0), wavelength=1.15, depth=0.2, nail=True):
        self.S, self.R, self.L, self.depth, self.wl = S, R, L, depth, wavelength
        prof = _profile_arc(R)
        prof += [(R, R + (L - R) * k / rings_shaft) for k in range(1, rings_shaft + 1)]
        verts, faces = [], []
        rings = []
        for r, z in prof:
            rings.append(len(verts))
            if r < 1e-9:
                verts.append((0.0, 0.0, z))
                continue
            for i in range(seg):
                a = 2 * math.pi * i / seg
                verts.append((r * math.cos(a) * (1 + 0.05 * min(1.0, z / L)), r * math.sin(a) * FLAT * (1 + 0.05 * min(1.0, z / L)), z))
        self.seg = seg
        self.rings = rings
        for k in range(len(prof) - 1):
            a0, a1 = rings[k], rings[k + 1]
            pole = prof[k][0] < 1e-9
            for i in range(seg):
                j = (i + 1) % seg
                if pole:
                    faces.append((a0, a1 + j, a1 + i))
                else:
                    faces.append((a0 + i, a0 + j, a1 + j, a1 + i))
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(verts, [], faces)
        mesh.update()
        for p in mesh.polygons:
            p.use_smooth = True
        mesh.materials.append(mat)
        self.obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(self.obj)
        self.obj.location = loc
        S.reg(self.obj)
        self.P0 = np.array([v.co[:] for v in mesh.vertices], dtype=np.float64)
        # outward direction (centre axis at z=min(z,R))
        c = self.P0.copy()
        c[:, 0] = 0.0
        c[:, 1] = 0.0
        c[:, 2] = np.minimum(self.P0[:, 2], R)
        n = self.P0 - c
        ln = np.linalg.norm(n, axis=1, keepdims=True)
        ln[ln < 1e-9] = 1.0
        self.N0 = n / ln
        x, y, z = self.P0[:, 0], self.P0[:, 1], self.P0[:, 2]
        theta = np.arctan2(y, x)
        # pad weight: 1 on the +x side (pad) and around the tip, fading to 0 on the dorsal side
        self.w = np.clip((np.cos(theta) + 0.35) / 0.9, 0.0, 1.0) ** 0.8
        # ridge phase: transverse folds that bend around the tip and wander a little (never a perfect grating)
        self.phase = (z + 0.3 * np.sin(2.3 * theta + 0.9 * z) + 0.18 * np.sin(5.0 * theta)) / wavelength * 2 * math.pi
        self.set_wrinkle(0.0)
        self.nail = None
        if nail:
            nm = rk.wet_tissue("g_mark", "#EDBBA9", sss=0.15, rough=0.22, coat=0.8, trans=0.0)
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(-R * 0.93, 0, R * 1.9), segments=40, ring_count=24)
            n_ = bpy.context.object
            n_.name = name + "_nail"
            n_.scale = (0.13 * R, 0.66 * R * FLAT, 1.15 * R)
            n_.data.materials.append(nm)
            rk.smooth(n_)
            n_.parent = self.obj
            self.nail = n_

    def set_wrinkle(self, a: float):
        a = max(0.0, min(1.0, a))
        ridge = (0.5 - 0.5 * np.cos(self.phase)) ** 1.6                       # 0 at the crest, deep grooves: the grooves are narrow, the crests round
        envelope = np.clip(self.P0[:, 2] / (0.25 * self.R), 0.0, 1.0)         # no folds right at the pole (the very tip is smooth)
        d = -self.depth * a * self.w * ridge * envelope                       # grooves go inward
        shrink = 1.0 - 0.055 * a * (0.4 + 0.6 * self.w)
        P = self.P0.copy()
        P[:, 0] *= shrink
        P[:, 1] *= shrink
        P += self.N0 * d[:, None]
        self.obj.data.vertices.foreach_set("co", P.astype(np.float32).ravel())
        self.obj.data.update()


def _half_lathe(name, loop, mat, seg=72, flat=FLAT, loc=(0, 0, 0)):
    """Half (y >= 0) solid of revolution of a CLOSED (r, z) loop with planar cut caps in the plane y = 0 (so the cut face is exactly flat and shows the layer cross-section)."""
    verts, faces = [], []
    n = len(loop)
    for s in range(seg + 1):
        a = math.pi * s / seg
        for r, z in loop:
            verts.append((r * math.cos(a), r * math.sin(a) * flat, z))
    for s in range(seg):
        for k in range(n):
            k2 = (k + 1) % n
            a, b = s * n + k, s * n + k2
            faces.append((a, b, b + n, a + n))
    faces.append(tuple(range(n))[::-1])                                           # cap at angle 0
    faces.append(tuple(seg * n + k for k in range(n)))                            # cap at angle pi
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    for p in mesh.polygons:
        p.use_smooth = False
    mesh.shade_smooth()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    mesh.materials.append(mat)
    return o


def fingertip_section(S, mats, name="sec", R=R_DEFAULT, L=L_DEFAULT, loc=(0, 0, 0), skin_t=0.16):
    """Cut-open fingertip. mats = dict(skin, pulp, bone). Returns dict(skin, pulp, bone, R, L, cut_y): the cut plane is y = loc.y; the camera looks along +y from y < 0,
    so the cut faces the camera and the vessels/nerve (put them at y just below the plane) bulge out of it."""
    arc_o = _profile_arc(R)
    arc_i = _profile_arc(R - skin_t, z0=skin_t * 0.9)
    skin = arc_o + [(R, L), (R - skin_t, L)] + arc_i[::-1]
    rb = R * 0.33
    zb = R * 0.95
    bone_arc = [(rb * math.sin(math.pi / 2 * k / 14), zb + rb * (1 - math.cos(math.pi / 2 * k / 14))) for k in range(15)]
    pulp = arc_i + [(R - skin_t, L), (rb, L)] + (bone_arc + [(rb, L)])[::-1][1:]
    pulp = arc_i + [(R - skin_t, L), (rb, L)] + bone_arc[::-1]
    bone = bone_arc + [(rb, L), (0.0, L)]
    out = {"R": R, "L": L, "cut_y": loc[1], "rb": rb, "zb": zb}
    out["skin"] = _half_lathe(name + "_skin", skin, mats["skin"], loc=loc)
    out["pulp"] = _half_lathe(name + "_pulp", pulp, mats["pulp"], loc=loc)
    out["bone"] = _half_lathe(name + "_bone", bone, mats["bone"], loc=loc)
    for k in ("skin", "pulp", "bone"):
        S.reg(out[k])
    return out
