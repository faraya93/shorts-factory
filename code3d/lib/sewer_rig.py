"""Route diorama for the toilet video: the house drain, the street sewer and a simplified treatment plant, in the SAME model language as toilet_rig
(cream cut-face shells with teal pockets, translucent water volumes, matte brown organic bits). Side section in the XZ plane; the camera descends.
Layout (z down the page): house floor z=0 | drain x=-2.2 down to z=-9 | street sewer along z=-9 to x=7 | down into S1 screens (z -26..-18) | S2 settling (-38..-30)
| S3 microbes (-50..-42) | S4 clarify + UV (-62..-54) | river | sludge pipe left to the digester (x -5..-0.6, z -62..-55) | septic tank far below (z -80..-72)."""
import math
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402
import toilet_rig as tl  # noqa: E402

Y0, Y1, YB0, YB1 = tl.Y0, tl.Y1, tl.YB0, tl.YB1
WY0, WY1 = tl.WY0, tl.WY1
P1 = [(-2.2, -2.4), (-2.2, -9.0), (7.0, -9.0), (7.0, -17.4)]
STATIONS = {"S1": (0.0, 8.0, -26.0, -18.0), "S2": (0.0, 8.0, -38.0, -30.0), "S3": (0.0, 8.0, -50.0, -42.0), "S4": (0.0, 8.0, -62.0, -54.0)}
DIGESTER = (-5.2, -0.6, -62.0, -55.0)
SEPTIC = (11.0, 19.0, -80.0, -72.0)
OUTLETS = {"S1": 1.0, "S2": 7.0, "S3": 1.0, "S4": 7.0}
INLETS = {"S1": 7.0, "S2": 1.0, "S3": 7.0, "S4": 1.0}
SEWAGE_HEX, CLEAN_HEX, MICROBE_HEX, WIPE_HEX, PAPER_HEX = "#8C7A4E", "#2F7DE6", "#C5DB4A", "#A25FC9", "#FFFDF6"


def offset_poly(pts, half):
    """Closed polygon around an orthogonal polyline (mitred corners)."""
    n = len(pts)
    normals = []
    for a, b in zip(pts, pts[1:]):
        dx, dz = b[0] - a[0], b[1] - a[1]
        l = math.hypot(dx, dz)
        normals.append((-dz / l, dx / l))
    left, right = [], []
    for i, p in enumerate(pts):
        if i == 0:
            nx, nz = normals[0]
            k = 1.0
        elif i == n - 1:
            nx, nz = normals[-1]
            k = 1.0
        else:
            n1, n2 = normals[i - 1], normals[i]
            dot = n1[0] * n2[0] + n1[1] * n2[1]
            nx, nz = (n1[0] + n2[0]) / (1 + dot), (n1[1] + n2[1]) / (1 + dot)
            k = 1.0
        left.append((p[0] + nx * half * k, p[1] + nz * half * k))
        right.append((p[0] - nx * half * k, p[1] - nz * half * k))
    return left + right[::-1]


class Materials:
    def __init__(self, base=None):
        base = base or tl.material_set()
        self.__dict__.update(base)
        self.sewage = self._glass("sewage", SEWAGE_HEX, 0.78)
        self.clean = base["water"]
        self.microbe = tr.plain("microbe", MICROBE_HEX, rough=0.4, coat=0.2)
        self.wipe = tr.plain("wipe", WIPE_HEX, rough=0.5)
        self.paper = tr.plain("paper", PAPER_HEX, rough=0.7)
        self.foam = tr.plain("foam", "#FFFFFF", rough=0.3)

    @staticmethod
    def _glass(name, hexv, alpha):
        m = tr.plain(name, hexv, rough=0.15)
        m.node_tree.nodes["Principled BSDF"].inputs["Alpha"].default_value = alpha
        m.surface_render_method = "BLENDED"
        return m


