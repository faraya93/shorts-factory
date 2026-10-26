"""v6-staged: the GLOSSY 3D CARTOON stage and the chunky boot (runs inside Blender).

Recipe: modelled chunky volumes, Principled glossy materials (exact palette hexes), one soft sun + ambient HDRI, soft
shadows, subtle depth of field, NO outlines, NO cel bands, a camera that always moves. The lavender backdrop is the world
colour as seen by the camera; the floor is a plane that renders as that exact lavender wherever it is lit and darkens
smoothly only inside shadows (so shadows read, the spec background does not move).

The boot's lacing panel is an empty ("panel") pitched along the instep; scene code authors flaps, eyelets, cord and needle in
the same flat panel coordinates as the lace world (x across, y up the lacing, z out of the panel) and `adopt` parents them.
"""

import math
import sys
from pathlib import Path
from types import SimpleNamespace

import bpy
from mathutils import Matrix, Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import lace_world as lw  # noqa: E402
import shapes as sh  # noqa: E402

AMBIENT = 0.75                                    # HDRI strength (fill light; the camera sees the flat backdrop)
SUN_ENERGY, SUN_ANGLE_DEG = 3.2, 9.0              # soft shadows come from the sun's angular size
SUN_FROM = Vector((-5.0, -6.5, 9.0))
FLOOR_SHADOW = 0.80                               # the floor's colour factor inside full shadow (1.0 = lit = exact backdrop)
FLOOR_LO, FLOOR_HI = 0.55, 1.08                   # probe luminance range mapped to the shadow factor (calibrated, see floor_debug)
APERTURE = 0.45                                   # f-stop of the subtle depth of field (scene units are large)
SHIFT_Y = 0.07                                    # lens shift: lowers the subject so the subtitle band stays clear

PITCH = math.radians(50.3)                        # the lacing panel's pitch along the instep
U = Vector((0.0, math.cos(PITCH), math.sin(PITCH)))
N = Vector((0.0, -math.sin(PITCH), math.cos(PITCH)))
PANEL_M = Vector((0.0, -1.49, 7.65))              # panel centre in world space
ROWS = lw.ROWS


