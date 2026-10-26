"""Library props appended from code3d/assets (runs inside Blender). Source first: never remodel what a library has."""

import math
from pathlib import Path

import bpy
from mathutils import Vector

import common as c


def load_tweezers(scale: float = 30.0, grip_hex: str = "#C6CFCE"):
    """BlenderKit 'Tweezers' (royalty free, Yahya Janani): two arms (upside / downside) under one empty, 8.4 cm long.
    The empty's origin is the TIP; the arms touch at the tip and diverge toward the hinge end at local x = -0.0836.
    Returns an object with .root (position/aim it), .set_open(deg) (opens or closes the grip) and .tip (the origin)."""
    blend = c.ASSETS / "models" / "blenderkit-tweezers.blend"
    with bpy.data.libraries.load(str(blend), link=False) as (src, dst):
        dst.objects = ["Tweezers", "upside", "downside"]
    for obj in dst.objects:
        bpy.context.scene.collection.objects.link(obj)
    root, up, down = (bpy.data.objects[n] for n in ("Tweezers", "upside", "downside"))
    # move each arm's origin to the hinge end so a rotation about y opens the tips
    hinge = Vector((-0.0836, 0.0, 0.0007))
    for arm in (up, down):
        bpy.context.view_layer.objects.active = arm
        arm.select_set(True)
        bpy.context.scene.cursor.location = root.matrix_world @ hinge
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        arm.select_set(False)
    # library assets bring their own colours: retint the (purple) plastic to the channel palette's steel grey
    plastic = bpy.data.materials["tw_Pl"]
    for node in plastic.node_tree.nodes:
        if node.type == "BSDF_PRINCIPLED":
            node.inputs["Base Color"].default_value = c.linear(grip_hex)
    root.scale = (scale, scale, scale)
    bpy.context.scene.cursor.location = (0, 0, 0)

    class Tweezers:
        def __init__(self):
            self.root, self.up, self.down = root, up, down

        def set_open(self, deg: float) -> None:
            self.up.rotation_euler.y = -math.radians(deg)
            self.down.rotation_euler.y = math.radians(deg)

        def place(self, tip: Vector, direction: Vector) -> None:
            """Put the tip at `tip`, with the tweezers pointing along `direction` (tip first)."""
            self.root.location = tip
            self.root.rotation_euler = direction.normalized().to_track_quat("X", "Z").to_euler()

    return Tweezers()
