"""huincha-de-medir scene 2 (B2 profile): push-through to the blade cross-sections end-on, then a plate presses each cantilever: the FLAT
strip folds, the CURVED arc resists (gold stress). Slot 294 frames (9.8 s)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(294, floor_z=-9.0)
T = SLOT / c.FPS
YF, YC, ZF, ZC, LB, SP = -2.4, 2.4, -2.8, 2.8, 9.0, 7.0
tr.rbox("clamp", (2.6, 8.4, 10.4), (-1.3, 0, 0.0), m.table, bevel=0.15)
bf = tr.Blade(m.blade.copy(), "flat")
bc = tr.Blade(m.blade.copy(), "curved")
plates = {}
for key, y, z0 in (("f", YF, ZF), ("c", YC, ZC)):
    plate = tr.rbox(f"plate_{key}", (1.8, 2.8, 0.5), (SP, y, z0 + 4.5), m.rubber, bevel=0.12)
    rod = tr.cyl(f"rod_{key}", 0.3, 4.5, (SP, y, z0 + 7.0), m.dark_metal, axis="Z", verts=32)
    plates[key] = (plate, rod)


def update(scene_):
    t = scene_.frame_current / c.FPS
    free_f = ZF + 4.5 - 7.9 * c.smooth(5.7, 7.5, t)
    free_c = ZC + 4.5 - 7.9 * c.smooth(7.7, 9.2, t)
    pf = min(1.0, max(0.0, (ZF + 0.3 - free_f) / 3.4))
    pc = min(1.0, max(0.0, (ZC + 0.3 - free_c) / 3.4))

    def th_f(s):
        k = min(1.0, max(0.0, (s - 3.0) / 0.7))
        return 1.35 * pf * k * k * (3 - 2 * k)

    bf.set(LB, th_f, lambda s: 0.0, origin=(0, YF, ZF))
    bc.set(LB, lambda s: 0.05 * pc * s / LB, None, origin=(0, YC, ZC))
    zc = bc.z_at(SP)
    for key, z in (("f", free_f), ("c", max(free_c, zc + 0.31))):
        plates[key][0].location.z = z
        plates[key][1].location.z = z + 2.5
    bf.stress(6.0 * pf, 3.4, 0.7)
    bc.stress(2.4 * c.smooth(8.0, 8.9, t), 4.6, 3.4)
    p = c.smooth(0, 5.2, t)
    q = c.smooth(0.0, 3.5, t)
    o = c.smooth(3.8, 6.5, t)
    pan = c.smooth(2.5, 4.3, t)                                    # end-on push-through: first the flat section, then the arc
    ty, tz = -2.4 * (1 - pan) + 2.4 * pan, -2.8 * (1 - pan) + 2.8 * pan
    ty, tz = ty * (1 - o), tz * (1 - o)
    tr.look(stage, (8.9 - 3.9 * o, ty, tz), 7.5 - 1.0 * q + 17 * o, 2 + 6 * o, 90 - 100 * o)


stage.run(update, args, SLOT, "tape-02")
