"""SPIKE (design proof, not a production): scene 2 re-modelled as CARTOON FROM THE SHAPE UP, same beats and timing as
v4's scene 2 (367-frame slot), rendered through the toon pass.

  limb    one fat egg-shaped capsule (a plain smooth ellipsoid, no shell, no boolean); the wound is DRAWN, not cut: a
          flat red lens with two chubby rounded lips lying on either side (each a clean convex shape that inks cleanly);
          it closes by sliding the lips together and narrowing the lens
  needle  OVERSIZED and chunky, dark steel (palette steel grey, HSV value x0.5), turns about its circle centre
  thread  a thick black cord
  camera  centred, iconic, a gentle orbit

Run: blender -b --python code3d/scenes/spike_cartoon_02.py -- production=<spike dir> mode=draft-full stills=4,140,367 out=<dir>
"""

import colorsys
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import stage as st  # noqa: E402
import suture as s  # noqa: E402
import toon  # noqa: E402

args = c.parse_args()
production = Path(args["production"])
SLOT = int(args.get("slot", 367))
T = SLOT / c.FPS

stage = st.Stage(production, args.get("mode", "draft-full"))
pal = stage.pal


def dark_steel(hex_color: str, value_factor: float = 0.5) -> str:
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, sat, v = colorsys.rgb_to_hsv(r, g, b)
    return "#{:02X}{:02X}{:02X}".format(*(round(255 * x) for x in colorsys.hsv_to_rgb(h, sat, v * value_factor)))


STEEL_DARK = dark_steel(pal["steel grey"])           # derivation rule: palette steel grey, HSV value x0.5
skin_m = toon.make_material("limb", pal["skin peach"])
core_m = toon.make_material("core", pal["tissue red"])
needle_m = toon.make_material("needle_dark", STEEL_DARK)
cord_m = toon.make_material("cord", "#17171B")

# --- the limb: ONE big rounded capsule-like form ---
A, HALF_LEN = 2.0, 4.4                               # cross-section radius, half length (a fat egg)


def ellipsoid(name, rx, ry, rz, material):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=72, ring_count=36)
    obj = bpy.context.object
    obj.name = name
    obj.scale = (rx, ry, rz)
    bpy.ops.object.transform_apply(scale=True)
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(material)
    return obj


limb = ellipsoid("limb", A, HALF_LEN, A, skin_m)

LENS_HALF_W, LENS_HALF_L = 0.55, 3.0                 # the wound: a flat red lens...
LIP_HALF_W, LIP_HALF_L, LIP_GAP0, LIP_GAP1 = 0.26, 3.1, 0.62, 0.20   # ...between two chubby lips
lens = ellipsoid("wound", LENS_HALF_W, LENS_HALF_L, 0.16, core_m)


def rounded_bar(name, half_w, half_l, half_h, material):
    """A chubby stadium-shaped bar (a box with a near-full bevel): rounded ends, a clean convex outline."""
    bpy.ops.mesh.primitive_cube_add(size=2)
    obj = bpy.context.object
    obj.name = name
    obj.scale = (half_w, half_l, half_h)
    bpy.ops.object.transform_apply(scale=True)
    mod = obj.modifiers.new("round", "BEVEL")
    mod.width, mod.segments, mod.limit_method = min(half_w, half_h) * 0.95, 10, "NONE"
    bpy.ops.object.shade_smooth()
    obj.data.materials.append(material)
    return obj


lip_l = rounded_bar("lip_L", LIP_HALF_W, LIP_HALF_L, 0.24, skin_m)
lip_r = rounded_bar("lip_R", LIP_HALF_W, LIP_HALF_L, 0.24, skin_m)

# --- the needle and the cord: oversized, chunky ---
R, CZ, ARC = 1.8, 3.2, 135.0                         # arc radius, circle centre height, arc length (degrees)
TIP0, TIP1 = -140.0, 105.0
THETA_OUT = math.degrees(math.asin((A * A - R * R - CZ * CZ) / (2 * R * CZ)))   # where the circle leaves the limb's surface
THETA_IN = -180.0 - THETA_OUT
needle = s.curved_needle(R, CZ, TIP0, ARC, r_tail=0.24, r_tip=0.04, material=needle_m)
cord = s.Thread(cord_m, points=160, thickness=0.13)
ENTRY_X, EXIT_X = R * math.cos(math.radians(THETA_IN)), R * math.cos(math.radians(THETA_OUT))


