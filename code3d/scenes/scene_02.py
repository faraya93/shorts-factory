"""v4-code3d scene 2 (curved-needle): a curved needle passes through both skin edges, the thread pulls them together.

Run: blender -b --python code3d/scenes/scene_02.py -- production=<dir> mode=draft|final \
     [stills=f1,f2,..] [frames=a-b] [out=<dir>]
Timeline (seconds, slot 12.23 s): needle hovers 0-1.2 | turns through the skin 1.2-6.2 | leaves, thread released 6.2-7.6 |
thread pulled taut and the cut closes 6.6-9.6 | hold to the end. Camera orbits slowly around the cut throughout.
"""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import suture as s  # noqa: E402

args = c.parse_args()
production = Path(args["production"])
mode = args.get("mode", "draft")
SLOT_FRAMES = int(args.get("slot", 367))    # narration slot in frames (367 = 12.2333 s at 30 fps for scene 2)
T = SLOT_FRAMES / c.FPS

# --- geometry (world units; skin surface at z = 0, the cut runs along y) ---
R, CZ, ARC = 1.3, 0.95, 140.0          # needle circle radius, centre height, needle arc length (degrees)
TIP0, TIP1 = -150.0, 105.0             # needle tip angle at the start / when the tail has left the skin
GAP0, GAP1 = 0.35, 0.03                # half-gap before / after pulling
FLOOR_Z = -0.2                         # the cut is shallow: the needle passes BELOW the floor, hidden by the tissue
THETA_OUT = math.degrees(math.asin(-CZ / R))       # where the circle leaves the skin on the right (about -47 deg)
THETA_IN = -180.0 - THETA_OUT                      # where it enters on the left (about -133 deg)
ENTRY_X = R * math.cos(math.radians(THETA_IN))     # negative: left of the cut
EXIT_X = R * math.cos(math.radians(THETA_OUT))     # positive: right of the cut

vi = c.identity(production)
pal = c.palette(vi)
scene = c.reset_scene()
c.setup_render(scene, mode)
c.studio_world(scene, pal["backdrop"], c.ASSETS / "hdri" / "studio_small_08_2k.hdr", strength=1.0)

# --- materials: library first (BlenderKit SSS skin shader tinted to the palette), palette colours elsewhere ---
skin = c.append_material(c.ASSETS / "materials" / "blenderkit-sss-skin-shader.blend", "SSS Skin Shader")
group = next(n for n in skin.node_tree.nodes if n.type == "GROUP")
group.inputs["Diffuse Color"].default_value = c.linear(pal["skin peach"])
group.inputs["unScatter Color"].default_value = c.linear(pal["shaded skin"])
group.inputs["Medium Scatter Color"].default_value = c.linear(pal["tissue red"])
tissue = c.principled("tissue", pal["tissue red"], roughness=0.55, subsurface=0.15)
steel = c.principled("needle", pal["steel grey"], roughness=0.15, metallic=1.0)
thread_mat = c.principled("thread", "#17171B", roughness=0.55)   # black thread (not in the palette; per the scene brief)

# --- objects ---
half_l = s.skin_half(-1, GAP0, 2.4, 6.0, skin, tissue)
half_r = s.skin_half(+1, GAP0, 2.4, 6.0, skin, tissue)
s.wound_floor(GAP0 + 0.01, 6.0, FLOOR_Z, tissue)
needle = s.curved_needle(R, CZ, TIP0, ARC, r_tail=0.085, r_tip=0.012, material=steel)
thread = s.Thread(thread_mat, points=140, thickness=0.028)
cam = c.make_camera(scene, lens=50.0)
c.add_light(scene, "AREA", (-4.5, -5.5, 7.5), energy=500, size=5.0, target=Vector((0, 0, 0)))

# knot where the thread is anchored: rides on the left skin half as the cut closes
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.055, location=(-1.9, 0.0, 0.03))
knot = bpy.context.object
bpy.ops.object.shade_smooth()
knot.data.materials.append(thread_mat)
knot.parent = half_l

NEXT_HOLE_Y = 0.55                     # where the running suture goes next (the free end comes to rest there)


def tail_pos(theta):
    return Vector((R * math.cos(math.radians(theta)), 0.0, CZ + R * math.sin(math.radians(theta))))


def update(scene_):
    t = scene_.frame_current / c.FPS
    rot = c.smooth(1.2, 6.2, t)
    tip = TIP0 + (TIP1 - TIP0) * rot
    tail = tip - ARC
    shift = (GAP0 - GAP1) * c.smooth(6.6, 9.6, t)
    half_l.location.x, half_r.location.x = +shift, -shift
    needle.rotation_euler.y = -math.radians(tip - TIP0)           # +theta turns the needle counter-clockwise (x right, z up)
    needle.location.z = CZ + 9.0 * c.smooth(6.2, 7.6, t)

    a = Vector((-1.9 + shift, 0.0, 0.012))                          # anchor knot on the left skin
    e_l = Vector((ENTRY_X + shift, 0.0, 0.012))
    e_r = Vector((EXIT_X - shift, 0.0, 0.012))
    under = [p for p in s.arc_points(0.0, CZ, R, THETA_IN, THETA_OUT, 4.0)]
    under = [Vector((p.x + (shift if p.x < 0 else -shift), 0, p.z)) for p in under]   # hidden: follows the closing edges
    if t < 6.2:
        if tail < THETA_IN:
            # tail still in the air on the left: thread hangs from the anchor to the tail
            end = tail_pos(tail)
            poly = [a.lerp(end, u / 8) + Vector((0, 0, max(0.012, 0.3 * 4 * (u / 8) * (1 - u / 8)))) for u in range(9)]
        elif tail <= THETA_OUT:
            poly = [a, e_l] + under[: max(1, int((tail - THETA_IN) / 4.0))] + [tail_pos(tail)]
        else:
            poly = [a, e_l] + under + [e_r] + s.arc_points(0.0, CZ, R, THETA_OUT, tail, 4.0)[1:]
    else:
        free0 = tail_pos(TIP1 - ARC)
        k = c.smooth(6.2, 9.0, t)
        target = Vector((ENTRY_X + shift, NEXT_HOLE_Y, 0.012))
        free = free0.lerp(target, k)
        free.z = max(0.012, free.z * (1 - k) + 0.012 * k)
        sag = 0.28 * (1 - k)
        pts = [e_r.lerp(free, u / 10) + Vector((0, 0, sag * 4 * (u / 10) * (1 - u / 10))) for u in range(11)]
        poly = [a, e_l] + under + [e_r] + pts[1:]
    thread.set(poly)

    az = -14.0 + 24.0 * c.smooth(0.0, T, t)
    c.orbit(cam, Vector((0.0, 0.25, 0.45)), 9.5, 50.0, az)


bpy.app.handlers.frame_change_pre.append(update)
out = Path(args.get("out", str(production / "build" / "code3d" / "scene-02")))

if "stills" in args:                                                # iteration: single frames only
    out.mkdir(parents=True, exist_ok=True)
    for f in [int(x) for x in args["stills"].split(",")]:
        scene.frame_set(f)
        scene.render.filepath = str(out / f"still-{f:04d}.png")
        bpy.ops.render.render(write_still=True)
else:
    a, b = (int(x) for x in args.get("frames", f"1-{SLOT_FRAMES}").split("-"))
    c.render_frames(scene, out, a, b)
