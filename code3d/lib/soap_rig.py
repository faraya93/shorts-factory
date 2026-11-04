"""Rig for 009 (jabon-agua-sola-no-quita-grasa): palette, a soap molecule (head + tail, ONE joined mesh, head along +z), orientation and sphere-point helpers."""
import math
import random
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402

OIL, WATER, HEAD, TAIL, BAR = "#F2A63B", "#5CC8FF", "#FF5FA2", "#FFE08A", "#FF9ACB"


def palette(S):
    return {"oil": S.hero("housing", OIL, rough=0.3, coat=0.3), "water": S.glass(WATER, alpha=0.6, rough=0.05), "water_solid": S.hero("small", WATER, rough=0.2, coat=0.3),
            "head": S.hero("mark", HEAD, rough=0.35, coat=0.3), "tail": S.hero("blade", TAIL, rough=0.45), "bar": S.hero("mark", BAR, rough=0.4, coat=0.3),
            "foam": S.glass("#FFFFFF", alpha=0.55, rough=0.05, name="foam"), "plate": S.plate_mat(), "board": S.board_mat()}


def molecule(S, M, name="mol"):
    """Head sphere at +z, tail cylinder below; one mesh with two materials (cloneable by swarm)."""
    head = mk.sphere(name + "_h", M["head"], 0.55, (0, 0, 0.55), seg=20)
    tail = tr.cyl(name + "_t", 0.17, 1.5, (0, 0, -0.5), M["tail"], axis="Z", verts=14)
    bpy.ops.object.select_all(action="DESELECT")
    head.select_set(True); tail.select_set(True)
    bpy.context.view_layer.objects.active = head
    bpy.ops.object.join()
    o = bpy.context.object
    o.name = name
    return S.reg(o)


def face(direction):
    """Euler that turns local +z (the head) toward `direction`."""
    return tuple(Vector((0, 0, 1)).rotation_difference(Vector(direction).normalized()).to_euler())


def sphere_points(n, seed=0):
    """Fibonacci sphere: n unit vectors spread evenly."""
    out = []
    ga = math.pi * (3 - math.sqrt(5))
    for i in range(n):
        z = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(max(0.0, 1 - z * z))
        out.append((r * math.cos(ga * i + seed), r * math.sin(ga * i + seed), z))
    return out


def ease(a, b, t):
    return sp.c.smooth(a, b, t)
