"""Polished-cartoon style pass (runs inside Blender), opt-in per production via `"render_style": "cartoon"` in scenes.json.

One pass restyles EVERY element so modelled and downloaded things share a single register, without touching the scene
scripts' choreography:
  materials  rebuilt in place by name as glossy Principled shaders with the EXACT palette hexes (no textures, no SSS):
             the library skin shader, ant, tweezers and fern foliage included;
  geometry   smooth shading everywhere, bigger bevels on every hard edge, subdivision on the organic library meshes;
  light      larger area lights, i.e. soft shadows.
The world backdrop (the exact spec colour) is never touched. Productions without the field render exactly as before.
"""

import json
from pathlib import Path

import bpy

import common as c

GLOSS_ROUGHNESS, GLOSS_COAT = 0.2, 0.65
THREAD_BLACK, JUNGLE_GREEN, FERN_GREEN = "#17171B", "#3B6C4A", "#5E9E6B"   # not in the palette: thread per the brief, jungle intentional
SKIP_GEOMETRY = {"jungle_back"}


def style_of(production: Path) -> str:
    return json.loads((Path(production) / "scenes.json").read_text(encoding="utf-8")).get("render_style", "photo")


def requested(production: Path) -> bool:
    return style_of(production) == "cartoon"


def _gloss(mat, hex_color: str, roughness: float = GLOSS_ROUGHNESS, metallic: float = 0.0, coat: float = GLOSS_COAT,
           alpha_image=None) -> None:
    """Rebuild `mat` in place as a glossy Principled shader of exactly `hex_color` (no textures, no subsurface)."""
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = c.linear(hex_color)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Coat Weight"].default_value = 0.0 if metallic else coat
    bsdf.inputs["Coat Roughness"].default_value = 0.06
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    if alpha_image is not None:                         # keep the library silhouette, drop the photo colours
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = alpha_image
        nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])


def material_table(pal: dict) -> dict:
    """Library/modelled material name -> (palette hex, glossy kwargs). Shared by the cartoon and toon passes."""
    steel, skin, tissue, shaded = pal["steel grey"], pal["skin peach"], pal["tissue red"], pal["shaded skin"]
    by_name = {  # material name -> (hex, kwargs)
        "SSS Skin Shader": (skin, {}), "skin": (skin, {}), "rim": (skin, {}), "mound": (skin, {}), "lip": (skin, {}),
        "tissue": (tissue, {}), "dermis": (shaded, {}), "fascia": (steel, {}),
        "needle": (steel, dict(metallic=1.0, roughness=0.18)), "steel": (steel, dict(metallic=1.0, roughness=0.18)),
        "tw_Met": (steel, dict(metallic=1.0, roughness=0.18)), "tw_Pl": (steel, {}),
        "thread": (THREAD_BLACK, dict(roughness=0.35)),
        "Ant": (tissue, {}), "Eye": (THREAD_BLACK, dict(roughness=0.08, coat=0.8)),
        "jungle_back": (JUNGLE_GREEN, dict(roughness=0.9, coat=0.0)),
    }
    return by_name


def restyle_materials(pal: dict) -> list:
    by_name = material_table(pal)
    done = []
    for mat in bpy.data.materials:
        if mat.name in by_name:
            hex_color, kw = by_name[mat.name]
            _gloss(mat, hex_color, **kw)
            done.append(mat.name)
        elif mat.name == "fern" or mat.name.startswith("fern."):
            image = next((n.image for n in mat.node_tree.nodes if n.type == "TEX_IMAGE"), None)
            _gloss(mat, FERN_GREEN, roughness=0.5, coat=0.2, alpha_image=image)
            done.append(mat.name)
    return done


def round_geometry() -> None:
    for obj in bpy.data.objects:
        if obj.type != "MESH" or obj.name in SKIP_GEOMETRY:
            continue
        for poly in obj.data.polygons:
            poly.use_smooth = True
        for mod in obj.modifiers:
            if mod.type == "BEVEL":                    # every hard edge gets a generous, pillowy round-over
                ext = [max(v.co[i] for v in obj.data.vertices) - min(v.co[i] for v in obj.data.vertices) for i in range(3)]
                mod.width = max(0.02, min(0.12, 0.35 * min(ext)))
                mod.segments = 6
        if obj.name in {"Ant", "upside", "downside"} and not any(m.type == "SUBSURF" for m in obj.modifiers):
            sub = obj.modifiers.new("cartoon_subsurf", "SUBSURF")   # organic / library meshes: subdivide
            sub.levels, sub.render_levels = 1, 2
    for curve in bpy.data.curves:
        curve.bevel_resolution = 6                      # rounder thread


def soften_light() -> None:
    for light in bpy.data.lights:
        if light.type == "AREA":
            light.size *= 2.0                           # bigger source = softer shadows


def apply_if_requested(production: Path, scene) -> None:
    """Call right before rendering. No-op unless the production asks for render_style 'cartoon'."""
    style = style_of(production)
    if style == "toon":                                 # cel/toon rendering language: its own module
        import toon
        toon.apply(production, scene)
        return
    if style != "cartoon":
        return
    pal = c.palette(c.identity(Path(production)))
    done = restyle_materials(pal)
    round_geometry()
    soften_light()
    print("CARTOON style applied; materials restyled:", ", ".join(sorted(done)))
