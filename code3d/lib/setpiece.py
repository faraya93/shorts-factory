"""Set-piece kit (2026-11-03 batch, productions 006-011): a small declarative layer over tape_rig / looks / machine_kit, so a scene script is a list of
EVENTS (things that appear, move, transform, with a moving camera) instead of hand-written frame maths. Runs inside Blender.

    S = sp.Shot(240)                      # begins the stage (look from scenes.json), reads the scene's word timings
    ball = S.ball("b", S.hero("big", "#E8A33D"), 1.0, (0, 0, 3), pop=(S.t("hola", default=1.0), 0.4))
    S.move(ball, [(0, (0, 0, 3)), (2, (4, 0, 3))])        # smooth keys; holds the ends
    S.cam([(0, (0, 0, 5), 34, 8, -10), (6, (2, 0, 4), 22, 14, 12)])   # t, target xyz, radius, elevation, azimuth: spline, never stops mid-way
    S.go()

Conventions: the camera looks along +y (x right, z up, smaller y is nearer the camera). Hero material NAMES are the gate roles of composition.py
(g_big, g_pin, g_mark, shell_y, rubber_k, blade ...): S.hero() uses them so the composition gate classifies the colours. Hiding = scale 1e-4 (never hide_render)."""
import math
import sys
from pathlib import Path

import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import machine_kit as mk  # noqa: E402
import pipeline_config as pcfg  # noqa: E402

ROLE = {"big": "g_big", "small": "g_pin", "mark": "g_mark", "housing": "shell_y", "rubber": "rubber_k", "blade": "blade", "water": "water", "plate": "plate",
        "board": "g_board", "ink": "ink"}
EPS = 1e-4


def lerp(a, b, k):
    if isinstance(a, (tuple, list)):
        return tuple(x + (y - x) * k for x, y in zip(a, b))
    return a + (b - a) * k


def interp(pts, t):
    """Smoothstep between keys [(t, v)...] (v scalar or tuple); holds the first/last value."""
    if t <= pts[0][0]:
        return pts[0][1]
    for (ta, va), (tb, vb) in zip(pts, pts[1:]):
        if t <= tb:
            k = (t - ta) / (tb - ta) if tb > ta else 1.0
            return lerp(va, vb, k * k * (3 - 2 * k))
    return pts[-1][1]


def spline(pts, t):
    """Cardinal (Catmull-Rom style) spline through keys [(t, tuple)...]: continuous velocity through the middle keys, eased at both ends."""
    if t <= pts[0][0]:
        return tuple(pts[0][1])
    if t >= pts[-1][0]:
        return tuple(pts[-1][1])
    n = len(pts)
    i = next(j for j in range(n - 1) if pts[j][0] <= t <= pts[j + 1][0])
    (t0, p0), (t1, p1) = pts[i], pts[i + 1]
    h = t1 - t0
    u = (t - t0) / h

    def tang(j):
        if j <= 0 or j >= n - 1:
            return (0.0,) * len(p0)
        (ta, pa), (tb, pb) = pts[j - 1], pts[j + 1]
        return tuple((y - x) / (tb - ta) for x, y in zip(pa, pb))
    m0, m1 = tang(i), tang(i + 1)
    h00, h10, h01, h11 = 2 * u ** 3 - 3 * u ** 2 + 1, u ** 3 - 2 * u ** 2 + u, -2 * u ** 3 + 3 * u ** 2, u ** 3 - u ** 2
    return tuple(h00 * a + h10 * h * ma + h01 * b + h11 * h * mb for a, b, ma, mb in zip(p0, p1, m0, m1))


def pulse(t, t0, dur=0.4, amp=1.0):
    """0 before t0, then a decaying bump (a heartbeat / impact)."""
    if t < t0:
        return 0.0
    k = (t - t0) / dur
    return amp * math.exp(-3.0 * k) * math.sin(min(k, 1.0) * math.pi) if k <= 1.0 else 0.0


