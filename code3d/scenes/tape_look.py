"""LOOK TEST for huincha-de-medir scene 3 (standout): the SAME moment (same blade/kink maths as tape_03) in three treatments, args look=A|B|C.
Real colours in all three: yellow painted housing, black rubber boot, bright steel blade with bold black markings.
A = near-black stage, close and big, strong key. B = warm off-white studio seamless with a soft shadow. C = saturated amber-to-deep gradient."""
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(299)
LOOK = args.get("look", "A")
T = SLOT / c.FPS
pal = stage.pal

# ---------------------------------------------------------------- real colours (shared by A, B, C)
YELLOW, BOOT = "#F2BD12", "#161618"


def bold_ticks():
    """Same tick tile as the rig but taller/wider so the markings read at phone size."""
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
m.shell = tr.pbr("shell_y", "Plastic010", "Plastic010", YELLOW, rough_mul=1.15, scale=0.4, normal=0.45, tint_mix=0.85, coat=0.25)   # painted, slightly worn
m.rubber = tr.pbr("rubber_k", "Rubber004", "Rubber004", BOOT, rough_mul=1.1, scale=0.5, normal=0.5, tint_mix=0.9)
m.dark_metal = tr.pbr("dark_metal2", "Metal038", "Metal038", "#8E8C92", metallic=1.0, rough_mul=1.0, scale=0.5, normal=0.3, tint_mix=0.5)

# ---------------------------------------------------------------- per-look stage
world = stage.scene.world.node_tree
cam_bg = next(n for n in world.nodes if n.type == "BACKGROUND" and n.inputs["Color"].links == ())    # the camera-ray background
env_bg = next(n for n in world.nodes if n.type == "BACKGROUND" and n is not cam_bg)
key, rim, fill = stage.key, stage.rim, stage.fill
glare = next(n for n in stage.scene.compositing_node_group.nodes if n.bl_idname == "CompositorNodeGlare")

if LOOK == "A":
    cam_bg.inputs["Color"].default_value = c.linear("#120F10")
    env_bg.inputs["Strength"].default_value = 0.95
    key.data.energy, key.data.size = 11000.0, 7.0
    rim.data.energy, fill.data.energy = 3200.0, 1800.0
    m.table = tr.plain("table", "#2B282D", rough=0.5)
elif LOOK == "B":
    cam_bg.inputs["Color"].default_value = c.linear("#E6DAC8")
    env_bg.inputs["Strength"].default_value = 0.9
    stage.halo.hide_render = True
    key.data.energy, key.data.size = 3200.0, 16.0
    key.location = Vector((-6.0, -14.0, 22.0))
    rim.data.energy, rim.data.color = 1200.0, (1.0, 0.95, 0.88)
    fill.data.energy = 900.0
    glare.inputs["Threshold"].default_value = 4.0
    m.table = tr.plain("table", "#D9CBB8", rough=0.6)
    bpy.ops.mesh.primitive_plane_add(size=600.0, location=(0, 0, tr.MOUTH_Z - 0.45 - 1.2))
    floor = bpy.context.object
    floor.name = "floor"
    floor.data.materials.append(tr.plain("floor", "#D2C3AF", rough=0.85))
    floor.is_shadow_catcher = True                     # Cycles: the floor shows only the shadows, over the seamless backdrop colour
else:  # C: saturated amber-to-deep gradient backdrop plane (emissive), real colours in front
    cam_bg.inputs["Color"].default_value = c.linear("#3A1208")
    env_bg.inputs["Strength"].default_value = 0.6
    stage.halo.hide_render = True
    key.data.energy, key.data.size = 8200.0, 8.0
    rim.data.energy, fill.data.energy = 900.0, 1500.0
    m.table = tr.plain("table", "#2A1A14", rough=0.5)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(8.0, 16.0, 0.0), rotation=(math.radians(90), 0, 0))
    bg = bpy.context.object
    bg.scale = (160.0, 160.0, 1.0)
    bg.visible_shadow = False
    mat = bpy.data.materials.new("amber_stage")
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.30, tuple(c.linear("#4A1408")[:3]) + (1.0,)
    ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.72, tuple(c.linear("#FF9A1C")[:3]) + (1.0,)
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = 1.0
    nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Y"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], em.inputs["Color"])
    nt.links.new(em.outputs["Emission"], out.inputs["Surface"])
    bg.data.materials.append(mat)

# ---------------------------------------------------------------- the scene-3 moment (identical maths to tape_03)
A = tr.Tape(m, loc=(0, 0, 0), name="tape")
tr.table(m)
DMAX, SK = 20.0, A.S(11.5)


def update(scene_):
    t = scene_.frame_current / c.FPS
    d = DMAX * tr.ease_out((t - 0.3) / 3.3)
    flat = c.smooth(5.0, 6.9, t)
    kink = 1.25 * c.smooth(7.0, 7.9, t) + 0.65 * c.smooth(7.9, 9.2, t)
    sag = 0.55 * c.smooth(7.8, 9.6, t)

    def th(s):
        k = 0.5 * (1 + math.tanh((s - SK) / 0.25))
        g = min(1.0, max(0.0, (s - 3.0) / 14.0))
        return kink * k + sag * g * g * (3 - 2 * g) + 0.003 * max(0.0, s - A.inner)

    def cs(s):
        return 1 - 0.96 * flat * math.exp(-((s - SK) / 0.9) ** 2)

    A.place_blade(d, theta=th, cs=cs)
    A.blade.stress(5.0 * flat, SK, 0.9)
    az0, el0, r0 = float(args.get("az", -36)), float(args.get("el", 12)), float(args.get("r", 34))
    tx, tz = float(args.get("tx", 7.0)), float(args.get("tz", -1.0))
    u = c.smooth(0, T, t)
    tr.look(stage, (tx, 0, tz), r0 - 3 * u, el0 - 1.5 * u, az0 + 5 * u)


stage.run(update, args, SLOT, f"look-{LOOK}")
