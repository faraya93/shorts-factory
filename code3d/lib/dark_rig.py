"""v7-drawn: the DARK-STAGE wound rig (runs inside Blender). Reference doctrine (CLAUDE.md "Reference doctrine"):
near-black void, passive greys, ONE gold accent = the active quantity (tension, growth, what is measured), navy cutaway
interior, red = failure, yellow-green = cells. Chunky simplified models, emissive gold with a soft halo shell (EEVEE 5 has no
bloom), a warm rim light and a warm halo behind the hero, and a camera that never rests.

Geometry (x across the cut, y into the screen, z up; skin surface z = 0): a WOUND BLOCK = two halves of stacked layers
(epidermis, dermis, fat) seen as a cross-section on the front face; the V-shaped cut is REAL geometry: `Wound.set_gap(g)` rewrites
the inner vertices of every layer, so the lips slide together without interpenetrating. Needles, threads and tweezers are laid
just in front of the cut face (y = FRONT) so the whole stitch path stays visible (a cutaway drawing).
"""

import json
import math
import sys
from pathlib import Path
from types import SimpleNamespace

import bmesh
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import shapes as sh  # noqa: E402
import suture as s  # noqa: E402

DEPTH, WIDTH, APEX = 1.8, 1.7, 1.40          # block depth (y), half-width, depth of the V
LAYERS = (("epi", 0.0, -0.34), ("derm", -0.34, -1.40), ("fat", -1.40, -3.90))
FRONT = -DEPTH - 0.12                       # y of the drawing plane in front of the cut face
AMBIENT = 0.22
SHELL = 2.2                                 # glow halo shell radius multiplier


def pal_hex(pal: dict, name: str) -> str:
    return pal[name]


