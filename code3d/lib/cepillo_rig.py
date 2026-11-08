"""Rig of production 012 (toothbrush beside the toilet): the bathroom set from library assets, the bowl water sheet and the droplet beads. Runs inside Blender. Scene units are centimetres (assets K=100)."""
import math
import sys
from pathlib import Path

import bmesh
import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_rig as ar  # noqa: E402
import common as c  # noqa: E402
import real_kit as rk  # noqa: E402

CUP_AT = (63.0, 28.0, 81.8)
BOWL = (0.0, -10.8)
WATER_Z = 30.0
RIM_Z = 45.0
HOLDER_AT = (-38.0, 8.0, 0.0)


def retint(mat, hex_color, role, rough=0.25, coat=0.4):
    """Named role + flat colour. The library materials drive Base Color from textures, so the link is cut first (asset_rig.retint only sets the default value)."""
    b = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    for l in list(b.inputs["Base Color"].links):
        mat.node_tree.links.remove(l)
    for name in ("Roughness", "Metallic"):
        for l in list(b.inputs[name].links):
            mat.node_tree.links.remove(l)
    b.inputs["Base Color"].default_value = c.linear(hex_color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = 0.0
    for l in list(b.inputs["Transmission Weight"].links):
        mat.node_tree.links.remove(l)
    b.inputs["Transmission Weight"].default_value = 0.0                        # the source cup is glass; opaque here (playbook: no nested transmission)
    b.inputs["Coat Weight"].default_value = coat
    mat.name = role
    return mat


def tiled_wall(S, hexc):
    m = S.board_mat(0.55)
    nt = m.node_tree
    b = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Rotation"].default_value = (math.pi / 2, 0, 0)
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.offset = 0.0
    br.inputs["Color1"].default_value = br.inputs["Color2"].default_value = c.linear(hexc)
    br.inputs["Mortar"].default_value = c.linear("#D9E6E4")
    br.inputs["Scale"].default_value = 1.0
    br.inputs["Mortar Size"].default_value = 0.35
    br.inputs["Mortar Smooth"].default_value = 0.1
    br.inputs["Brick Width"].default_value = 25.0
    br.inputs["Row Height"].default_value = 25.0
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    nt.links.new(mp.outputs["Vector"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    return S.box("wall", (420.0, 4.0, 320.0), (0.0, 36.5, 160.0), m, bevel=0.2)


class Set:
    pass


def bathroom(S, colours, cup_at=CUP_AT):
    """Toilet (lid open), sink against the wall, cup of toothbrushes on the sink's ledge, toilet brush in its holder, tiled wall. Returns the parts the scenes animate."""
    B = Set()
    B.wall = tiled_wall(S, S.p.get("support_board", "#3F7C85"))
    t = ar.load(S, "toilet")
    B.lid = next(o for o in t.objs if o.name.startswith("toilet_lid"))
    for o in t.objs:
        if o.name.startswith("toilet_body"):
            retint(o.material_slots[0].material, colours["ceramic"], "g_big", rough=0.14, coat=0.6)
        elif o.name.startswith(("toilet_seat", "toilet_lid")):
            retint(o.material_slots[0].material, colours["seat"], "shell_y", rough=0.25, coat=0.4)
    s = ar.load(S, "bathroom-sink", loc=(62.0, 22.0, 0.0), rot=(0, 0, math.pi))
    for o in s.objs:
        if o.name.startswith("sink_body"):
            retint(o.material_slots[0].material, colours["ceramic"], "g_big", rough=0.14, coat=0.6)
    h = ar.load(S, "toothbrush-in-cup", loc=cup_at)
    B.cup_root = h.root
    for o in h.objs:
        if o.name.startswith("cup"):
            retint(o.material_slots[0].material, colours["cup"], "rubber_k", rough=0.3, coat=0.5)
        else:
            retint(o.material_slots[0].material, colours["toothbrush"], "g_pin", rough=0.3, coat=0.3)
            bris = o.material_slots[len(o.material_slots) - 1].material
            retint(bris, "#F4F4F2", "foam", rough=0.5, coat=0.0)
    B.brush_b = next(o for o in h.objs if o.name.startswith("brush_b"))
    tb = ar.load(S, "toilet-brush", loc=HOLDER_AT)
    B.tb_root = S.empty("tb_brush_root", HOLDER_AT)
    for o in tb.objs:
        if o.name.startswith("brush"):
            o.parent = B.tb_root
            retint(o.material_slots[0].material, colours["brush"], "g_mark", rough=0.35, coat=0.2)
            retint(o.material_slots[len(o.material_slots) - 1].material, "#F0EEE8", "foam", rough=0.6, coat=0.0)
        else:
            retint(o.material_slots[0].material, colours["brush"], "g_mark", rough=0.35, coat=0.2)
    return B


def head_of(obj, top=3.2):
    """World centre of the top of a toothbrush (the head): macro camera target."""
    bpy.context.view_layer.update()
    pts = [obj.matrix_world @ v.co for v in obj.data.vertices]
    zmax = max(p.z for p in pts)
    near = [p for p in pts if p.z > zmax - top]
    return tuple(sum((p for p in near), Vector()) / len(near))


def lid_angle(B, deg):
    B.lid.rotation_euler.x = math.radians(deg)


class Water:
    """The bowl's water: a shallow ellipse (one transmission layer over the ceramic), height rewritten per frame. update(fn) with fn(R, TH, t) -> dz, R in 0..1."""

    def __init__(self, S, a=8.5, b=15.0, z=WATER_Z, centre=BOWL, rings=46, segs=120):
        self.z = z
        rr = np.linspace(0.02, 1.0, rings)
        th = np.linspace(0, 2 * math.pi, segs, endpoint=False)
        self.R, self.TH = np.meshgrid(rr, th, indexing="ij")
        self.X = centre[0] + a * self.R * np.cos(self.TH)
        self.Y = centre[1] + b * self.R * np.sin(self.TH)
        v = np.stack([self.X.ravel(), self.Y.ravel(), np.full(self.X.size, z)], axis=1)
        f = [(i * segs + j, i * segs + (j + 1) % segs, (i + 1) * segs + (j + 1) % segs, (i + 1) * segs + j) for i in range(rings - 1) for j in range(segs)]
        f.append(tuple(range(segs - 1, -1, -1)))
        me = bpy.data.meshes.new("bowl_water")
        me.from_pydata(v.tolist(), [], f)
        me.update()
        for p in me.polygons:
            p.use_smooth = True
        self.obj = bpy.data.objects.new("bowl_water", me)
        bpy.context.scene.collection.objects.link(self.obj)
        me.materials.append(rk.water("clear_water", tint="#E6F6FA"))
        self.obj.visible_shadow = False
        S.reg(self.obj)
        n = 96                                                                 # pale floor under the surface: refraction otherwise sees the unlit trap and the water goes dark
        ring = [(centre[0] + a * math.cos(2 * math.pi * i / n), centre[1] + b * math.sin(2 * math.pi * i / n), z - 2.2) for i in range(n)]
        fl = bpy.data.meshes.new("bowl_floor")
        fl.from_pydata(ring, [], [tuple(range(n))])
        fl.update()
        floor = bpy.data.objects.new("bowl_floor", fl)
        bpy.context.scene.collection.objects.link(floor)
        m, _nt, bf, _o = rk._principled("clear_floor")
        bf.inputs["Base Color"].default_value = c.linear("#E4F0F1")
        bf.inputs["Emission Color"].default_value = c.linear("#E4F0F1")
        bf.inputs["Emission Strength"].default_value = 0.25
        fl.materials.append(m)
        S.reg(floor)

    def update(self, dz):
        co = np.stack([self.X.ravel(), self.Y.ravel(), (self.z + np.asarray(dz)).ravel()], axis=1).astype(np.float32)
        self.obj.data.vertices.foreach_set("co", co.ravel())
        self.obj.data.update()


def turbulence(R, TH, t, amp):
    """Rim jets feeding a swirl: spiral waves running inward, strongest near the wall."""
    a = np.sin(14.0 * R - 9.0 * t + 3.0 * TH) * (0.35 + 0.65 * R) + 0.6 * np.sin(23.0 * R + 13.0 * t - 5.0 * TH) * R + 0.4 * np.sin(6.0 * TH + 7.0 * t) * R ** 2
    return amp * a


class Beads:
    """Up to n droplets in ONE mesh, rewritten per frame (thousands of objects would cost more than the render). set(xyz, radii): radii 0 collapses a bead."""

    def __init__(self, S, name, n, mat):
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
        self.unit = np.array([v.co[:] for v in bm.verts], dtype=np.float32)
        tris = [tuple(v.index for v in f.verts) for f in bm.faces]
        bm.free()
        self.n, nv = n, len(self.unit)
        me = bpy.data.meshes.new(name)
        verts = np.zeros((n * nv, 3))
        faces = [tuple(i * nv + x for x in f) for i in range(n) for f in tris]
        me.from_pydata(verts.tolist(), [], faces)
        me.update()
        for p in me.polygons:
            p.use_smooth = True
        self.obj = bpy.data.objects.new(name, me)
        bpy.context.scene.collection.objects.link(self.obj)
        me.materials.append(mat)
        self.obj.visible_shadow = False
        S.reg(self.obj)

    def set(self, xyz, radii):
        co = (xyz[:, None, :] + radii[:, None, None] * self.unit[None, :, :]).astype(np.float32)
        self.obj.data.vertices.foreach_set("co", co.reshape(-1))
        self.obj.data.update()
        self.obj.data.update_tag()


def bead_mat(name="clear_drops", hex_color="#DDF1F7", emit=0.15):
    m = rk.emissive(name, hex_color, 1.0) if False else None
    m, nt, b, _out = rk._principled(name)
    b.inputs["Base Color"].default_value = c.linear(hex_color)
    b.inputs["Roughness"].default_value = 0.06
    b.inputs["Coat Weight"].default_value = 1.0
    b.inputs["Emission Color"].default_value = c.linear(hex_color)
    b.inputs["Emission Strength"].default_value = emit
    return m


class Plume:
    """The droplets' life as a deterministic function: rise (u 0..1), hang (drift t), settle (u toward targets). All positions in cm; the same seed gives the same cloud in every scene."""

    def __init__(self, n, seed=12, flat=1.0):
        r = np.random.default_rng(seed)
        self.n = n
        self.th = r.uniform(0, 2 * np.pi, n)
        self.rad = np.sqrt(r.uniform(0, 1, n))
        self.H = 40.0 + 130.0 * r.uniform(0, 1, n) ** 1.6
        self.delay = r.uniform(0, 0.28, n)
        self.size = r.uniform(0.32, 0.8, n)
        self.phase = r.uniform(0, 2 * np.pi, n)
        self.flat = flat
        self.tint = r.uniform(0, 1, n) < 0.3
        self.r = r

    def rise(self, u):
        k = np.clip((u - self.delay) / (1.0 - self.delay), 0.0, 1.0)
        h = self.H * (1.0 - np.exp(-3.4 * k)) / (1.0 - np.exp(-3.4))
        z = WATER_Z + 2.0 + h
        spread = 6.0 + 0.34 * np.clip(z - RIM_Z, 0.0, None)
        x = BOWL[0] + self.rad * np.cos(self.th) * spread + 1.6 * np.sin(self.phase + z * 0.09)
        y = BOWL[1] + (self.rad * np.sin(self.th) * spread * self.flat + 1.6 * np.cos(self.phase + z * 0.07) * self.flat)
        return np.stack([x, y, z], axis=1), k > 0.0

    def hang(self, t):
        p, _ = self.rise(np.ones(self.n))
        p = p.copy()
        p[:, 0] += 3.0 * np.sin(self.phase + 0.5 * t)
        p[:, 1] += 2.0 * np.cos(self.phase * 1.3 + 0.4 * t)
        p[:, 2] += 2.2 * np.sin(self.phase * 0.7 + 0.6 * t)
        return p

    def settle(self, start, target, u):
        k = np.clip(u, 0.0, 1.0) ** 2
        p = start + (target - start) * k[:, None]
        p[:, 0] += (1 - k) * 2.0 * np.sin(self.phase + u * 8.0)
        return p

    def landing(self, head):
        """Where each droplet ends: 25 % the seat ring, 15 % the bristles, the rest the floor around the bowl."""
        n = self.n
        c_ = self.r.uniform(0, 1, n)
        t = np.zeros((n, 3))
        a = self.r.uniform(0, 2 * np.pi, n)
        seat = c_ < 0.25
        spread = self.r.uniform(0.92, 1.28, n)
        t[seat] = np.stack([BOWL[0] + 13.5 * spread[seat] * np.cos(a[seat]), BOWL[1] + 17.0 * spread[seat] * np.sin(a[seat]), np.full(seat.sum(), RIM_Z + 2.0)], axis=1)
        br = (c_ >= 0.25) & (c_ < 0.40)
        t[br] = np.array(head) + self.r.uniform(-1.3, 1.3, (br.sum(), 3))
        fl = c_ >= 0.40
        rad = self.r.uniform(22, 95, fl.sum())
        t[fl] = np.stack([BOWL[0] + rad * np.cos(a[fl]), BOWL[1] - 8.0 + rad * 0.45 * np.sin(a[fl]), np.full(fl.sum(), 0.3)], axis=1)
        return t, seat, br, fl
