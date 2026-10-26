"""True cel/toon rendering pass (runs inside Blender), opt-in per production via `"render_style": "toon"` in scenes.json.

This changes the RENDERING LANGUAGE, not the geometry or the choreography:
  1. FLAT CEL SHADING  every material becomes: Diffuse light probe -> Shader to RGB -> constant colour ramp -> Emission.
     Three flat bands with HARD steps, no gradients, no specular, no textures, no subsurface:
         lit    = the exact palette hex
         shadow = same hue and saturation, HSV value x SHADOW_V (0.72)
         deep   = same hue and saturation, HSV value x DEEP_V   (0.50)
     A single hard-shadow sun (the old key light's direction) drives the steps; the HDRI is turned down to ambient fill.
  2. OUTLINES          Freestyle: one dark outline colour and one pixel width on every object, modelled or downloaded
                       (fern cards and the jungle plane are excluded: their rectangles are not their silhouettes).
                       Outline colour = HSV(hue of the backdrop, saturation 0.45, value 0.17); width OUTLINE_PX at 1080x1920
                       (scaled with the render resolution so drafts look like the final).
  3. FLAT BACKDROP     the world's exact spec colour is never touched (camera rays see it flat); depth of field is off.
"""

import colorsys
import math
from pathlib import Path

import bpy
from mathutils import Vector

import cartoon
import common as c

SHADOW_V, DEEP_V = 0.72, 0.50          # band derivation: HSV value multipliers (hue and saturation kept)
T_SHADOW, T_LIT = 0.30, 0.58           # ramp thresholds on the light-probe luminance (calibrated on the draft frames)
OUTLINE_SAT, OUTLINE_VAL = 0.45, 0.17  # outline colour derived from the backdrop hue
OUTLINE_PX = 4.0                       # line width at 1080x1920
AMBIENT = 0.30                         # HDRI strength left as ambient fill
SUN_ENERGY = math.pi                   # sun strength pi -> a white diffuse facing the sun reads ~1.0
KEY_FROM = Vector((-4.5, -5.5, 7.5))   # the direction of the original key light


def _hex(rgb) -> str:
    return "#{:02X}{:02X}{:02X}".format(*(round(255 * x) for x in rgb))


def band_hexes(hex_color: str) -> tuple:
    """(lit, shadow, deep): lit = the exact hex; the others keep hue and saturation and scale the HSV value."""
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return (hex_color, _hex(colorsys.hsv_to_rgb(h, s, v * SHADOW_V)), _hex(colorsys.hsv_to_rgb(h, s, v * DEEP_V)))