class Shot:
    def __init__(self, default_slot: int, floor_z: float = -1.2, plinth: bool = False):
        self.args, self.production, self.stage, self.m, self.SLOT = tr.begin(default_slot, floor_z=floor_z)
        self.scene_no = int(pcfg.script_stem().rsplit("_", 1)[-1])
        self.name = pcfg.script_stem().replace("_", "-")
        if self.args.get("cpu"):                                                    # previews that must not touch the GPU while a final render runs
            sc = self.stage.scene
            sc.render.engine, sc.cycles.device, sc.cycles.samples, sc.cycles.use_denoising = "CYCLES", "CPU", 10, False
            sc.render.threads_mode, sc.render.threads, sc.render.resolution_percentage = "FIXED", 4, 40
        self.T = self.SLOT / c.FPS
        self.W = mk.Words(self.production, self.scene_no)
        self.p = __import__("looks").current() or {}
        self.items, self.fns, self.camkeys, self.lines = [], [], None, []
        if plinth:
            self.plinth()

    # ------------------------------------------------------------------ time and look
    def t(self, word, k=0, default=0.0):
        return self.W.t(word, k, default)

    def hero(self, role, hex_color, rough=0.45, metal=0.0, coat=0.15, alpha=None):
        mat = tr.plain(ROLE.get(role, role), hex_color, rough=rough, metallic=metal, coat=coat)
        if alpha is not None:
            mat.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = alpha
            mat.surface_render_method = "BLENDED"
        return mat

    def glass(self, hex_color, alpha=0.5, rough=0.08, name="water"):
        return self.hero(name, hex_color, rough=rough, coat=0.0, alpha=alpha)

    def emit(self, hex_color, strength=2.0, name="emit"):
        return tr.gold_emit(name, hex_color, strength)

    @property
    def accent(self):
        return self.m.gold

    @property
    def error(self):
        return self.m.red

    @property
    def ink(self):
        return self.m.table

    def plate_mat(self, rough=0.5):
        return tr.plain("plate", self.p.get("support_plate", "#EEEEEE"), rough=rough)

    def board_mat(self, rough=0.7):
        return tr.plain("g_board", self.p.get("support_board", "#DDDDDD"), rough=rough)

    def plinth(self, w=26.0, d=8.0, h=1.2):
        return tr.rbox("plinth", (w, d, h), (0, 0, -h / 2 + 0.0), self.m.table, bevel=0.3)

    # ------------------------------------------------------------------ registration of animated things
    def reg(self, o, loc=None, rot=None, sc=None, pop=None, gone=None):
        d = {"loc": loc, "rot": rot, "sc": sc, "pop": pop, "gone": gone, "base": tuple(o.scale)}
        self.items.append((o, d))
        if pop is not None:
            o.scale = tuple(b * EPS for b in o.scale)
        return o

    def move(self, o, keys):
        next(d for ob, d in self.items if ob is o)["loc"] = keys
        return o

    def spin(self, o, keys):
        next(d for ob, d in self.items if ob is o)["rot"] = keys
        return o

    def size(self, o, keys):
        next(d for ob, d in self.items if ob is o)["sc"] = keys
        return o

    def pop(self, o, t0, dur=0.4):
        d = next(d for ob, d in self.items if ob is o)
        d["pop"] = (t0, dur)
        return o

    def gone(self, o, t1, dur=0.3):
        d = next(d for ob, d in self.items if ob is o)
        d["gone"] = (t1, dur)
        return o

    def every_frame(self, fn):
        self.fns.append(fn)

    # ------------------------------------------------------------------ primitives (all return the registered object)
    def box(self, name, size, loc, mat, bevel=0.12, rot=(0, 0, 0), parent=None, **tk):
        return self.reg(tr.rbox(name, size, loc, mat, bevel=bevel, rot=rot, parent=parent), **tk)

    def ball(self, name, mat, r, loc=(0, 0, 0), shape=(1, 1, 1), parent=None, seg=24, **tk):
        return self.reg(mk.sphere(name, mat, r, loc, shape=shape, parent=parent, seg=seg), **tk)

    def cyl(self, name, radius, length, loc, mat, axis="Z", parent=None, verts=48, bevel=0.0, **tk):
        return self.reg(tr.cyl(name, radius, length, loc, mat, axis=axis, parent=parent, verts=verts, bevel=bevel), **tk)

    def cone(self, name, r1, r2, length, loc, mat, rot=(0, 0, 0), verts=32, parent=None, **tk):
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r1, radius2=r2, depth=length, location=loc, rotation=rot)
        o = bpy.context.object
        o.name = name
        tr._finish(o, mat)
        if parent:
            o.parent = parent
        return self.reg(o, **tk)

    def torus(self, name, major, minor, loc, mat, rot=(0, 0, 0), parent=None, **tk):
        bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=48, minor_segments=16, location=loc, rotation=rot)
        o = bpy.context.object
        o.name = name
        tr._finish(o, mat)
        if parent:
            o.parent = parent
        return self.reg(o, **tk)

    def empty(self, name, loc=(0, 0, 0), parent=None, **tk):
        return self.reg(tr.empty(name, loc, parent), **tk)

    def clone(self, src, name=None):
        """Linked duplicate (shares the mesh): cheap swarms. Starts hidden; a swarm function places it."""
        base = next(d for ob, d in self.items if ob is src)["base"]
        o = src.copy()
        if name:
            o.name = name
        bpy.context.scene.collection.objects.link(o)
        o.parent = None
        o.scale = tuple(EPS * b for b in base)
        self.items.append((o, {"loc": None, "rot": None, "sc": None, "pop": None, "gone": None, "base": base, "sw": None}))
        return o

    def swarm(self, n, src, fn):
        """n linked copies of `src`; fn(i, t) -> (xyz, scale) or (xyz, scale, rot) or None (hidden). The template `src` itself is hidden for good."""
        objs = [self.clone(src, f"{src.name}_{i}") for i in range(n)]
        next(d for ob, d in self.items if ob is src)["pop"] = (1e9, 1.0)
        mine = [d for ob, d in self.items if ob in objs]

        def upd(t):
            for i, (o, d) in enumerate(zip(objs, mine)):
                d["sw"] = fn(i, t)
        self.fns.insert(0, upd)
        return objs

    def line(self, name, pts, r, mat, grow=None, smooth=True, loc=(0, 0, 0)):
        """Tube along 3D points; grow=(t0, t1) draws it from start to end over that time (bevel factor); None = fully drawn."""
        cu = bpy.data.curves.new(name, "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = r, 3, True
        sp = cu.splines.new("POLY" if not smooth else "NURBS")
        sp.points.add(len(pts) - 1)
        for pnt, q in zip(sp.points, pts):
            pnt.co = (q[0], q[1], q[2], 1.0)
        if smooth:
            sp.order_u, sp.use_endpoint_u = min(4, len(pts)), True
        o = bpy.data.objects.new(name, cu)
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        cu.materials.append(mat)
        if grow:
            cu.bevel_factor_end = 0.0
            self.lines.append((cu, grow))
        return o

    def heightfield(self, name, mat, size=(8.0, 8.0), n=(120, 120), loc=(0, 0, 0)):
        return HeightField(self, name, mat, size, n, loc)

    # ------------------------------------------------------------------ camera
    def cam(self, wps):
        """wps = [(t, (tx, ty, tz), radius, elevation_deg, azimuth_deg), ...]"""
        self.camkeys = [(w[0], (*w[1], w[2], w[3], w[4])) for w in wps]

    # ------------------------------------------------------------------ run
    def _update(self, scene_, *_):
        t = scene_.frame_current / c.FPS
        for fn in self.fns:
            fn(t)
        for o, d in self.items:
            b = d["base"]
            if "sw" in d:                                                             # swarm member: placed by its function (or hidden)
                r = d["sw"]
                if r is None:
                    o.scale = tuple(EPS * x for x in b)
                else:
                    o.location = r[0]
                    k = r[1]
                    o.scale = tuple(max(EPS * x, x * k) for x in b) if not isinstance(k, (tuple, list)) else tuple(max(EPS * x, x * kk) for x, kk in zip(b, k))
                    if len(r) > 2:
                        o.rotation_euler = r[2]
                continue
            if d["loc"] is not None:
                o.location = interp(d["loc"], t)
            if d["rot"] is not None:
                o.rotation_euler = interp(d["rot"], t)
            k = interp(d["sc"], t) if d["sc"] is not None else 1.0
            if d["pop"] is not None:
                t0, dur = d["pop"]
                f = EPS if t < t0 else max(EPS, tr.back((t - t0) / dur))
                k = tuple(kk * f for kk in k) if isinstance(k, (tuple, list)) else k * f
            if d["gone"] is not None and t >= d["gone"][0]:
                f = max(EPS, 1.0 - c.smooth(d["gone"][0], d["gone"][0] + d["gone"][1], t))
                k = tuple(kk * f for kk in k) if isinstance(k, (tuple, list)) else k * f
            o.scale = tuple(max(EPS * x, x * kk) for x, kk in zip(b, k)) if isinstance(k, (tuple, list)) else tuple(max(EPS * x, x * k) for x in b)
        for cu, (t0, t1) in self.lines:
            cu.bevel_factor_end = c.smooth(t0, t1, t)
        if self.camkeys:
            v = spline(self.camkeys, t)
            tr.look(self.stage, (v[0], v[1], v[2]), v[3], v[4], v[5])
        if self.args.get("debug"):
            cam = self.stage.cam
            print(f"[dbg] t={t:.2f} cam={tuple(round(x, 1) for x in cam.location)} rot={tuple(round(x, 2) for x in cam.rotation_euler)}")
            for o, d in self.items[:6]:
                print(f"[dbg]   {o.name} loc={tuple(round(x, 1) for x in o.matrix_world.translation)} scale={tuple(round(x, 3) for x in o.scale)}")

    def go(self):
        self.stage.run(self._update, self.args, self.SLOT, self.name)


class HeightField:
    """A subdivided plane whose heights are rewritten per frame: update(fn) with fn(X, Y, t) -> Z (numpy arrays). Smooth shaded."""

    def __init__(self, shot, name, mat, size, n, loc):
        self.nx, self.ny = n
        xs = np.linspace(-size[0] / 2, size[0] / 2, self.nx)
        ys = np.linspace(-size[1] / 2, size[1] / 2, self.ny)
        self.X, self.Y = np.meshgrid(xs, ys)
        mesh = bpy.data.meshes.new(name)
        verts = np.stack([self.X.ravel(), self.Y.ravel(), np.zeros(self.X.size)], axis=1)
        faces = [(j * self.nx + i, j * self.nx + i + 1, (j + 1) * self.nx + i + 1, (j + 1) * self.nx + i) for j in range(self.ny - 1) for i in range(self.nx - 1)]
        mesh.from_pydata(verts.tolist(), [], faces)
        mesh.update()
        for poly in mesh.polygons:
            poly.use_smooth = True
        self.obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(self.obj)
        self.obj.location = loc
        mesh.materials.append(mat)
        shot.reg(self.obj)

    def update(self, Z):
        co = np.stack([self.X.ravel(), self.Y.ravel(), np.asarray(Z, dtype=np.float64).ravel()], axis=1).astype(np.float32)
        self.obj.data.vertices.foreach_set("co", co.ravel())
        self.obj.data.update()