def gloss(name, hex_color, roughness=0.28, metallic=0.0, coat=0.55, alpha=1.0, transmission=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = c.linear(hex_color)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Coat Weight"].default_value = 0.0 if metallic else coat
    bsdf.inputs["Coat Roughness"].default_value = 0.05
    if alpha < 1.0:
        bsdf.inputs["Alpha"].default_value = alpha
        mat.surface_render_method = "BLENDED"
    return mat


def materials(pal: dict) -> SimpleNamespace:
    """Glossy materials; `skin`/`red`/`steel`/`needle`/`cord` mirror the lace-world names so its helpers are reusable."""
    steel = pal["steel grey"]
    return SimpleNamespace(
        leather=gloss("leather", pal["leather brown"], 0.42, coat=0.2), skin=gloss("flap", pal["flap leather"], 0.32, coat=0.6),
        toecap=gloss("toecap", pal["toe cap brown"], 0.3, coat=0.6), sole=gloss("sole", pal["sole cream"], 0.45, coat=0.3),
        red=gloss("tissue", pal["tissue red"], 0.35, coat=0.5), steel=gloss("steel", steel, 0.2, metallic=1.0),
        needle=gloss("needle", lw.dark_steel(steel), 0.2, metallic=1.0), cord=gloss("cord", pal["thread black"], 0.38, coat=0.5),
        ant=gloss("ant", pal["tissue red"], 0.3, coat=0.7), shaded=gloss("shaded", pal["shaded skin"], 0.35, coat=0.5),
        bubble=gloss("bubble", "#CFE3FF", 0.02, coat=0.0, alpha=0.22), black=gloss("black", pal["thread black"], 0.08, coat=0.8))


class GlossStage:
    def __init__(self, production: Path, mode: str = "draft"):
        self.production, self.mode = Path(production), mode
        self.pal = c.palette(c.identity(self.production))
        self.scene = c.reset_scene()
        c.setup_render(self.scene, mode)
        c.studio_world(self.scene, self.pal["backdrop"], c.ASSETS / "hdri" / "studio_small_08_2k.hdr", AMBIENT)
        try:
            self.scene.eevee.use_raytracing = True
        except AttributeError:
            pass
        self.cam = c.make_camera(self.scene, lens=50.0)
        self.cam.data.sensor_fit, self.cam.data.sensor_height = "VERTICAL", 36.0
        self.cam.data.shift_y = SHIFT_Y
        self.cam.data.dof.use_dof = True
        self.cam.data.dof.aperture_fstop = APERTURE
        sun = bpy.data.lights.new("sun", "SUN")
        sun.energy, sun.angle = SUN_ENERGY, math.radians(SUN_ANGLE_DEG)
        obj = bpy.data.objects.new("sun", sun)
        obj.rotation_euler = (-SUN_FROM).to_track_quat("-Z", "Y").to_euler()
        self.scene.collection.objects.link(obj)
        self.floor = self._floor(self.pal["backdrop"])

    def _floor(self, backdrop_hex: str):
        bpy.ops.mesh.primitive_plane_add(size=400.0)
        obj = bpy.context.object
        obj.name = "floor"
        obj["world_fixed"] = 1
        mat = bpy.data.materials.new("floor")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        probe = nt.nodes.new("ShaderNodeBsdfDiffuse")
        probe.inputs["Color"].default_value = (1, 1, 1, 1)
        to_rgb = nt.nodes.new("ShaderNodeShaderToRGB")
        bw = nt.nodes.new("ShaderNodeRGBToBW")
        rng = nt.nodes.new("ShaderNodeMapRange")
        rng.clamp = True
        rng.inputs["From Min"].default_value, rng.inputs["From Max"].default_value = FLOOR_LO, FLOOR_HI
        rng.inputs["To Min"].default_value, rng.inputs["To Max"].default_value = FLOOR_SHADOW, 1.0
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type, mix.blend_type = "RGBA", "MULTIPLY"
        mix.inputs["Factor"].default_value = 1.0
        mix.inputs["A"].default_value = c.linear(backdrop_hex)
        emit = nt.nodes.new("ShaderNodeEmission")
        nt.links.new(probe.outputs["BSDF"], to_rgb.inputs["Shader"])
        nt.links.new(to_rgb.outputs["Color"], bw.inputs["Color"])
        nt.links.new(bw.outputs["Val"], rng.inputs["Value"])
        nt.links.new(rng.outputs["Result"], mix.inputs["B"])
        nt.links.new(mix.outputs["Result"], emit.inputs["Color"])
        nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
        obj.data.materials.append(mat)
        self.floor_nodes = (rng, to_rgb, mat)
        return obj

    def run(self, update, args: dict, slot: int, name: str) -> None:
        bpy.app.handlers.frame_change_pre.append(update)
        out = Path(args.get("out", str(self.production / "build" / "code3d" / name)))
        if "stills" in args:
            out.mkdir(parents=True, exist_ok=True)
            for f in [int(x) for x in args["stills"].split(",")]:
                self.scene.frame_set(f)
                self.scene.render.filepath = str(out / f"still-{f:04d}.png")
                bpy.ops.render.render(write_still=True)
        else:
            a, b = (int(x) for x in args.get("frames", f"1-{slot}").split("-"))
            c.render_frames(self.scene, out, a, b)


def begin(default_slot: int):
    """Common start of a v6 scene script: (args, production, stage, materials, slot_frames)."""
    args = c.parse_args()
    production = Path(args["production"])
    stage = GlossStage(production, args.get("mode", "draft"))
    return args, production, stage, materials(stage.pal), int(args.get("slot", default_slot))


def look(stage, target, radius: float, el: float, az: float) -> None:
    """Orbit camera around `target`; the depth of field always focuses on the target."""
    c.orbit(stage.cam, Vector(target), radius, el, az)
    stage.cam.data.dof.focus_distance = (Vector(target) - stage.cam.location).length


def to_world(p) -> Vector:
    """Panel-frame point -> world point (for aiming the camera at things on the panel)."""
    return PANEL_M + Vector(p).x * Vector((1, 0, 0)) + Vector(p).y * U + Vector(p).z * N


def build_boot(m, hx: float = 4.0):
    """The chunky boot: cream sole, brown leather body (extruded side profile), toe cap, heel, red collar lining. Returns the
    pitched `panel` empty; everything built here is world-fixed (not adopted by the panel)."""
    panel = lw.empty("panel", PANEL_M)
    panel.rotation_euler = (PITCH, 0.0, 0.0)
    surf = PANEL_M - 0.55 * N                                      # the body's top surface along the lacing, under the flaps
    s0, s1 = surf - 5.2 * U, surf + 4.9 * U
    prof = [(-8.0, 1.0), (-8.5, 1.8), (-8.3, 3.0), (-7.4, 3.8), (-5.8, 3.9), (s0.y, s0.z), (s1.y, s1.z), (2.3, 12.0), (3.3, 12.4),
            (5.0, 12.4), (5.8, 11.8), (5.6, 9.5), (5.9, 6.0), (6.8, 3.0), (7.1, 1.2), (6.5, 1.0)]
    body = sh.extruded_polygon("body", prof, 2 * hx, m.leather, loc=(-hx, 0, 0), bevel=1.5)
    for v in body.data.vertices:                                   # taper the shaft: narrower at the ankle than at the toe
        v.co.z = hx + (v.co.z - hx) * (1.0 - 0.24 * min(1.0, max(0.0, (v.co.y - 3.5) / 8.5)))
    body.rotation_euler = Matrix(((0, 0, 1), (1, 0, 0), (0, 1, 0))).to_euler()       # profile (y, z) -> world, extruded along x
    rim = sh.ring("collar_rim", 2.45, 0.6, m.skin, loc=(0, 4.2, 12.05))
    rim.scale = (1.0, 0.88, 1.0)
    parts = [body, rim,
             sh.rounded_bar("sole", hx + 0.5, 8.0, 0.6, m.sole, loc=(0, -0.3, 0.6), bevel_frac=0.9),
             sh.ellipsoid("toecap", hx - 0.35, 2.3, 1.7, m.toecap, loc=(0, -6.4, 2.45)),
             sh.rounded_bar("heel", hx - 0.1, 1.3, 1.0, m.toecap, loc=(0, 6.3, 1.9)),
             sh.ellipsoid("mouth", 2.6, 2.1, 0.5, m.toecap, loc=(0, 4.2, 11.65)),
             sh.ellipsoid("lining", 2.2, 1.7, 0.4, m.red, loc=(0, 4.2, 11.85))]
    for p in parts:
        p["world_fixed"] = 1
    return panel


def adopt(panel) -> None:
    """Parent every free-standing object (flaps, eyelets, cords, needle...) to the panel; world-fixed ones stay."""
    for obj in bpy.data.objects:
        if obj is panel or obj.parent is not None or obj.get("world_fixed") or obj.type in ("CAMERA", "LIGHT"):
            continue
        obj.parent = panel


def back(k: float, s: float = 1.7) -> float:
    """Ease-out with overshoot (springy settle): 0 -> 1, peaking ~10% over 1 near the end (follow-through)."""
    k = min(1.0, max(0.0, k))
    return 1 + (s + 1) * (k - 1) ** 3 + s * (k - 1) ** 2


ZE, ZC = 0.55, 0.85                                # eyelet height and cord height above the panel (panel frame)


class Flaps:
    """The two leather flaps of the boot with their eyelets (children of the flaps) and the red tongue between them."""

    def __init__(self, m, hx: float = 1.5, hy: float = 4.7, hz: float = 0.45, eyelets: bool = True):
        self.hx, self.hy = hx, hy
        self.flap = {side: sh.rounded_bar(f"flap_{side}", hx, hy, hz, m.skin) for side in (-1, 1)}
        self.tongue = sh.rounded_bar("tongue", 1.3, hy + 0.55, 0.2, m.red, loc=(0, 0.35, -0.32))
        self.rings = {}
        if eyelets:
            for side in (-1, 1):
                for i, y in enumerate(ROWS):
                    ring = sh.ring("eyelet", 0.3, 0.1, m.steel)
                    lw.parent(ring, self.flap[side], (-side * (hx - 0.7), y, ZE))
                    self.rings[(side, i)] = ring

    def set(self, g0: float, k: float = 0.0, tilt: float = 0.0, lift: float = 0.0):
        """Gap g(y) = g0 + k*y between the inner edges; `tilt` (radians) lowers the outer edges (flaps fall open like wings)."""
        phi = math.atan(k / 2)
        for side in (-1, 1):
            self.flap[side].location = (side * (g0 / 2 + self.hx), 0, lift)
            self.flap[side].rotation_euler = (0.0, side * tilt, -side * phi)
        self.tongue.scale.x = ((g0 + abs(k) * self.hy) / 2 + 0.05) / 1.3
        return lw.gap_fn(g0, k)


def eyelet_at(side: int, row: int, g, tilt: float = 0.0) -> Vector:
    """Eyelet centre in panel coordinates (exact when tilt == 0; the tilt only lifts it slightly)."""
    return Vector((side * (g(ROWS[row]) / 2 + 0.7), ROWS[row], ZE + 0.8 * math.sin(tilt)))


def lift(v, z: float = ZC) -> Vector:
    return Vector((v.x, v.y, z))
