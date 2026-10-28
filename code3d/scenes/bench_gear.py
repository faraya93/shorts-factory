"""RENDER TEST BENCH (owner 2026-10-28; no production defaults are changed). Test scene = engranajes-papel scene 1 (glossy coated gears + the cream
gradient + the contact shadow), frames chosen by the runner. variant=cyc_A (the current production profile) | cyc_B (tuned) | cyc_C (tuned + Fast GI)
| ee_A | ee_B (EEVEE; B adds baked stage probes) | ref (1024 spp reference). `print_cfg=1` prints the effective configuration and exits."""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import gear_rig as gr  # noqa: E402

args = c.parse_args()
VAR = args.get("variant", "cyc_A")
mode = "draft-full" if VAR.startswith("ee_") else "final"
sys.argv = [a for a in sys.argv]                      # begin() reads production/mode/look/samples from the same arg list
args_extra = {"mode": mode}
a_, production, stage, m, SLOT = tr.begin(250, floor_z=-7.6)   # reads mode= from argv; Stage mode is fixed there
sc = stage.scene
cy = sc.cycles

mats = gr.Train._materials(m)
Y = 0.6
tp = gr.Gear("t_pin", 20, (-1.6, 4.0), Y, mats["input"], marker=mats["marker"])
tq = gr.Gear("t_par", 20, (1.6, 4.0), Y, mats["pinion"], marker=mats["marker"])
bp = gr.Gear("b_pin", gr.NP, (-2.0, -2.9), Y, mats["input"], marker=mats["marker"])
bb = gr.Gear("b_big", gr.NB, (2.0, -2.9), Y, mats["big"], marker=mats["marker"], holes=mats["ink"])
shelf = tr.rbox("shelf", (13.0, 1.4, 0.7), (0.0, Y + 0.5, -6.4), mats["ink"], bevel=0.25)
T = SLOT / c.FPS


def cfg_dump() -> str:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    devs = [(d.name, d.type, d.use) for d in prefs.devices]
    lines = [f"engine={sc.render.engine} device={cy.device} compute_device_type={prefs.compute_device_type} devices={devs}",
             f"samples(ceiling)={cy.samples} adaptive={cy.use_adaptive_sampling} threshold={cy.adaptive_threshold} adaptive_min_samples={cy.adaptive_min_samples}",
             f"denoise={cy.use_denoising} denoiser={cy.denoiser} denoising_use_gpu={cy.denoising_use_gpu} quality={cy.denoising_quality} prefilter={cy.denoising_prefilter} passes={cy.denoising_input_passes}",
             f"bounces max={cy.max_bounces} diffuse={cy.diffuse_bounces} glossy={cy.glossy_bounces} transmission={cy.transmission_bounces} volume={cy.volume_bounces} transparent={cy.transparent_max_bounces}",
             f"caustics refl={cy.caustics_reflective} refr={cy.caustics_refractive} fast_gi={cy.use_fast_gi}/{cy.fast_gi_method} ao_bounces_render={cy.ao_bounces_render} light_tree={cy.use_light_tree}",
             f"persistent_data={sc.render.use_persistent_data} metalrt={prefs.metalrt} oidn_gpu_available={prefs.has_oidn_gpu_devices()} tiles auto={cy.use_auto_tile}",
             f"resolution={sc.render.resolution_x}x{sc.render.resolution_y} {sc.render.resolution_percentage}% compositor_nodes={(sc.compositing_node_group.nodes.keys() if sc.compositing_node_group else None)}"]
    return "\n".join(lines)


def tune_cycles(v: str):
    if v in ("cyc_B", "cyc_C"):
        cy.samples = 128                         # ceiling
        cy.use_adaptive_sampling = True
        cy.adaptive_threshold = 0.04
        cy.adaptive_min_samples = 24
        cy.denoising_use_gpu = True
        cy.transmission_bounces = 0
        cy.volume_bounces = 0
        cy.caustics_reflective = cy.caustics_refractive = False
        cy.diffuse_bounces, cy.glossy_bounces, cy.max_bounces = 3, 4, 8
        sc.render.use_persistent_data = True
    if v == "cyc_C":
        cy.use_fast_gi = True
        cy.fast_gi_method = "REPLACE"
        cy.ao_bounces_render = 2
    if v == "ref":
        cy.samples = 1024
        cy.adaptive_threshold = 0.001
        cy.max_bounces = 12


