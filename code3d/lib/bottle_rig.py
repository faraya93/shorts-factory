"""Supporting props for 010 (corazon-botellas-al-dia): a single-mesh water bottle (lathe profile, two material slots: plastic and cap), and the heartbeat helper.
The HERO of the video is the library asset 'human-heart'."""
import math
import sys
from pathlib import Path

import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402

PLASTIC, CAP = "#2A64C8", "#FFFFFF"
PROFILE = [(0.0, 0.0), (1.35, 0.0), (1.6, 0.35), (1.6, 5.0), (1.25, 5.9), (0.75, 6.5), (0.72, 7.5), (0.95, 7.5), (0.95, 8.2), (0.0, 8.2)]


def palette(S):
    return {"plastic": S.hero("big", PLASTIC, rough=0.25, coat=0.4), "cap": S.hero("mark", CAP, rough=0.4), "glass": S.glass("#BFE3F5", alpha=0.35, rough=0.05),
            "blood": S.hero("rubber", "#C8323C", rough=0.3), "plate": S.plate_mat()}


def bottle(S, M, name="bottle", loc=(0, 0, 0), seg=20, **tk):
    rings, faces, mats = [], [], []
    verts = []
    for (r, z) in PROFILE:
        base = len(verts)
        for i in range(seg):
            a = 2 * math.pi * i / seg
            verts.append((r * math.cos(a), r * math.sin(a), z))
        rings.append(base)
    for ri in range(len(PROFILE) - 1):
        for i in range(seg):
            a, b = rings[ri] + i, rings[ri] + (i + 1) % seg
            c, d = rings[ri + 1] + (i + 1) % seg, rings[ri + 1] + i
            faces.append((a, b, c, d))
            mats.append(1 if PROFILE[ri + 1][1] > 7.4 and ri >= 6 else 0)
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    for p, m in zip(mesh.polygons, mats):
        p.use_smooth = True
        p.material_index = m
    mesh.materials.append(M["plastic"]); mesh.materials.append(M["cap"])
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    return S.reg(o, **tk)


def beat_amount(t, bpm=72.0):
    """0..1 heartbeat pulse (a fast double bump per cycle)."""
    ph = (t * bpm / 60.0) % 1.0
    return max(math.exp(-((ph - 0.08) / 0.05) ** 2), 0.55 * math.exp(-((ph - 0.30) / 0.07) ** 2))
