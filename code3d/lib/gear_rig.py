"""Hero rig for the gear-ratio video (engranajes-papel): a COMPOUND spur-gear train, hard surfaces only, one rig revisited in every scene.
Pairs of (pinion 10 teeth -> big gear 40 teeth), module M, so every stage divides speed by 4. Meshing is exact: the driven gear's angle is
solved from the driver's (see Train.set_input). Gears live in the world XZ plane (camera looks along +y); local-z of the gear mesh is the axle.
Palette (Papel): big gears cobalt, pinions deep blue, the INPUT pinion + crank in vermilion (the active quantity), ink plinth, taupe board."""

import math
import sys
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import tape_rig as tr  # noqa: E402

M = 0.16                      # module: pitch radius = teeth * M / 2
NP, NB = 10, 40               # pinion / big-gear teeth: ratio 4:1 per stage
RP, RB = NP * M / 2, NB * M / 2          # 0.8 / 3.2
DIST = RP + RB                           # 4.0 centre distance of a meshing pair
THICK = 0.5
PLANE_STEP = 0.62
PHI_DEG = (55, 125)
COBALT, DEEP, CREAM, INK, TAUPE = "#2F63D6", "#1F3FA0", "#FFF8E6", "#1D1B2E", "#CFC1A6"


def gear_mesh(name: str, n: int, material, thick: float = THICK) -> bpy.types.Object:
    """Spur gear with trapezoid teeth, extruded along local +z (centred), pitch radius n*M/2."""
    r = n * M / 2
    ro, rr = r + M, r - 1.25 * M
    pitch = 2 * math.pi / n
    pts = []
    for i in range(n):
        a = i * pitch
        pts += [(rr, a - 0.275 * pitch), (ro, a - 0.15 * pitch), (ro, a + 0.15 * pitch), (rr, a + 0.275 * pitch), (rr, a + 0.5 * pitch)]
    bm = bmesh.new()
    verts = [bm.verts.new((rad * math.cos(ang), rad * math.sin(ang), -thick / 2)) for rad, ang in pts]
    face = bm.faces.new(verts)
    ext = bmesh.ops.extrude_face_region(bm, geom=[face])
    top = [v for v in ext["geom"] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, vec=(0, 0, thick), verts=top)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh)
    bm.free()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    mod = o.modifiers.new("bevel", "BEVEL")
    mod.width, mod.segments, mod.limit_method = 0.045, 2, "ANGLE"
    tr._finish(o, material)
    return o


class Gear:
    """One gear: an empty carries world position/plane (rotated so mesh-z = world -y); `spin` (the mesh) rotates about its axle."""

    def __init__(self, name, n, pos, plane_y, material, marker=None, holes=None, parent=None):
        self.n, self.pos, self.plane_y = n, pos, plane_y
        self.root = tr.empty(f"{name}_root", (pos[0], plane_y, pos[1]))
        self.root.rotation_euler = (math.pi / 2, 0, 0)
        self.mesh = gear_mesh(name, n, material)
        self.mesh.parent = self.root
        r = n * M / 2
        hub = tr.cyl(f"{name}_hub", 0.3, THICK + 0.36, (0, 0, 0), holes or material, axis="Z", parent=self.mesh, verts=32, bevel=0.05)
        self.extras = [hub]
        if n >= 20 and holes:                               # lightening holes on the big gears
            for k in range(6):
                a = k * math.pi / 3
                h = tr.cyl(f"{name}_hole{k}", 0.34 * r / 3.2 * 1.1, THICK + 0.02, (0.6 * r * math.cos(a), 0.6 * r * math.sin(a), 0), holes,
                           axis="Z", parent=self.mesh, verts=24, bevel=0.0)
                self.extras.append(h)
        if marker:                                          # a bright dot on the rim: makes turns countable
            mk = tr.cyl(f"{name}_mark", 0.13 if n < 20 else 0.2, THICK + 0.06, (0.78 * r, 0, 0), marker, axis="Z", parent=self.mesh, verts=20)
            self.extras.append(mk)
        self.mesh.parent = self.root
        self.scale_all(1.0)

    def set_angle(self, a: float) -> None:
        self.mesh.rotation_euler.z = a

    def scale_all(self, s: float) -> None:
        s = max(1e-4, s)
        self.root.scale = (s, s, s)