def eevee_floor():
    """EEVEE has no shadow catcher: floor = shadow-to-RGB -> alpha, so only the contact shadow shows over the seamless world colour."""
    fl = bpy.data.objects["floor"]
    mat = bpy.data.materials.new("floor_shadow")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    dif = nt.nodes.new("ShaderNodeBsdfDiffuse")
    s2r = nt.nodes.new("ShaderNodeShaderToRGB")
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    inv = nt.nodes.new("ShaderNodeMath")
    inv.operation = "SUBTRACT"
    inv.inputs[0].default_value = 1.0
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = 0.55
    clear = nt.nodes.new("ShaderNodeBsdfTransparent")
    blk = nt.nodes.new("ShaderNodeEmission")
    blk.inputs["Color"].default_value = (0.05, 0.03, 0.02, 1)
    mix = nt.nodes.new("ShaderNodeMixShader")
    dif.inputs["Color"].default_value = (1, 1, 1, 1)
    nt.links.new(dif.outputs["BSDF"], s2r.inputs["Shader"])
    nt.links.new(s2r.outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs["Red"], inv.inputs[1])
    nt.links.new(inv.outputs["Value"], mul.inputs[0])
    nt.links.new(mul.outputs["Value"], mix.inputs["Fac"])
    nt.links.new(clear.outputs["BSDF"], mix.inputs[1])
    nt.links.new(blk.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    mat.surface_render_method = "BLENDED"
    fl.data.materials.clear()
    fl.data.materials.append(mat)
    fl.is_shadow_catcher = False


def tune_eevee(v: str):
    e = sc.eevee
    eevee_floor()
    e.taa_render_samples = 64
    e.use_raytracing = True
    if v == "ee_B":
        e.taa_render_samples = 128
        e.use_fast_gi = True
        # stage probes: one sphere probe at the hero (glossy reflections) + one volume probe over the stage (diffuse GI), baked ONCE
        bpy.ops.object.lightprobe_add(type="SPHERE", location=(0, -4, 0.6))
        sp = bpy.context.object
        sp.scale = (14, 14, 14)
        bpy.ops.object.lightprobe_add(type="VOLUME", location=(0, 0, 0.6))
        vp = bpy.context.object
        vp.scale = (14, 8, 14)
        vp.data.resolution_x, vp.data.resolution_y, vp.data.resolution_z = 8, 4, 8
        try:
            bpy.ops.object.lightprobe_cache_bake(subset="ALL")
            print("PROBES baked")
        except Exception as ex:                                      # noqa: BLE001
            print("PROBE BAKE FAILED:", ex)


def update(scene_):
    t = scene_.frame_current / c.FPS
    th = 2 * math.pi * 0.9 * t
    th2 = 2 * math.pi * 0.6 * t
    tp.set_angle(th2)
    tq.set_angle(math.pi - math.pi / 20 - th2)
    bp.set_angle(th)
    bb.set_angle(math.pi - math.pi / gr.NB - (gr.NP / gr.NB) * th)
    u = c.smooth(0, T, t)
    tr.look(stage, (0.5, 0, 0.5 + 0.6 * u), 30.0 - 5.0 * u, 5.0, -2.0 - 12.0 * u)


if VAR.startswith("ee_"):
    tune_eevee(VAR)
else:
    tune_cycles(VAR)
    abl = args.get("abl", "")                  # ablations on top of cyc_B: which single switch is worth how much
    if abl == "cpu_oidn":
        cy.denoising_use_gpu = False
    elif abl == "no_persist":
        sc.render.use_persistent_data = False
    elif abl == "thr02":
        cy.adaptive_threshold = 0.02
    elif abl == "prod_bounces":
        cy.max_bounces, cy.diffuse_bounces, cy.glossy_bounces, cy.transmission_bounces = 6, 4, 4, 12
    elif abl == "min0":
        cy.adaptive_min_samples = 0
if args.get("print_cfg"):
    print("CFG[" + VAR + "]\n" + (cfg_dump() if not VAR.startswith("ee_") else f"EEVEE taa={sc.eevee.taa_render_samples} raytracing={sc.eevee.use_raytracing}"))
    sys.exit(0)
stage.run(update, args, SLOT, "bench")
