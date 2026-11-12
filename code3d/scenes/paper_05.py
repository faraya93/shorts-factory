"""paper 5 (espacio): the column keeps climbing; the sky darkens from the coral stage to black and stars appear while the camera pulls far back and sideways, the column crossing the whole sky; the ground curves away below."""
import sys
from pathlib import Path

from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import paper_rig as pr  # noqa: E402
import real_kit as rk  # noqa: E402
import setpiece as sp  # noqa: E402

S = sp.Shot(177, floor_z=-0.05)
m = pr.Mats(S)
pr.big(S)
earth = pr.earth(m)
col = pr.column(m, "stack", w=26.0, d=34.0, loc=(0.0, 0.0, 0.0), pitch=6.0)       # wide enough that its layered paper edge reads at the pulled-back distance
sky = pr.Sky(S)
pr.sun(S, 1.2, rot=(1.1, 0.0, 1.9))                  # raking light from the left so the front face keeps its layer lines
lift = pr.av.lights(S, 5.0)
for lt in (S.stage.key, S.stage.rim, S.stage.fill):
    lt.data.energy *= 0.25
cam_t = [(0.0, 0.0, 200.0)]


def centre(t):
    return cam_t[0]


fig_root, fig = pr.figure(S, m, "scale", (-52.0, -70.0, 0.0), rot_z=0.35, k=26.0)      # context staging: a person at the column's foot says "a stack of paper"
loose = [pr.tr.rbox(f"loose_{i}", (34.0, 46.0, 0.9), (0, 0, 0), m.paper, bevel=0.1) for i in range(7)]      # loose sheets drifting past: the unmistakable cue that this is paper
spots = [(-48, 330, -95), (52, 360, -20), (-40, 300, 40), (58, 340, 85), (-55, 380, 120), (44, 310, 150), (-30, 350, -150)]      # right, forward, up of the camera
stars = pr.stars(S, m, 60, centre, lambda t: pr.smooth(1.4, 3.2, t), dist=1400.0)


def upd(t):
    h = 150.0 + 380.0 * pr.smooth(0.0, 4.6, t)
    pr.set_height(col, h)
    k = pr.smooth(0.2, 3.6, t)
    sky.set(k, hide_floor=True)
    rad = sp.interp([(0, 330.0), (S.T, 640.0)], t)
    tz = sp.interp([(0, 90.0), (S.T, 270.0)], t)
    cam_t[0] = (0.0, 0.0, tz)
    pr.look(S, (0.0, 0.0, tz), rad, sp.interp([(0, 2.0), (S.T, 6.0)], t), sp.interp([(0, -42.0), (S.T, -22.0)], t))
    rot = S.stage.cam.rotation_euler.to_matrix()
    fwd, right, up = rot @ Vector((0, 0, -1)), rot @ Vector((1, 0, 0)), rot @ Vector((0, 1, 0))
    for i, (o, (sx, sf, su)) in enumerate(zip(loose, spots)):
        o.location = S.stage.cam.location + fwd * sf + right * (sx + 6.0 * t * (1 if i % 2 else -1)) + up * (su + 10.0 * t)
        o.rotation_euler = (0.5 * t + i, 0.35 * t * (1 + i % 3) + 0.7 * i, 0.2 * t + 0.4 * i)
    lift(0.0, 0.0)


S.every_frame(upd)
rk.softboxes(0.7, centre=(0, -30, 200))
S.go()