class Train:
    """Six shafts: pinion_0 (input) ... big_5 (output). Pair k = pinion on shaft k meshing big on shaft k+1, direction PHI[k] in the XZ plane."""

    def __init__(self, m, stages: int = 5, origin=(0.0, 0.0), board=True):
        self.m, self.stages = m, stages
        self.phi = [math.radians(PHI_DEG[k % 2]) for k in range(stages)]
        self.shaft = [origin]
        for k in range(stages):
            px, pz = self.shaft[-1]
            self.shaft.append((px + DIST * math.cos(self.phi[k]), pz + DIST * math.sin(self.phi[k])))
        mats = self._materials(m)
        self.pinion, self.big = {}, {}
        for k in range(stages):
            mat = mats["input"] if k == 0 else mats["pinion"]
            self.pinion[k] = Gear(f"pinion{k}", NP, self.shaft[k], self.plane(k), mat, marker=mats["marker"] if k in (0,) else None)
        for k in range(1, stages + 1):
            self.big[k] = Gear(f"big{k}", NB, self.shaft[k], self.plane(k - 1), mats["big"], marker=mats["marker"] if k == stages else None, holes=mats["ink"])
        # crank on the input pinion (the "manivela"): a vermilion bar + knob, child of the pinion so it spins with it
        p0 = self.pinion[0]
        bar = tr.rbox("crank_bar", (1.5, 0.22, 0.22), (0.7, 0, THICK / 2 + 0.3), mats["input"], bevel=0.06, parent=p0.mesh)
        knob = tr.cyl("crank_knob", 0.2, 0.5, (1.4, 0, THICK / 2 + 0.52), mats["input"], axis="Z", parent=p0.mesh, verts=24, bevel=0.04)
        self.crank = [bar, knob]
        # output arm on the last big gear (pushes the block in scene 5)
        bl = self.big[stages]
        arm = tr.rbox("out_arm", (3.9, 0.3, 0.3), (1.9, 0, -THICK / 2 - 0.35), mats["ink"], bevel=0.08, parent=bl.mesh)
        self.arm = arm
        self.arm_y = self.plane(stages - 1) + THICK / 2 + 0.35
        self.parts = [g for g in list(self.pinion.values()) + list(self.big.values())]
        if board:
            xs = [p[0] for p in self.shaft]; zs = [p[1] for p in self.shaft]
            cx, cz = (min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2
            w, h = (max(xs) - min(xs)) + 2 * RB + 1.2, (max(zs) - min(zs)) + RB + RB + 1.2
            yb = self.plane(0) + THICK / 2 + 0.75
            self.board = tr.rbox("board", (w, 0.5, h), (cx, yb, cz), mats["taupe"], bevel=0.35)
            self.plinth = tr.rbox("plinth", (w + 1.0, 3.0, 1.2), (cx, yb - 1.1, cz - h / 2 - 0.6), mats["ink"], bevel=0.3)
            # axles: thin ink rods from each gear plane to the board
            self.axle = {}
            for k in range(self.stages + 1):
                top = yb - 0.25
                bot = self.plane(min(k, self.stages - 1)) - THICK / 2 - 0.2
                self.axle[k] = tr.cyl(f"axle{k}", 0.1, top - bot, (self.shaft[k][0], (top + bot) / 2, self.shaft[k][1]), mats["ink"], axis="Y", verts=16)

    def plane(self, pair: int) -> float:
        """Depth (world y, away from the camera) of pair `pair`; later stages sit NEARER the camera so every pinion is in front of its big gear."""
        return PLANE_STEP * (self.stages - pair + 1)

    @staticmethod
    def _materials(m):
        ink = tr.plain("ink", INK, rough=0.55)
        return {"big": tr.pbr("g_big", "Plastic010", "Plastic010", COBALT, rough_mul=1.0, scale=0.4, normal=0.25, tint_mix=0.9, coat=0.3),
                "pinion": tr.pbr("g_pin", "Plastic010", "Plastic010", DEEP, rough_mul=1.0, scale=0.4, normal=0.25, tint_mix=0.9, coat=0.3),
                "input": m.gold, "ink": ink, "marker": tr.plain("g_mark", CREAM, rough=0.4, coat=0.2),
                "taupe": tr.plain("g_board", TAUPE, rough=0.7)}

    # ---- kinematics ---------------------------------------------------------------------------------
    def angles(self, theta0: float) -> list[float]:
        """Shaft angles for an input angle: exact mesh phase, speed ratio NP/NB per stage, alternating direction."""
        th = [theta0]
        for k in range(self.stages):
            ph = self.phi[k]
            th.append(ph + math.pi - math.pi / NB - (NP / NB) * (th[k] - ph))
        return th

    def input_for_output(self, th_out: float) -> float:
        """Input angle that puts the LAST shaft at th_out (inverse of `angles`)."""
        th = th_out
        for k in reversed(range(self.stages)):
            ph = self.phi[k]
            c_k = ph + math.pi - math.pi / NB + (NP / NB) * ph
            th = (NB / NP) * (c_k - th)
        return th

    def set_input(self, theta0: float) -> list[float]:
        th = self.angles(theta0)
        for k, g in self.pinion.items():
            g.set_angle(th[k])
        for k, g in self.big.items():
            g.set_angle(th[k])
        return th

    def pop(self, k_pair: int, s: float) -> None:
        """Scale pair k's gears (pinion k, big k+1) -- used to build the chain stage by stage."""
        self.pinion[k_pair].scale_all(s)
        self.big[k_pair + 1].scale_all(s)
        for k in (k_pair, k_pair + 1):                     # axles appear with their gears
            if getattr(self, "axle", None) and not (k == k_pair and s < 1.0 and k_pair > 0):
                self.axle[k].scale = (max(1e-4, s),) * 3


def block_and_floor(m, x, z):
    """Heavy ink block for the force scene."""
    return tr.rbox("heavy_block", (3.2, 2.2, 2.6), (x, 0.0, z), tr.plain("blockm", INK, rough=0.5), bevel=0.25)
