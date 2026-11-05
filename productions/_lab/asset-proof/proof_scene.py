"""Asset-system proof stills (lab only). Headless:
  caffeinate -dimsu blender -b --factory-startup --python productions/_lab/asset-proof/proof_scene.py -- job=hand shot=1 out=<png> [test=1]
job=hand    006 key scene: a library hand (assets/library/human-hand, via asset_library.load_hero) dips into water.
            Water route: PHYSICALLY BASED WATER MATERIAL (Principled, IOR 1.333, full transmission) in a glass tray, rippled surface by displacement. NOT Mantaflow.
job=popcorn 011: library popcorn box (assets/library/popcorn) with its separate pieces erupting.
Identity: Coral, read from build/identity-export.json (factory/identity.py). Render profile: render.profiles.tuned, with ONE recorded deviation for the hand
job: transmission_bounces 0 -> 8 (refraction cannot render with 0; see docs gap in productions/_lab/asset-proof/report.md)."""
import math
import random
import sys
from pathlib import Path

import bpy
import mathutils
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(ROOT / "code3d" / "lib"))
import asset_library as al  # noqa: E402
import common as c  # noqa: E402
import pipeline_config as cfg  # noqa: E402

args = c.parse_args()
JOB, SHOT, OUT = args["job"], int(args.get("shot", 1)), args["out"]
TEST = args.get("test") == "1"
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
P = cfg.preset("coral")
prof_name, prof = cfg.render_profile({"profile": "tuned"})
lin = c.linear


def mat_plain(name, hexc, rough=0.5, metal=0.0):
    return c.principled(name, hexc, rough, metal)


# ---------- render profile (tuned Cycles) ----------
scene.render.engine = "CYCLES"
cy = scene.cycles
cy.samples = prof["samples_ceiling"]; cy.adaptive_threshold = prof["adaptive_threshold"]; cy.adaptive_min_samples = prof["min_samples"]
cy.use_adaptive_sampling = True; cy.use_denoising = True
try:
    cy.denoiser = "OPENIMAGEDENOISE"; cy.denoising_use_gpu = prof["denoise_gpu"]
except Exception:
    pass
cy.diffuse_bounces = prof["diffuse_bounces"]; cy.glossy_bounces = prof["glossy_bounces"]; cy.max_bounces = prof["max_bounces"]
cy.volume_bounces = prof["volume_bounces"]
cy.transmission_bounces = int(args["tb"]) if "tb" in args else (8 if JOB == "hand" else prof["transmission_bounces"])     # recorded deviation (hand job only)
scene.render.use_persistent_data = prof["persistent_data"]
try:
    cy.use_fast_gi = prof["fast_gi"]
except Exception:
    pass
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "METAL"; prefs.get_devices()
    for d in prefs.devices:
        d.use = True
    cy.device = "GPU"
except Exception as e:
    print("GPU not set:", e)
scene.render.resolution_x, scene.render.resolution_y = (540, 960) if TEST else (1080, 1920)
if TEST:
    cy.samples = 32
scene.view_settings.view_transform = "Standard"; scene.view_settings.look = "None"
scene.render.image_settings.file_format = "PNG"

# ---------- coral stage: gradient backdrop (emission, exact identity colours) + ink plinth ----------
top, bot = P["top"], P["bottom"]
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 1.2, 0.5), rotation=(math.pi / 2, 0, 0))
bd = bpy.context.object; bd.scale = (6, 6, 1); bd.name = "stage_backdrop"
bm = bpy.data.materials.new("stage"); bm.use_nodes = True; nt = bm.node_tree; nt.nodes.clear()
tc = nt.nodes.new("ShaderNodeTexCoord"); gr = nt.nodes.new("ShaderNodeTexGradient"); cr = nt.nodes.new("ShaderNodeValToRGB")
cr.color_ramp.elements[0].color = lin(bot); cr.color_ramp.elements[1].color = lin(top)
em = nt.nodes.new("ShaderNodeEmission"); out = nt.nodes.new("ShaderNodeOutputMaterial")
nt.links.new(tc.outputs["UV"], gr.inputs["Vector"]); gr.gradient_type = "LINEAR"
mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Rotation"].default_value = (0, 0, math.radians(90)); mp.inputs["Location"].default_value = (0, 1, 0)
nt.links.new(tc.outputs["UV"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], gr.inputs["Vector"])
nt.links.new(gr.outputs["Fac"], cr.inputs["Fac"]); nt.links.new(cr.outputs["Color"], em.inputs["Color"]); nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
bd.data.materials.append(bm)
# world: HDRI lights, camera sees black-free coral mid
c.studio_world(scene, bot, ROOT / "code3d/assets/hdri/studio_small_08_2k.hdr", strength=0.55)
bpy.ops.mesh.primitive_cylinder_add(radius=0.55, depth=0.04, location=(0, 0, -0.02), vertices=96)
pl = bpy.context.object; pl.name = "plinth"; pl.data.materials.append(mat_plain("plinth_ink", P["plinth"], 0.45))
bpy.ops.object.shade_smooth()