def surf(x: float) -> float:                         # the limb's skin height at x (+ the lips' bump), so the cord rests on top
    return math.sqrt(max(A * A - x * x, 0.0)) + 0.05 + 0.3 * math.exp(-(x * x) / 0.45)


def tail_pos(theta):
    return Vector((R * math.cos(math.radians(theta)), 0.0, CZ + R * math.sin(math.radians(theta))))


def update(scene_):
    t = scene_.frame_current / c.FPS
    tip = TIP0 + (TIP1 - TIP0) * c.smooth(1.2, 6.2, t)
    tail = tip - ARC
    close = c.smooth(6.6, 9.6, t)
    gap = LIP_GAP0 + (LIP_GAP1 - LIP_GAP0) * close                               # the lips slide together...
    for lip, side in ((lip_l, -1), (lip_r, +1)):
        lip.location = (side * gap, 0.0, math.sqrt(max(A * A - gap * gap, 0.0)) - 0.02)
    lens.scale = (1 - 0.95 * close, 1.0, 1.0)                                    # ...and the red lens narrows (mesh radii are baked in)
    lens.location = (0.0, 0.0, A - 0.03)
    needle.rotation_euler.y = -math.radians(tip - TIP0)
    needle.location.z = CZ + 9.0 * c.smooth(6.2, 7.6, t)

    anchor = Vector((ENTRY_X - 0.45, 0.0, surf(ENTRY_X - 0.45)))
    e_l, e_r = Vector((ENTRY_X, 0.0, surf(ENTRY_X))), Vector((EXIT_X, 0.0, surf(EXIT_X)))
    under = s.arc_points(0.0, CZ, R, THETA_IN, THETA_OUT, 4.0)
    if t < 6.2:
        if tail < THETA_IN:
            end = tail_pos(tail)
            poly = [anchor.lerp(end, u / 8) + Vector((0, 0, max(0.05, 0.5 * 4 * (u / 8) * (1 - u / 8)))) for u in range(9)]
        elif tail <= THETA_OUT:
            poly = [anchor, e_l] + under[: max(1, int((tail - THETA_IN) / 4.0))] + [tail_pos(tail)]
        else:
            poly = [anchor, e_l] + under + [e_r] + s.arc_points(0.0, CZ, R, THETA_OUT, tail, 4.0)[1:]
    else:
        free0 = tail_pos(TIP1 - ARC)
        k = c.smooth(6.2, 9.0, t)
        target = Vector((ENTRY_X + 0.1, 0.8, surf(ENTRY_X + 0.1)))
        free = free0.lerp(target, k)
        free.z = max(surf(free.x), free.z * (1 - k) + surf(free.x) * k)
        pts = []
        for u in range(21):                                  # surface-following path from the exit hole to the free end
            f = u / 20
            x, y = e_r.x + (free.x - e_r.x) * f, e_r.y + (free.y - e_r.y) * f
            pts.append(Vector((x, y, surf(x) + 0.5 * (1 - k) * 4 * f * (1 - f))))
        poly = [anchor, e_l] + under + [e_r] + pts[1:]
    cord.set(poly)
    az = float(args.get("az0", 30)) + (float(args.get("az1", 36)) - float(args.get("az0", 30))) * c.smooth(0.0, T, t)
    c.orbit(stage.cam, Vector((0.0, 0.1, float(args.get("tz", 1.0)))), float(args.get("radius", 17)), float(args.get("el", 36)), az)
    sun = bpy.data.objects.get("toon_sun")                   # spike-only lighting: the terminator must cross the form
    if sun:
        sun.rotation_euler = (-Vector([float(v) for v in args.get("sun", "-2,-6,6").split(",")])).to_track_quat("-Z", "Y").to_euler()
    off = args.get("lines_off", "crease").split(",")          # spike-only: which Freestyle edge types to switch off
    for ls in bpy.context.scene.view_layers[0].freestyle_settings.linesets:
        for kind in ("crease", "silhouette", "border", "contour", "material_boundary", "external_contour"):
            setattr(ls, f"select_{kind}", kind not in off)


stage.run(update, args, SLOT, "spike")
print(f"SPIKE geometry: needle arc R={R} thick 0.24->0.04, limb radius {A}, entry/exit angles {THETA_IN:.1f}/{THETA_OUT:.1f}; "
      f"dark steel {STEEL_DARK} (palette steel grey, HSV value x0.5)")
