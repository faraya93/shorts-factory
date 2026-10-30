"""Hero rig for the magnets video (imanes-coral): a bar magnet (four blocks so a cut can recolour the halves), paper clips, an aluminium can,
a copper coin, a stainless bar, a retort-style stand and an iron-filings field. Hard surfaces only, no people. Coral look: the stage is the background only;
the support board / plinth / hero colours come from the production (looks + scenes.json hero_colours).
World: camera looks along +y, x right, z up. Everything lives near y = 0 in the XZ plane."""
import math
import random
import sys
from pathlib import Path

import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

BAR_L, BAR_H, BAR_D = 5.0, 1.15, 1.15          # bar magnet size (x, z, y)
BLK = BAR_L / 4
STEEL, ALU, COPPER, STAINLESS = "#8E9DB4", "#D5DAE2", "#8A4421", "#4E586A"
N_HEX, S_HEX = "#2F63D6", "#F5D26B"          # hero colours: N pole cobalt, S pole butter yellow (cream merged with the board: gate 4.5)
FALLBACK_INK, FALLBACK_BOARD = "#1E1E22", "#CFC1A6"


def materials():
    import looks
    p = looks.current()
    return {"ink": tr.plain("ink", p["plinth"] if p else FALLBACK_INK, rough=0.55),
            "board": tr.plain("g_board", p["support_board"] if p else FALLBACK_BOARD, rough=0.7),
            "n": tr.plain("mag_n", N_HEX, rough=0.35, coat=0.2), "s": tr.plain("mag_s", S_HEX, rough=0.35, coat=0.2),
            "steel": tr.plain("blade", STEEL, rough=0.35, metallic=0.25), "alu": tr.plain("alu", ALU, rough=0.3, metallic=0.25),
            "copper": tr.plain("copper", COPPER, rough=0.4, metallic=0.2), "stainless": tr.plain("stainless", STAINLESS, rough=0.3, metallic=0.25),
            "filings": tr.plain("filings", ((__import__("looks").current() or {}).get("plinth", "#222230")), rough=0.5)}


def clip_path(w=0.8, length=2.0, d=0.16):
    """Gem paper-clip centre line (x, z): four vertical runs joined by three semicircles."""
    xs = [-w / 2, w / 2, -(w / 2 - d), (w / 2 - 2 * d)]
    z_top, z_bot = length / 2 - w / 2, -length / 2 + w / 2
    pts = [(xs[0], -0.1 * length)]
    def arc(x0, x1, zc, up):
        r = abs(x1 - x0) / 2
        cx = (x0 + x1) / 2
        return [(cx + (x0 - cx) * math.cos(a), zc + (1 if up else -1) * abs(x0 - cx) * math.sin(a)) for a in np.linspace(0, math.pi, 16)[1:]]
    pts += [(xs[0], z_top)]
    pts += arc(xs[0], xs[1], z_top, True)
    pts += [(xs[1], z_bot)]
    pts += arc(xs[1], xs[2], z_bot, False)
    zt3 = z_top - 0.3
    pts += [(xs[2], zt3)]
    pts += arc(xs[2], xs[3], zt3, True)
    pts += [(xs[3], -0.25 * length)]
    return pts


def make_clip(name, material, wire=0.075, scale=1.0):
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth, cu.bevel_resolution = wire, 4
    sp = cu.splines.new("POLY")
    pts = clip_path()
    sp.points.add(len(pts) - 1)
    for p, (x, z) in zip(sp.points, pts):
        p.co = (x * scale, 0.0, z * scale, 1.0)
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    cu.materials.append(material)
    root = tr.empty(name + "_root")
    o.parent = root
    return root


class Magnet:
    """A bar magnet of four blocks along local x; (b0 b1 | b2 b3) = N N | S S. `halves(cut)` recolours so each half is a full magnet after the cut."""

    def __init__(self, name, mats, length=BAR_L, thick=1.0):
        self.mats, self.name, self.thick = mats, name, thick
        self.root = tr.empty(name + "_root")
        blk = length / 4
        self.blocks = []
        for i in range(4):
            mat = mats["n"] if i < 2 else mats["s"]
            self.blocks.append(tr.rbox(f"{name}_b{i}", (blk * 0.995, BAR_D * thick, BAR_H * thick), ((i - 1.5) * blk, 0, 0), mat, bevel=0.1, parent=self.root))
        self.length = length

    def set_halves_cut(self, cut: bool) -> None:
        """After the cut each half carries both poles: block 1 turns S, block 2 turns N."""
        m = self.mats
        self.blocks[1].data.materials[0] = m["s"] if cut else m["n"]
        self.blocks[2].data.materials[0] = m["n"] if cut else m["s"]

    def place(self, x, z, rot_z=0.0, rot_y=0.0):
        self.root.location = (x, 0.0, z)
        self.root.rotation_euler = (0.0, rot_y, rot_z)

    def split(self, gap):
        """Move the two halves apart along x (gap in BU between the halves' inner faces)."""
        for i, b in enumerate(self.blocks):
            blk = self.length / 4
            b.location.x = (i - 1.5) * blk + (-gap / 2 if i < 2 else gap / 2)


