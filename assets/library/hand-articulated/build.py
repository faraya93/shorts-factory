"""hand-articulated: build and pose script (run inside Blender: exec(open(path).read())).

Source mesh: Sketchfab "Free Pack - VR Hands (Rigged)" by polyone, CC-BY-4.0, uid b3b8309e59c748e3956531c8f57dd233
(imported with the MCP import_asset, target_size 0.2). `cleanup()` keeps the right hand, removes the left hand, applies transforms at real
scale (0.19 m long) and renames. `POSES` are joint angles; `bake_actions()` stores each as an Action on the armature (pose_<name>).
Joint convention (measured 2026-11-11): bone rest frames are arbitrary FBX leftovers, so rotations are expressed about ARMATURE axes:
fingers point -Z, palm faces -Y, fingers spread along X. Finger flexion = negative rotation about X; thumb flexion = negative X,
thumb opposition/spread = Y and Z. `rot` composes (x, y, z) degrees as an armature-space rotation and converts to the bone's local frame.
"""
import math
import bpy
from mathutils import Matrix, Euler

ARM, MESH = "hand_armature", "hand_mesh"
FINGERS = ("Index", "Middle", "Ring", "Pinky")


def cleanup():
    arm, m = bpy.data.objects["Object_4"], bpy.data.objects["Object_6"]
    # (the interactive session removed the left hand by vertex-group dominance, deleted J_Left bones, applied scale 2.7 about the wrist, parented mesh to armature)
    raise RuntimeError("cleanup was performed interactively; see job/report.md for the steps. Re-download the source and repeat if the .blend is lost.")


def bone(f, j):
    arm = bpy.data.objects[ARM]
    return arm.pose.bones[[b.name for b in arm.pose.bones if b.name.startswith(f"J_Right_Hand{f}{j}_")][0]]


def rot(pb, x=0.0, y=0.0, z=0.0):
    B = pb.bone.matrix_local.to_3x3()
    R = Euler((math.radians(x), math.radians(y), math.radians(z)), "XYZ").to_matrix()
    pb.rotation_mode = "QUATERNION"
    pb.rotation_quaternion = (B.inverted() @ R @ B).to_quaternion()


def reset():
    for pb in bpy.data.objects[ARM].pose.bones:
        pb.rotation_mode = "QUATERNION"
        pb.rotation_quaternion = (1, 0, 0, 0)


# finger: (mcp, pip, dip) flexion in degrees (positive = curl), spread = rotation of the MCP about Y (degrees)
# thumb: list of (x, y, z) per joint 1..3 ; wrist: (x, y, z)
POSES = {
    # relaxed open hand (brief state 1)
    "open": {"fingers": {"Index": (12, 14, 8, -3), "Middle": (15, 16, 8, 0), "Ring": (18, 18, 10, 3), "Pinky": (22, 20, 10, 6)}, "thumb": [(-5, 0, -8), (-8, 0, 0), (-8, 0, 0)]},
    # gripping a lever / door handle, bar radius 16 mm at (y -58, z -12) mm (state 2)
    "lever": {"fingers": {"Index": (60, 75, 40, 0), "Middle": (62, 78, 42, 0), "Ring": (64, 78, 42, 0), "Pinky": (66, 76, 40, 0)}, "thumb": [(0, 0, 30), (0, 30, 0), (-15, 0, 0)]},
    # gripping a steering wheel rim (same grip, rim radius 17 mm; the wrist is turned) (state 3)
    "wheel": {"fingers": {"Index": (58, 72, 38, 0), "Middle": (60, 76, 40, 0), "Ring": (62, 76, 40, 0), "Pinky": (64, 74, 38, 0)}, "thumb": [(0, 0, 30), (0, 30, 0), (-12, 0, 0)], "wrist": (0, 0, 0)},
    # reaching, palm resting flat on a car door panel (state 4)
    "door": {"fingers": {"Index": (8, 10, 6, -4), "Middle": (10, 12, 6, 0), "Ring": (12, 12, 6, 4), "Pinky": (14, 14, 8, 8)}, "thumb": [(-3, 0, -10), (-5, 0, 0), (-5, 0, 0)]},
    # holding a knife handle: tighter, thumb on the side (state 5)
    "knife": {"fingers": {"Index": (66, 82, 48, 0), "Middle": (70, 86, 50, 0), "Ring": (72, 86, 50, 0), "Pinky": (72, 82, 46, 0)}, "thumb": [(0, 0, 28), (0, 28, 0), (-14, 0, 0)]},
    # fumbling with a mask: uneven curls, pinky and ring loose (state 6; second frame "mask_b" is the same grab one beat later)
    "mask": {"fingers": {"Index": (45, 55, 30, -6), "Middle": (55, 65, 35, 0), "Ring": (25, 30, 15, 6), "Pinky": (15, 18, 10, 12)}, "thumb": [(-10, 0, 20), (-10, 20, 0), (-10, 0, 0)]},
    "mask_b": {"fingers": {"Index": (30, 40, 25, -8), "Middle": (35, 45, 25, -2), "Ring": (50, 60, 35, 4), "Pinky": (45, 55, 30, 10)}, "thumb": [(-5, 0, 10), (-10, 12, 0), (-10, 0, 0)]},
    # pressing a button with the index finger (extra proof)
    "press": {"fingers": {"Index": (14, 8, 4, 0), "Middle": (80, 95, 55, 0), "Ring": (82, 95, 55, 0), "Pinky": (82, 90, 50, 0)}, "thumb": [(-25, 0, 20), (-25, 10, 0), (-20, 0, 0)]},
    # knuckle-cracking: fist, thumb pressing the index finger's middle joint (extra proof)
    "crack": {"fingers": {"Index": (85, 105, 45, 0), "Middle": (88, 100, 50, 0), "Ring": (88, 100, 50, 0), "Pinky": (85, 95, 45, 0)}, "thumb": [(0, -20, 20), (-30, 20, 0), (-30, 0, 0)]},
}


def apply(name):
    p = POSES[name]
    reset()
    for f in FINGERS:
        mcp, pip, dip, spread = p["fingers"].get(f, (0, 0, 0, 0))
        for j, a in ((1, mcp), (2, pip), (3, dip)):
            rot(bone(f, j), x=-a, y=spread if j == 1 else 0)
    for j, (x, y, z) in enumerate(p.get("thumb", [(0, 0, 0)] * 3), start=1):
        rot(bone("Thumb", j), x, y, z)
    wp = bpy.data.objects[ARM].pose.bones["J_Right_Hand_024"]
    rot(wp, *p.get("wrist", (0, 0, 0)))
    bpy.context.view_layer.update()
