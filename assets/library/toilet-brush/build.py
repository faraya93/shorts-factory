"""Final pass on the baked toilet brush: drop any bristle whose root crowds an earlier one (mesh QA: coplanar pairs between touching bristles). Earlier passes on this save gave each bristle a random roll and embedded its root in the core.
    .venv/bin/python tools/blender_run.py -- -b assets/library/toilet-brush/toilet-brush.blend --python assets/library/toilet-brush/build.py"""
import sys
from pathlib import Path

import bmesh
import bpy

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "factory"))
import asset_library as al  # noqa: E402

MIN_GAP = 0.0035
ob = bpy.data.objects["brush"]
mi = len(ob.data.materials) - 1
bm = bmesh.new()
bm.from_mesh(ob.data)
bm.faces.ensure_lookup_table()
seen, kept, kill = set(), [], []
for f in bm.faces:
    if f.material_index != mi or f.index in seen:
        continue
    island, stack = set(), [f]
    while stack:
        x = stack.pop()
        if x.index not in island:
            island.add(x.index)
            stack += [g for e in x.edges for g in e.link_faces]
    seen |= island
    faces = [bm.faces[i] for i in island]
    verts = sorted({v for g in faces for v in g.verts}, key=lambda v: v.index)
    tip = verts[-1].co
    if any((tip - k).length < MIN_GAP for k in kept):
        kill += verts
    else:
        kept.append(tip.copy())
bmesh.ops.delete(bm, geom=kill, context="VERTS")
bm.to_mesh(ob.data)
bm.free()
ob.data.update()
print(f"bristles kept {len(kept)}, removed {len(seen) and 0 + len(kill) // 9}")
print(al.save_collection("toilet-brush", "asset"))