cam = c.make_camera(scene, 55)
c.add_light(scene, "AREA", (-0.7, -0.5, 1.0), 55, 0.8, Vector((0, 0, 0.1)))
c.add_light(scene, "AREA", (-0.6, 0.5, 0.7), 35, 0.6, Vector((0, 0, 0.1)))     # rim from behind


def root_empty(name, loc=(0, 0, 0), rot=(0, 0, 0)):
    e = bpy.data.objects.new(name, None); scene.collection.objects.link(e); e.location = loc; e.rotation_euler = rot
    return e


def aim(loc, target, lens=55):
    cam.location = Vector(loc); cam.data.lens = lens
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()


# ======================= HAND + WATER =======================
if JOB == "hand":
    TRAY_W, TRAY_D, TRAY_H, WALL, LEVEL = 0.34, 0.24, 0.13, 0.006, 0.10
    glass = bpy.data.materials.new("glass"); glass.use_nodes = True
    b = next(n for n in glass.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = lin("#EAF6F3"); b.inputs["Roughness"].default_value = 0.02; b.inputs["IOR"].default_value = 1.45
    b.inputs["Transmission Weight"].default_value = 1.0
    water = bpy.data.materials.new("water_pbr"); water.use_nodes = True
    b = next(n for n in water.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = lin("#DDF3F2"); b.inputs["Roughness"].default_value = 0.0; b.inputs["IOR"].default_value = 1.333
    b.inputs["Transmission Weight"].default_value = 1.0

    def box(name, sx, sy, sz, loc, m):
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o = bpy.context.object; o.name = name; o.scale = (sx, sy, sz)
        bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m); return o
    box("tray_floor", TRAY_W, TRAY_D, WALL, (0, 0, WALL / 2), glass)
    box("tray_wall_l", WALL, TRAY_D, TRAY_H, (-TRAY_W / 2 + WALL / 2, 0, TRAY_H / 2), glass)
    box("tray_wall_r", WALL, TRAY_D, TRAY_H, (TRAY_W / 2 - WALL / 2, 0, TRAY_H / 2), glass)
    box("tray_wall_f", TRAY_W, WALL, TRAY_H, (0, -TRAY_D / 2 + WALL / 2, TRAY_H / 2), glass)
    box("tray_wall_b", TRAY_W, WALL, TRAY_H, (0, TRAY_D / 2 - WALL / 2, TRAY_H / 2), glass)
    # water body: subdivided box, ripples displace the top vertices only
    iw, idp = TRAY_W - 2 * WALL - 0.001, TRAY_D - 2 * WALL - 0.001
    wb = box("water", iw, idp, LEVEL - WALL - 0.0005, (0, 0, WALL + 0.0005 + (LEVEL - WALL - 0.0005) / 2), water)
    import bmesh
    bmq = bmesh.new(); bmq.from_mesh(wb.data)
    bmesh.ops.subdivide_edges(bmq, edges=bmq.edges[:], cuts=90, use_grid_fill=True)
    bmq.to_mesh(wb.data); bmq.free()
    vg = wb.vertex_groups.new(name="top")
    zt = LEVEL - 0.0005 - 0.0001
    vg.add([v.index for v in wb.data.vertices if v.co.z > zt], 1.0, "REPLACE")
    bpy.ops.object.select_all(action="DESELECT"); wb.select_set(True); bpy.context.view_layer.objects.active = wb
    bpy.ops.object.shade_smooth()
    hand_col = al.load_hero("human-hand")
    objs = list(hand_col.objects)
    tilt = math.radians(float(args.get("tilt", 18)))
    hroot = root_empty("hand_root", (0.0, -0.02, float(args.get("dip", 0.065))), (0, tilt, math.radians(float(args.get("yaw", 0)))))
    for o in objs:
        o.parent = hroot
    skin = objs[0].data.materials[0]
    skin_n = next(n for n in skin.node_tree.nodes if n.name == "wrinkle_amount")
    skin_n.outputs[0].default_value = float(args.get("wrinkle", 0))
    if args.get("nomask") == "1":
        mul = next(n for n in skin.node_tree.nodes if n.type == "MATH"); mul.inputs[0].default_value = 1.0
        for l in list(skin.node_tree.links):
            if l.to_node == mul and l.to_socket == mul.inputs[0]:
                skin.node_tree.links.remove(l)
    if "mrmin" in args:
        mr = next(n for n in skin.node_tree.nodes if n.type == "MAP_RANGE")
        mr.inputs["From Min"].default_value = float(args["mrmin"]); mr.inputs["From Max"].default_value = float(args["mrmax"])
    skin_b = next(n for n in skin.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    skin_b.inputs["Base Color"].default_value = lin(args.get("skin", "#B5754F"))        # stylised retint, not a scan colour
    # ripple source = empty at the fingertips' waterline
    rip = root_empty("ripple_src", (0.0, -0.02, LEVEL))
    tex = bpy.data.textures.new("ripples", "WOOD"); tex.wood_type = "RINGS"; tex.noise_basis = "BLENDER_ORIGINAL"; tex.noise_type = "SOFT_NOISE"; tex.turbulence = 0.15
    dm = wb.modifiers.new("ripples", "DISPLACE"); dm.texture = tex; dm.texture_coords = "OBJECT"; dm.texture_coords_object = rip
    dm.vertex_group = "top"; dm.strength = 0.0012; dm.mid_level = 0.5
    tex.intensity = 1.0; tex.contrast = 1.4
    rip.scale = (0.5, 0.5, 0.5)   # wood rings period = 1 texture unit / empty scale: ~1 cm ripple spacing
    shots = {
        1: ((0.42, -0.62, 0.34), (0, -0.02, 0.15), 52),      # establishing, 3/4, dry smooth fingers dipping
        2: ((0.03, -0.30, 0.09), (0, -0.02, 0.085), 65),      # tray-side, fingertips through the glass and the surface
        3: ((0.05, -0.30, 0.19), (0.0, -0.02, 0.175), 110),      # close-up of the lifted hand: WRINKLED fingertips (run with dip=0.14 wrinkle=1)
        4: ((0.0, -0.8, 0.52), (0, -0.02, 0.1), 52),          # top-down-ish, hand and tray from above
    }
    loc, tgt, lens = shots[SHOT]
    aim(loc, tgt, lens)

# ======================= POPCORN =======================
else:
    col = al.load_hero("popcorn")
    box_o = col.objects["box"]
    pieces = [o for o in col.objects if o.name.startswith("popcorn_")]
    cream = c.principled("popcorn_cream", args.get("cream", "#F7E7C2"), 0.75)
    for o in pieces:
        o.data.materials.clear(); o.data.materials.append(cream)
    # box stripes retinted to ink / cream (stage red would merge with coral)
    m = box_o.data.materials[0]; nt = m.node_tree
    bs = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"); tex = next(n for n in nt.nodes if n.type == "TEX_IMAGE")
    ramp = nt.nodes.new("ShaderNodeValToRGB"); rgb2bw = nt.nodes.new("ShaderNodeRGBToBW")
    ramp.color_ramp.elements[0].position = 0.25; ramp.color_ramp.elements[0].color = lin(P["plinth"])
    ramp.color_ramp.elements[1].position = 0.45; ramp.color_ramp.elements[1].color = lin("#FFF3E0")
    nt.links.new(tex.outputs["Color"], rgb2bw.inputs["Color"]); nt.links.new(rgb2bw.outputs["Val"], ramp.inputs["Fac"]); nt.links.new(ramp.outputs["Color"], bs.inputs["Base Color"])
    random.seed(11)
    erupt = int(args.get("erupt", 0))
    if erupt:
        chosen = random.sample([o for o in pieces if o.location.z > 0.17], erupt)
        for o in chosen:
            o.location += Vector((random.uniform(-0.09, 0.09), random.uniform(-0.09, 0.09), random.uniform(0.06, 0.28)))
            o.rotation_mode = "XYZ"; o.rotation_euler = (random.uniform(0, 6.28), random.uniform(0, 6.28), random.uniform(0, 6.28))
    shots = {
        1: ((0.0, -0.62, 0.22), (0, 0, 0.12), 50),
        2: ((0.0, -0.66, 0.2), (0, 0, 0.2), 50),
        3: ((0.12, -0.3, 0.42), (0, 0, 0.17), 80),
    }
    loc, tgt, lens = shots[SHOT]
    aim(loc, tgt, lens)

scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
print("RENDERED", OUT)
