"""inodoro scene 4 (sello): the bowl refills; the water left in the bend is a seal that stops the gas coming up the drain."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import toilet_rig as tl  # noqa: E402

args, production, stage, m, SLOT = tr.begin(183, floor_z=-1.2)
tl.cpu_draft(stage, args)
T = SLOT / c.FPS
K = tl.Toilet()
import bpy
gas = tl.gas_material()
puffs = []
for i in range(3):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.5)
    o = bpy.context.object
    o.name = f"gas{i}"
    o.data.materials.append(gas)
    o.scale = (1e-4,) * 3
    o.visible_shadow = False
    puffs.append(o)
seal = tl.ring(m, "seal_ring", (0.9, -1.0, 3.5), 1e-4, 1e-4)
GP = [(-2.2, -0.5), (-2.2, 5.25), (-0.2, 5.25), (-0.2, 4.95)]


def gas_at(s):
    segs = list(zip(GP, GP[1:]))
    ls = [math.dist(a, b) for a, b in segs]
    d = s * sum(ls)
    for (a, b), l in zip(segs, ls):
        if d <= l:
            k = d / l
            return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
        d -= l
    return GP[-1]


def update(scene_):
    t = scene_.frame_current / c.FPS
    bowl = tl.keys(t, [(0.2, 2.6), (2.0, tl.WATERLINE)])
    tank = tl.keys(t, [(0.0, 9.2), (6.1, 12.4)])
    K.state(tank=tank, bowl=bowl, tube=bowl, leg2=(5.9, 5.9), hole=0.0)
    K.put_waste(0, 3.7, 9.0, s=0.0); K.put_waste(1, 4.7, 9.0, s=0.0)
    k = tr.back((t - 2.6) / 0.5) if t > 2.6 else 0.0
    seal.scale = (max(1e-4, 1.35 * k), 1.0, max(1e-4, 1.35 * k)) if k > 0 else (1e-4, 1.0, 1e-4)
    for i, g in enumerate(puffs):
        s = (t - (3.8 + 0.45 * i)) / 1.5
        if 0.0 < s < 1.0:
            x, z = gas_at(min(1.0, s))
            grow = tr.back(min(1.0, s * 6.0))
            fade = 1.0 if s < 0.94 else max(0.0, (1.0 - s) / 0.06)
            g.location = (x, -0.1, z)
            g.scale = (grow * fade,) * 3
        else:
            g.scale = (1e-4,) * 3
    tr.look(stage, (0.4, 0, 5.2), 22.0 + 3.0 * c.smooth(0, T, t), 6.0, -2.0 + 6.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "toilet-04")