def make_can(name, mats, x, z, r=0.95, h=3.4):
    root = tr.empty(name + "_root", (x, 0.0, z))
    tr.cyl(name + "_body", r, h, (0, 0, 0), mats["alu"], axis="Z", parent=root, verts=64, bevel=0.06)
    tr.cyl(name + "_lid", r * 0.86, 0.12, (0, 0, h / 2 + 0.04), mats["alu"], axis="Z", parent=root, verts=64, bevel=0.03)
    tr.cyl(name + "_tab", 0.2, 0.06, (0.2, 0, h / 2 + 0.12), mats["stainless"], axis="Z", parent=root, verts=24)
    return root


def make_coin(name, mats, x, z, r=1.0):
    root = tr.empty(name + "_root", (x, 0.0, z))
    tr.cyl(name + "_disc", r, 0.28, (0, 0, 0), mats["copper"], axis="Y", parent=root, verts=64, bevel=0.05)
    tr.cyl(name + "_ring", r * 0.72, 0.1, (0, -0.16, 0), mats["copper"], axis="Y", parent=root, verts=64, bevel=0.03)
    return root


def make_bar(name, mats, x, z, length=2.4):
    root = tr.empty(name + "_root", (x, 0.0, z))
    tr.rbox(name + "_rod", (length, 0.7, 0.7), (0, 0, 0), mats["stainless"], bevel=0.18, parent=root)
    return root


def dipole_lines(n_lines=26, xp=2.55, bounds=(4.6, 6.2), spacing=0.3, seed=3):
    """Field-line sample points (x, z, angle) of two opposite point poles at (-xp, 0) [N, source] and (+xp, 0) [S, sink], traced as streamlines."""
    qs = ((-xp, +1.0), (xp, -1.0))

    def field(x, z):
        bx = bz = 0.0
        for px, q in qs:
            dx, dz = x - px, z
            r3 = (dx * dx + dz * dz) ** 1.5 + 1e-9
            bx += q * dx / r3
            bz += q * dz / r3
        n = math.hypot(bx, bz) + 1e-12
        return bx / n, bz / n

    out = []
    for k in range(n_lines):
        a = 2 * math.pi * (k + 0.5) / n_lines
        x, z = -xp + 0.32 * math.cos(a), 0.32 * math.sin(a)
        if abs(x) < BAR_L / 2 and abs(z) < BAR_H / 2 + 0.05:
            continue
        pts = [(x, z)]
        for _ in range(900):
            dx, dz = field(x, z)
            mx, mz = field(x + dx * 0.04, z + dz * 0.04)
            x, z = x + mx * 0.08, z + mz * 0.08
            if abs(x) > bounds[0] or abs(z) > bounds[1] or math.hypot(x - xp, z) < 0.3:
                break
            if abs(x) < BAR_L / 2 - 0.1 and abs(z) < BAR_H / 2 + 0.05:
                break
            pts.append((x, z))
        acc, last, prev = 0.0, pts[0], pts[0]
        res = []
        for p in pts[1:]:
            acc += math.dist(p, prev)
            prev = p
            if acc >= spacing:
                acc = 0.0
                ang = math.atan2(*reversed(field(*p)))
                res.append((p[0], p[1], ang))
        out += res
    return out


