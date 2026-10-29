"""Stage looks for the tape rig (design system, owner 2026-10-27): lighting + palette ONLY, never choreography.
begin(look=...) calls apply() right after the Stage is built and BEFORE the scene creates its objects, so the replaced materials are used.
Looks: A (near-black, real colours), E (dark teal), CEL (celeste studio: the proposed light stage), D0 (round-2 pale celeste)."""
import math

import bpy
from mathutils import Vector

import common as c
import tape_rig as tr

YELLOW, BOOT = "#F2BD12", "#161618"
EMBER, ERR_LIGHT = "#E8590C", "#C92A2A"          # accent / error on a light stage (gold has 1.1:1 on celeste, see docs/design-system.md)
CEL_TOP, CEL_BOTTOM = "#8FD6F2", "#62B4DC"        # celeste seamless: lighter behind the caption band, deeper low


def real_colours(stage, m, accent_hex=None, error_hex=None):
    """Real hero colours: yellow painted housing, black rubber, bright steel blade with bold markings; optional accent/error swap."""
    pal = dict(stage.pal)
    if accent_hex:
        pal["accent gold"] = accent_hex
        pal["accent amber"] = accent_hex
    if error_hex:
        pal["error red"] = error_hex

    def bold_ticks():
        import numpy as np
        W, H = 4096, 64
        a = np.zeros((H, W, 4), dtype=np.float32)
        a[..., 3] = 1.0
        px_per = W / tr.TILE
        for k in range(int(tr.TILE * 10)):
            x = int(round(k * 0.1 * px_per))
            h, w = (60, 16) if k % 10 == 0 else (44, 12) if k % 5 == 0 else (26, 8)
            a[H - h:, max(0, x - w // 2): x + (w + 1) // 2, 0] = 1.0
        img = bpy.data.images.new("blade_ticks_bold", W, H, alpha=True, float_buffer=False)
        img.pixels.foreach_set(a.ravel())
        img.colorspace_settings.name = "Non-Color"
        img.pack()
        return img

    tr.ticks_image = bold_ticks
    m.blade = tr.blade_material(pal, "#E9E9EC")
    m.shell = tr.pbr("shell_y", "Plastic010", "Plastic010", YELLOW, rough_mul=1.15, scale=0.4, normal=0.45, tint_mix=0.85, coat=0.25)
    m.rubber = tr.pbr("rubber_k", "Rubber004", "Rubber004", BOOT, rough_mul=1.1, scale=0.5, normal=0.5, tint_mix=0.9)
    m.dark_metal = tr.pbr("dark_metal2", "Metal038", "Metal038", "#8E8C92", metallic=1.0, rough_mul=1.0, scale=0.5, normal=0.3, tint_mix=0.5)
    m.gold = tr.gold_emit("gold", pal["accent gold"], 9.0)
    m.gold_dim = tr.gold_emit("gold_dim", pal["accent amber"], 1.6)
    m.red = tr.gold_emit("red", pal["error red"], 6.0)
    m.spring = tr.plain("spring", pal["accent amber"], rough=0.3, metallic=1.0)
    sp = m.spring.node_tree.nodes["Principled BSDF"]
    sp.inputs["Emission Color"].default_value = c.linear(pal["accent gold"])
    sp.inputs["Emission Strength"].default_value = 0.4
    return pal


def _world(stage):
    nt = stage.scene.world.node_tree
    cam = next(n for n in nt.nodes if n.type == "BACKGROUND" and n.inputs["Color"].links == ())
    env = next(n for n in nt.nodes if n.type == "BACKGROUND" and n is not cam)
    return nt, cam, env


def _gradient_backdrop(nt, cam, top_hex, bottom_hex):
    """Screen-space vertical gradient (Window coordinates) as the camera-ray colour: lighter at the top (caption band)."""
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.05, tuple(c.linear(bottom_hex)[:3]) + (1.0,)
    ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.95, tuple(c.linear(top_hex)[:3]) + (1.0,)
    nt.links.new(tc.outputs["Window"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Y"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], cam.inputs["Color"])


def _seamless_floor(floor_hex, z=None):
    bpy.ops.mesh.primitive_plane_add(size=600.0, location=(0, 0, tr.MOUTH_Z - 0.45 - 1.2 if z is None else z))
    fl = bpy.context.object
    fl.name = "floor"
    fl.data.materials.append(tr.plain("floor", floor_hex, rough=0.85))
    fl.is_shadow_catcher = True                          # Cycles: only the soft shadows show, over the seamless backdrop


def _directions() -> dict:
    import json
    from pathlib import Path
    d = json.load(open(Path(__file__).resolve().parents[2] / "factory" / "directions.json"))
    return {k: v for k, v in d.items() if not k.startswith("_")}


def apply_direction(stage, m, name: str, args: dict | None = None) -> None:
    """Identity direction (factory/directions.json): screen-space gradient stage + shadow-catcher floor + plinth + accent/error swap.
    Same studio lighting as CEL (cheap, tuned); only palette differs, so per-direction cost differences are the palette's own."""
    d = _directions()[name]
    nt, cam, env = _world(stage)
    key, rim, fill = stage.key, stage.rim, stage.fill
    glare = next(n for n in stage.scene.compositing_node_group.nodes if n.bl_idname == "CompositorNodeGlare")
    fz = float(args["floor_z"]) if args and "floor_z" in args else None
    real_colours(stage, m, d["accent"], d["error"])
    stage.halo.hide_render = True
    glare.inputs["Threshold"].default_value = 4.0
    _gradient_backdrop(nt, cam, d["top"], d["bottom"])
    _seamless_floor(d["bottom"], fz)
    m.table = tr.plain("table", d["plinth"], rough=0.55)
    env.inputs["Strength"].default_value = 0.85
    key.data.energy, key.data.size = 2600.0, 9.0
    key.location = Vector((-6.0, -14.0, 22.0))
    rim.data.energy, rim.data.color = 1000.0, (0.97, 0.98, 1.0)
    fill.data.energy = 800.0
    if args:
        if "thr" in args:
            stage.scene.cycles.adaptive_threshold = float(args["thr"])
        if "bounces" in args:
            stage.scene.cycles.max_bounces = int(args["bounces"])


def tuned_profile(stage) -> None:
    """The tuned Cycles profile of docs/render-bench.md (cyc_B): GPU denoise, looser adaptive threshold, min samples 24, no transmission/volume,
    bounce limits 3/4/8, persistent data. Samples stay the ceiling given by `samples=`."""
    cy, sc = stage.scene.cycles, stage.scene
    cy.use_adaptive_sampling = True
    cy.adaptive_threshold = 0.04
    cy.adaptive_min_samples = 24
    cy.denoising_use_gpu = True
    cy.transmission_bounces = 0
    cy.volume_bounces = 0
    cy.diffuse_bounces, cy.glossy_bounces, cy.max_bounces = 3, 4, 8
    sc.render.use_persistent_data = True


def apply(stage, m, look: str, args: dict | None = None) -> None:
    out = apply_direction(stage, m, look, args) if look in _directions() else _apply_legacy(stage, m, look, args)
    if args and args.get("profile") == "tuned":
        tuned_profile(stage)
    return out


def _apply_legacy(stage, m, look: str, args: dict | None = None) -> None:
    nt, cam, env = _world(stage)
    key, rim, fill = stage.key, stage.rim, stage.fill
    glare = next(n for n in stage.scene.compositing_node_group.nodes if n.bl_idname == "CompositorNodeGlare")
    halo_emit = next(n for n in stage.halo.data.materials[0].node_tree.nodes if n.bl_idname == "ShaderNodeEmission")
    fz = float(args["floor_z"]) if args and "floor_z" in args else None   # scenes with objects below the table (1, 2) pass a lower floor
    light = look in ("CEL", "D0")
    real_colours(stage, m, EMBER if light else None, ERR_LIGHT if light else None)
    if look == "A":
        cam.inputs["Color"].default_value = c.linear("#120F10")
        env.inputs["Strength"].default_value = 0.55
        key.data.energy, key.data.size = 11000.0, 7.0
        rim.data.energy, fill.data.energy = 3200.0, 1800.0
        m.table = tr.plain("table", "#2B282D", rough=0.5)
    elif look == "E":
        cam.inputs["Color"].default_value = c.linear("#0B2A2F")
        env.inputs["Strength"].default_value = 0.55
        halo_emit.inputs["Color"].default_value = c.linear("#2A8F96")
        halo_emit.inputs["Strength"].default_value = 0.55
        key.data.energy, key.data.size = 11000.0, 7.0
        rim.data.energy, rim.data.color = 3200.0, c.linear("#CFF3F0")[:3]
        fill.data.energy = 1800.0
        m.table = tr.plain("table", "#1E3C42", rough=0.5)
    else:                                             # CEL / D0: celeste studio, tuned cheap light
        stage.halo.hide_render = True
        glare.inputs["Threshold"].default_value = 4.0
        if look == "CEL":
            _gradient_backdrop(nt, cam, CEL_TOP, CEL_BOTTOM)
            _seamless_floor("#62B4DC", fz)
            m.table = tr.plain("table", "#2B4C70", rough=0.55)          # deep-navy plinth: separates white/silver/yellow bases
        else:
            cam.inputs["Color"].default_value = c.linear("#B9DCF0")
            _seamless_floor("#A9CDE4", fz)
            m.table = tr.plain("table", "#E6EEF4", rough=0.6)
        env.inputs["Strength"].default_value = 0.85
        key.data.energy, key.data.size = 2600.0, 9.0
        key.location = Vector((-6.0, -14.0, 22.0))
        rim.data.energy, rim.data.color = 1000.0, (0.95, 0.98, 1.0)
        fill.data.energy = 800.0
    if args:
        if "thr" in args:
            stage.scene.cycles.adaptive_threshold = float(args["thr"])
        if "bounces" in args:
            stage.scene.cycles.max_bounces = int(args["bounces"])
