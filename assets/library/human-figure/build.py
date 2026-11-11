"""human-figure: procedural build and pose script (run inside Blender: exec(open(path).read()); build(); bake_actions()).

Own work, no sourced mesh (sourcing found only realistic or branded rigs, see job/report.md). A faceless capsule mannequin, 1.78 m tall, facing -Y,
left side at +X, standing on z=0. Every body part is a closed lofted mesh bound rigidly (weight 1) to one bone; round end caps overlap at the joints
so bends read as continuous. Colour blocks are separate material slots a production recolours: fig_skin, fig_shirt, fig_pants, fig_boots.
Joints: pelvis, spine, chest, neck, head, shoulders (upperarm), elbows (forearm), wrists (hand), hips (thigh), knees (shin), ankles (foot).
Pose rotations are degrees about ARMATURE axes at each joint (x = pitch: negative swings a hanging limb FORWARD, i.e. toward -Y; y = roll/abduct;
z = twist); see `rot`. A pose gives the LEFT side; the right side mirrors (y and z negated) unless a "R_<bone>" key overrides it.
"""
import math
import bpy
import bmesh
from mathutils import Matrix, Vector, Euler

ARM = "figure_armature"
COL = "asset"
SEG = 20

COLOURS = {  # defaults; productions recolour through hero_colours
    "fig_skin": (0.85, 0.62, 0.48), "fig_shirt": (0.16, 0.45, 0.80), "fig_pants": (0.18, 0.20, 0.30), "fig_boots": (0.35, 0.20, 0.10),
}


def material(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*COLOURS[name], 1)
    b.inputs["Roughness"].default_value = 0.6
    return m


def capsule_rings(length, r, sx=1.0, sy=1.0, cap=7):
    """profile of a capsule along local z from 0 to length: hemispherical caps of radius r, straight middle."""
    bottom = []
    for i in range(cap + 1):
        a = (math.pi / 2) * (i / cap)           # 0 = pole, pi/2 = equator
        bottom.append((r * (1 - math.cos(a)), r * math.sin(a) * sx, r * math.sin(a) * sy))
    top = [(length - z, rx, ry) for z, rx, ry in reversed(bottom)]
    return bottom + top


