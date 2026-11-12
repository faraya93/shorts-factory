"""Rig of production 021 (how many times you would fold a sheet of paper to reach the Moon): a sheet that folds on a hinge, stacks of thin layered slabs, a tall layered paper column
(stripes by world height, so the layers stay put while it grows), a ridged snow-capped mountain, cloud puffs, the Moon (procedural craters), a star field, the sky-to-space backdrop
colour, a curved Earth limb, a long paper strip with a thick wad, and the sealed standing human-figure. Rigid parts are code primitives; the figure is a sealed library asset placed
through avion_rig.place. Runs inside Blender.
Scene units are centimetres of a toy scale (a person is about 16 units tall; a sheet is 16 x 22); x right, y away from the camera, z up. Driven per frame by the scene script."""
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import avion_rig as av  # noqa: E402
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

EPS = 1e-4
PAPER, EDGE, SEAM = "#E9E2D4", "#7A7060", "#B9B1A2"
SNOW, ROCK = "#F4F7FA", "#7A6F6A"
MOON, MARE = "#A9A7A3", "#7A7876"
SPACE = "#14121F"
FIG_K = 8.5                              # figure scale: 1.85 m mesh -> 15.7 units
STUDENT = ("#C68A62", "#D9483B", "#3A3F5C", "#EDEDED")
ease = av.ease
look = av.look


def smooth(a, b, t):
    return ease((t - a) / (b - a)) if b > a else (1.0 if t >= b else 0.0)


def vis(o, on):
    o.scale = (1.0, 1.0, 1.0) if on else (EPS, EPS, EPS)


class Mats:
    """Paper tones, the stage ink, the accent. The plate and board take the production's support colours."""

    def __init__(self, S):
        self.paper = S.hero("big", PAPER, rough=0.7, coat=0.0)
        edge_hex = "#7A7060"                                 # layer tone: far enough from the coral stage (gate: CIEDE2000 >= 20 once rendered)
        self.edge = S.hero("small", edge_hex, rough=0.7, coat=0.0)
        self.snow = tr.plain("snow", SNOW, rough=0.55)
        self.cloud = tr.plain("cloud_white", "#F6F2EE", rough=0.9)
        self.earth = tr.plain("earth_coral", "#EC9172", rough=0.85)
        self.star = tr.gold_emit("star", "#FFFFFF", 6.0)
        self.plate = S.plate_mat(rough=0.7)
        self.board = S.board_mat()
        self.ink = S.ink
        self.accent = S.accent
        self.red = S.error


def big(S, far=200000.0):
    """Long-distance sets: a far clip plane that does not cut the column."""
    S.stage.cam.data.clip_end = far


def sun(S, energy=3.2, rot=(math.radians(52), 0.0, math.radians(-38))):
    d = bpy.data.lights.new("sun", "SUN")
    d.energy = energy
    o = bpy.data.objects.new("sun", d)
    bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = rot
    return o


# ------------------------------------------------------------------ sheet and layers
class Sheet:
    """A sheet lying on z = 0 that folds in half on its centre line: one half stays, the other turns over on a hinge."""

    def __init__(self, m, name="sheet", w=16.0, d=22.0, t=0.35, loc=(0.0, 0.0, 0.0)):
        self.w, self.t = w, t
        self.root = tr.empty(f"{name}_root", loc)
        self.a = tr.rbox(f"{name}_a", (w / 2, d, t), (w / 4, 0, t / 2), m.paper, bevel=0.05, parent=self.root)
        self.pivot = tr.empty(f"{name}_pivot", (0, 0, t), parent=self.root)
        self.b = tr.rbox(f"{name}_b", (w / 2, d, t), (-w / 4, 0, -t / 2), m.paper, bevel=0.05, parent=self.pivot)

    def fold(self, k):
        self.pivot.rotation_euler = (0.0, math.pi * ease(k), 0.0)


