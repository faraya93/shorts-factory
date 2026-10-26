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


def load_ant(scale: float = 90.0):
    """BlenderKit 'Ant (Rigged)' (CC0, Nik Kottmann): 50 bones. The ant faces -y; its mandibles are the bones L.Nose and
    R.Nose (x = +/-0.0008, mouth at local y = -0.0087, z = 0.0108). The armature origin is on the ground between the feet.
    Returns an object with .arm (armature), .set_jaws(deg) (opens or closes the mandibles) and .place(location)."""
    blend = c.ASSETS / "models" / "blenderkit-ant-rigged.blend"
    with bpy.data.libraries.load(str(blend), link=False) as (src, dst):
        dst.objects = ["Ant (Rigged)", "Ant"]
    for obj in dst.objects:
        bpy.context.scene.collection.objects.link(obj)
    arm = bpy.data.objects["Ant (Rigged)"]
    arm.scale = (scale, scale, scale)
    for name in ("L.Nose", "R.Nose"):
        arm.pose.bones[name].rotation_mode = "XYZ"

    class Ant:
        def __init__(self):
            self.arm = arm
            self.scale = scale

        def mouth(self, location: Vector) -> Vector:
            """World position of the mouth for an ant placed with its feet-origin at `location`."""
            return location + Vector((0.0, -0.0087, 0.0108)) * self.scale

        def place(self, location: Vector) -> None:
            self.arm.location = location

        def set_jaws(self, deg: float) -> None:
            self.arm.pose.bones["L.Nose"].rotation_euler.z = math.radians(deg)
            self.arm.pose.bones["R.Nose"].rotation_euler.z = -math.radians(deg)

    return Ant()


def jungle(stage, green_hex: str = "#3B6C4A", count: int = 9):
    """A softly blurred jungle behind the action: library fern cards (BlenderKit 'Tall Forest Fern') scattered in front
    of a dark green backdrop plane. The scene's camera depth of field does the blurring."""
    blend = c.ASSETS / "models" / "blenderkit-tall-forest-fern.blend"
    with bpy.data.libraries.load(str(blend), link=False) as (src, dst):
        dst.objects = ["Tall Forest Fern", "Picsart_24-11-03_17-17-16-746.006"]
    root, card = (bpy.data.objects[n] for n in ("Tall Forest Fern", "Picsart_24-11-03_17-17-16-746.006"))
    bpy.context.scene.collection.objects.link(root)
    bpy.context.scene.collection.objects.link(card)
    root.hide_render = True
    # dark green backdrop
    bpy.ops.mesh.primitive_plane_add(size=60, location=(0, 14, 4), rotation=(math.pi / 2, 0, 0))
    plane = bpy.context.object
    plane.data.materials.append(c.principled("jungle_back", green_hex, roughness=1.0))
    placed = []
    for i in range(count):
        copy = card.copy()
        copy.data = card.data
        copy.parent = None
        copy.location = (-9 + 18 * (i / (count - 1)), 8.5 + (i % 3) * 1.6, 0.5 + (i % 2) * 1.2)
        copy.rotation_euler = (0, 0, math.radians(35 * ((i % 5) - 2)))
        copy.scale = (6.0, 6.0, 6.0)
        copy.visible_shadow = False                        # soft jungle: the cards must not cast hard shadows
        bpy.context.scene.collection.objects.link(copy)
        placed.append(copy)
    card.hide_render = True
    return placed
