"""Design-system validation hero: a classic red-and-white thermos (versatility test), lit by looks.apply via begin(look=...)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

args, production, stage, m, SLOT = tr.begin(299)
T = SLOT / c.FPS
tr.table(m)
ZT = tr.MOUTH_Z - 0.45
red = tr.pbr("red_p", "Plastic010", "Plastic010", "#CC2229", rough_mul=0.9, scale=0.4, normal=0.3, tint_mix=0.9, coat=0.5)
white = tr.pbr("white_p", "Plastic010", "Plastic010", "#F2F1EE", rough_mul=0.9, scale=0.4, normal=0.2, tint_mix=0.9, coat=0.3)
blk = tr.plain("blk_p", "#151517", rough=0.5)
tr.cyl("th_body", 2.3, 8.0, (0, 0, ZT + 4.0), red, axis="Z", verts=64, bevel=0.35)
tr.cyl("th_band", 2.36, 0.5, (0, 0, ZT + 8.2), blk, axis="Z", verts=64, bevel=0.08)
tr.cyl("th_cup", 2.2, 2.6, (0, 0, ZT + 9.6), white, axis="Z", verts=64, bevel=0.4)
tr.cyl("th_base", 2.4, 0.5, (0, 0, ZT + 0.25), white, axis="Z", verts=64, bevel=0.1)


def update(scene_):
    u = c.smooth(0, T, scene_.frame_current / c.FPS)
    # framed for the proposed rules: hero inside y 28-76% (below the caption band), 54% of frame width
    tr.look(stage, (0, 0, 2.6), 56.0 - 2 * u, 12.0, -30 + 8 * u)


stage.run(update, args, SLOT, "thermos-val")
