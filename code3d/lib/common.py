"""code3d shared library (runs inside Blender): identity palette, exact colours, render setup, studio world, camera.

Rules (see CLAUDE.md "code3d sourcing and optimization"): colours come from the production's visual_identity block
(exact hex), the world shows the spec backdrop to the camera while the library HDRI only lights the scene, and
DRAFT renders (half resolution, few samples) are the default while iterating.
"""

import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "code3d" / "assets"
FPS, FULL_W, FULL_H = 30, 1080, 1920


def linear(hex_color: str, alpha: float = 1.0) -> tuple:
    """sRGB hex -> linear RGBA (Blender works in linear space; exact hex values need this conversion)."""
    c = [int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple((v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4) for v in c) + (alpha,)


def identity(production: Path) -> dict:
    return json.loads((production / "scenes.json").read_text(encoding="utf-8"))["visual_identity"]


def palette(vi: dict) -> dict:
    """name -> hex, plus 'backdrop' (the spec background)."""
    out = {c["name"]: c["hex"] for c in vi["palette"] if c.get("name")}
    out["backdrop"] = vi["background"]["hex"]
    return out


def parse_args() -> dict:
    """Arguments after `--`: key=value pairs (production, mode, frames, out ...)."""
    raw = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    return dict(a.split("=", 1) for a in raw)


def reset_scene() -> bpy.types.Scene:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


def setup_render(scene, mode: str = "draft") -> None:
    """draft = half resolution + few samples (iteration); final = 1080x1920 + more samples (rendered once)."""
    scene.render.engine = "BLENDER_EEVEE"
    scale = 50 if mode == "draft" else 100                # "draft-full": 1080x1920 with the draft sample count
    scene.render.resolution_x, scene.render.resolution_y = FULL_W, FULL_H
    scene.render.resolution_percentage = scale
    scene.render.fps = FPS
    scene.eevee.taa_render_samples = 12 if mode.startswith("draft") else 96
    scene.view_settings.view_transform = "Standard"   # the default tone-mapper shifts colours
    scene.view_settings.look = "None"
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False


def studio_world(scene, backdrop_hex: str, hdri: Path, strength: float = 1.0) -> None:
    """HDRI lights the scene; the camera sees the exact backdrop colour (mix on 'Is Camera Ray')."""
    world = bpy.data.worlds.new("studio")
    scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(str(hdri))
    lit = nt.nodes.new("ShaderNodeBackground")
    lit.inputs["Strength"].default_value = strength
    cam = nt.nodes.new("ShaderNodeBackground")
    cam.inputs["Color"].default_value = linear(backdrop_hex)
    cam.inputs["Strength"].default_value = 1.0
    path = nt.nodes.new("ShaderNodeLightPath")
    mix = nt.nodes.new("ShaderNodeMixShader")
    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(env.outputs["Color"], lit.inputs["Color"])
    nt.links.new(path.outputs["Is Camera Ray"], mix.inputs["Fac"])
    nt.links.new(lit.outputs["Background"], mix.inputs[1])
    nt.links.new(cam.outputs["Background"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])


def principled(name: str, hex_color: str, roughness: float = 0.5, metallic: float = 0.0, subsurface: float = 0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = linear(hex_color)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if subsurface:
        bsdf.inputs["Subsurface Weight"].default_value = subsurface
    return mat


def append_material(blend: Path, name: str):
    """Link-free append of a library material (never re-download: assets live in code3d/assets)."""
    with bpy.data.libraries.load(str(blend), link=False) as (src, dst):
        dst.materials = [name]
    return bpy.data.materials[name]


def make_camera(scene, lens: float = 50.0):
    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = lens
    cam = bpy.data.objects.new("cam", cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    return cam


def orbit(cam, target: Vector, radius: float, elevation_deg: float, azimuth_deg: float) -> None:
    """Place the camera on a sphere around `target`: azimuth 0 = looking along +y from the -y side."""
    el, az = math.radians(elevation_deg), math.radians(azimuth_deg)
    cam.location = target + Vector((radius * math.sin(az) * math.cos(el), -radius * math.cos(az) * math.cos(el),
                                    radius * math.sin(el)))
    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_light(scene, kind: str, location, energy: float, size: float = 3.0, target: Vector = Vector((0, 0, 0))):
    data = bpy.data.lights.new("key", kind)
    data.energy = energy
    if kind == "AREA":
        data.size = size
    light = bpy.data.objects.new("key", data)
    light.location = location
    light.rotation_euler = (target - Vector(location)).to_track_quat("-Z", "Y").to_euler()
    scene.collection.objects.link(light)
    return light


def smooth(a: float, b: float, t: float) -> float:
    k = min(1.0, max(0.0, (t - a) / (b - a)))
    return k * k * (3 - 2 * k)


def render_frames(scene, out_dir: Path, start: int, end: int) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    scene.frame_start, scene.frame_end = start, end
    scene.render.filepath = str(out_dir / "f-")
    bpy.ops.render.render(animation=True)
