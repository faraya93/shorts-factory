"""Rig of production 023 (why you get a shock when you step out of a car): the sealed cartoon car (roof splittable), the recurring person (sealed human-figure, poses blended
between the sealed key poses, an arm raised to reach, an accent glow for the charge), the sealed hand with a sleeve, accent beads, flickering arcs, a geometric fuel dispenser and
the cage of accent bars. Rigid, geometric parts are code primitives; the person, the hand and the car are sealed library assets placed through avion_rig.place. Runs inside Blender.
Scene units follow rayo_rig: the car is 42 long, 9 wide, 16 tall (10 units per metre); the car's nose points to -x, the camera sits on the -y side; z up."""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Euler, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import avion_rig as av  # noqa: E402
import rayo_rig as ry  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

K = ry.K
FIG_K = 1.0 * K
DOOR_Y = -9.8                      # the sealed car's flank on the camera side (measured by 020: the body box spans y -9.8..9.3)
ease = av.ease
look = av.look


class Mats(ry.Mats):
    """Hero colours come from scenes.json hero_colours; the ground plate takes the production's support colour."""


def lights(S):
    return av.lights(S)


def ground(S, m, length=320.0, width=170.0, name="ground"):
    """The plain ground slab the car and the person stand on (support plate colour)."""
    return tr.rbox(name, (length, width, 0.6), (0, 0, -0.3), m.road, bevel=0.2)


def car(S, m, roof=True, name="hero"):
    """The sealed cartoon car on z = 0, nose toward -x, no driver; the roof group is split off so a scene may slide it away."""
    return ry.car(S, m, name, roof=roof, driver=False)


# ------------------------------------------------------------------ the person
def _rot_quat(pb, x, y, z):
    """Armature-space rotation (degrees) as the bone's local quaternion (the convention of assets/library/human-figure/build.py)."""
    B = pb.bone.matrix_local.to_3x3()
    R = Euler((math.radians(x), math.radians(y), math.radians(z)), "XYZ").to_matrix()
    return (B.inverted() @ R @ B).to_quaternion()


