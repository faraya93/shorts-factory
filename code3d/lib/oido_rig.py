"""Rig of production 024 (why you should not clean your ears with a cotton swab): the sealed ear-canal asset (outer ear plus a cream block with a half-open canal trough, open toward the
camera), the sealed cotton-swab asset, the amber wax lining of the canal, the skin bands and flakes that ride outward like a slow conveyor, dust specks, the wax pile and the wax plug,
and the slim accent rings that draw sound. Rigid or geometric parts are primitives; the ear and the swab are sealed library assets placed through avion_rig.place. Runs inside Blender.
Every length below is in asset millimetres (the ear block is 62 wide, the canal axis runs along +x at height CZ with radius CR and the eardrum wall at x = DX); P() and R() turn them into
scene units (KS scene units per mm). The camera sits on the -y side, y grows into the plate behind, z is up. Driven per frame by the scene script."""
import math
import random
import sys
from pathlib import Path

import bmesh
import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
import asset_rig as ar  # noqa: E402
import avion_rig as av  # noqa: E402
import tape_rig as tr  # noqa: E402

KS = 0.7                                  # scene units per asset millimetre
K = 1000.0                                # asset metres to millimetres
CZ, CR, DX = 33.9, 9.5, 50.0              # canal axis height, canal radius, eardrum wall x (asset mm, as built in the asset)
SWAB_K = 2.2                              # the swab is drawn 2.2x so its tip fills the enlarged canal
SWAB_HALF = 37.5 * SWAB_K                 # half length of the swab in mm
LIGHT_K = 2.0
ease = av.ease
look = av.look
lights = av.lights


def P(x, y, z):
    return (x * KS, y * KS, z * KS)


def R(v):
    return v * KS


def smooth(a, b, t):
    return ease((t - a) / max(1e-6, b - a))


class Mats:
    """Hero colours come from scenes.json hero_colours (module constants are the fallbacks); the plate and board take the production's support colours."""

    def __init__(self, S):
        hc = (S.p or {}).get("hero") or {}
        self.skin_hex = hc.get("skin", "#EBC3A6")
        self.bone_hex = hc.get("bone", "#F1E6C8")
        self.canal_hex = hc.get("canal", "#C9776A")
        self.drum_hex = hc.get("drum", "#8F7A86")
        self.wax = S.hero("small", hc.get("wax", "#D9992E"), rough=0.32, coat=0.35)
        self.band = S.hero("rubber", hc.get("band", "#B8665A"), rough=0.5)
        self.dust = tr.plain("dust", "#76706A", rough=0.9)
        self.plate = S.plate_mat(rough=0.7)
        self.board = S.board_mat()
        self.ink = S.ink
        self.accent = S.accent
        self.red = S.error


def half_pipe(name, x0, x1, r, mat, zc=CZ, thick=2.0, nx=24, na=24, seed=1, lumps=0.0, parent=None):
    """A half pipe along x (axis at height zc, y >= 0 half: the open side faces the camera), radius r mm, thickness `thick` mm growing inward, optional lumpy radius. Returns the object."""
    rnd = random.Random(seed)
    ph = [(rnd.uniform(0, 6.3), rnd.uniform(0.6, 1.4)) for _ in range(3)]

    def pos(i, j):
        x = x0 + (x1 - x0) * i / (nx - 1)
        a = math.pi * j / na
        rr = r - lumps * sum(math.sin(f * x * 0.7 + p + 2.0 * a * (k + 1)) for k, (p, f) in enumerate(ph)) / 3.0 - lumps * 0.6
        return P(x, rr * math.sin(a), zc + rr * math.cos(a))
    return av.grid_surface(name, nx, na, pos, mat, thick=R(thick), flip=True, parent=parent)