def emissive(name, hex_color, strength, alpha=1.0, roughness=0.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    emit = nt.nodes.new("ShaderNodeEmission")
    emit.inputs["Color"].default_value = c.linear(hex_color)
    emit.inputs["Strength"].default_value = strength
    if alpha >= 1.0:
        nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
    else:
        clear = nt.nodes.new("ShaderNodeBsdfTransparent")
        mix = nt.nodes.new("ShaderNodeMixShader")
        mix.inputs["Fac"].default_value = alpha
        nt.links.new(clear.outputs["BSDF"], mix.inputs[1])
        nt.links.new(emit.outputs["Emission"], mix.inputs[2])
        nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
        mat.surface_render_method = "BLENDED"
    return mat


def matte(name, hex_color, roughness=0.55, metallic=0.0, spec=0.35):
    mat = c.principled(name, hex_color, roughness=roughness, metallic=metallic)
    mat.node_tree.nodes["Principled BSDF"].inputs["Specular IOR Level"].default_value = spec
    return mat


def materials(pal: dict) -> SimpleNamespace:
    p = lambda n: pal[n]
    return SimpleNamespace(
        epi=matte("epi", p("passive light grey"), 0.5), derm=matte("derm", p("passive grey"), 0.55),
        fat=matte("fat", p("passive dark grey"), 0.6), wall=matte("wall", p("cross-section navy"), 0.7),
        steel=matte("steel", p("passive light grey"), 0.25, metallic=1.0), thread=matte("thread", p("passive light grey"), 0.5),
        dark=matte("darkthread", p("passive dark grey"), 0.5, spec=0.6),
        ant=c.principled("ant", p("passive dark grey"), roughness=0.3),
        gold=emissive("gold", p("accent gold"), 7.0), gold_soft=emissive("gold_soft", p("accent gold"), 2.0, alpha=0.20),
        amber=emissive("amber", p("accent amber"), 3.0), red=emissive("red", p("error red"), 4.0), redwall=matte("redwall", "#8E2F2F", 0.5),
        cells=emissive("cells", p("biology yellow-green"), 1.6), skin_new=emissive("skin_new", p("accent gold"), 1.1),
        teal=emissive("teal", p("annotation teal"), 2.0))


class DarkStage:
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
        self.cam.data.shift_y = 0.06
        self.cam.data.dof.use_dof = False
        self.key = c.add_light(self.scene, "AREA", (-3.5, -11.0, 4.0), 1500.0, size=7.0, target=Vector((0, 0, -1.2)))
        self.rim = c.add_light(self.scene, "AREA", (4.5, 5.0, 5.0), 900.0, size=4.0, target=Vector((0, 0, -1.0)))
        self.rim.data.color = c.linear(self.pal["accent amber"])[:3]
        self.halo = self._halo()
        self.anchors = {}

    def _halo(self):
        """A warm radial glow plane behind the hero, near the top of the frame (reference: V2 8.1 s, 25.0 s)."""
        bpy.ops.mesh.primitive_plane_add(size=9.0, location=(0, 9.0, 3.2), rotation=(math.radians(90), 0, 0))
        obj = bpy.context.object
        obj.name = "halo"
        mat = bpy.data.materials.new("halo")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        tex = nt.nodes.new("ShaderNodeTexCoord")
        mapn = nt.nodes.new("ShaderNodeMapping")
        mapn.inputs["Location"].default_value = (-1.0, -1.0, 0)
        mapn.inputs["Scale"].default_value = (2.0, 2.0, 1.0)
        grad = nt.nodes.new("ShaderNodeTexGradient")
        grad.gradient_type = "SPHERICAL"
        pw = nt.nodes.new("ShaderNodeMath")
        pw.operation, pw.inputs[1].default_value = "POWER", 2.4
        emit = nt.nodes.new("ShaderNodeEmission")
        emit.inputs["Color"].default_value = c.linear("#C8601A")
        emit.inputs["Strength"].default_value = 0.85
        clear = nt.nodes.new("ShaderNodeBsdfTransparent")
        mix = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(tex.outputs["UV"], mapn.inputs["Vector"])
        nt.links.new(mapn.outputs["Vector"], grad.inputs["Vector"])
        nt.links.new(grad.outputs["Fac"], pw.inputs[0])
        nt.links.new(pw.outputs["Value"], mix.inputs["Fac"])
        nt.links.new(clear.outputs["BSDF"], mix.inputs[1])
        nt.links.new(emit.outputs["Emission"], mix.inputs[2])
        nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
        mat.surface_render_method = "BLENDED"
        obj.data.materials.append(mat)
        obj.visible_shadow = False
        return obj

    def track(self, name: str, point, frame: int) -> None:
        """Record a world point's screen position (fractions of the frame, y down) so overlays can follow it."""
        co = world_to_camera_view(self.scene, self.cam, Vector(point))
        self.anchors.setdefault(name, []).append([frame / c.FPS, round(co.x, 4), round(1.0 - co.y, 4)])

    def run(self, update, args: dict, slot: int, name: str) -> None:
        def handler(scene_):
            update(scene_)
        bpy.app.handlers.frame_change_pre.append(handler)
        out = Path(args.get("out", str(self.production / "build" / "code3d" / name)))
        if "stills" in args:
            out.mkdir(parents=True, exist_ok=True)
            for f in [int(x) for x in args["stills"].split(",")]:
                self.scene.frame_set(f)
                self.scene.render.filepath = str(out / f"still-{f:04d}.png")
                bpy.ops.render.render(write_still=True)
        else:
            a, b = (int(x) for x in args.get("frames", f"1-{slot}").split("-"))
            for f in range(a, b + 1):                      # anchors for the Editor's tracked overlays (cheap: no render)
                self.scene.frame_set(f)
            out.mkdir(parents=True, exist_ok=True)
            (out / "anchors.json").write_text(json.dumps(self.anchors))
            c.render_frames(self.scene, out, a, b)


def begin(default_slot: int):
    args = c.parse_args()
    production = Path(args["production"])
    stage = DarkStage(production, args.get("mode", "draft"))
    return args, production, stage, materials(stage.pal), int(args.get("slot", default_slot))


def look(stage, target, radius: float, el: float, az: float) -> None:
    c.orbit(stage.cam, Vector(target), radius, el, az)


def show(obj, visible: bool) -> None:
    """Park hidden objects far below the stage (toggling hide_render per frame is unreliable); restores the home z."""
    if "home_z" not in obj:
        obj["home_z"] = obj.location.z
    obj.location.z = obj["home_z"] if visible else -500.0


def back(k: float, s_: float = 1.7) -> float:
    k = min(1.0, max(0.0, k))
    return 1 + (s_ + 1) * (k - 1) ** 3 + s_ * (k - 1) ** 2


# ------------------------------------------------------------------------------------------------------ the block
class Wound:
    """A cross-section block: two halves of stacked layers around a V-shaped cut whose width g (at the surface) is animated."""

    def __init__(self, m, origin=(0.0, 0.0, 0.0), tint=None):
        self.root = bpy.data.objects.new("wound", None)
        bpy.context.scene.collection.objects.link(self.root)
        self.root.location = origin
        self.layers = []                        # (obj, side, z_top, z_bot)
        mats = {"epi": m.epi, "derm": m.derm, "fat": m.fat}
        for side in (-1, 1):
            for name, zt, zb in LAYERS:
                obj = self._cuboid(f"{name}_{side}", mats[name])
                self.layers.append((obj, side, zt, zb))
        self.interior = bpy.data.objects.new("wound_interior", None)
        wedge = sh.extruded_polygon("wedge", [(-WIDTH * 0.9, -0.06), (WIDTH * 0.9, -0.06), (0.0, -APEX - 0.05)], 2 * DEPTH - 0.1, m.redwall, loc=(0, 0, 0), bevel=0.02)
        wedge.rotation_euler = (math.radians(90), 0, 0)
        wedge.location = (0, DEPTH - 0.05, 0.0)
        wedge.parent = self.root
        self.wedge = wedge
        wall = sh.rounded_bar("wall", WIDTH + 0.3, 0.12, abs(LAYERS[-1][2]) / 2 + 0.1, m.wall,
                              loc=(0, DEPTH + 0.35, LAYERS[-1][2] / 2 + 0.0), bevel_frac=0.3)
        wall.parent = self.root
        self.set_gap(1.0)

    def _cuboid(self, name, material):
        mesh = bpy.data.meshes.new(name)
        bm = bmesh.new()
        vs = [bm.verts.new((0, y, 0)) for y in (-DEPTH, DEPTH) for _ in range(4)]
        for q in ((0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
            bm.faces.new([vs[i] for i in q])
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        obj.parent = self.root
        mod = obj.modifiers.new("round", "BEVEL")
        mod.width, mod.segments, mod.limit_method = 0.07, 4, "NONE"
        mesh.materials.append(material)
        for poly in mesh.polygons:
            poly.use_smooth = True
        return obj

    def inner_x(self, side: int, z: float, g: float) -> float:
        """x of the cut face at depth z for a V of surface width g (closes at APEX)."""
        return side * (g / 2) * max(0.0, 1.0 - (-z) / APEX)

    def set_gap(self, g: float) -> None:
        for obj, side, zt, zb in self.layers:
            xi_t, xi_b = self.inner_x(side, zt, g), self.inner_x(side, zb, g)
            outer = side * WIDTH
            for k, y in enumerate((-DEPTH, DEPTH)):
                base = 4 * k
                obj.data.vertices[base + 0].co = (xi_t, y, zt)
                obj.data.vertices[base + 1].co = (outer, y, zt)
                obj.data.vertices[base + 2].co = (outer, y, zb)
                obj.data.vertices[base + 3].co = (xi_b, y, zb)
            obj.data.update()

    def world(self, x, z, y=FRONT) -> Vector:
        return Vector((x, y, z)) + self.root.location


# ----------------------------------------------------------------------------------------------------- instruments
def straight_needle(m, length=4.2, radius=0.12):
    """A thin straight needle with its TIP at the returned root empty's origin, pointing down (-z), eye ring at the tail."""
    root = bpy.data.objects.new("straight_needle", None)
    bpy.context.scene.collection.objects.link(root)
    body = sh.cone_needle("straight_body", Vector((0, 0, length)), Vector((0, 0, 0)), radius, 0.012, m.steel)
    eye = sh.ring("straight_eye", 0.11, 0.028, m.steel, loc=(0, 0, length + 0.12), rot=(math.radians(90), 0, 0))
    for o in (body, eye):
        o.parent = root
    return root


def curved_needle(m, radius=1.45, center_z=0.0, arc_deg=105.0, tip0=150.0):
    return s.curved_needle(radius, center_z, tip0, arc_deg, 0.15, 0.02, m.steel), tip0, arc_deg


def glow_thread(m, points=160, thickness=0.045, halo=True):
    """A gold glowing thread (emissive core + a soft halo shell). Returns (core, shell) Thread objects."""
    core = s.Thread(m.gold, points=points, thickness=thickness)
    shell = s.Thread(m.gold_soft, points=points, thickness=thickness * SHELL) if halo else None
    return core, shell


def set_thread(pair, pts):
    pair[0].set(pts)
    if pair[1] is not None:
        pair[1].set(pts)


def tweezers(m, tip_gap=0.12, length=2.4, root_name="tweezers"):
    """Two steel arms hinged at the far end; returns (root empty, [(pivot, sign)]). The tips are at the root's origin."""
    root = bpy.data.objects.new(root_name, None)
    bpy.context.scene.collection.objects.link(root)
    V = Vector((1.5, 0, 1.9))
    pivots = []
    for dx in (-tip_gap, tip_gap):
        pivot = bpy.data.objects.new(f"pivot_{dx}", None)
        bpy.context.scene.collection.objects.link(pivot)
        pivot.parent, pivot.location = root, V
        arm = sh.bar_between(f"arm_{dx}", Vector((dx, 0, 0)) - V, Vector((0, 0, 0)), 0.085, m.steel)
        arm.parent = pivot
        pivots.append((pivot, 1 if dx > 0 else -1))
    return root, pivots


def ant(m, scale=1.0):
    """A chunky black ant built from ellipsoids and thick legs; returns (root, jaw pivots). Faces -x."""
    root = bpy.data.objects.new("ant", None)
    bpy.context.scene.collection.objects.link(root)
    parts = (("head", (0.30, 0.26, 0.26), (-0.55, 0, 0.0)), ("thorax", (0.32, 0.22, 0.22), (-0.05, 0, 0.0)),
             ("abdomen", (0.55, 0.34, 0.32), (0.62, 0, 0.0)))
    for name, rad, loc in parts:
        o = sh.ellipsoid(name, *rad, m.ant, loc=loc, segments=32, rings=16)
        o.parent = root
    jaws = []
    for side in (-1, 1):
        pivot = bpy.data.objects.new(f"jaw_{side}", None)
        bpy.context.scene.collection.objects.link(pivot)
        pivot.parent, pivot.location = root, (-0.78, side * 0.12, -0.02)
        jaw = sh.bar_between("jaw", Vector((0, 0, 0)), Vector((-0.34, -side * 0.10, 0)), 0.05, m.ant)
        jaw.parent = pivot
        jaws.append((pivot, side))
        for x, spread in ((-0.35, 0.18), (-0.05, 0.22), (0.30, 0.26)):
            leg = s.Thread(m.ant, points=24, thickness=0.035)
            pts = [Vector((x, side * 0.10, -0.05)), Vector((x - 0.05, side * (0.35 + spread), 0.30)), Vector((x - 0.15, side * (0.62 + spread), -0.28))]
            leg.set(s.resample(pts + [pts[-1]], 24))
            leg.obj.parent = root
    root.scale = (scale,) * 3
    return root, jaws