def _glow_mats(objs, hex_color):
    """Give every material of the meshes its own copy with an emission colour (strength 0) and return the shader nodes to drive."""
    lin = tuple((int(hex_color[i:i + 2], 16) / 255.0) ** 2.2 for i in (1, 3, 5)) + (1.0,)
    nodes, seen = [], {}
    for o in objs:
        if o.type != "MESH":
            continue
        for slot in o.material_slots:
            mat = slot.material
            if mat is None or mat.node_tree is None:
                continue
            if mat.name not in seen:
                mc = mat if mat.name.rsplit("_", 1)[-1].isdigit() else mat.copy()
                nd = next((n for n in mc.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
                if nd is not None:
                    nd.inputs["Emission Color"].default_value = lin
                    nd.inputs["Emission Strength"].default_value = 0.0
                    nodes.append(nd)
                seen[mat.name] = mc
            slot.material = seen[mat.name]
    return nodes


class Person:
    """The recurring person: sealed human-figure, one armature. set() poses it (blend of two sealed poses, optional reach with the right arm)."""

    def __init__(self, S, name="viewer", k=FIG_K):
        self.S = S
        self.root, self.objs = av.place("human-figure", None, k, loc=(0, 0, 0), rot=(0, 0, 0))
        self.arm = next(o for o in self.objs if o.type == "ARMATURE")
        av.tint_figure(self.objs, ry.DRIVER)
        for j, o in enumerate(self.objs):
            o.name = f"fig_{name}_{j}"
        self.tab = {}
        for n in ("standing", "walking", "seated"):
            av.pose_armature(self.arm, "pose_" + n)
            self.tab[n] = {pb.name: (tuple(pb.rotation_quaternion), tuple(pb.location)) for pb in self.arm.pose.bones}
        self.arm.animation_data.action = None
        self.glow_nodes = _glow_mats(self.objs, S.p.get("accent", "#0A5C6B"))
        self.reach_q = {}
        for bone, ang in (("upperarm.R", (-52, 0, 0)), ("forearm.R", (-8, 0, 0))):
            self.reach_q[bone] = _rot_quat(self.arm.pose.bones[bone], *ang)

    def set(self, loc, rot_z, a="standing", b="standing", k=0.0, reach=0.0):
        self.root.location = loc
        self.root.rotation_euler = (0, 0, rot_z)
        for pb in self.arm.pose.bones:
            qa, la = self.tab[a][pb.name]
            qb, lb = self.tab[b][pb.name]
            if sum(x * y for x, y in zip(qa, qb)) < 0:
                qb = tuple(-x for x in qb)
            q = [x + (y - x) * k for x, y in zip(qa, qb)]
            n = math.sqrt(sum(x * x for x in q)) or 1.0
            pb.rotation_quaternion = tuple(x / n for x in q)
            pb.location = tuple(x + (y - x) * k for x, y in zip(la, lb))
        if reach > 0.0:
            for bone, rq in self.reach_q.items():
                pb = self.arm.pose.bones[bone]
                q0 = pb.rotation_quaternion.copy()
                pb.rotation_quaternion = q0.slerp(rq, reach)
        bpy.context.view_layer.update()

    def glow(self, level):
        for nd in self.glow_nodes:
            nd.inputs["Emission Strength"].default_value = 1.6 * max(0.0, min(1.0, level))

    def hand(self):
        """World position of the right hand (end of the hand bone) in the current pose."""
        return self.arm.matrix_world @ self.arm.pose.bones["hand.R"].tail


def aura(S, m, pos_fn, level_fn, n=26, rad=4.2, h0=1.0, h1=14.0, r=0.38, name="bead", mat=None):
    """Beads (accent unless `mat`) orbiting a body at pos_fn(t): the number visible grows with level_fn(t) (0..1)."""
    src = S.ball(f"{name}_src", mat or S.accent, r)

    def f(i, t):
        lv = level_fn(t)
        if i >= lv * n:
            return None
        px, py, pz = pos_fn(t)
        ph = 6.2832 * ((i * 0.618) % 1.0) + t * (1.4 + 0.5 * (i % 3))
        rr = rad * (0.8 + 0.3 * (((i * 7) % 5) / 5.0))
        z = h0 + (h1 - h0) * ((i * 0.37) % 1.0)
        return ((px + rr * math.cos(ph), py + rr * math.sin(ph), pz + z), 0.7 + 0.5 * math.sin(t * 3.0 + i))
    S.swarm(n, src, f)


def _arc(S, name, p0, p1, mat, t0, t1, t_off, r, seed, n=7, jit=0.28):
    """One zigzag tube p0 -> p1, jittered across the line in every axis (so it zigzags seen from any side), drawn over t0..t1 and hidden again at t_off."""
    import random
    rnd = random.Random(seed)
    span = math.dist(p0, p1)
    pts = []
    for i in range(n + 1):
        k = i / n
        p = [a + (b - a) * k for a, b in zip(p0, p1)]
        if 0 < i < n:
            p = [v + rnd.uniform(-1, 1) * jit * span for v in p]
        pts.append(tuple(p))
    o = S.line(name, pts, r, mat, grow=(t0, t1), smooth=False)

    def hide(t):
        o.hide_render = o.hide_viewport = t >= t_off
    S.every_frame(hide)
    return o


def spark(S, p0, p1, t0, t1, flashes=4, seed=3, r=0.3, name="arc", rays=0, rays_len=1.0, fine=1):
    """A crackle of short arcs between p0 and p1 over t0..t1: each flash is a fresh zigzag drawn in 0.08 s, with a pulsing glow at the far end (object names start with `name`)."""
    dt = (t1 - t0) / flashes
    core = S.emit("#FFF6E0", 12.0, name=f"{name}_core")
    for i in range(flashes):
        a = t0 + i * dt
        _arc(S, f"{name}_{i}", p0, p1, core, a, a + 0.08, a + dt, r, seed + 5 * i, n=fine * 7, jit=0.28 / fine)
        if rays:
            import random
            rnd = random.Random(seed + 11 * i)
            for kk in range(rays):
                ang = rnd.uniform(0, 6.2832)
                ln = rnd.uniform(0.8, 1.6) * rays_len
                end = (p1[0] + ln * math.cos(ang), p1[1] + rnd.uniform(-0.2, 0.0) * ln, p1[2] + ln * math.sin(ang))
                ro = S.line(f"{name}_ray{i}_{kk}", [p1, end], r * 0.3, core, grow=(a, a + 0.06), smooth=False)
                S.every_frame(lambda t, o=ro, off=a + dt: setattr(o, "hide_render", t >= off) or setattr(o, "hide_viewport", t >= off))
    flash = S.ball(f"{name}_flash", core, 0.12 + 0.9 * r, p1)
    S.size(flash, [(0.0, 0.0), (t0 - 0.01, 0.0), (t0 + 0.06, 1.0), (t1 - 0.1, 0.5), (t1, 0.0)])
    return flash


# ------------------------------------------------------------------ the fuel dispenser (geometric)
def pump(S, m, loc, nozzle_to, name="pump"):
    """A fuel dispenser on an island: tall body, display window, a drop pictogram, hose and nozzle that ends at `nozzle_to` (the car's filler). Object names start with `pump_`."""
    x, y, z = loc
    body = S.hero("big", "#C9CED4", rough=0.35, metal=0.1)
    dark = S.hero("small", "#2D2A2B", rough=0.5)
    glassm = tr.plain(f"{name}_screen", "#F6F2EE", rough=0.3)
    tr.rbox(f"{name}_island", (20.0, 12.0, 1.4), (x, y, z + 0.7), S.hero("big", "#E4E7EC", rough=0.5), bevel=0.3)
    tr.rbox(f"{name}_body", (9.0, 6.0, 20.0), (x, y, z + 11.4), body, bevel=0.8)
    tr.rbox(f"{name}_top", (10.0, 7.0, 2.4), (x, y, z + 22.6), dark, bevel=0.6)
    tr.rbox(f"{name}_screen", (6.0, 0.5, 3.6), (x, y - 3.1, z + 17.0), glassm, bevel=0.2)
    tr.rbox(f"{name}_panel", (6.0, 0.5, 5.0), (x, y - 3.1, z + 10.0), dark, bevel=0.2)
    S.ball(f"{name}_drop", S.accent, 1.1, (x, y - 3.5, z + 10.4), shape=(1, 0.3, 1.25))
    S.cone(f"{name}_dropTip", 0.85, 0.0, 1.6, (x, y - 3.5, z + 12.1), S.accent, rot=(math.radians(90), 0, 0))
    tr.rbox(f"{name}_holster", (2.0, 1.4, 3.0), (x + (4.6 if nozzle_to[0] > x else -4.6), y - 2.5, z + 12.5), dark, bevel=0.3)
    start = (x + (4.8 if nozzle_to[0] > x else -4.8), y - 3.0, z + 12.0)
    mid = ((start[0] + nozzle_to[0]) / 2, (y + nozzle_to[1]) / 2 - 3.0, z + 3.0)
    S.line(f"{name}_hose", [start, (start[0] + (nozzle_to[0] - start[0]) * 0.2, start[1] - 2, z + 6.0), mid, (nozzle_to[0] + 1.5, nozzle_to[1] - 3.0, nozzle_to[2] - 1.0), (nozzle_to[0], nozzle_to[1] - 1.0, nozzle_to[2])],
           0.55, dark, smooth=True)
    tr.rbox(f"{name}_grip", (3.6, 1.1, 1.6), (nozzle_to[0] + 0.5, nozzle_to[1] - 2.4, nozzle_to[2] + 0.2), dark, bevel=0.3)
    tr.rbox(f"{name}_spout", (0.9, 3.2, 0.9), (nozzle_to[0], nozzle_to[1] + 0.2, nozzle_to[2]), body, bevel=0.2)
    return start


def cage(S, t0, dt=1.0):
    return ry.cage(S, S.accent, t0, dt=dt)