def layers(m, n, w=16.0, d=22.0, t=1.6, loc=(0.0, 0.0, 0.0), name="layer"):
    """n thin slabs stacked on z = loc z, alternating paper and edge tone; slab i sits at z = i * t."""
    out = []
    for i in range(n):
        out.append(tr.rbox(f"{name}_{i}", (w, d, t * 0.94), (loc[0], loc[1], loc[2] + i * t + t / 2), m.paper if i % 2 == 0 else m.edge, bevel=0.08))
    return out


# ------------------------------------------------------------------ the column
def striped(name, c0, c1, pitch):
    """Paper tones alternating by WORLD height every `pitch` units: layers that stay in place while the object grows. The pitch is the node named `pitch`."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.7
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    val = nt.nodes.new("ShaderNodeValue")
    val.name = "pitch"
    val.outputs[0].default_value = pitch
    div = nt.nodes.new("ShaderNodeMath")
    div.operation = "DIVIDE"
    fl = nt.nodes.new("ShaderNodeMath")
    fl.operation = "FLOOR"
    md = nt.nodes.new("ShaderNodeMath")
    md.operation, md.inputs[1].default_value = "MODULO", 2.0
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = c.linear(c0)
    mix.inputs["B"].default_value = c.linear(c1)
    nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Z"], div.inputs[0])
    nt.links.new(val.outputs[0], div.inputs[1])
    nt.links.new(div.outputs[0], fl.inputs[0])
    nt.links.new(fl.outputs[0], md.inputs[0])
    nt.links.new(md.outputs[0], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    return mat


def column(m, name="col", w=5.0, d=6.5, loc=(0.0, 0.0, 0.0), pitch=1.0):
    """A box of unit height on z = loc z (origin at its foot): set scale z to the height each frame. Returns the object; `.pitch` is its pitch node."""
    me = bpy.data.meshes.new(f"column_{name}")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = (v.co.x * w, v.co.y * d, v.co.z + 0.5)
    bm.to_mesh(me)
    bm.free()
    mat = striped(f"column_mat_{name}", PAPER, "#D2C9B8", pitch)         # soft layer tone: the column must not outshout what stands beside it
    me.materials.append(mat)
    o = bpy.data.objects.new(f"column_{name}", me)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    return o


def set_pitch(o, pitch):
    o.data.materials[0].node_tree.nodes["pitch"].outputs[0].default_value = pitch


def set_height(o, h):
    o.scale = (1.0, 1.0, max(EPS, h))


# ------------------------------------------------------------------ mountain, clouds, moon, stars, sky
def _ridge(x, y, seed):
    r = random.Random(seed)
    v = 0.0
    for k in range(5):
        f = 0.045 * (1.9 ** k)
        v += (0.55 ** k) * abs(math.sin(f * x + r.uniform(0, 6.3)) * math.cos(f * 1.3 * y + r.uniform(0, 6.3)))
    return v


def mountain(name="mount", H=70.0, R=62.0, seed=3, loc=(0.0, 0.0, 0.0)):
    """A ridged snow-capped massif: three peaks on a round footprint, rock below and snow above a noisy snow line (colour by object height)."""
    rings, segs = 56, 150
    peaks = [(0.0, 0.0, H, R * 0.85), (-0.42 * R, 0.1 * R, H * 0.62, R * 0.55), (0.4 * R, -0.12 * R, H * 0.5, R * 0.5)]
    bm = bmesh.new()
    grid = []
    for j in range(rings + 1):
        r = R * j / rings
        row = []
        for i in range(segs):
            a = 2 * math.pi * i / segs
            x, y = r * math.cos(a), r * math.sin(a)
            z = 0.0
            for (px, py, ph, pr) in peaks:
                dd = math.hypot(x - px, y - py) + 5.0 * _ridge(x, y, seed)
                z = max(z, ph * max(0.0, 1.0 - dd / pr) ** 1.25)
            z += 2.2 * _ridge(x * 1.7, y * 1.7, seed + 9) * min(1.0, z / (0.25 * H))
            if j == rings:
                z = 0.0
            row.append(bm.verts.new((x, y, z)))
        grid.append(row)
    for j in range(rings):
        for i in range(segs):
            bm.faces.new((grid[j][i], grid[j][(i + 1) % segs], grid[j + 1][(i + 1) % segs], grid[j + 1][i]))
    me = bpy.data.meshes.new(f"{name}_mesh")
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    mat = bpy.data.materials.new(f"{name}_mat")
    mat.use_nodes = True
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.75
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    noise = nt.nodes.new("ShaderNodeTexNoise")
    noise.inputs["Scale"].default_value = 0.35
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = "ADD"
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation, mul.inputs[1].default_value = "MULTIPLY", H * 0.16
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.0, c.linear(ROCK)
    ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.62, c.linear(SNOW)
    nrm = nt.nodes.new("ShaderNodeMapRange")
    nrm.inputs["From Min"].default_value, nrm.inputs["From Max"].default_value = 0.0, H
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
    nt.links.new(tc.outputs["Object"], noise.inputs["Vector"])
    nt.links.new(noise.outputs["Fac"], mul.inputs[0])
    nt.links.new(sep.outputs["Z"], add.inputs[0])
    nt.links.new(mul.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], nrm.inputs["Value"])
    nt.links.new(nrm.outputs["Result"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    me.materials.append(mat)
    o = bpy.data.objects.new(f"{name}_main", me)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    return o


def clouds(S, m, n, centre, spread, seed=5, name="cloud"):
    """A scatter of flattened white puffs around `centre` (x, y, z), `spread` = (sx, sy, sz). Returns the root empty."""
    rnd = random.Random(seed)
    root = tr.empty(f"{name}_root", centre)
    for i in range(n):                                       # n puffs, each a lump of three overlapping balls
        cx, cy, cz = rnd.uniform(-spread[0], spread[0]), rnd.uniform(-spread[1], spread[1]), rnd.uniform(-spread[2], spread[2])
        for j, (dx, dz, k) in enumerate(((0.0, 0.0, 1.0), (-6.5, -1.0, 0.75), (6.0, -1.5, 0.8))):
            S.ball(f"{name}_{i}_{j}", m.cloud, rnd.uniform(5.5, 7.5) * k, (cx + dx, cy, cz + dz), shape=(1.2, 1.0, 0.85), parent=root)
    return root


def moon(S, name="moon", R=24.0, loc=(0.0, 0.0, 0.0), seed=2):
    """A grey cratered sphere: Voronoi craters as bump, dark mare patches from low-frequency noise."""
    mat = bpy.data.materials.new(f"{name}_mat")
    mat.use_nodes = True
    nt = mat.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Roughness"].default_value = 0.92
    tc = nt.nodes.new("ShaderNodeTexCoord")
    def craters(scale, reach):
        v = nt.nodes.new("ShaderNodeTexVoronoi")
        v.feature, v.distance = "F1", "EUCLIDEAN"
        v.inputs["Scale"].default_value = scale / R
        v.inputs["Randomness"].default_value = 1.0
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs["From Min"].default_value, mr.inputs["From Max"].default_value = 0.0, reach
        nt.links.new(tc.outputs["Object"], v.inputs["Vector"])
        nt.links.new(v.outputs["Distance"], mr.inputs["Value"])
        return mr.outputs["Result"]
    big_c, small_c = craters(3.4, 0.42), craters(10.0, 0.40)
    add = nt.nodes.new("ShaderNodeMath")
    add.operation = "ADD"
    half = nt.nodes.new("ShaderNodeMath")
    half.operation, half.inputs[1].default_value = "MULTIPLY", 0.35
    nt.links.new(small_c, half.inputs[0])
    nt.links.new(big_c, add.inputs[0])
    nt.links.new(half.outputs[0], add.inputs[1])
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 1.0
    bump.inputs["Distance"].default_value = R * 0.05
    mare = nt.nodes.new("ShaderNodeTexNoise")
    mare.inputs["Scale"].default_value = 1.1 / R
    mare.inputs["Detail"].default_value = 3.0
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position, ramp.color_ramp.elements[0].color = 0.42, c.linear(MARE)
    ramp.color_ramp.elements[1].position, ramp.color_ramp.elements[1].color = 0.58, c.linear(MOON)
    nt.links.new(tc.outputs["Object"], mare.inputs["Vector"])
    nt.links.new(add.outputs[0], bump.inputs["Height"])
    nt.links.new(mare.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], b.inputs["Base Color"])
    nt.links.new(bump.outputs["Normal"], b.inputs["Normal"])
    o = S.ball(f"{name}_main", mat, R, loc, seg=96)
    return o


def stars(S, m, n, centre_fn, k_fn, dist=900.0, seed=11):
    """n pinpoint emissive stars on a far hemisphere that follows the camera target; k_fn(t) -> 0..1 fades them in."""
    rnd = random.Random(seed)
    spots = []
    for _ in range(n):
        a, e = rnd.uniform(-1.3, 1.3), rnd.uniform(-0.25, 0.9)
        spots.append((dist * math.sin(a) * math.cos(e), dist * math.cos(a) * math.cos(e), dist * math.sin(e), rnd.uniform(0.5, 1.2)))
    src = S.ball("star_src", m.star, 1.6, (0, 0, 0))

    def fn(i, t):
        k = k_fn(t)
        if k <= 0.02:
            return None
        cx, cy, cz = centre_fn(t)
        x, y, z, s = spots[i]
        return ((cx + x, cy + y, cz + z), s * k)
    return S.swarm(n, src, fn)


class Sky:
    """The coral stage backdrop and its floor, blended to space: set(k) with k 0 = the stage, 1 = near-black ink."""

    def __init__(self, S):
        nt = S.stage.scene.world.node_tree
        self.ramp = next(n for n in nt.nodes if n.type == "VALTORGB")
        self.base = [tuple(e.color) for e in self.ramp.color_ramp.elements]
        self.floor = bpy.data.objects.get("floor")
        self.space = tuple(c.linear(SPACE)[:3]) + (1.0,)

    def set(self, k, hide_floor=False):
        for e, b in zip(self.ramp.color_ramp.elements, self.base):
            e.color = tuple(b[i] + (self.space[i] - b[i]) * k for i in range(4))
        if self.floor is not None:
            self.floor.hide_render = hide_floor


def earth(m, R=1500.0, name="earth"):
    """The ground as a big coral sphere whose top touches z = 0, so the horizon curves away when the camera is high."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=R, segments=128, ring_count=64, location=(0, 0, -R - 0.05))
    o = bpy.context.object
    o.name = f"{name}_main"
    for p in o.data.polygons:
        p.use_smooth = True
    o.data.materials.append(m.earth)
    return o


# ------------------------------------------------------------------ the strip and the figure
def strip(m, name="strip", w=5.0, loc=(0.0, 0.0, 0.0)):
    """A flat paper ribbon of unit length along +y from its start (origin there): set scale y to the length each frame."""
    me = bpy.data.meshes.new(f"{name}_mesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co = (v.co.x * w, v.co.y + 0.5, v.co.z * 0.3 + 0.15)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(m.paper)
    o = bpy.data.objects.new(f"{name}_main", me)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    return o


def figure(S, m, name, loc, rot_z=0.0, cols=None, k=FIG_K):
    """The sealed human-figure, standing, feet on loc z. Returns (root, objs); objects are named fig_<name>_<j>."""
    root, objs = av.place("human-figure", None, k, loc=loc, rot=(0, 0, rot_z))
    av.pose_armature(next(o for o in objs if o.type == "ARMATURE"), "pose_standing")
    if cols:
        av.tint_figure(objs, cols)
    for j, o in enumerate(objs):
        o.name = f"fig_{name}_{j}"
    return root, objs