class Ear:
    """The sealed ear with the plate behind it and the wax lining; ear.root is the ear's empty."""

    def __init__(self, S, m, lining=(0.8, 19.0)):
        root, objs = av.place("ear-canal", None, K * KS)
        self.root, self.objs, self.m = root, objs, m
        for o in objs:
            if o.type != "MESH":
                continue
            for slot in o.material_slots:
                mt = slot.material
                if mt is None:
                    continue
                if mt.name.startswith("ear_skin"):
                    slot.material = ar.retint(mt.copy(), m.skin_hex, role="shell_y")[0]
                elif mt.name.startswith("ear_bone"):
                    slot.material = ar.retint(mt.copy(), m.bone_hex, role="g_big")[0]
                elif mt.name.startswith("ear_canal_skin"):
                    slot.material = ar.retint(mt.copy(), m.canal_hex, role="rubber_k")[0]
                elif mt.name.startswith("ear_drum"):
                    slot.material = ar.retint(mt.copy(), m.drum_hex, role="g_mark")[0]
            if o.name == "ear_pinna":                                                        # a clean straight cut of the scan's jagged crop edge, just inside the block's left face
                bm = bmesh.new()
                bm.from_mesh(o.data)
                bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=(-0.0009, 0, 0), plane_no=(1, 0, 0), clear_outer=True)
                bm.to_mesh(o.data)
                bm.free()
            o.name = "ear_" + o.name
        tr.rbox("plate_back", P(300, 3.0, 220), P(10, 42.0, 30.0), m.plate, bevel=0.5)
        self.lining = None
        if lining:
            self.lining = half_pipe("wax_lining", lining[0], lining[1], CR - 0.35, m.wax, thick=2.4, lumps=0.55, seed=3)


class Conveyor:
    """Skin bands (thin half rings) riding outward along the canal wall, with amber wax flakes and grey dust specks on them. Everything is cloned (S.swarm) so each is placed in world units.
    speed in mm/s (0 = at rest); bands wrap around the canal length [1, DX - 1]; things near either end shrink so nothing pops."""

    def __init__(self, S, m, nb=7, nf=9, nd=6, seed=5, x_lo=1.0, x_hi=DX - 1.0, lined=True):
        self.S, self.m, self.lined = S, m, lined
        self.lo, self.hi = x_lo, x_hi
        self.L = x_hi - x_lo
        rnd = random.Random(seed)
        src = half_pipe("band_src", -1.0, 1.0, CR - 0.25, m.band, zc=0.0, thick=0.5, nx=2, na=24)
        self.bands = S.swarm(nb, S.reg(src), lambda i, t: None)
        for k, o in enumerate(self.bands):
            o.name = f"band_{k}"
        self.nb = nb
        fsrc = S.ball("flake_src", m.wax, R(1.7), (0, 0, 0), shape=(1.5, 1.0, 0.8))
        self.flakes = S.swarm(nf, fsrc, lambda i, t: None)
        for k, o in enumerate(self.flakes):
            o.name = f"flake_{k}"
        self.fl = [(rnd.uniform(self.lo, self.hi), rnd.uniform(0.35, 2.75)) for _ in range(nf)]       # start x, angle a (0 top .. pi bottom)
        dsrc = S.ball("dust_src", m.dust, R(1.1), (0, 0, 0))
        self.dust = S.swarm(nd, dsrc, lambda i, t: None)
        for k, o in enumerate(self.dust):
            o.name = f"dust_{k}"
        self.du = [(rnd.uniform(self.lo, self.hi), rnd.uniform(0.35, 2.75)) for _ in range(nd)]

    def _fade(self, x):
        return min(1.0, max(0.0, (x - self.lo) / 5.0), max(0.0, (self.hi - x) / 5.0))

    def wall(self, x, a, r):
        """The world point on the canal wall at axial x, angle a (0 top .. pi bottom, y >= 0 half), radius r mm. Where the wax lining covers the wall (x < 19) the point is lifted onto the lining."""
        r = r - 2.2 * min(1.0, max(0.0, (22.0 - x) / 4.0)) if self.lined else r
        return P(x, r * math.sin(a), CZ + r * math.cos(a))

    def _put(self, o, val):
        next(d for ob, d in self.S.items if ob is o)["sw"] = val

    def update(self, t, speed, bands_on=1.0, flakes_on=1.0, dust_on=1.0, dust_in=None):
        """Place everything for time t. Bands and flakes wrap around the canal at `speed` mm/s. dust_in(i) -> (t0, t1, x_stick) makes dust i drift in from outside the entrance
        (t0), stick to the wall at x_stick (t1) and then ride outward with the conveyor and leave through the opening; with dust_in None the specks sit where the conveyor puts them."""
        for i, o in enumerate(self.bands):
            x0 = self.lo + (i + 0.5) * self.L / self.nb
            x = self.lo + ((x0 - self.lo - speed * t) % self.L)
            k = self._fade(x) * bands_on
            self._put(o, None if k < 0.02 else (P(x, 0, CZ), (1.0, max(k, 0.02), max(k, 0.02))))
        for i, o in enumerate(self.flakes):
            x0, a = self.fl[i]
            x = self.lo + ((x0 - self.lo - speed * t) % self.L)
            k = self._fade(x) * flakes_on
            self._put(o, None if k < 0.02 else (self.wall(x, a, CR - 1.8), max(k, 0.02)))
        for i, o in enumerate(self.dust):
            x0, a = self.du[i]
            if dust_in is None:
                x = self.lo + ((x0 - self.lo - speed * t) % self.L)
                k = self._fade(x) * dust_on
                self._put(o, None if k < 0.02 else (self.wall(x, a, CR - 0.9), max(k, 0.02)))
                continue
            t0, t1, xs = dust_in(i)
            if t < t0:
                self._put(o, None)
            elif t < t1:                                          # drifts in along the axis from outside, then settles on the wall
                u = smooth(t0, t1, t)
                x = -16.0 + (xs + 16.0) * u
                k = dust_on * min(1.0, (t - t0) / 0.25)
                self._put(o, (self.wall(x, a * u + 1.45 * (1 - u), CR - 0.9 - 4.0 * (1 - u)), max(k, 0.02)))
            else:
                x = xs - speed * (t - t1)
                k = dust_on * max(0.0, min(1.0, (x - 0.0) / 4.0))
                self._put(o, None if k < 0.02 else (self.wall(x, a, CR - 0.9), max(k, 0.02)))


