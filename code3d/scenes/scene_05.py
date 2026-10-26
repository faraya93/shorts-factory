"""v4-code3d scene 5 (risk): a row of stitches on healed skin; the skin grows over one stitch; tweezers (library asset)
grip it and lift it out.

Run: blender -b --python code3d/scenes/scene_05.py -- production=<dir> mode=draft|final [stills=..] [frames=a-b] [out=..]
Timeline (s, slot 6.17): row of stitches 0-1.0 | skin grows over stitch 3 1.0-2.6 | tweezers enter 2.2-3.6 | grip 3.6-4.0 |
the stitch is lifted out and the mound flattens 4.0-5.4 | hold. Camera pushes in while orbiting a quarter turn.
"""

import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import props  # noqa: E402
import stage as st  # noqa: E402
import suture as s  # noqa: E402

args = c.parse_args()
SLOT = int(args.get("slot", 185))                      # narration slot: 6.17 s
T = SLOT / c.FPS

stage = st.Stage(Path(args["production"]), args.get("mode", "draft"))
GAP = 0.03
s.skin_half(-1, GAP, 2.6, 5.0, stage.skin, stage.tissue)
s.skin_half(+1, GAP, 2.6, 5.0, stage.skin, stage.tissue)
s.wound_floor(GAP + 0.01, 5.0, -0.1, stage.tissue)

STITCH_Y = [-1.6, -0.8, 0.0, 0.8, 1.6]
TARGET = 2                                             # index of the stitch that gets overgrown and pulled out
HALF, HUMP = 0.5, 0.11                                 # half span across the cut, arch height
threads = [s.Thread(stage.thread_mat, points=40, thickness=0.03) for _ in STITCH_Y]

# the skin that grows over the stitch: a flattened ellipsoid of the same skin material, hidden at first
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, STITCH_Y[TARGET], 0.0), segments=48, ring_count=24)
mound = bpy.context.object
bpy.ops.object.shade_smooth()
mound.data.materials.append(c.principled("mound", stage.pal["skin peach"], roughness=0.5, subsurface=0.1))

tw = props.load_tweezers(scale=30.0, grip_hex=stage.pal["steel grey"])
AIM = Vector((-0.55, -0.35, -0.75))                    # tweezers point down and to the left, coming from the top right
GRIP = Vector((0.0, STITCH_Y[TARGET], 0.16))           # where the tips take hold of the stitch


def arch(y, lift=0.0, grip=None, span=1.0):
    """One stitch: an arch over the cut whose ends are tucked into the skin; `lift` pulls the middle up to `grip`."""
    pts = []
    for i in range(41):
        u = i / 40
        x = -HALF + 2 * HALF * u
        z = -0.06 + (HUMP + 0.06) * math.sin(math.pi * u) ** 0.6
        p = Vector((x, y, z))
        if grip is not None:
            w = math.sin(math.pi * u) ** 1.5                # the middle follows the tweezers: apex = the grip point
            p = p.lerp(Vector((grip.x + x * 0.12, grip.y, grip.z)), lift * w)
            p.z += c.smooth(0.55, 1.0, lift) * 1.1 * abs(2 * u - 1) ** 3   # the ends come out of the skin
        pts.append(p)
    return pts


def update(scene_):
    t = scene_.frame_current / c.FPS
    grow = c.smooth(1.0, 2.6, t) * (1 - c.smooth(4.3, 5.3, t))        # skin grows over the stitch, then flattens again
    mound.scale = (0.78, 0.30, 0.01 + 0.15 * grow)
    mound.location.z = -0.01
    lift = c.smooth(4.0, 5.4, t)
    approach = c.smooth(2.2, 3.6, t)
    tip = (GRIP + Vector((2.6, 1.6, 3.2)) * (1 - approach)) + Vector((0, 0, 1.9 * lift))
    tw.place(tip, AIM)
    tw.set_open(8.0 * (1 - c.smooth(3.6, 4.0, t)) * (0.4 + 0.6 * approach))   # open on the way in, closed on the grip
    for i, (th, y) in enumerate(zip(threads, STITCH_Y)):
        if i != TARGET:
            th.set(arch(y))
        else:
            th.set(arch(y, lift=lift, grip=Vector((GRIP.x, GRIP.y, GRIP.z + 1.9 * lift)), span=1.0) if lift > 0 else arch(y))
    k = c.smooth(0.0, T, t)                                            # push in while orbiting a quarter turn
    c.orbit(stage.cam, Vector((0.0, 0.0, 0.3 + 0.6 * k)), 8.5 - 2.6 * k, 38.0, -20.0 + 85.0 * k)


stage.run(update, args, SLOT, "scene-05")
