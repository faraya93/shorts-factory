"""IDENTITY ROUND 2 (look/palette ONLY; choreography is tape_03 verbatim). Looks A (control) | B2 | D | E, hero=tape|thermos.
Original look test header: LOOK TEST for huincha-de-medir scene 3 (standout): the SAME moment (same blade/kink maths as tape_03) in three treatments, args look=A|B|C.
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
HERO = args.get("hero", "tape")
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

if "thr" in args:
    stage.scene.cycles.adaptive_threshold = float(args["thr"])
if "bounces" in args:
    stage.scene.cycles.max_bounces = int(args["bounces"])

# ---------------------------------------------------------------- per-look stage (lighting / palette only)
world = stage.scene.world.node_tree
cam_bg = next(n for n in world.nodes if n.type == "BACKGROUND" and n.inputs["Color"].links == ())    # the camera-ray background
env_bg = next(n for n in world.nodes if n.type == "BACKGROUND" and n is not cam_bg)
key, rim, fill = stage.key, stage.rim, stage.fill
glare = next(n for n in stage.scene.compositing_node_group.nodes if n.bl_idname == "CompositorNodeGlare")
halo_emit = next(n for n in stage.halo.data.materials[0].node_tree.nodes if n.bl_idname == "ShaderNodeEmission")


def seamless(backdrop_hex, floor_hex):
    """Studio seamless: world colour is the backdrop; the floor is a Cycles shadow catcher, so only the soft shadows show over it."""
    cam_bg.inputs["Color"].default_value = c.linear(backdrop_hex)
    stage.halo.hide_render = True
    glare.inputs["Threshold"].default_value = 4.0
    bpy.ops.mesh.primitive_plane_add(size=600.0, location=(0, 0, tr.MOUTH_Z - 0.45 - 1.2))
    fl = bpy.context.object
    fl.name = "floor"
    fl.data.materials.append(tr.plain("floor", floor_hex, rough=0.85))
    fl.is_shadow_catcher = True


if LOOK == "A":
    cam_bg.inputs["Color"].default_value = c.linear("#120F10")
    env_bg.inputs["Strength"].default_value = 0.55
    key.data.energy, key.data.size = 11000.0, 7.0
    rim.data.energy, fill.data.energy = 3200.0, 1800.0
    m.table = tr.plain("table", "#2B282D", rough=0.5)
elif LOOK == "B2":           # warm studio, deeper tone, cheaper light (smaller key, lower ambient)
    seamless("#D5C0A2", "#C9B393")
    env_bg.inputs["Strength"].default_value = 0.8
    key.data.energy, key.data.size = 2600.0, 9.0
    key.location = Vector((-6.0, -14.0, 22.0))
    rim.data.energy, rim.data.color = 1000.0, (1.0, 0.95, 0.88)
    fill.data.energy = 800.0
    m.table = tr.plain("table", "#C4AE8E", rough=0.6)
elif LOOK == "D":            # celeste studio
    seamless("#B9DCF0", "#A9CDE4")
    env_bg.inputs["Strength"].default_value = 0.85
    key.data.energy, key.data.size = 2600.0, 9.0
    key.location = Vector((-6.0, -14.0, 22.0))
    rim.data.energy, rim.data.color = 1000.0, (0.95, 0.98, 1.0)
    fill.data.energy = 800.0
    m.table = tr.plain("table", "#E6EEF4", rough=0.6)
else:                        # E: dark teal stage
    cam_bg.inputs["Color"].default_value = c.linear("#0B2A2F")
    env_bg.inputs["Strength"].default_value = 0.55
    halo_emit.inputs["Color"].default_value = c.linear("#2A8F96")
    halo_emit.inputs["Strength"].default_value = 0.55
    key.data.energy, key.data.size = 11000.0, 7.0
    rim.data.energy, rim.data.color = 3200.0, c.linear("#CFF3F0")[:3]
    fill.data.energy = 1800.0
    m.table = tr.plain("table", "#1E3C42", rough=0.5)

# ---------------------------------------------------------------- the scene-3 moment (identical maths to tape_03)
if HERO == "tape":
    A = tr.Tape(m, loc=(0, 0, 0), name="tape")
    tr.table(m)
else:   # versatility hero: a classic red-and-white thermos on the same platform, same stage
    tr.table(m)
    ZT = tr.MOUTH_Z - 0.45
    red = tr.pbr("red_p", "Plastic010", "Plastic010", "#CC2229", rough_mul=0.9, scale=0.4, normal=0.3, tint_mix=0.9, coat=0.5)
    white = tr.pbr("white_p", "Plastic010", "Plastic010", "#F2F1EE", rough_mul=0.9, scale=0.4, normal=0.2, tint_mix=0.9, coat=0.3)
    blk = tr.plain("blk_p", "#151517", rough=0.5)
    tr.cyl("th_body", 2.3, 8.0, (0, 0, ZT + 4.0), red, axis="Z", verts=64, bevel=0.35)
    tr.cyl("th_band", 2.36, 0.5, (0, 0, ZT + 8.2), blk, axis="Z", verts=64, bevel=0.08)
    tr.cyl("th_cup", 2.2, 2.6, (0, 0, ZT + 9.6), white, axis="Z", verts=64, bevel=0.4)
    tr.cyl("th_base", 2.4, 0.5, (0, 0, ZT + 0.25), white, axis="Z", verts=64, bevel=0.1)
DMAX = 20.0
SK = A.S(11.5) if HERO == "tape" else 0.0


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

    if HERO == "tape":
        A.place_blade(d, theta=th, cs=cs)
        A.blade.stress(5.0 * flat, SK, 0.9)
    if HERO == "thermos":
        u = c.smooth(0, T, t)
        tr.look(stage, (0, 0, 2.4), 30.0 - 2 * u, 14.0, -30 + 8 * u)
        return
    az0, el0, r0 = float(args.get("az", -36)), float(args.get("el", 12)), float(args.get("r", 34))
    tx, tz = float(args.get("tx", 7.0)), float(args.get("tz", -1.0))
    u = c.smooth(0, T, t)
    tr.look(stage, (tx, 0, tz), r0 - 3 * u, el0 - 1.5 * u, az0 + 5 * u)


stage.run(update, args, SLOT, f"look-{LOOK}")