class Swab:
    """The sealed swab (2.2x), lying along +x; tip_at(x, y, z, tilt) puts its +x tip at the given asset-mm point."""

    def __init__(self, S, m):
        root, objs = av.place("cotton-swab", None, K * KS * SWAB_K)
        self.root, self.objs = root, objs
        for o in objs:
            o.name = "swab_" + o.name
            if o.type != "MESH":
                continue
            for slot in o.material_slots:
                mt = slot.material
                if mt is None:
                    continue
                if mt.name.startswith("swab_cotton"):
                    slot.material = ar.retint(mt.copy(), "#F6F3EE", role="blade")[0]
                elif mt.name.startswith("swab_stick"):
                    slot.material = ar.retint(mt.copy(), "#8FB7C9", role="blade")[0]
        S.reg(root)
        self.S = S

    def tip_at(self, x, y, z, tilt=0.0, roll=0.0, pitch=0.0):
        """Tip point (asset mm). The tip points along (cos pitch cos tilt, cos pitch sin tilt, -sin pitch): tilt 0 = along +x (into the canal), tilt about 1.9 = mostly +y (coming at
        the plate from the camera side, handle toward the right front); roll turns it about its own axis."""
        dx, dy, dz = math.cos(pitch) * math.cos(tilt), math.cos(pitch) * math.sin(tilt), -math.sin(pitch)
        cx, cy, cz = x - SWAB_HALF * dx, y - SWAB_HALF * dy, z - SWAB_HALF * dz
        self.root.location = P(cx, cy, cz - 2.3 * SWAB_K * math.cos(pitch))
        self.root.rotation_euler = (roll, pitch, tilt)

    def hide(self, on=True):
        self.root.scale = (1e-4,) * 3 if on else (1.0,) * 3


def ring(S, name, mat, r=8.0, minor=0.42):
    """One slim sound ring, axis along x (a torus turned about y). Scene scripts move it and set its scale."""
    o = S.torus(name, R(r), R(minor), (0, 0, 0), mat, rot=(0, math.pi / 2, 0))
    return o


def lumps(S, m, name, pts, r=3.0, seed=7, pops=None):
    """A mass of overlapping amber lumps at asset-mm points; returns the objects (the scene script pops/moves them). pops[i] = (t0, dur) makes lump i pop in at t0."""
    rnd = random.Random(seed)
    out = []
    for i, p in enumerate(pts):
        rr = r * rnd.uniform(0.8, 1.25)
        kw = {"pop": pops[i]} if pops and pops[i] else {}
        out.append(S.ball(f"{name}_{i}", m.wax, R(rr), P(*p), shape=(rnd.uniform(0.9, 1.4), 1.0, rnd.uniform(0.85, 1.1)), **kw))
    return out
