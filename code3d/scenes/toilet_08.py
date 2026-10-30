"""inodoro scene 8 (final): S4 disinfects the water (UV bar) and it returns to the river; the sludge goes to the digester; the septic tank settles and filters."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import toilet_rig as tl  # noqa: E402
import sewer_rig as sw  # noqa: E402

args, production, stage, m, SLOT = tr.begin(301, floor_z=-1.2)
tl.cpu_draft(stage, args)
T = SLOT / c.FPS
K = tl.Toilet()
K.state(tank=12.0)
M = sw.Materials(K.mats)
P = sw.Plant(M)
sw.add_grate(M)
for o in (K.waste[0], K.waste[1]):
    o.scale = (1e-4,) * 3
tan = tl.Box("s4_tan", M.sewage, y0=-0.5); blue = tl.Box("s4_blue", M.clean)
uv = tr.rbox("uv_bar", (5.4, 0.8, 0.42), (3.8, -0.1, -55.9), m.gold, bevel=0.1)
tr.rbox("uv_arm0", (0.3, 0.7, 1.4), (1.3, -0.1, -55.0), M.ink, bevel=0.05)
tr.rbox("uv_arm1", (0.3, 0.7, 1.4), (6.3, -0.1, -55.0), M.ink, bevel=0.05)
ring = tl.ring(m, "uv_ring", (3.8, -1.0, -57.2), 1e-4, 1e-4)
out_blue = tl.Box("river_stream", M.clean)
dig = tl.Box("dig_fill", M.waste)
sl_stream = tl.Box("sludge_stream", M.waste)
drops = [P.new_blob(f"drop{i}", M.clean, 0.18, (1, 1, 1)) for i in range(8)]
sep_w = tl.Box("sep_w", M.sewage); sep_sl = tl.Box("sep_sludge", M.waste); sep_scum = tl.Box("sep_scum", M.paper)
bits = [P.new_blob(f"sb{i}", M.waste, 0.28, (1, 0.8, 0.8)) for i in range(6)]
leach = [tr.cyl(f"leach{i}", 0.16, 1.2, (20.6 + 1.2 * i, -0.1, -74.5), M.ink, axis="Y", verts=16) for i in range(3)]


def update(scene_):
    t = scene_.frame_current / c.FPS
    w = tl.keys(t, [(1.3, 0.0), (2.4, 3.5)])                         # the blue sweeps outwards from under the UV bar
    tan.set(0.5, 7.5, -61.5, -57.2) if w < 3.45 else tan.set(0, 0, 0, 0)
    blue.set(max(0.5, 3.8 - w), min(7.5, 3.8 + w), -61.5, -57.2) if w > 0.05 else blue.set(0, 0, 0, 0)
    r = tl.keys(t, [(1.3, 0.0), (1.8, 1.0), (2.4, 0.0)])
    ring.scale = (max(1e-4, 3.4 * r), 1.0, max(1e-4, 1.2 * r))
    out_blue.set(6.3, 7.7, -66.0, -62.2) if t > 2.0 else out_blue.set(0, 0, 0, 0)
    for i, d in enumerate(drops):
        k = ((t - 2.0) * 1.2 + 0.125 * i) % 1.0
        P.put(d, 7.0 + 0.2 * math.sin(i), -62.5 - 3.0 * k, s=math.sin(math.pi * k) if t > 2.1 else 1e-4)
    f = tl.keys(t, [(3.0, 0.0), (4.4, 1.0)])
    sl_stream.set(-2.9, -2.1, -37.2 - 17.4 * f, -37.2) if f > 0.02 else sl_stream.set(0, 0, 0, 0)
    dig.set(-4.6, -1.2, -61.5, -61.5 + 3.2 * f)
    # septic
    sep_w.set(11.5, 18.5, -79.5, -75.0)
    s_l = tl.keys(t, [(7.2, 0.0), (8.1, 1.3)])
    sep_sl.set(11.5, 18.5, -79.5, -79.5 + s_l) if s_l > 0.02 else sep_sl.set(0, 0, 0, 0)
    sc = tl.keys(t, [(7.4, 0.0), (8.1, 0.45)])
    sep_scum.set(11.5, 18.5, -75.0 - sc, -75.0) if sc > 0.02 else sep_scum.set(0, 0, 0, 0)
    for i, bt in enumerate(bits):
        k = (t - (5.7 + 0.18 * i)) / 1.8
        z = tl.keys(k, [(0.0, -66.0), (0.35, -73.5), (1.0, -79.0 + 0.2 * (i % 3))])
        P.put(bt, 14.5 + 0.5 * (i % 3 - 1) * c.smooth(0.3, 0.9, k), z, s=1.0 if 0 < k < 1.0 else 1e-4)
    pan_x = tl.keys(t, [(0.0, 3.8), (2.8, 3.8), (4.0, -1.0), (5.0, -1.0), (7.0, 15.0), (10.0, 15.5)])
    pan_z = tl.keys(t, [(0.0, -58.0), (2.8, -58.0), (4.0, -58.0), (5.0, -58.0), (7.0, -75.0), (10.0, -76.0)])
    tr.look(stage, (pan_x, 0, pan_z), 22.0, 8.0, -3.0 + 6.0 * c.smooth(0, T, t))

stage.run(update, args, SLOT, "toilet-08")
