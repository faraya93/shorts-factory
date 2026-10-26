"""v4-code3d scene 6 (ant-twist): a big friendly ant (library asset) bites both edges of a cut together like a staple.
Macro on the jaws first, then the camera pulls back and up to reveal the blurred jungle.

Run: blender -b --python code3d/scenes/scene_06.py -- production=<dir> mode=draft|final [stills=..] [frames=a-b] [out=..]
Timeline (s, slot 7.57): macro, jaws open, skin lips rise 0-3.4 | jaws close, lips pinch together, cut closes 2.2-4.2 |
camera pulls back and up 1.8-7.2 | hold.
"""

import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import props  # noqa: E402
import stage as st  # noqa: E402
import suture as s  # noqa: E402

args = c.parse_args()
SLOT = int(args.get("slot", 227))                      # narration slot: 7.57 s
T = SLOT / c.FPS
JAW_SIGN = float(args.get("jaw_sign", 1.0))            # +1/-1: which way the mandible bones open (checked on stills)

stage = st.Stage(Path(args["production"]), args.get("mode", "draft"), key_energy=650.0)
SCALE, Y_MOUTH = 90.0, -0.3
ant = props.load_ant(SCALE)
ant.place(Vector((0.0, Y_MOUTH + 0.0087 * SCALE, 0.0)))        # mouth lands at (0, Y_MOUTH, ~0.97)
mouth = ant.mouth(ant.arm.location)
props.jungle(stage)

half_l = s.skin_half(-1, 0.13, 2.6, 5.0, stage.skin, stage.tissue)
half_r = s.skin_half(+1, 0.13, 2.6, 5.0, stage.skin, stage.tissue)
s.wound_floor(0.14, 5.0, -0.12, stage.tissue)
lip_mat = c.principled("lip", stage.pal["skin peach"], roughness=0.5, subsurface=0.1)   # the SSS shader blows out on thin boxes
FIN_L = s.box("lip_L", -0.04, 0.04, -0.3, 0.3, 0.0, 1.0, lip_mat, bevel=0.02)   # the cut's lips, drawn up by the jaws
FIN_R = s.box("lip_R", -0.04, 0.04, -0.3, 0.3, 0.0, 1.0, lip_mat, bevel=0.02)

for obj in list(half_l.children) + list(half_r.children):   # the skin blocks are just the ground: no shadow onto the backdrop
    obj.visible_shadow = False

cam_data = stage.cam.data
cam_data.dof.use_dof = True
cam_data.dof.aperture_fstop = 1.6


def update(scene_):
    t = scene_.frame_current / c.FPS
    close = c.smooth(2.2, 4.2, t)
    gap = 0.13 - 0.10 * close                              # the slabs close as the lips are pinched
    half_l.location.x, half_r.location.x = 0.13 - gap, -(0.13 - gap)
    rise = c.smooth(0.2, 1.8, t)
    h = 0.02 + 0.9 * rise                                  # lips rise up to the jaws
    for fin, side in ((FIN_L, -1), (FIN_R, +1)):
        fin.scale = (1.0, 1.0, h)
        fin.location = (side * (gap + 0.04), Y_MOUTH + 0.05, 0.0)
    ant.set_jaws(JAW_SIGN * 40.0 * (1 - close))
    k = c.smooth(1.8, T - 0.4, t)                          # camera: macro on the jaws -> pulled back and up
    target = mouth.lerp(Vector((0.0, Y_MOUTH + 1.1, 0.7)), k)
    c.orbit(stage.cam, target, 2.6 + 5.4 * k, 14.0 + 20.0 * k, -18.0 + 30.0 * k)
    cam_data.dof.focus_distance = (stage.cam.location - target).length


stage.run(update, args, SLOT, "scene-06")
