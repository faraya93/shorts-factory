"""Library-asset rig (2026-11-04 remake batch): places a sealed library asset (assets/library/<slug>, via factory/asset_library.load_hero) inside a set-piece Shot.
Assets are in real metres; the scene works in centimetres, so `load` scales by K=100 unless told otherwise. Runs inside Blender.

    hero = ar.load(S, "human-hand", loc=(0, 0, 10), skin_hex="#F0B894", role="big")
    hero.root                      # registered empty: S.move / S.spin / S.size work on it
    hero.objs                      # the asset's objects (parented to hero.root, scaled to scene units)
Materials are retinted per production (hero_colours) and renamed to the composition gate's role names (g_big, g_pin ...), so the gate classifies them."""
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_library as al  # noqa: E402
import common as c  # noqa: E402

K = 100.0


class Hero:
    def __init__(self, root, objs, col):
        self.root, self.objs, self.col = root, objs, col


def load(S, slug, loc=(0, 0, 0), rot=(0, 0, 0), k=K, pop=None):
    col = al.load_hero(slug)
    root = S.empty(slug + "_root", loc, pop=pop)
    root.rotation_euler = rot
    objs = list(col.objects)
    for o in objs:
        o.parent = root
        o.scale = tuple(x * k for x in o.scale)
        o.location = tuple(x * k for x in o.location)
    return Hero(root, objs, col)


def retint(obj_or_mat, hex_color, role=None, rough=None):
    """Set the Principled base colour of a material (or of an object's every slot) and rename it to a gate role."""
    mats = [obj_or_mat] if isinstance(obj_or_mat, bpy.types.Material) else [m for m in obj_or_mat.data.materials if m]
    for m in mats:
        b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        b.inputs["Base Color"].default_value = c.linear(hex_color)
        if rough is not None:
            b.inputs["Roughness"].default_value = rough
        if role:
            m.name = role
    return mats


def node(mat, name):
    return mat.node_tree.nodes[name]


def unparent(objs, keep_visible=True):
    """Detach objects from their root keeping the world transform (so each can be moved on its own)."""
    bpy.context.view_layer.update()
    for o in objs:
        mw = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = mw
