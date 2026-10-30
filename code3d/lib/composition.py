"""Frame-composition probe (Blender side). After a beauty still, render a flat "class mask" still of the same frame: every material is replaced
by an emission colour that encodes its role (stage, support, hero, accent, error). tools/composition_gate.py reads beauty + mask and tabulates
the pairwise colour distances IN FRAME. Role by material name below; unknown materials are 'other' and ignored."""
import bpy

import common as c

CLASS_COLOURS = {   # unique flat colours (sRGB 0-255); the gate reads them back by exact match
    "stage": (255, 0, 255), "support_board": (0, 255, 0), "support_plinth": (0, 200, 120), "support_panel": (0, 120, 60), "support_plate": (120, 255, 120),
    "hero_big": (0, 0, 255), "hero_small": (0, 120, 255), "hero_marker": (120, 120, 255), "hero_housing": (255, 128, 0), "hero_rubber": (128, 64, 0),
    "hero_blade": (255, 255, 128), "hero_other": (160, 160, 160), "accent": (255, 255, 0), "error": (255, 0, 0), "other": (60, 60, 60)}
BY_MATERIAL = {   # base material name (suffix .001 stripped) -> class
    "g_board": "support_board", "table": "support_plinth", "ink": "support_plinth", "blockm": "support_panel", "block": "support_panel", "plate": "support_plate",
    "g_big": "hero_big", "g_pin": "hero_small", "g_mark": "hero_marker", "shell_y": "hero_housing", "rubber_k": "hero_rubber", "blade": "hero_blade",
    "dark_metal2": "hero_other", "coil": "hero_other", "metal": "hero_other", "slot": "hero_other",
    "mag_n": "hero_big", "mag_s": "hero_housing", "alu": "hero_small", "copper": "hero_rubber", "stainless": "hero_other", "filings": "other", "water": "hero_big", "waste": "hero_rubber", "sewage": "hero_housing", "microbe": "hero_small", "wipe": "hero_blade", "paper": "other", "foam": "other", "gas": "other", "gold": "accent", "gold_dim": "accent", "spring": "accent", "red": "error"}


def _base(name: str) -> str:
    return name.split(".")[0]


def begin_masks(scene) -> None:
    """Replace every material by its class emission, the world by flat magenta, and strip bloom/denoise: call ONCE after the beauty stills."""
    mats = {k: _flat_emission(k, v) for k, v in CLASS_COLOURS.items()}
    for obj in scene.objects:
        if obj.type != "MESH":
            continue
        if obj.name == "floor":
            obj.hide_render = True                       # the shadow catcher must not paint the mask
            continue
        for slot in obj.material_slots:
            cls = BY_MATERIAL.get(_base(slot.material.name), "other") if slot.material else "other"
            slot.material = mats[cls]
    world = bpy.data.worlds.new("mask_world")
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Color"].default_value = c.linear("#FF00FF")
    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    scene.world = world
    cy = scene.cycles
    cy.samples, cy.use_adaptive_sampling, cy.use_denoising, cy.max_bounces = 4, False, False, 1
    cy.filter_width = 0.01
    scene.compositing_node_group = None                  # no bloom on the mask


def save_mask_still(scene, path: str) -> None:
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


def _flat_emission(name: str, rgb):
    mat = bpy.data.materials.new("mask_" + name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = c.linear("#%02X%02X%02X" % rgb)
    e.inputs["Strength"].default_value = 1.0
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(e.outputs["Emission"], out.inputs["Surface"])
    return mat
