"""Blender side of tools/visibility_check.py: started with --python-expr BEFORE the scene script, so no scene script or hashed rig library changes. Hides the objects named in SF_VIS_HIDE (comma-separated
fnmatch globs) from the render after every frame update, which produces the element-free plate of the same frame. SF_VIS_DUMP=1 prints the object names on the first frame and exits."""
import fnmatch
import os

import bpy
from bpy.app.handlers import persistent

GLOBS = [g for g in os.environ.get("SF_VIS_HIDE", "").split(",") if g]


@persistent
def _apply(scene, *_):
    if os.environ.get("SF_VIS_DUMP"):
        print("VIS_OBJECTS " + "|".join(sorted(o.name for o in bpy.data.objects if o.type in {"MESH", "CURVE", "VOLUME", "META", "SURFACE"})), flush=True)
        os._exit(0)
    hit = 0
    for o in bpy.data.objects:
        if any(fnmatch.fnmatchcase(o.name, g) for g in GLOBS):
            o.hide_render, hit = True, hit + 1
    print(f"VIS_HIDDEN {hit}", flush=True)


bpy.app.handlers.frame_change_post.append(_apply)
