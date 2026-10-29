"""Stage looks for the rigs: lighting + palette ONLY, never choreography. begin(look=...) calls apply() right after the Stage is built and BEFORE the
scene creates its objects, so the replaced materials are used. EVERY identity colour (stage gradient, plinth, board, accent, error, halo, rim) comes from the
channel config snapshot (code3d/lib/pipeline_config.py <- factory/identity.py <- channels/umbrella-es.yaml); `look=<preset name>` picks the preset
(legacy aliases A, E, CEL keep working). Hero colours (below) are properties of the hero objects, not channel identity."""
import math

import bpy
from mathutils import Vector

import common as c
import pipeline_config as cfg
import tape_rig as tr

YELLOW, BOOT = "#F2BD12", "#161618"          # HERO colours of the tape (painted housing, rubber boot); not identity
LEGACY_LOOKS = {"A": "reference-dark", "E": "dark-teal", "CEL": "celeste"}
_ACTIVE: dict | None = None


def current() -> dict | None:
    """The preset applied by apply() in this Blender session (rigs read plinth/board/accent from it)."""
    return _ACTIVE


def real_colours(stage, m, accent_hex=None, error_hex=None):
    """Real hero colours: yellow painted housing, black rubber, bright steel blade with bold markings; optional accent/error swap."""
    pal = dict(stage.pal)
    tr.EMISSION_GAIN = float((_ACTIVE or {}).get("emission_gain", 1.0))      # config: scales every accent/error emissive so the render matches its swatch family
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
    m.gold = tr.gold_emit("gold", pal["accent gold"], 9.0 * tr.EMISSION_GAIN)
    m.gold_dim = tr.gold_emit("gold_dim", pal["accent amber"], 1.6 * tr.EMISSION_GAIN)
    m.red = tr.gold_emit("red", pal["error red"], 6.0 * tr.EMISSION_GAIN)
    m.spring = tr.plain("spring", pal["accent amber"], rough=0.3, metallic=1.0)
    sp = m.spring.node_tree.nodes["Principled BSDF"]
    sp.inputs["Emission Color"].default_value = c.linear(pal["accent gold"])
    sp.inputs["Emission Strength"].default_value = 0.4 * tr.EMISSION_GAIN
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


def _lights(stage, studio: bool, p: dict, env):
    key, rim, fill = stage.key, stage.rim, stage.fill
    if studio:                                         # cheap bright studio: one big soft key, cool rim, soft fill
        env.inputs["Strength"].default_value = 0.85
        key.data.energy, key.data.size = 2600.0, 9.0
        key.location = Vector((-6.0, -14.0, 22.0))
        rim.data.energy, rim.data.color = 1000.0, (0.97, 0.98, 1.0)
        fill.data.energy = 800.0
    else:                                              # dark stage: strong key, rim and halo carry the subject
        env.inputs["Strength"].default_value = 0.55
        key.data.energy, key.data.size = 11000.0, 7.0
        rim.data.energy, fill.data.energy = 3200.0, 1800.0
        if p.get("rim"):
            rim.data.color = c.linear(p["rim"])[:3]


def apply(stage, m, look: str, args: dict | None = None) -> None:
    """Apply an identity preset to the stage: gradient backdrop, shadow-catcher floor, plinth, accent/error, lighting rig."""
    global _ACTIVE
    d = cfg.data(args)
    name = d["active"] if look in ("active", "", None) else LEGACY_LOOKS.get(look, look)
    p = d["presets"][name]
    _ACTIVE = p
    nt, cam, env = _world(stage)
    glare = next(n for n in stage.scene.compositing_node_group.nodes if n.bl_idname == "CompositorNodeGlare")
    fz = float(args["floor_z"]) if args and "floor_z" in args else None
    real_colours(stage, m, p["accent"], p["error"])
    m.table = tr.plain("table", p["plinth"], rough=0.55)
    m.block = tr.pbr("block", "Plastic010", "Plastic010", p["support_panel"], rough_mul=1.0, scale=0.35, normal=0.2, tint_mix=0.4)
    if p["lighting"] == "studio":
        stage.halo.hide_render = True
        glare.inputs["Threshold"].default_value = 4.0
        _gradient_backdrop(nt, cam, p["top"], p["bottom"])
        _seamless_floor(p["bottom"], fz)
    else:
        cam.inputs["Color"].default_value = c.linear(p["top"])
        if p.get("halo"):
            halo_emit = next(n for n in stage.halo.data.materials[0].node_tree.nodes if n.bl_idname == "ShaderNodeEmission")
            halo_emit.inputs["Color"].default_value = c.linear(p["halo"])
            halo_emit.inputs["Strength"].default_value = 0.55
    _lights(stage, p["lighting"] == "studio", p, env)
    if args:                                           # bench overrides on top of the configured render profile
        if "thr" in args:
            stage.scene.cycles.adaptive_threshold = float(args["thr"])
        if "bounces" in args:
            stage.scene.cycles.max_bounces = int(args["bounces"])
