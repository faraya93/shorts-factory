"""Headless Blender smoke test: cube + light + camera -> PNG. Usage: blender -b --python spikes/blender_smoke.py -- <out.png> [ENGINE]"""

import sys

import bpy

out = sys.argv[sys.argv.index("--") + 1]
engine = sys.argv[sys.argv.index("--") + 2] if len(sys.argv) > sys.argv.index("--") + 2 else "BLENDER_EEVEE"

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.engine = engine
scene.render.resolution_x, scene.render.resolution_y = 540, 960
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = out


def linear(hex_color: str) -> tuple:
    """sRGB hex -> linear RGBA: Blender works in linear space, so exact hex values need this conversion."""
    c = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c) + (1.0,)


# Exact colours need (1) node-based world/material (world.color and diffuse_color are viewport-only) and
# (2) the Standard view transform (the default tone-mapper shifts colours).
scene.view_settings.view_transform = "Standard"
scene.world = bpy.data.worlds.new("bg")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = linear("#E2D5F1")  # channel backdrop
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0

bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0), rotation=(0.5, 0.3, 0.6))
cube = bpy.context.object
mat = bpy.data.materials.new("skin")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = linear("#E0B0A0")  # skin peach
cube.data.materials.append(mat)

bpy.ops.object.light_add(type="SUN", location=(3, -3, 5))
bpy.context.object.data.energy = 3.0
bpy.ops.object.camera_add(location=(5.5, -6.5, 4.5), rotation=(1.0, 0, 0.75))
scene.camera = bpy.context.object

bpy.ops.render.render(write_still=True)
print("rendered with", scene.render.engine, "->", out)
