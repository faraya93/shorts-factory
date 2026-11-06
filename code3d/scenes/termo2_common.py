"""Shared helpers for the termo2 scenes (not a scene: no number suffix)."""
import math
import bpy
from mathutils import Vector


def grow_ray(o, p0, p1, t0, t1, t_off=None, t_off1=None):
    """Return an update fn(t): the ray grows from p0 to p1 between t0 and t1 (and, if t_off given, shrinks away from p0 toward p1 between t_off and t_off1)."""
    a, b = Vector(p0), Vector(p1)
    d = b - a
    L = d.length

    def upd(t):
        u = min(max((t - t0) / (t1 - t0), 0.0), 1.0)
        v = 0.0 if t_off is None else min(max((t - t_off) / (t_off1 - t_off), 0.0), 1.0)
        n = max(u - v, 1e-3)
        o.scale = (1, 1, n)
        o.location = a + d * (v + (u - v) / 2)
    return upd


def window(P, z0, z1):
    """Narrow (or move) the cut window of a built thermos: the shells' cut materials hold two Math nodes with the window heights (defaults 3.2 and 24.5)."""
    for key in ("outer", "inner"):
        for slot in P[key].material_slots:
            for n in slot.material.node_tree.nodes:
                if n.type == "MATH" and n.operation == "GREATER_THAN" and abs(n.inputs[1].default_value - 3.2) < 1e-6:
                    n.inputs[1].default_value = z0
                if n.type == "MATH" and n.operation == "LESS_THAN" and abs(n.inputs[1].default_value - 24.5) < 1e-6:
                    n.inputs[1].default_value = z1
