"""Rig of production 018 (why your voice sounds strange when recorded): the library skull (human-skull, one mesh, faces -Y) as speaker and as listener, a chunky phone with a record dot and level
bars, sound as emissive accent rings (air path), a bone glow plus climbing rings (bone path), ear pulses and a red zigzag for the false belief. Runs inside Blender.
Scene units are centimetres; the skull asset is 0.144 m tall, so K=180 gives a 26 cm skull. x right, y away from the camera, z up. The skull faces -Y at rest; rotating it by +90 degrees about z makes it face +x."""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Euler, Vector

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_rig as ar  # noqa: E402
import common as c  # noqa: E402
import setpiece as sp  # noqa: E402
import tape_rig as tr  # noqa: E402

K = 180.0
EPS = 1e-4
GLOW_MAX = 1.0
GLOW_EMIT = 0.3                                   # share of emission in the glow: a full emission mix floods the bone to a flat silhouette (draft 2026-11-10)
EAR = (0.043, 0.006, 0.066)                      # asset metres, the +x ear canal opening (mirror x for the other side)
MOUTH = (0.0, -0.062, 0.030)                     # asset metres, the front teeth
BONE = "#EAE0B8"
PHONE_TRIM = "#EDE6D3"
SPK = (-17.0, 0.0, 0.0)                          # the speaker skull faces +x
LIS = (22.0, 0.0, 0.0)                           # the listener skull faces -x
PHONE = (5.0, -14.0, 12.0)                      # the phone stands in front of the beam to the listener, turned a little toward the camera
PHONE_YAW = math.radians(-55.0)
SPK_YAW, LIS_YAW = math.radians(90.0), math.radians(-90.0)


def ease(k):
    k = min(1.0, max(0.0, k))
    return k * k * (3 - 2 * k)


# ------------------------------------------------------------------ the stage
def stage_set(S, x0=-70.0, x1=80.0):
    """Cream cutaway plate behind the cast and the ink plinth under it."""
    S.box("board", (x1 - x0 + 120.0, 1.0, 170.0), ((x0 + x1) / 2, 24.0, 55.0), S.plate_mat(), bevel=0.6)
    S.box("plinth", (x1 - x0, 44.0, 2.4), ((x0 + x1) / 2, 2.0, -1.2), S.ink, bevel=0.5)


