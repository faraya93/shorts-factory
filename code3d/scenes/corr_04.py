"""corr 4 (chispa): see productions/mecanalia-es/023*/script.json. Close-up: the charged hand (sealed hand-articulated, pose door, in a shirt sleeve) nears the metal of the car door; at a finger's width an arc jumps from the
fingertip to the door and the glow drains out of the hand at once. The camera pushes in slowly toward the gap."""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import avion_rig as av  # noqa: E402
import corr_rig as cr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

S = sp.Shot(194, floor_z=-0.6)
m = cr.Mats(S)
cr.ground(S, m)
car = cr.car(S, m)
lift = cr.lights(S)
TILT = math.radians(58)
D = Vector((0.0, math.sin(TILT), -math.cos(TILT)))                 # the fingers' direction
root, objs = av.place("hand-articulated", None, 10.0, loc=(0, 0, 0), rot=(TILT, 0, 0))
av.pose_armature(next(o for o in objs if o.type == "ARMATURE"), "pose_door")
for j, o in enumerate(objs):
    o.name = f"hand_{j}"
bpy.context.view_layer.update()
dg = bpy.context.evaluated_depsgraph_get()
pts = []
for o in objs:
    if o.type == "MESH":
        ev = o.evaluated_get(dg)
        me = ev.to_mesh()
        pts += [ev.matrix_world @ v.co for v in me.vertices]
        ev.to_mesh_clear()
tip = max(pts, key=lambda p: p.dot(D))
wrist = min(pts, key=lambda p: p.dot(D))
tip_off, wrist_off = tip - root.location, wrist - root.location
nodes = cr._glow_mats(objs, S.p.get("accent", "#0A5C6B"))
shirt = S.hero("big", "#2973CC", rough=0.5)
sleeve = tr.cyl("hand_sleeve", 0.95, 16.0, (0, 0, 0), shirt, axis="Z", verts=32, bevel=0.3)
sleeve.rotation_mode = "QUATERNION"
sleeve.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(D)
ZH, XH, GAP = 9.6, 0.5, 2.2                                       # the chrome handle of the front door sits at x -0.9..2, z 9.2..9.9, skin at y -9.4 (probe of the sealed car)
T_SP = S.t("salta", default=3.1)
tipY = lambda t: sp.interp([(0.0, cr.DOOR_Y - 11.0), (T_SP - 0.15, cr.DOOR_Y - GAP)], t) + 0.25 * math.sin(t * 20.0) * (1 if t > T_SP - 0.15 else 0)
cr.spark(S, (XH, cr.DOOR_Y - GAP, ZH), (XH, -9.5, ZH), T_SP, T_SP + 3.1, flashes=6, r=0.07, rays=7, rays_len=0.9, fine=2)
level = lambda t: sp.interp([(0.0, 0.6), (T_SP - 0.2, 1.0), (T_SP + 0.1, 1.0), (T_SP + 0.5, 0.0)], t)
cr.aura(S, m, lambda t: (XH, tipY(t) - 3.0, ZH), level, n=14, rad=1.8, h0=-1.0, h1=1.5, r=0.2, name="handbead")


def upd(t):
    p = Vector((XH, tipY(t), ZH))
    root.location = p - tip_off
    w = p - tip_off + wrist_off
    sleeve.location = w - D * 8.0
    for nd in nodes:
        nd.inputs["Emission Strength"].default_value = 1.6 * level(t)
    lift(0.0, 0.0)


S.every_frame(upd)
S.cam([(0.0, (XH, cr.DOOR_Y - 4.0, ZH), 22.0, 6.0, -72.0), (T_SP - 0.1, (XH, -10.8, ZH), 15.0, 4.0, -70.0), (S.T, (XH, -10.8, ZH), 12.0, 3.0, -66.0)])
rk.softboxes(0.7, centre=(0, -30, 50))
S.go()