def outline_hex(backdrop_hex: str) -> str:
    r, g, b = (int(backdrop_hex[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, _, _ = colorsys.rgb_to_hsv(r, g, b)
    return _hex(colorsys.hsv_to_rgb(h, OUTLINE_SAT, OUTLINE_VAL))


def _toon_material(mat, hex_color: str, alpha_image=None) -> None:
    deep, shadow, lit = (band_hexes(hex_color)[i] for i in (2, 1, 0))
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    probe = nt.nodes.new("ShaderNodeBsdfDiffuse")
    probe.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)         # white: the output is the pure light intensity
    to_rgb = nt.nodes.new("ShaderNodeShaderToRGB")
    bw = nt.nodes.new("ShaderNodeRGBToBW")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "CONSTANT"                          # hard steps, never a gradient
    els = ramp.color_ramp.elements
    els[0].position, els[1].position = 0.0, T_SHADOW
    els.new(T_LIT)
    els[0].color, els[1].color, els[2].color = c.linear(deep), c.linear(shadow), c.linear(lit)
    emit = nt.nodes.new("ShaderNodeEmission")
    nt.links.new(probe.outputs["BSDF"], to_rgb.inputs["Shader"])
    nt.links.new(to_rgb.outputs["Color"], bw.inputs["Color"])
    nt.links.new(bw.outputs["Val"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], emit.inputs["Color"])
    if alpha_image is None:
        nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
        return
    tex = nt.nodes.new("ShaderNodeTexImage")                            # keep the library silhouette (alpha) only
    tex.image = alpha_image
    clear = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
    nt.links.new(clear.outputs["BSDF"], mix.inputs[1])
    nt.links.new(emit.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])


def make_material(name: str, hex_color: str):
    """A new toon material authored directly (for objects modelled in the toon language from the first object)."""
    mat = bpy.data.materials.new(name)
    _toon_material(mat, hex_color)
    return mat


def restyle_materials(pal: dict) -> list:
    """Every named material, modelled or downloaded, becomes a toon material of its palette hex."""
    table, done = cartoon.material_table(pal), []
    for mat in bpy.data.materials:
        if mat.name in table:
            _toon_material(mat, table[mat.name][0])
            done.append(mat.name)
        elif mat.name == "fern" or mat.name.startswith("fern."):
            image = next((n.image for n in mat.node_tree.nodes if n.type == "TEX_IMAGE"), None)
            _toon_material(mat, cartoon.FERN_GREEN, alpha_image=image)
            done.append(mat.name)
    return done


def key_light_and_ambient() -> None:
    """One hard-shadow sun in the old key light's direction; the HDRI only fills ambient light (camera sees the backdrop)."""
    for obj in [o for o in bpy.data.objects if o.type == "LIGHT"]:
        bpy.data.objects.remove(obj)
    sun = bpy.data.lights.new("toon_sun", "SUN")
    sun.energy, sun.angle = SUN_ENERGY, math.radians(0.5)
    obj = bpy.data.objects.new("toon_sun", sun)
    obj.rotation_euler = (-KEY_FROM).to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.collection.objects.link(obj)
    world = bpy.context.scene.world
    for node in world.node_tree.nodes:
        if node.type == "BACKGROUND" and node.inputs["Color"].is_linked:   # the HDRI lighting node, not the camera backdrop
            node.inputs["Strength"].default_value = AMBIENT


def outlines(scene, backdrop_hex: str) -> str:
    """Freestyle: same colour, same pixel width on every object; fern cards and the jungle plane are left out."""
    no_line = bpy.data.collections.new("no_outline")
    scene.collection.children.link(no_line)
    for obj in bpy.data.objects:
        if obj.type == "MESH" and (obj.name == "jungle_back" or "Picsart" in obj.name):
            for coll in list(obj.users_collection):
                coll.objects.unlink(obj)
            no_line.objects.link(obj)
    scene.render.use_freestyle = True
    scene.render.line_thickness_mode = "ABSOLUTE"
    layer = scene.view_layers[0]
    layer.use_freestyle = True
    settings = layer.freestyle_settings
    settings.crease_angle = math.radians(120)
    for existing in list(settings.linesets):
        settings.linesets.remove(existing)
    ls = settings.linesets.new("outline")
    ls.select_silhouette = ls.select_border = ls.select_contour = ls.select_crease = ls.select_material_boundary = True
    ls.select_external_contour = True
    ls.select_by_collection, ls.collection, ls.collection_negation = True, no_line, "EXCLUSIVE"   # exclude the fern cards / plane
    color = outline_hex(backdrop_hex)
    ls.linestyle.color = c.linear(color)[:3]
    ls.linestyle.alpha = 1.0
    ls.linestyle.thickness = OUTLINE_PX * scene.render.resolution_percentage / 100.0
    return color


def apply(production: Path, scene) -> None:
    pal = c.palette(c.identity(Path(production)))
    done = restyle_materials(pal)
    key_light_and_ambient()
    color = outlines(scene, pal["backdrop"])
    for cam in bpy.data.cameras:
        cam.dof.use_dof = False                                         # cel look: no blur
    print("TOON style applied; materials:", ", ".join(sorted(done)))
    print(f"TOON rules: bands lit=exact hex | shadow=HSV value x{SHADOW_V} | deep=HSV value x{DEEP_V}; "
          f"thresholds {T_SHADOW}/{T_LIT}; outline {color} {OUTLINE_PX}px@1080x1920; ambient {AMBIENT}; sun {SUN_ENERGY:.2f}")