def loft(name, rings, mat, bone, origin=(0, 0, 0), direction=(0, 0, 1), roll_dir=(1, 0, 0)):
    """rings: [(t, rx, ry)] along local z. Closed mesh, end rings should be tiny/zero radius (poles)."""
    verts, faces = [], []
    n = SEG
    rings = list(rings)
    pole0 = pole1 = None
    if rings[0][1] == 0 and rings[0][2] == 0:        # a zero-radius end ring is a single pole vertex, not 20 coincident ones
        pole0 = rings.pop(0)[0]
    if rings[-1][1] == 0 and rings[-1][2] == 0:
        pole1 = rings.pop()[0]
    for t, rx, ry in rings:
        for k in range(n):
            a = 2 * math.pi * k / n
            verts.append((rx * math.cos(a), ry * math.sin(a), t))
    for i in range(len(rings) - 1):
        for k in range(n):
            a, b = i * n + k, i * n + (k + 1) % n
            faces.append((a, b, b + n, a + n))
    c0 = len(verts); verts.append((0, 0, pole0 if pole0 is not None else rings[0][0]))
    for k in range(n):
        faces.append((c0, (k + 1) % n, k))
    c1 = len(verts); verts.append((0, 0, pole1 if pole1 is not None else rings[-1][0]))
    base = (len(rings) - 1) * n
    for k in range(n):
        faces.append((c1, base + k, base + (k + 1) % n))
    z = Vector(direction).normalized()
    x = (Vector(roll_dir) - z * Vector(roll_dir).dot(z)).normalized()
    y = z.cross(x)
    M = Matrix(((x.x, y.x, z.x, origin[0]), (x.y, y.y, z.y, origin[1]), (x.z, y.z, z.z, origin[2]), (0, 0, 0, 1)))
    me = bpy.data.meshes.new(name)
    me.from_pydata([M @ Vector(v) for v in verts], [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(material(mat))
    vg = ob.vertex_groups.new(name=bone)
    vg.add(list(range(len(me.vertices))), 1.0, "REPLACE")
    bpy.data.collections[COL].objects.link(ob)
    return ob


def seg(name, mat, bone, p0, p1, r, sx=1.0, sy=1.0):
    d = Vector(p1) - Vector(p0)
    return loft(name, capsule_rings(d.length, r, sx, sy), mat, bone, p0, d)


BONES = {  # name: (parent, head, tail)
    "root": (None, (0, 0, 0), (0, 0, 0.12)),
    "pelvis": ("root", (0, 0, 0.92), (0, 0, 1.05)),
    "spine": ("pelvis", (0, 0, 1.05), (0, 0, 1.25)),
    "chest": ("spine", (0, 0, 1.25), (0, 0, 1.46)),
    "neck": ("chest", (0, 0, 1.46), (0, 0, 1.60)),
    "head": ("neck", (0, 0, 1.60), (0, 0, 1.80)),
}
for s, sg in (("L", 1), ("R", -1)):
    BONES.update({
        f"upperarm.{s}": ("chest", (0.215 * sg, 0, 1.45), (0.215 * sg, 0, 1.17)),
        f"forearm.{s}": (f"upperarm.{s}", (0.215 * sg, 0, 1.17), (0.215 * sg, 0, 0.92)),
        f"hand.{s}": (f"forearm.{s}", (0.215 * sg, 0, 0.92), (0.215 * sg, 0, 0.74)),
        f"thigh.{s}": ("pelvis", (0.095 * sg, 0, 0.92), (0.095 * sg, 0, 0.50)),
        f"shin.{s}": (f"thigh.{s}", (0.095 * sg, 0, 0.50), (0.095 * sg, 0, 0.10)),
        f"foot.{s}": (f"shin.{s}", (0.095 * sg, 0, 0.10), (0.095 * sg, -0.17, 0.07)),
    })


def build():
    if COL not in bpy.data.collections:
        c = bpy.data.collections.new(COL); bpy.context.scene.collection.children.link(c)
    for n in COLOURS:
        material(n)
    # armature
    ad = bpy.data.armatures.new(ARM)
    arm = bpy.data.objects.new(ARM, ad)
    bpy.data.collections[COL].objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    for n, (par, h, t) in BONES.items():
        eb = ad.edit_bones.new(n); eb.head, eb.tail = h, t
        eb.roll = 0
        if par:
            eb.parent = ad.edit_bones[par]
            eb.use_connect = False
    bpy.ops.object.mode_set(mode="OBJECT")
    parts = []
    P = parts.append
    # torso: pelvis (pants), lower torso and chest (shirt), neck and head (skin)
    P(loft("fig_pelvis", [(0.80, 0.0, 0.0), (0.84, .10, .075), (0.90, .160, .100), (0.99, .165, .100), (1.06, .150, .095), (1.10, .0, .0)], "fig_pants", "pelvis"))
    P(loft("fig_abdomen", [(1.00, 0.0, 0.0), (1.04, .150, .092), (1.15, .150, .092), (1.26, .160, .098), (1.29, .0, .0)], "fig_shirt", "spine"))
    P(loft("fig_chest", [(1.22, 0.0, 0.0), (1.26, .150, .097), (1.34, .172, .105), (1.43, .185, .105), (1.49, .150, .085), (1.53, .060, .050), (1.55, 0.0, 0.0)], "fig_shirt", "chest"))
    P(seg("fig_neck", "fig_skin", "neck", (0, 0, 1.47), (0, 0, 1.64), 0.045))
    P(loft("fig_head", [(1.60, 0.0, 0.0), (1.62, .045, .050), (1.66, .085, .095), (1.72, .098, .108), (1.78, .088, .098), (1.83, .045, .050), (1.85, 0.0, 0.0)], "fig_skin", "head"))
    for s, sg in (("L", 1), ("R", -1)):
        x = 0.215 * sg
        P(seg(f"fig_upperarm.{s}", "fig_shirt", f"upperarm.{s}", (x, 0, 1.46), (x, 0, 1.17), 0.058))
        P(seg(f"fig_forearm.{s}", "fig_shirt", f"forearm.{s}", (x, 0, 1.18), (x, 0, 0.95), 0.050))
        P(seg(f"fig_hand.{s}", "fig_skin", f"hand.{s}", (x, 0, 0.96), (x, 0, 0.72), 0.040, 1.15, 0.7))
        xh = 0.095 * sg
        P(seg(f"fig_thigh.{s}", "fig_pants", f"thigh.{s}", (xh, 0, 0.93), (xh, 0, 0.50), 0.088))
        P(seg(f"fig_shin.{s}", "fig_pants", f"shin.{s}", (xh, 0, 0.51), (xh, 0, 0.16), 0.067))
        P(seg(f"fig_bootshaft.{s}", "fig_boots", f"shin.{s}", (xh, 0, 0.09), (xh, 0, 0.22), 0.075))
        P(seg(f"fig_foot.{s}", "fig_boots", f"foot.{s}", (xh, 0.05, 0.065), (xh, -0.17, 0.062), 0.066, 1.0, 0.95))
    for o in parts:
        o.parent = arm
        md = o.modifiers.new("Armature", "ARMATURE"); md.object = arm
    return arm


def bone(n):
    return bpy.data.objects[ARM].pose.bones[n]


def rot(pb, x=0.0, y=0.0, z=0.0):
    B = pb.bone.matrix_local.to_3x3()
    R = Euler((math.radians(x), math.radians(y), math.radians(z)), "XYZ").to_matrix()
    pb.rotation_mode = "QUATERNION"
    pb.rotation_quaternion = (B.inverted() @ R @ B).to_quaternion()


def reset():
    for pb in bpy.data.objects[ARM].pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)


SIDED = ("upperarm", "forearm", "hand", "thigh", "shin", "foot")
POSES = {
    "standing": {"upperarm": (4, -7, 0), "forearm": (-10, 0, 0), "thigh": (0, -2, 0), "head": (0, 0, 0)},
    "walking": {"thigh": (-28, -2, 0), "R_thigh": (20, 2, 0), "shin": (8, 0, 0), "R_shin": (30, 0, 0), "foot": (-5, 0, 0), "R_foot": (-10, 0, 0),
                "upperarm": (24, -5, 0), "R_upperarm": (-26, 5, 0), "forearm": (-12, 0, 0), "R_forearm": (-30, 0, 0), "spine": (-3, 0, 0)},
    "jumping": {"root_loc": (0, 0, 0.45), "thigh": (-45, -6, 0), "shin": (70, 0, 0), "foot": (-20, 0, 0), "upperarm": (-155, 14, 0), "forearm": (-15, 0, 0), "spine": (-4, 0, 0), "head": (-8, 0, 0)},
    "falling": {"root_loc": (0, 0, 0.9), "pelvis": (62, 8, 25), "upperarm": (-35, -100, 0), "R_upperarm": (-95, 80, 0), "forearm": (-30, 0, 0), "R_forearm": (-10, 0, 0),
                "thigh": (-25, -35, 0), "R_thigh": (30, 45, 0), "shin": (35, 0, 0), "R_shin": (55, 0, 0), "head": (-25, 10, 15), "spine": (10, 0, 5)},
    "seated": {"root_loc": (0, 0, -0.42), "thigh": (-88, -3, 0), "shin": (88, 0, 0), "foot": (-3, 0, 0), "upperarm": (-55, -4, 0), "forearm": (-40, 0, 0), "hand": (-10, 0, 0), "spine": (-4, 0, 0)},
    "sunk": {"root_loc": (0, 0, -0.92), "upperarm": (-120, 35, 0), "forearm": (-20, 0, 0), "head": (-18, 0, 0), "spine": (-3, 0, 0), "thigh": (0, -1, 0)},
}


def apply(name):
    p = POSES[name]
    reset()
    arm = bpy.data.objects[ARM]
    for k, v in p.items():
        if k == "root_loc":
            bone("root").location = bone("root").bone.matrix_local.to_3x3().inverted() @ Vector(v)
            continue
        if k in SIDED:
            x, y, z = v
            rot(bone(k + ".L"), x, y, z)
            if "R_" + k not in p:
                rot(bone(k + ".R"), x, -y, -z)
        elif k.startswith("R_"):
            rot(bone(k[2:] + ".R"), *v)
        else:
            rot(bone(k), *v)
    bpy.context.view_layer.update()


def bake_actions():
    arm = bpy.data.objects[ARM]
    arm.animation_data_create()
    for n in POSES:
        apply(n)
        act = bpy.data.actions.new("pose_" + n); act.use_fake_user = True
        arm.animation_data.action = act
        for pb in arm.pose.bones:
            pb.keyframe_insert("rotation_quaternion", frame=1, group=pb.name)
            pb.keyframe_insert("location", frame=1, group=pb.name)
        tr = arm.animation_data.nla_tracks.new(); tr.name = "pose_" + n
        tr.strips.new("pose_" + n, 1, act); tr.mute = True
        arm.animation_data.action = None
    reset()