# ------------------------------------------------------------------ the skull
def skull_material(S, hexc=None):
    """Bone: flat Principled in the hero's bone colour, mixed toward the accent emission by the Value node `vib` (0 = plain bone, 1 = lit in the accent)."""
    hexc = hexc or ((S.p or {}).get("hero") or {}).get("bone", BONE)
    m = S.hero("big", hexc, rough=0.55, coat=0.1)
    nt = m.node_tree
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    acc = next(n for n in S.accent.node_tree.nodes if n.type == "EMISSION")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = acc.inputs["Color"].default_value
    em.inputs["Strength"].default_value = acc.inputs["Strength"].default_value
    vib = nt.nodes.new("ShaderNodeValue")
    vib.name = "vib"
    vib.outputs[0].default_value = 0.0
    tint = nt.nodes.new("ShaderNodeMixRGB")                                  # the bone turns toward the accent by hue (the shading and relief stay) ...
    tint.inputs["Color1"].default_value = bsdf.inputs["Base Color"].default_value
    tint.inputs["Color2"].default_value = acc.inputs["Color"].default_value
    nt.links.new(vib.outputs[0], tint.inputs["Fac"])
    nt.links.new(tint.outputs["Color"], bsdf.inputs["Base Color"])
    lite = nt.nodes.new("ShaderNodeMath")                                    # ... and a little emission rides on top
    lite.operation = "MULTIPLY"
    lite.inputs[1].default_value = GLOW_EMIT
    nt.links.new(vib.outputs[0], lite.inputs[0])
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(lite.outputs[0], mix.inputs[0])
    nt.links.new(bsdf.outputs["BSDF"], mix.inputs[1])
    nt.links.new(em.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    return m


class Skull:
    def __init__(self, root, obj, mat, yaw):
        self.root, self.obj, self.mat, self.yaw = root, obj, mat, yaw
        self.nod_amp = 0.0

    def glow(self, k):
        self.mat.node_tree.nodes["vib"].outputs[0].default_value = max(0.0, min(1.0, k)) * GLOW_MAX

    def world(self, local_m):
        """World position of an asset-space point (metres): through the root's rotation and location, at scene scale."""
        r = self.root
        return Vector(r.rotation_euler.to_matrix() @ (Vector(local_m) * K)) + Vector(r.location)

    def mouth(self):
        return self.world(MOUTH)

    def ear(self, side=1):
        return self.world((side * EAR[0], EAR[1], EAR[2]))

    def pose(self, t, nods, amp=0.07):
        """Pitch the head a little at each time in `nods` (the skull stands for a head that speaks)."""
        n = sum(sp.pulse(t, t0, 0.35, amp) for t0 in nods)
        self.root.rotation_euler = (n, 0.0, self.yaw)


def load_skull(S, loc=SPK, yaw=SPK_YAW, mat=None, pop=None):
    h = ar.load(S, "human-skull", loc=loc, rot=(0, 0, yaw), k=K, pop=pop)
    mat = mat or skull_material(S)
    o = h.objs[0]
    o.data.materials.clear()
    o.data.materials.append(mat)
    return Skull(h.root, o, mat, yaw)


def clone_skull(S, src, loc=LIS, yaw=LIS_YAW, pop=None):
    """A linked copy of the loaded skull with its own bone material (so its glow never lights)."""
    root = S.empty("skull_b_root", loc, pop=pop)
    root.rotation_euler = (0, 0, yaw)
    o = src.obj.copy()
    o.name = "skull_b"
    bpy.context.scene.collection.objects.link(o)
    o.parent = root
    o.location, o.scale = src.obj.location.copy(), src.obj.scale.copy()
    mat = src.mat.copy()
    o.data = src.obj.data
    o.material_slots[0].link = "OBJECT"
    o.material_slots[0].material = mat
    return Skull(root, o, mat, yaw)


# ------------------------------------------------------------------ the phone
class Phone:
    def __init__(self, S, loc=PHONE, yaw=PHONE_YAW, name="phone", scale=1.0):
        hc = (S.p or {}).get("hero") or {}
        self.S = S
        trim = S.hero("housing", hc.get("phone_trim", PHONE_TRIM), rough=0.35, metal=0.15)
        loc = (loc[0], loc[1], loc[2] * scale)                                   # the phone stands on the plinth whatever its scale
        self.loc = loc
        self.root = S.empty(f"{name}_root", loc)
        self.root.rotation_euler = (0, 0, yaw)
        next(d for ob, d in S.items if ob is self.root)["base"] = (scale, scale, scale)
        r = self.root
        tr.rbox(f"{name}_body", (12.0, 1.6, 24.0), (0, 0, 0), trim, bevel=1.0, parent=r)
        screen = S.plate_mat(rough=0.4)                                          # a lit sky-blue screen (the plate colour): the teal level bars and the record dot read on it
        tr.rbox(f"{name}_screen", (10.4, 0.3, 21.4), (0, -0.85, -0.1), screen, bevel=0.5, parent=r)
        tr.cyl(f"{name}_cam", 0.6, 0.3, (3.8, -0.95, 10.2), trim, axis="Y", verts=16, parent=r)
        self.dot = tr.cyl(f"{name}_dot", 1.0, 0.3, (0, -1.1, 8.0), S.accent, axis="Y", verts=24, parent=r)
        self.dot.scale = (EPS, EPS, EPS)
        self.bars = []
        for j in range(5):
            b = tr.rbox(f"{name}_bar{j}", (1.7, 0.3, 1.0), ((j - 2) * 2.2, -1.0, -6.0), S.accent, bevel=0.3, parent=r)
            b.scale = (1.0, 1.0, EPS)
            self.bars.append(b)

    def set_dot(self, k):
        k = max(EPS, ease(k))
        self.dot.scale = (k, k, k)

    def set_bars(self, t, arrivals, live=1.0):
        """Each arriving ring kicks the five level bars (a short ripple across them); `live` scales the whole meter."""
        for j, b in enumerate(self.bars):
            h = sum(sp.pulse(t, a + 0.06 * j, 0.45) for a in arrivals)
            h = live * min(1.0, h) * (6.0 + 6.0 * (0.5 + 0.5 * math.sin(2.3 * j)))
            h = max(EPS, h)
            b.scale = (1.0, 1.0, h)
            b.location = (b.location[0], b.location[1], -8.0 + h / 2)


# ------------------------------------------------------------------ rings
class Pool:
    """n accent torus rings (major radius 1, scaled per frame). `put` places one; unused rings stay at EPS."""

    def __init__(self, S, n, name, parent=None, minor=0.16):
        self.objs = []
        for i in range(n):
            bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=minor, major_segments=56, minor_segments=10)
            o = bpy.context.object
            o.name = f"{name}_{i}"
            tr._finish(o, S.accent)
            o.visible_shadow = False
            o.scale = (EPS, EPS, EPS)
            if parent is not None:
                o.parent = parent
            self.objs.append(o)

    def put(self, i, loc, rot, scale):
        o = self.objs[i]
        o.location, o.rotation_euler = loc, rot
        o.scale = tuple(scale) if isinstance(scale, (tuple, list)) else (scale,) * 3

    def off(self, i):
        self.objs[i].scale = (EPS, EPS, EPS)