class Filings:
    """One mesh of thin slivers. `set(u)`: u 0 = scattered at random, u 1 = organised along the field lines (per-sliver delay)."""

    def __init__(self, mats, y=-0.08, n_extra=0, seed=5, region=(4.6, 6.2)):
        rng = random.Random(seed)
        tg = dipole_lines()
        self.n = len(tg) + n_extra
        self.target = np.array([(x, z) for x, z, _ in tg], dtype=np.float64)
        self.ang1 = np.array([a for _, _, a in tg])
        self.start = np.array([(rng.uniform(-region[0], region[0]), rng.uniform(-region[1], region[1])) for _ in range(self.n)])
        self.ang0 = np.array([rng.uniform(-math.pi, math.pi) for _ in range(self.n)])
        self.delay = np.array([rng.uniform(0.0, 0.5) for _ in range(self.n)])
        self.y = y
        L, W, T = 0.2, 0.06, 0.05
        self.local = np.array([[sx * L / 2, sy * T / 2, sz * W / 2] for sx in (-1, 1) for sz in (-1, 1) for sy in (-1, 1)])
        faces = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
        verts = np.zeros((self.n * 8, 3))
        f = [tuple(i * 8 + v for v in face) for i in range(self.n) for face in faces]
        mesh = bpy.data.meshes.new("filings")
        mesh.from_pydata(verts.tolist(), [], f)
        mesh.update()
        self.obj = bpy.data.objects.new("filings", mesh)
        bpy.context.scene.collection.objects.link(self.obj)
        self.obj.data.materials.append(mats["filings"])
        self.obj.visible_shadow = False
        self.set(0.0)

    def set(self, u: float, visible: float = 1.0) -> None:
        k = np.clip((u - self.delay * 0.6) / 0.4, 0.0, 1.0)
        k = k * k * (3 - 2 * k)
        pos = self.start + (self.target - self.start) * k[:, None]
        d = (self.ang1 - self.ang0 + math.pi / 2) % math.pi - math.pi / 2                  # slivers are symmetric: take the short way
        ang = self.ang0 + d * k
        jx = np.cos(ang)[:, None] * self.local[:, 0] - np.sin(ang)[:, None] * self.local[:, 2]
        jz = np.sin(ang)[:, None] * self.local[:, 0] + np.cos(ang)[:, None] * self.local[:, 2]
        s = visible
        xs = pos[:, 0:1] + jx * s
        zs = pos[:, 1:2] + jz * s
        ys = np.full_like(xs, self.y) + self.local[:, 1] * s
        co = np.stack([xs, ys, zs], axis=-1).reshape(-1, 3)
        self.obj.data.vertices.foreach_set("co", co.ravel())
        self.obj.data.update()


def stage_plinth(mats, w=18.0, top=0.0):
    return tr.rbox("plinth", (w, 4.0, 1.2), (0.0, 0.6, top - 0.6), mats["ink"], bevel=0.3)


def setup():
    """Materials + plinth; hides the shadow-catcher floor (its horizon band shows at this camera distance, the ink plinth grounds the set)."""
    fl = bpy.data.objects.get("floor")
    if fl:
        fl.hide_render = True
    mats = materials()
    stage_plinth(mats)
    return mats


def pop(root, t, t0, dur=0.4):
    """Scale-in with overshoot starting at t0 (hidden before)."""
    s = 1e-4 if t < t0 else max(1e-4, tr.back((t - t0) / dur))
    root.scale = (s, s, s)
    return s


def lerp(a, b, k):
    return a + (b - a) * k


def board(mats, z0, w=10.6, h=12.8, y=0.9):
    return tr.rbox("board", (w, 0.4, h), (0.0, y, z0), mats["board"], bevel=0.2)


def ring(m, name, sx, sz, loc, minor=0.045):
    bpy.ops.mesh.primitive_torus_add(major_radius=1.0, minor_radius=minor, major_segments=96, minor_segments=10, location=loc, rotation=(math.pi / 2, 0, 0))
    o = bpy.context.object
    o.name = name
    o.scale = (sx, 1.0, sz)
    o.data.materials.append(m.gold)
    o.visible_shadow = False
    return o


def stand(mats, x, z_top, z_floor, arm_to):
    """Retort-style stand: a post on the plinth and an arm that holds a magnet above it. Returns the arm root (arm_to = x of the holder end)."""
    root = tr.empty("stand_root", (x, 0.0, 0.0))
    tr.rbox("stand_post", (0.5, 0.6, z_top - z_floor), (0, 0.8, (z_top + z_floor) / 2), mats["ink"], bevel=0.12, parent=root)
    tr.rbox("stand_arm", (abs(arm_to - x) + 0.5, 0.6, 0.45), ((arm_to - x) / 2, 0.8, z_top), mats["ink"], bevel=0.12, parent=root)
    tr.rbox("stand_hold", (0.4, 0.6, 0.7), (arm_to - x, 0.8, z_top - 0.5), mats["ink"], bevel=0.1, parent=root)
    return root
