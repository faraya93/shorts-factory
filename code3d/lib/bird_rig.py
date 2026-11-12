"""Rig of the bird asset (block B5, 2026-11-11; serves production 028): a stylised generic bird (pigeon/goose silhouette, no species detail) built from primitives (own work, route
code-primitive): plump body, neck, head with a beak and an eye, fan tail, two legs with feet, and two jointed wings. States: perched (wings folded along the body, feet on y = 0, z = 0) and
flying (wings spread, `Bird.wings(k)` 0 folded .. 1 fully spread, with a flap offset). The bird faces +x; the wings spread along +-y. Runs inside Blender.
Scene units are centimetres of a toy scale (the perched body is about 7 long); `scale` multiplies everything (a bigger bird is the same asset scaled)."""
import math
import sys
from pathlib import Path

import bmesh
import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tape_rig as tr  # noqa: E402


def _blob(name, radii, loc, mat, parent, rot=(0, 0, 0), sub=3):
    bm = bmesh.new()
    bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=1.0)
    for v in bm.verts:
        v.co.x *= radii[0]
        v.co.y *= radii[1]
        v.co.z *= radii[2]
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(o)
    me.materials.append(mat)
    o.location, o.rotation_euler, o.parent = loc, rot, parent
    return o


class Mats:
    def __init__(self, body="#8E98A6", dark="#5B6573", wing="#6F7A89", belly="#C9CFD8", beak="#E8A33C", eye="#17171C", leg="#D4766A"):
        self.body, self.dark, self.wing, self.belly = (tr.plain(f"bird_{n}", h, rough=0.55) for n, h in (("body", body), ("dark", dark), ("wing", wing), ("belly", belly)))
        self.beak, self.eye, self.leg = tr.plain("bird_beak", beak, rough=0.4), tr.plain("bird_eye", eye, rough=0.2), tr.plain("bird_leg", leg, rough=0.5)


class Bird:
    def __init__(self, m=None, name="bird", loc=(0.0, 0.0, 0.0), scale=1.0, rot_z=0.0):
        m = m or Mats()
        self.root = tr.empty(f"{name}_root", loc)
        self.root.rotation_euler = (0.0, 0.0, rot_z)
        self.root.scale = (scale,) * 3
        r = self.root
        z0 = 3.2                                                                    # body centre height above the feet
        _blob(f"{name}_body", (3.6, 2.3, 2.3), (0.0, 0.0, z0), m.body, r)
        _blob(f"{name}_belly", (3.0, 1.9, 1.5), (0.35, 0.0, z0 - 0.7), m.belly, r)
        _blob(f"{name}_neck", (1.5, 1.3, 1.9), (3.0, 0.0, z0 + 1.3), m.dark, r, rot=(0, math.radians(-20), 0))
        _blob(f"{name}_head", (1.35, 1.2, 1.2), (3.9, 0.0, z0 + 2.8), m.dark, r)
        tr.rbox(f"{name}_beak", (1.1, 0.5, 0.45), (5.35, 0.0, z0 + 2.65), m.beak, bevel=0.15, parent=r)
        for s in (-1, 1):
            _blob(f"{name}_eye{s}", (0.28, 0.28, 0.28), (4.25, s * 0.95, z0 + 3.05), m.eye, r, sub=2)
            tr.cyl(f"{name}_leg{s}", 0.22, z0 - 0.8, (0.2, s * 0.9, (z0 - 0.8) / 2), m.leg, axis="Z", parent=r, verts=12)
            tr.rbox(f"{name}_foot{s}", (1.3, 0.8, 0.22), (0.7, s * 0.9, 0.12), m.leg, bevel=0.08, parent=r)
        for i, a in enumerate((-24, -12, 0, 12, 24)):                              # the fan tail
            tr.rbox(f"{name}_tail{i}", (3.0, 0.65, 0.22), (-5.0, 0.0, z0 - 0.2), m.wing, bevel=0.08, parent=r, rot=(0, math.radians(-8), math.radians(a)))
        self.pivots = []
        for s in (1, -1):
            piv = tr.empty(f"{name}_wing{s}", (0.4, s * 1.9, z0 + 0.9), parent=r)
            _blob(f"{name}_wingarm{s}", (1.6, 2.6, 0.38), (0.0, s * 2.4, 0.0), m.wing, piv)
            for i in range(5):                                                      # primaries: boxes along the span, longer toward the tip
                ln = 2.0 + 0.5 * i
                tr.rbox(f"{name}_prim{s}{i}", (1.1, ln, 0.18), (-0.7 - 0.55 * i * 0.6, s * (4.0 + ln / 2 + 0.3 * i), -0.05), m.wing, bevel=0.06, parent=piv)
            self.pivots.append((piv, s))
        self.wings(0.0)

    def wings(self, k: float, flap: float = 0.0) -> None:
        """k = 0 folded along the body .. 1 spread; flap raises/lowers the spread wings (radians)."""
        for piv, s in self.pivots:
            piv.rotation_euler = (s * (flap if k > 0.5 else 0.0), 0.0, s * math.radians(90.0) * (1.0 - k))
            piv.scale = (1.0, 1.0 - 0.45 * (1.0 - k), 1.0)
