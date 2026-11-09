"""Rig of production 015 (why flies rub their legs): the housefly asset with its two front-leg bones, a revolved plate and the library props (trash bag, banana, bread slice). Runs inside Blender. Scene units are centimetres; the fly is enlarged (the asset is 9.6 cm at K=100, a real fly is under 1 cm)."""
import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Matrix, Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_library as al  # noqa: E402
import asset_rig as ar  # noqa: E402
import common as c  # noqa: E402

K = ar.K
RUB_PITCH = -58.0                                                               # raises both front legs in front of the head (measured on the asset, 2026-11-09)
RUB_YAW = {"legA": -14.0, "legB": 32.0}                                         # tips meet near the midline
RUB_SWING = 9.0


class Fly:
    def __init__(self, root, arm, body):
        self.root, self.arm, self.body = root, arm, body


def fly(S, loc=(0.0, 0.0, 0.0), yaw=0.0, size=1.0, pop=None):
    """The housefly: root empty (registered, so S.move / S.spin work), armature scaled to scene units, body mesh with the leg bones."""
    col = al.load_hero("housefly")
    root = S.empty("fly_root", loc, pop=pop)
    root.rotation_euler = (0.0, 0.0, yaw)
    arm = next(o for o in col.objects if o.type == "ARMATURE")
    body = next(o for o in col.objects if o.type == "MESH")
    arm.parent = root
    arm.scale = (K * size,) * 3
    for n in ("legA", "legB"):
        arm.pose.bones[n].rotation_mode = "QUATERNION"
    return Fly(root, arm, body)


def _rot(arm, name, axis, deg):
    pb = arm.pose.bones[name]
    sh = pb.head.copy()
    pb.matrix = Matrix.Translation(sh) @ Matrix.Rotation(math.radians(deg), 4, axis) @ Matrix.Translation(-sh) @ pb.matrix
    bpy.context.view_layer.update()


def rub(F, amount, phase=0.0):
    """Front legs: amount 0 = resting (as scanned), 1 = raised and meeting in front of the head; phase drives the rubbing swing (radians)."""
    for n in ("legA", "legB"):
        F.arm.pose.bones[n].rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
    bpy.context.view_layer.update()
    if amount <= 1e-4:
        return
    s = math.sin(phase) * RUB_SWING * amount
    _rot(F.arm, "legA", "Y", RUB_PITCH * amount)
    _rot(F.arm, "legB", "Y", RUB_PITCH * amount)
    _rot(F.arm, "legA", "Z", RUB_YAW["legA"] * amount - s)
    _rot(F.arm, "legB", "Z", RUB_YAW["legB"] * amount + s)


def tarsus(F, which="legA"):
    """World position (scene units) of a front leg's tip."""
    return tuple(F.arm.matrix_world @ F.arm.pose.bones[which].tail)


def mouth(F):
    """World position (scene units) of the fly's mouth: the lowest point of the head front in the rest pose, found once on the asset mesh (head is +x)."""
    if not hasattr(F, "_mouth"):
        legs = {F.body.vertex_groups[n].index for n in ("legA", "legB")}
        pts = [v.co for v in F.body.data.vertices if abs(v.co.y) < 0.012 and v.co.z > 0.008 and not any(g.group in legs for g in v.groups)]       # centre line, not a front-leg vertex
        front = sorted(pts, key=lambda p: -p.x)[:300]                                                                       # the head front
        low = min(front, key=lambda p: p.z)
        F._mouth = Vector(low)
    return tuple(F.arm.matrix_world @ F._mouth)


def plate(S, loc=(0.0, 0.0, 0.0), radius=13.0, hexc="#FFF3E0"):
    """A dinner plate as a lathe: flat rim, shallow well. Genuinely geometric, reads instantly (declared in scene_elements)."""
    prof = [(0.0, 0.0), (radius * 0.55, 0.0), (radius * 0.62, 0.5), (radius * 0.80, 0.9), (radius, 1.9), (radius + 0.5, 2.1), (radius + 0.3, 2.4), (radius * 0.97, 2.1),
            (radius * 0.80, 1.2), (radius * 0.62, 0.8), (0.0, 0.8)]
    me = bpy.data.meshes.new("plate")
    bm = bmesh.new()
    vs = [bm.verts.new((x, 0.0, z)) for x, z in prof]
    es = [bm.edges.new((a, b)) for a, b in zip(vs, vs[1:])]
    bmesh.ops.spin(bm, geom=vs + es, axis=(0, 0, 1), cent=(0, 0, 0), angle=math.tau, steps=64, use_duplicate=False)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    o = bpy.data.objects.new("plate", me)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    me.materials.append(S.hero("plate", hexc, rough=0.18, coat=0.6))
    return S.reg(o)


def prop(S, slug, loc=(0.0, 0.0, 0.0), rot=(0.0, 0.0, 0.0), k=K):
    """A sealed library prop at scene scale (asset_rig.load)."""
    return ar.load(S, slug, loc=loc, rot=rot, k=k)


def retint_all(hero, hex_color, role, rough=0.4, coat=0.2):
    """Flat colour for every material of a prop (cuts the texture links, as in 012)."""
    for o in hero.objs:
        for m in o.data.materials:
            if not m:
                continue
            b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
            for name in ("Base Color", "Roughness", "Metallic"):
                for l in list(b.inputs[name].links):
                    m.node_tree.links.remove(l)
            b.inputs["Base Color"].default_value = c.linear(hex_color)
            b.inputs["Roughness"].default_value = rough
            b.inputs["Metallic"].default_value = 0.0
            b.inputs["Coat Weight"].default_value = coat
            m.name = role


def counter(S, hexc=None):
    """The kitchen counter: a wide board under the set (support colour from scenes.json)."""
    return S.box("counter", (420.0, 260.0, 4.0), (0.0, 20.0, -2.0), S.board_mat(0.6), bevel=0.3)