class Plant:
    def __init__(self, mats: Materials, septic=True):
        self.m = mats
        self.parts = {}
        soil = tr.rbox("soil", (50.0, 1.6, 86.0), (5.0, 1.6, -45.4), mats.ink, bevel=0.3)
        self.soil = soil
        self._pipe("P1", P1)
        for k, (x0, x1, z0, z1) in STATIONS.items():
            self._basin(k, x0, x1, z0, z1, outlet_x=OUTLETS[k], holes=[(-0.3, 0.9, -37.9, -36.5)] if k == "S2" else ())
        for k, nxt in (("S1", "S2"), ("S2", "S3"), ("S3", "S4")):
            ox = OUTLETS[k]
            self._pipe(f"link_{k}", [(ox, STATIONS[k][2] - 0.2), (ox, STATIONS[nxt][3] + 0.4)])
        self._pipe("river_pipe", [(OUTLETS["S4"], STATIONS["S4"][2] - 0.2), (OUTLETS["S4"], -66.0)])
        self._pipe("sludge_pipe", [(0.0, -37.2), (-2.5, -37.2), (-2.5, -54.6)])
        self._basin("DIG", *DIGESTER, outlet_x=None, dome=True)
        if septic:
            self._basin("SEP", *SEPTIC, outlet_x=None, holes=[(18.3, 19.4, -75.2, -73.8)])
            self._pipe("sep_in", [(14.5, -62.0), (14.5, -72.4)])
            self._pipe("sep_out", [(19.0, -74.5), (24.0, -74.5)])
            self._stream([(14.5, -62.0), (14.5, -72.4)])
            tr.rbox("house", (5.0, 1.4, 3.4), (14.5, 0.0, -60.4), mats.porcelain, bevel=0.12)
            tr.rbox("house_roof", (5.8, 1.5, 0.7), (14.5, 0.0, -58.4), mats.lever, bevel=0.15)
        # river: a clear blue strip under the last outlet
        self.river = tr.rbox("river", (14.0, 1.4, 1.4), (3.0, 0.0, -67.4), mats.clean, bevel=0.3)
        # flow inside the pipes: sewage streams (static, 60 % deep) so the pipes do not read as empty
        self._stream(P1)
        for k, nxt in (("S1", "S2"), ("S2", "S3"), ("S3", "S4")):
            ox = OUTLETS[k]
            self._stream([(ox, STATIONS[k][2] - 0.2), (ox, STATIONS[nxt][3] + 0.4)])
        self._stream([(0.0, -37.2), (-2.5, -37.2), (-2.5, -54.6)])

    # ---- building blocks -----------------------------------------------------------------------------
    def _shell(self, name, outer, cavities):
        shell = tl.prism(name, outer, Y0, Y1, self.m.porcelain)
        tl.carve(shell, cavities)
        tl.bevel(shell, 0.05)
        back = tl.prism(name + "_back", outer, YB0, YB1, self.m.back)
        self.parts[name] = (shell, back)

    def _pipe(self, name, pts):
        outer = offset_poly(pts, 1.1)
        inner = offset_poly(pts, 0.7)
        self._shell(name, outer, [tl.prism(name + "_c", inner, Y0 - 0.3, Y1 + 0.3, None)])

    def _stream(self, pts):
        """A thin sewage stream along the pipe: boxes along each leg."""
        for (a, b) in zip(pts, pts[1:]):
            x0, x1 = sorted((a[0], b[0])); z0, z1 = sorted((a[1], b[1]))
            vertical = abs(a[0] - b[0]) < 1e-6
            box = tl.Box(f"stream_{len(self.parts)}_{a}", self.m.sewage)
            if vertical:
                box.set(a[0] - 0.4, a[0] + 0.4, z0, z1)
            else:
                box.set(x0, x1, a[1] - 0.7, a[1] - 0.05)

    def _basin(self, name, x0, x1, z0, z1, outlet_x=None, dome=False, wall=0.5, holes=()):
        outer = tl.rect(x0, x1, z0, z1)
        cav = [tl.prism(name + "_cav", tl.rect(x0 + wall, x1 - wall, z0 + wall, z1 + 2.0), Y0 - 0.3, Y1 + 0.3, None)]
        if outlet_x is not None:
            cav.append(tl.prism(name + "_hole", tl.rect(outlet_x - 0.7, outlet_x + 0.7, z0 - 0.3, z0 + 1.0), Y0 - 0.3, Y1 + 0.3, None))
        for k, h in enumerate(holes):
            cav.append(tl.prism(f"{name}_xh{k}", tl.rect(*h), Y0 - 0.3, Y1 + 0.3, None))
        self._shell(name, outer, cav)

    # ---- elements ------------------------------------------------------------------------------------
    def new_blob(self, name, mat, size, shape=(1.0, 0.8, 0.8)):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=1.0)
        o = bpy.context.object
        o.name = name
        o.scale = tuple(size * v for v in shape)
        o["base"] = list(o.scale)
        for p in o.data.polygons:
            p.use_smooth = True
        o.data.materials.append(mat)
        return o

    @staticmethod
    def put(o, x, z, s=1.0, y=-0.78, rot=0.0):
        b = o["base"]
        k = max(1e-4, s)
        o.location = (x, y, z)
        o.scale = (b[0] * k, b[1] * k, b[2] * k)
        o.rotation_euler = (0, rot, 0)

    def water_box(self, name, mat, x0, x1, z0, z1):
        b = tl.Box(name, mat)
        b.set(x0, x1, z0, z1)
        return b


def path_point(pts, s):
    """Point at arc-length fraction s along a polyline."""
    segs = list(zip(pts, pts[1:]))
    ls = [math.dist(a, b) for a, b in segs]
    d = max(0.0, min(1.0, s)) * sum(ls)
    for (a, b), l in zip(segs, ls):
        if d <= l:
            k = d / l if l else 0.0
            return a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k
        d -= l
    return pts[-1]


GRATE_Z, GRATE_X = -22.0, (0.8, 7.2)


def add_grate(m):
    """Horizontal screen across S1: bars run along the depth axis, so the section shows a comb of squares; small things fall through, wipes lie on it."""
    n = 12
    bars = []
    for i in range(n):
        x = GRATE_X[0] + (GRATE_X[1] - GRATE_X[0]) * i / (n - 1)
        bars.append(tr.rbox(f"grate{i}", (0.3, 1.2, 0.34), (x, -0.1, GRATE_Z), m.ink, bevel=0.07))
    return bars