def aim(vec):
    """Euler rotation that points a torus's axis (local z) along vec."""
    return tuple(Vector(vec).normalized().to_track_quat("Z", "Y").to_euler())


def air(pool, t, emits, origin, target, speed, r0=2.6, grow=0.16, stop=None):
    """Rings leave `origin` at each time in `emits`, travel toward `target` at `speed`, widen with distance and are absorbed at `stop` (default: the target). Returns the arrival times."""
    o, d = Vector(origin), Vector(target) - Vector(origin)
    dist = stop if stop is not None else d.length
    d.normalize()
    rot = aim(d)
    arr = []
    for i, te in enumerate(emits):
        dd = speed * (t - te)
        arr.append(te + dist / speed)
        if i >= len(pool.objs):
            continue
        if dd < 0.0 or dd > dist:
            pool.off(i)
            continue
        fade = 1.0 - ease((dd - (dist - 2.5)) / 2.5)
        pool.put(i, tuple(o + d * dd), rot, max(EPS, (r0 + grow * dd) * fade) * ease(dd / 1.5 + 0.2))
    return arr


def profile(z_m):
    """Rough horizontal extent of the skull (fraction of its widest) at asset height z (metres): the dome narrows toward the crown, the jaw toward the chin."""
    return math.sqrt(max(0.0, 1.0 - ((z_m - 0.085) / 0.085) ** 2)) * 0.8 + 0.2


def climb(pool, t, emits, dur=1.3, z0=0.0, z1=0.15):
    """Bone rings: horizontal ellipses hugging the skull (children of its root) that climb from the jaw to the crown."""
    for i, te in enumerate(emits):
        if i >= len(pool.objs):
            break
        k = (t - te) / dur
        if k < 0.0 or k > 1.0:
            pool.off(i)
            continue
        z = z0 + (z1 - z0) * k
        p = profile(z) * 1.18
        rx, ry = 0.046 * K * p, 0.066 * K * p
        pool.put(i, (0.0, 0.0, z * K), (0, 0, 0), (max(EPS, rx), max(EPS, ry), max(EPS, (rx + ry) / 2 * 0.8)))
        fade = min(1.0, k / 0.12, (1.0 - k) / 0.2)
        pool.objs[i].scale = tuple(max(EPS, s * max(0.0, fade)) for s in pool.objs[i].scale)


def ear_pulse(pool, t, emits, side=1, dur=1.0, r0=0.8, r1=4.2):
    """Rings that spread on the skull's side at the ear canal (children of its root, axis along local x)."""
    for i, te in enumerate(emits):
        if i >= len(pool.objs):
            break
        k = (t - te) / dur
        if k < 0.0 or k > 1.0:
            pool.off(i)
            continue
        r = r0 + (r1 - r0) * ease(k)
        fade = min(1.0, k / 0.1, (1.0 - k) / 0.35)
        pool.put(i, (side * (EAR[0] * K + 0.4), EAR[1] * K, EAR[2] * K), (0, math.pi / 2, 0), max(EPS, r * max(0.0, fade)))


# ------------------------------------------------------------------ the false belief
def zigzag(S, a, b, n=9, amp=3.2, r=0.28, grow=(0.0, 1.0)):
    """A jagged red line from a to b: the voice as the phone is feared to hand it back."""
    pts = []
    A, B = Vector(a), Vector(b)
    for i in range(n + 1):
        p = A + (B - A) * (i / n)
        s = 0.0 if i in (0, n) else (amp if i % 2 else -amp) * (0.6 + 0.4 * math.sin(i * 2.1))
        pts.append((p.x, p.y, p.z + s))
    o = S.line("zig_line", pts, r, S.error, grow=grow, smooth=False)
    return o


def unspool(zig, k):
    """Retract a zigzag from its start (k 0 -> 1): the belief dissolving."""
    zig.data.bevel_factor_start = max(0.0, min(1.0, k))
