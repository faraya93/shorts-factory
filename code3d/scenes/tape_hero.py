"""huincha-de-medir HERO STILL (art direction): the tape rig with the curved blade extended, 3/4 view on the dark stage."""
import math, sys
from pathlib import Path
from mathutils import Vector
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import common as c
import tape_rig as tr

args, production, stage, m, SLOT = tr.begin(1)
tp = tr.Tape(m, loc=(0, 0, 0))
tr.table(m)
L = float(args.get("L", 9.0))
def update(scene_):
    tp.place_blade(L, theta=lambda s: 0.015 * s, floor=None, hook_slide=1.0)
    tp.blade.stress(float(args.get("stress", 0.0)), 6.0, 1.2)
    az = float(args.get("az", -38)); el = float(args.get("el", 14)); r = float(args.get("r", 20))
    tr.look(stage, (float(args.get("tx", 3.5)), 0, float(args.get("tz", -1.2))), r, el, az)
stage.run(update, args, 1, "hero")
