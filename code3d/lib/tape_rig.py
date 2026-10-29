"""huincha-de-medir: the hero TAPE-MEASURE rig on the dark stage (runs inside Blender; EEVEE drafts, Cycles finals).

Hard-surface only, one rig revisited by every scene: housing (two side shells, spines, nose, rubber boot), the BLADE (a per-frame mesh whose
cross-section arc, droop and kink are animated), the end HOOK (a plate that slides on slotted rivets), the blade COIL, the flat spiral SPRING
(the motor) and the brake pad. Units: 1 BU ~ 17 cm of blade (the blade is drawn 20 BU = 3.4 m long at most, and chunky: stylised proportions).
Axes: the blade extends along +x from the housing mouth; its width runs along y; z is up. Dark stage rules (CLAUDE.md Reference doctrine): near-black void,
passive greys, ONE gold accent = the active quantity (stress, tension), teal/red only as Editor overlays.
"""

import json
import math
import sys
from pathlib import Path
from types import SimpleNamespace

import bpy
import numpy as np
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402

ASSETS = c.ASSETS / "materials"
HOUSING_X, HOUSING_Z, HOUSING_Y = 4.2, 4.0, 2.7          # housing size (x, z, y); shells at |y| in [0.78, 1.35]
BLADE_W = 1.4                                            # blade width (y)
BLADE_T = 0.05
MOUTH_X, MOUTH_Z = HOUSING_X / 2, -1.55                  # where the blade leaves the housing
COIL_R0, COIL_R1 = 1.75, 1.38                            # blade coil outer radius: fully wound -> mostly paid out
LMAX = 20.0                                              # blade length drawn for the "3.4 m" limit
TILE = 10.0                                              # BU per tick-texture tile
FPS = c.FPS


def ease_out(p: float) -> float:
    p = min(1.0, max(0.0, p))
    return 1 - (1 - p) ** 3


def back(k: float, s_: float = 1.7) -> float:
    k = min(1.0, max(0.0, k))
    return 1 + (s_ + 1) * (k - 1) ** 3 + s_ * (k - 1) ** 2


def show(obj, visible: bool) -> None:
    """Hide by parking far below the stage (toggling hide_render per frame crashed Blender 5.2 with Freestyle; kept for safety)."""
    if "home" not in obj:
        obj["home"] = list(obj.location)
    obj.location = obj["home"] if visible else (obj["home"][0], obj["home"][1], -500.0)


# ------------------------------------------------------------------------------------------------------ materials
def _tex(nt, path, colorspace="sRGB"):
    node = nt.nodes.new("ShaderNodeTexImage")
    node.image = bpy.data.images.load(str(path), check_existing=True)
    node.image.colorspace_settings.name = colorspace
    return node


def pbr(name, folder, prefix, base_hex, metallic=0.0, rough_mul=1.0, scale=0.35, normal=0.35, tint_mix=0.65, coat=0.0):
    """A PBR material from an ambientCG folder (Color / Roughness / NormalGL), colour-keyed to the palette hex: the texture supplies
    the VARIATION (luminance), the palette hex supplies the colour. Box projection in object space, so no UVs are needed."""
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Scale"].default_value = (scale, scale, scale)
    nt.links.new(coord.outputs["Object"], mapping.inputs["Vector"])
    d = ASSETS / folder
    col = _tex(nt, d / f"{prefix}_2K-JPG_Color.jpg")
    rough = _tex(nt, d / f"{prefix}_2K-JPG_Roughness.jpg", "Non-Color")
    nrm = _tex(nt, d / f"{prefix}_2K-JPG_NormalGL.jpg", "Non-Color")
    for t in (col, rough, nrm):
        t.projection, t.projection_blend = "BOX", 0.25
        nt.links.new(mapping.outputs["Vector"], t.inputs["Vector"])
    bw = nt.nodes.new("ShaderNodeRGBToBW")
    nt.links.new(col.outputs["Color"], bw.inputs["Color"])
    hexc = nt.nodes.new("ShaderNodeRGB")
    hexc.outputs[0].default_value = c.linear(base_hex)
    mul = nt.nodes.new("ShaderNodeMix")
    mul.data_type, mul.blend_type = "RGBA", "MULTIPLY"
    mul.inputs["Factor"].default_value = 1.0
    mul.inputs["A"].default_value = (1, 1, 1, 1)
    gain = nt.nodes.new("ShaderNodeMath")                      # keep the mean brightness near 1 so the hex stays the hex
    gain.operation = "MULTIPLY"
    gain.inputs[1].default_value = 1.5
    nt.links.new(bw.outputs["Val"], gain.inputs[0])
    var = nt.nodes.new("ShaderNodeMix")
    var.data_type, var.blend_type = "RGBA", "MIX"
    var.inputs["Factor"].default_value = tint_mix
    var.inputs["A"].default_value = (1, 1, 1, 1)
    comb = nt.nodes.new("ShaderNodeCombineColor")
    for i in range(3):
        nt.links.new(gain.outputs["Value"], comb.inputs[i])
    nt.links.new(comb.outputs["Color"], var.inputs["B"])
    nt.links.new(var.outputs["Result"], mul.inputs["B"])
    mul2 = nt.nodes.new("ShaderNodeMix")
    mul2.data_type, mul2.blend_type = "RGBA", "MULTIPLY"
    mul2.inputs["Factor"].default_value = 1.0
    nt.links.new(hexc.outputs[0], mul2.inputs["A"])
    nt.links.new(mul.outputs["Result"], mul2.inputs["B"])
    nt.links.new(mul2.outputs["Result"], bsdf.inputs["Base Color"])
    rm = nt.nodes.new("ShaderNodeMath")
    rm.operation = "MULTIPLY"
    rm.inputs[1].default_value = rough_mul
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(rough.outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs["Red"], rm.inputs[0])
    nt.links.new(rm.outputs["Value"], bsdf.inputs["Roughness"])
    nmap = nt.nodes.new("ShaderNodeNormalMap")
    nmap.inputs["Strength"].default_value = normal
    nt.links.new(nrm.outputs["Color"], nmap.inputs["Color"])
    nt.links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Metallic"].default_value = metallic
    if coat:
        bsdf.inputs["Coat Weight"].default_value = coat
        bsdf.inputs["Coat Roughness"].default_value = 0.12
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def plain(name, hex_color, rough=0.5, metallic=0.0, coat=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = c.linear(hex_color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metallic
    if coat:
        b.inputs["Coat Weight"].default_value = coat
    return mat


def gold_emit(name, hex_color, strength):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = c.linear(hex_color)
    e.inputs["Strength"].default_value = strength
    nt.links.new(e.outputs["Emission"], out.inputs["Surface"])
    mat["strength_node"] = e.name
    return mat


def ticks_image() -> bpy.types.Image:
    """The unnumbered tick tile: fine ticks every 0.1 BU, mid every 0.5, long every 1.0 (BU), ~410 px per BU; red channel = ink mask."""
    W, H = 4096, 64
    a = np.zeros((H, W, 4), dtype=np.float32)
    a[..., 3] = 1.0
    px_per = W / TILE
    for k in range(int(TILE * 10)):
        x = int(round(k * 0.1 * px_per))
        if k % 10 == 0:
            h, w = 46, 9
        elif k % 5 == 0:
            h, w = 32, 7
        else:
            h, w = 18, 5
        a[H - h:, max(0, x - w // 2): x + (w + 1) // 2, 0] = 1.0                    # ticks grow from the top edge (v = 1)
    img = bpy.data.images.new("blade_ticks", W, H, alpha=True, float_buffer=False)
    img.pixels.foreach_set(a.ravel())
    img.colorspace_settings.name = "Non-Color"
    img.pack()
    return img


def blade_material(pal, hex_steel):
    """Brushed steel (ambientCG Metal012, box-mapped) with the printed ticks (UV) and a GOLD stress glow driven by three node values
    (amplitude, arc-length centre, width) that the scene animates; everything stays grey until the narration activates it."""
    mat = pbr("blade", "Metal012", "Metal012", hex_steel, metallic=0.85, rough_mul=1.7, scale=0.5, normal=0.15, tint_mix=0.5)
    nt = mat.node_tree
    bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
    uv = nt.nodes.new("ShaderNodeUVMap")
    tick = nt.nodes.new("ShaderNodeTexImage")
    tick.image = ticks_image()
    tick.extension = "REPEAT"
    tick.interpolation = "Linear"
    nt.links.new(uv.outputs["UV"], tick.inputs["Vector"])
    ink = nt.nodes.new("ShaderNodeMix")
    ink.data_type, ink.blend_type = "RGBA", "MIX"
    ink.inputs["B"].default_value = c.linear("#0B0A0C")
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    nt.links.new(tick.outputs["Color"], sep.inputs["Color"])
    nt.links.new(sep.outputs["Red"], ink.inputs["Factor"])
    src = bsdf.inputs["Base Color"].links[0].from_socket
    nt.links.new(src, ink.inputs["A"])
    nt.links.new(ink.outputs["Result"], bsdf.inputs["Base Color"])
    # gold stress mask: exp(-((s - centre)/width)^2) * amplitude, s = U * TILE (arc length from the hook end)
    sepuv = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(uv.outputs["UV"], sepuv.inputs["Vector"])
    s = nt.nodes.new("ShaderNodeMath"); s.operation = "MULTIPLY"; s.inputs[1].default_value = TILE
    nt.links.new(sepuv.outputs["X"], s.inputs[0])
    centre = nt.nodes.new("ShaderNodeValue"); centre.name = "stress_centre"; centre.outputs[0].default_value = 0.0
    width = nt.nodes.new("ShaderNodeValue"); width.name = "stress_width"; width.outputs[0].default_value = 1.0
    amp = nt.nodes.new("ShaderNodeValue"); amp.name = "stress_amp"; amp.outputs[0].default_value = 0.0
    sub = nt.nodes.new("ShaderNodeMath"); sub.operation = "SUBTRACT"
    nt.links.new(s.outputs["Value"], sub.inputs[0]); nt.links.new(centre.outputs[0], sub.inputs[1])
    div = nt.nodes.new("ShaderNodeMath"); div.operation = "DIVIDE"
    nt.links.new(sub.outputs["Value"], div.inputs[0]); nt.links.new(width.outputs[0], div.inputs[1])
    sq = nt.nodes.new("ShaderNodeMath"); sq.operation = "POWER"; sq.inputs[1].default_value = 2.0
    nt.links.new(div.outputs["Value"], sq.inputs[0])
    neg = nt.nodes.new("ShaderNodeMath"); neg.operation = "MULTIPLY"; neg.inputs[1].default_value = -1.0
    nt.links.new(sq.outputs["Value"], neg.inputs[0])
    ex = nt.nodes.new("ShaderNodeMath"); ex.operation = "EXPONENT"
    nt.links.new(neg.outputs["Value"], ex.inputs[0])
    strength = nt.nodes.new("ShaderNodeMath"); strength.operation = "MULTIPLY"
    nt.links.new(ex.outputs["Value"], strength.inputs[0]); nt.links.new(amp.outputs[0], strength.inputs[1])
    bsdf.inputs["Emission Color"].default_value = c.linear(pal["accent gold"])
    nt.links.new(strength.outputs["Value"], bsdf.inputs["Emission Strength"])
    return mat


def materials(pal: dict) -> SimpleNamespace:
    m = SimpleNamespace()
    m.blade = blade_material(pal, "#BDBAC0")
    m.shell = pbr("shell", "Plastic010", "Plastic010", "#4A474F", rough_mul=1.0, scale=0.4, normal=0.25, tint_mix=0.5, coat=0.15)
    m.rubber = pbr("rubber", "Rubber004", "Rubber004", "#77747C", rough_mul=1.0, scale=0.5, normal=0.5, tint_mix=0.6)
    m.metal = pbr("metal", "Metal038", "Metal038", pal["passive light grey"], metallic=1.0, rough_mul=1.0, scale=0.5, normal=0.3, tint_mix=0.5)
    m.dark_metal = pbr("dark_metal", "Metal038", "Metal038", "#6D6A70", metallic=1.0, rough_mul=1.1, scale=0.5, normal=0.3, tint_mix=0.5)
    m.slot = plain("slot", "#0B0A0C", rough=0.7)
    m.coil = pbr("coil", "Metal012", "Metal012", "#9A979E", metallic=0.9, rough_mul=1.5, scale=0.5, normal=0.1, tint_mix=0.5)
    m.table = plain("table", "#232024", rough=0.55, metallic=0.0, coat=0.0)
    m.block = pbr("block", "Plastic010", "Plastic010", "#4B484E", rough_mul=1.0, scale=0.35, normal=0.2, tint_mix=0.4)
    m.gold = gold_emit("gold", pal["accent gold"], 9.0)
    m.gold_dim = gold_emit("gold_dim", pal["accent amber"], 1.6)
    m.spring = plain("spring", pal["accent amber"], rough=0.3, metallic=1.0)
    sp = m.spring.node_tree.nodes["Principled BSDF"]
    sp.inputs["Emission Color"].default_value = c.linear(pal["accent gold"])
    sp.inputs["Emission Strength"].default_value = 0.4
    m.red = gold_emit("red", pal["error red"], 6.0)
    return m


# ------------------------------------------------------------------------------------------------------ stage
class Stage:
    def __init__(self, production: Path, mode: str = "draft"):
        self.production, self.mode = Path(production), mode
        self.pal = c.palette(c.identity(self.production))
        self.scene = c.reset_scene()
        self.final = mode == "final"
        self._render_setup()
        c.studio_world(self.scene, self.pal["backdrop"], c.ASSETS / "hdri" / "studio_small_08_2k.hdr", 0.32)
        self.cam = c.make_camera(self.scene, lens=50.0)
        self.cam.data.sensor_fit, self.cam.data.sensor_height = "VERTICAL", 36.0
        self.cam.data.shift_y = 0.05
        self.key = c.add_light(self.scene, "AREA", (-9.0, -16.0, 12.0), 4200.0, size=9.0, target=Vector((3, 0, -1)))
        self.rim = c.add_light(self.scene, "AREA", (12.0, 12.0, 7.0), 1700.0, size=6.0, target=Vector((3, 0, -1)))
        self.rim.data.color = c.linear("#FFE3C4")[:3]
        self.fill = c.add_light(self.scene, "AREA", (14.0, -14.0, 3.0), 900.0, size=10.0, target=Vector((3, 0, -1)))
        self.halo = self._halo()
        self.mats = materials(self.pal)
        self._glare()

    def _render_setup(self):
        sc = self.scene
        c.setup_render(sc, "final" if self.final else "draft-full")
        if self.final:
            sc.render.engine = "CYCLES"
            sc.cycles.device = "GPU"
            prefs = bpy.context.preferences.addons["cycles"].preferences
            prefs.compute_device_type = "METAL"
            prefs.refresh_devices()
            for d in prefs.devices:
                d.use = d.type == "METAL"
            self._apply_render_profile(sc)
            sc.cycles.caustics_reflective = sc.cycles.caustics_refractive = False
            sc.render.use_overwrite = False                         # resumable: existing frames are skipped
            sc.render.use_placeholder = False
        sc.render.film_transparent = False

    @staticmethod
    def _apply_render_profile(sc) -> None:
        """Cycles quality from the channel config (render.profiles, per-scene-type override, `profile=`/`samples=` args): see
        channels/umbrella-es.yaml. Defaults = the tuned stack: GPU denoise, adaptive 0.04, min 24, ceiling 128, persistent data, Fast GI off."""
        import pipeline_config
        args = c.parse_args()
        name, pr = pipeline_config.render_profile(args)
        cy = sc.cycles
        cy.samples = int(args.get("samples", pr["samples_ceiling"]))            # the ceiling: adaptive sampling stops earlier where converged
        cy.use_adaptive_sampling = True
        cy.adaptive_threshold, cy.adaptive_min_samples = float(pr["adaptive_threshold"]), int(pr["min_samples"])
        cy.use_denoising, cy.denoiser = True, "OPENIMAGEDENOISE"
        cy.denoising_use_gpu = bool(pr["denoise_gpu"])
        cy.transmission_bounces, cy.volume_bounces = int(pr["transmission_bounces"]), int(pr["volume_bounces"])
        cy.diffuse_bounces, cy.glossy_bounces, cy.max_bounces = int(pr["diffuse_bounces"]), int(pr["glossy_bounces"]), int(pr["max_bounces"])
        cy.use_fast_gi = bool(pr["fast_gi"])
        sc.render.use_persistent_data = bool(pr["persistent_data"])
        print(f"[render profile] {name}: {pr}")

    def _halo(self):
        bpy.ops.mesh.primitive_plane_add(size=34.0, location=(7.0, 14.0, 6.0), rotation=(math.radians(90), 0, 0))
        obj = bpy.context.object
        obj.name = "halo"
        mat = bpy.data.materials.new("halo")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        tex = nt.nodes.new("ShaderNodeTexCoord")
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Location"].default_value = (-1.0, -1.0, 0)
        mp.inputs["Scale"].default_value = (2.6, 2.6, 1.0)
        grad = nt.nodes.new("ShaderNodeTexGradient")
        grad.gradient_type = "SPHERICAL"
        pw = nt.nodes.new("ShaderNodeMath")
        pw.operation, pw.inputs[1].default_value = "POWER", 2.4
        emit = nt.nodes.new("ShaderNodeEmission")
        emit.inputs["Color"].default_value = c.linear("#C8601A")
        emit.inputs["Strength"].default_value = 0.42
        clear = nt.nodes.new("ShaderNodeBsdfTransparent")
        mix = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(tex.outputs["UV"], mp.inputs["Vector"])
        nt.links.new(mp.outputs["Vector"], grad.inputs["Vector"])
        nt.links.new(grad.outputs["Fac"], pw.inputs[0])
        nt.links.new(pw.outputs["Value"], mix.inputs["Fac"])
        nt.links.new(clear.outputs["BSDF"], mix.inputs[1])
        nt.links.new(emit.outputs["Emission"], mix.inputs[2])
        nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
        mat.surface_render_method = "BLENDED"
        obj.data.materials.append(mat)
        obj.visible_shadow = False
        obj.visible_glossy = False
        return obj

    def _glare(self):
        """Compositor bloom for the gold accent (Blender 5.2: scene.compositing_node_group)."""
        g = bpy.data.node_groups.new("comp", "CompositorNodeTree")
        g.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
        rl = g.nodes.new("CompositorNodeRLayers")
        gl = g.nodes.new("CompositorNodeGlare")
        out = g.nodes.new("NodeGroupOutput")
        gl.inputs["Type"].default_value = "Fog Glow"
        gl.inputs["Threshold"].default_value = 1.0
        gl.inputs["Strength"].default_value = 0.55
        gl.inputs["Size"].default_value = 0.6
        gl.inputs["Quality"].default_value = "Medium"
        g.links.new(rl.outputs["Image"], gl.inputs["Image"])
        g.links.new(gl.outputs["Image"], out.inputs["Image"])
        self.scene.compositing_node_group = g

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


def begin(default_slot: int, floor_z: float | None = None):
    args = c.parse_args()
    production = Path(args["production"])
    stage = Stage(production, args.get("mode", "draft"))
    if args.get("look"):                                  # design-system look (lighting/palette only); absent = the original grey-hero rig
        import looks
        looks.apply(stage, stage.mats, args["look"], {**args, **({"floor_z": floor_z} if floor_z is not None else {})})
    return args, production, stage, stage.mats, int(args.get("slot", default_slot))


def look(stage, target, radius: float, el: float, az: float) -> None:
    c.orbit(stage.cam, Vector(target), radius, el, az)


# ------------------------------------------------------------------------------------------------------ geometry
def _finish(obj, material, smooth=True):
    if smooth:
        for poly in obj.data.polygons:
            poly.use_smooth = True
    obj.data.materials.append(material)
    return obj


def rbox(name, size, loc, material, bevel=0.18, seg=4, parent=None, rot=(0, 0, 0)):
    """A bevelled box of full size (x, y, z)."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = o.modifiers.new("bevel", "BEVEL")
    mod.width, mod.segments, mod.limit_method = min(bevel, min(size) * 0.45), seg, "NONE"
    _finish(o, material)
    if parent:
        o.parent = parent
    return o


def cyl(name, radius, length, loc, material, axis="Y", parent=None, verts=48, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=length, location=loc,
                                        rotation={"X": (0, math.radians(90), 0), "Y": (math.radians(90), 0, 0), "Z": (0, 0, 0)}[axis])
    o = bpy.context.object
    o.name = name
    if bevel:
        mod = o.modifiers.new("bevel", "BEVEL")
        mod.width, mod.segments = bevel, 3
    _finish(o, material)
    if parent:
        o.parent = parent
    return o


def empty(name, loc=(0, 0, 0), parent=None):
    o = bpy.data.objects.new(name, None)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    if parent:
        o.parent = parent
    return o


class Blade:
    """The blade as one mesh whose vertices are rewritten every frame. Centreline from a tangent-angle profile theta(s) (rotation about y,
    positive = drooping toward -z); cross-section parabola with sagitta sag * cs(s) (edges up = the printed concave face). Arc length s runs
    from the housing mouth (s = 0) to the hook end (s = L)."""
    NS, NW = 260, 15

    def __init__(self, material, name="blade", width=BLADE_W, sag=0.30):
        self.w, self.sag0 = width, sag
        NS, NW = self.NS, self.NW
        self.mesh = bpy.data.meshes.new(name)
        verts = [(0, 0, 0)] * (NS * NW)
        faces = [(i * NW + j, i * NW + j + 1, (i + 1) * NW + j + 1, (i + 1) * NW + j) for i in range(NS - 1) for j in range(NW - 1)]
        self.mesh.from_pydata(verts, [], faces)
        uv = self.mesh.uv_layers.new(name="UVMap")
        self.v_u = np.zeros((NS, NW), dtype=np.float32)
        for poly in self.mesh.polygons:
            for k, li in enumerate(poly.loop_indices):
                vi = self.mesh.loops[li].vertex_index
                uv.data[li].uv = (0.0, (vi % NW) / (NW - 1))
        self.uv = uv
        self.loop_row = np.array([self.mesh.loops[i].vertex_index for i in range(len(self.mesh.loops))]) // NW
        self.obj = bpy.data.objects.new(name, self.mesh)
        bpy.context.scene.collection.objects.link(self.obj)
        mod = self.obj.modifiers.new("solid", "SOLIDIFY")
        mod.thickness, mod.offset = BLADE_T, -1.0
        self.mesh.materials.append(material)
        for p in self.mesh.polygons:
            p.use_smooth = True
        self.ys = np.linspace(-width / 2, width / 2, NW)
        self.end_frame = (Vector((0, 0, 0)), 0.0)
        self.L = 0.0

    def set(self, L, theta=None, cs=None, origin=(0.0, 0.0, 0.0), floor=None):
        """L: extended length (BU). theta(s) -> tangent angle (rad, droop positive); cs(s) -> cross-section factor 0..1 (1 = full arc)."""
        L = max(L, 1e-3)
        NS, NW = self.NS, self.NW
        s = np.linspace(0.0, L, NS)
        th = np.array([theta(x) for x in s]) if theta else np.zeros(NS)
        csf = np.array([cs(x) for x in s]) if cs else np.ones(NS)
        ds = np.diff(s, prepend=s[0])
        x = np.cumsum(np.cos(th) * ds)
        z = -np.cumsum(np.sin(th) * ds)
        if floor is not None:                                     # (z_floor, x_max): the blade lies on a surface that ends at x_max
            zf, xmax = floor
            z = np.where(x + origin[0] < xmax, np.maximum(z, zf - origin[2]), z)
        T = np.stack([np.cos(th), np.zeros(NS), -np.sin(th)], axis=1)
        U = np.stack([np.sin(th), np.zeros(NS), np.cos(th)], axis=1)
        P = np.stack([x, np.zeros(NS), z], axis=1) + np.array(origin)
        sag = self.sag0 * csf
        y = self.ys[None, :]
        prof = sag[:, None] * (2 * y / self.w) ** 2                # edges up
        co = P[:, None, :] + y[..., None] * np.array([0, 1, 0]) + prof[..., None] * U[:, None, :]
        self.mesh.vertices.foreach_set("co", co.astype(np.float32).ravel())
        u = (s / TILE).astype(np.float32)
        loops_u = u[self.loop_row]
        uvd = np.empty(len(self.mesh.loops) * 2, dtype=np.float32)
        vv = np.empty(len(self.mesh.loops), dtype=np.float32)
        self.uv.data.foreach_get("uv", uvd)
        uvd[0::2] = loops_u
        self.uv.data.foreach_set("uv", uvd)
        self.mesh.update()
        self.cl_s, self.cl_x, self.cl_z = s, P[:, 0], P[:, 2]            # centreline, for placing plates / weights on the blade
        self.end_frame = (Vector(P[-1]), float(th[-1]), Vector(U[-1]), Vector(T[-1]))
        self.L = L
        return self.end_frame

    def z_at(self, s_: float) -> float:
        return float(np.interp(s_, self.cl_s, self.cl_z))

    def x_at(self, s_: float) -> float:
        return float(np.interp(s_, self.cl_s, self.cl_x))

    def set_fast(self, L, theta=None, cs=None, origin=(0.0, 0.0, 0.0), floor=None):
        """Same as set() but UVs are only rewritten when L changed enough to matter (U = s/TILE rescales with L)."""
        return self.set(L, theta, cs, origin, floor)

    def stress(self, amp: float, centre: float = 0.0, width: float = 1.0) -> None:
        nt = self.obj.data.materials[0].node_tree
        nt.nodes["stress_amp"].outputs[0].default_value = amp
        nt.nodes["stress_centre"].outputs[0].default_value = centre
        nt.nodes["stress_width"].outputs[0].default_value = width


def spiral_strip(name, r_in, r_out, turns, width, material, steps=360, thick=0.05, twist=None, loc=(0, 0, 0)):
    """A flat strip wound in a spiral in the x-z plane (axis along y): r = r_in + (r_out - r_in) * a / (2 pi turns). Returns (obj, rebuild)
    where rebuild(twist_amount, r_out_scale) rewrites the vertices (inner turns rotate by twist_amount, the outer end stays fixed)."""
    NW = 2
    mesh = bpy.data.meshes.new(name)
    faces = [(i * 2, i * 2 + 1, (i + 1) * 2 + 1, (i + 1) * 2) for i in range(steps - 1)]
    mesh.from_pydata([(0, 0, 0)] * (steps * 2), [], faces)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(obj)
    obj.location = loc
    mod = obj.modifiers.new("solid", "SOLIDIFY")
    mod.thickness, mod.offset = thick, 0.0
    mesh.materials.append(material)
    for p in mesh.polygons:
        p.use_smooth = True
    mod2 = obj.modifiers.new("bevel", "BEVEL")
    mod2.width, mod2.segments, mod2.limit_method, mod2.angle_limit = thick * 0.4, 2, "ANGLE", math.radians(40)

    def rebuild(twist_amount=0.0, scale=1.0, r_in_=None):
        a = np.linspace(0, 2 * math.pi * turns, steps)
        rin = r_in if r_in_ is None else r_in_
        r = (rin + (r_out - rin) * a / a[-1]) * scale
        ang = a + twist_amount * (1 - a / a[-1]) ** 1.5                     # inner turns rotate most, the outer end stays fixed
        x, z = r * np.cos(ang), r * np.sin(ang)
        co = np.zeros((steps, 2, 3), dtype=np.float32)
        co[:, 0, 0], co[:, 0, 2], co[:, 0, 1] = x, z, -width / 2
        co[:, 1, 0], co[:, 1, 2], co[:, 1, 1] = x, z, width / 2
        mesh.vertices.foreach_set("co", co.ravel())
        mesh.update()

    rebuild()
    return obj, rebuild


class Tape:
    """The whole hero rig. `root` hangs the housing; the blade is NOT parented (placed in world coordinates by `place_blade`). The housing is
    HOLLOW (thin top/back/front walls) so the exploded view can show the coil, the spring and the brake: `front_group` carries the front side
    shell, its rubber bumper and its hub boss and is lifted away in scene 5."""

    def __init__(self, m, loc=(0, 0, 0), name="tape", with_innards=True, hook=True):
        self.m = m
        self.root = empty(name, loc)
        r = self.root
        hy = 0.78 + 0.28
        gap = 1.56
        self.front_group = empty("front_group", (0, 0, 0), r)
        self.back_group = empty("back_group", (0, 0, 0), r)
        for sgn, grp, nm in ((-1, self.front_group, "f"), (1, self.back_group, "b")):
            sh_ = rbox(f"shell_{nm}", (HOUSING_X, 0.56, HOUSING_Z), (0, sgn * hy, 0), m.shell, bevel=0.26, seg=8, parent=grp)
            bump = rbox(f"bumper_{nm}", (2.7, 0.2, 2.6), (-1.0, sgn * (hy + 0.37), -0.95), m.rubber, bevel=0.5, seg=8, parent=grp)
            ring = cyl(f"boss_ring_{nm}", 1.42, 0.10, (-0.35, sgn * (hy + 0.30), MOUTH_Z + COIL_R0), m.dark_metal, parent=grp, verts=64, bevel=0.03)
            core = cyl(f"boss_core_{nm}", 1.12, 0.12, (-0.35, sgn * (hy + 0.33), MOUTH_Z + COIL_R0), m.rubber, parent=grp, verts=64, bevel=0.03)
            cap = cyl(f"boss_cap_{nm}", 0.34, 0.14, (-0.35, sgn * (hy + 0.38), MOUTH_Z + COIL_R0), m.dark_metal, parent=grp, verts=32, bevel=0.02)
            if sgn == -1:
                self.shell_f = sh_
        self.top = rbox("top_wall", (HOUSING_X - 0.2, gap, 0.2), (0.0, 0, 1.92), m.shell, bevel=0.06, parent=r)
        self.back = rbox("back_wall", (0.2, gap, HOUSING_Z - 0.2), (-1.95, 0, 0.0), m.shell, bevel=0.06, parent=r)
        self.front = rbox("front_wall", (0.22, gap, 2.0), (1.95, 0, 0.4), m.shell, bevel=0.06, parent=r)
        self.nose = rbox("nose", (2.2, gap, 0.38), (1.0, 0, -1.81), m.dark_metal, bevel=0.06, parent=r)
        self.floor_wall = rbox("floor_wall", (HOUSING_X - 0.2, gap, 0.2), (0.0, 0, -1.92), m.shell, bevel=0.06, parent=r)
        self.boot_nose = rbox("boot_nose", (1.5, 2.95, 0.55), (1.5, 0, -1.95), m.rubber, bevel=0.25, seg=6, parent=r)
        self.button = rbox("lock_button", (0.9, 0.7, 0.28), (0.6, 0, 2.08), m.dark_metal, bevel=0.07, parent=r)
        self.cx, self.cz0 = -0.35, MOUTH_Z + COIL_R0
        self.inner = MOUTH_X - self.cx                       # blade length that lies inside the housing (from the coil tangent to the mouth)
        self.blade = Blade(m.blade.copy())
        self.hook = Hook(m) if hook else None
        self.coil = self.spring = self.pad = None
        if with_innards:
            self._innards()

    def _innards(self):
        m, r = self.m, self.root
        self.coil, self.coil_rebuild = spiral_strip("coil", 0.55, COIL_R0, 7, BLADE_W, m.coil, steps=420, thick=0.06,
                                                    loc=(self.cx, 0, self.cz0))
        self.coil.parent = r
        self.spring_group = empty("spring_group", (self.cx, 0, self.cz0), r)
        self.spring, self.spring_rebuild = spiral_strip("spring", 0.14, 0.52, 4.5, 1.0, m.spring, steps=300, thick=0.05)
        self.spring.parent = self.spring_group
        cyl("hub", 0.13, 1.7, (0, 0, 0), m.dark_metal, parent=self.spring_group, verts=32)
        self.pad_pivot = empty("pad_pivot", (1.45, 0, MOUTH_Z + 0.12), r)
        self.pad = rbox("brake_pad", (0.9, 1.2, 0.32), (0, 0, 0.26 + 0.9), m.rubber, bevel=0.07, parent=self.pad_pivot)   # raised by default
        self.lever = rbox("brake_lever", (1.9, 0.5, 0.2), (0.2, 0, 1.45), m.dark_metal, bevel=0.06, parent=self.pad_pivot)
        self.lever.rotation_euler = (0, math.radians(8), 0)

    def set_coil(self, paid_out: float, paid_max: float = 14.0, rot_extra: float = 0.0) -> float:
        """Coil radius from how much blade has been paid out; the coil turns with it. Returns the coil outer radius."""
        R = COIL_R0 - (COIL_R0 - COIL_R1) * min(1.0, paid_out / paid_max)
        self.coil_rebuild(0.0, R / COIL_R0)
        self.coil.location.z = MOUTH_Z + R
        self.spring_group.location.z = MOUTH_Z + R
        self.coil.rotation_euler.y = -paid_out / max(R, 0.5) + rot_extra
        return R

    def mouth(self) -> Vector:
        return Vector((MOUTH_X, 0.0, MOUTH_Z)) + self.root.location

    def S(self, d: float) -> float:
        """Arc length (from the coil tangent) of the point d BU beyond the mouth."""
        return self.inner + d

    def place_blade(self, d, theta=None, cs=None, floor=None, hook_slide=0.0):
        """d = blade length outside the housing. theta/cs take arc length from the coil tangent (use S(d))."""
        origin = (self.cx + self.root.location.x, self.root.location.y, MOUTH_Z + self.root.location.z)
        end = self.blade.set(self.inner + max(d, 0.001), theta, cs, origin=origin, floor=floor)
        if self.hook is not None:
            self.hook.place(end, hook_slide)
            show(self.hook.root, d > 0.05) if False else None
        return end


class Hook:
    """The end hook: a lip plate (thickness HT) held on the blade end by two rivets in slots, so it slides exactly its own thickness HT.
    slide 0 = pushed in (lip occupies [E, E+HT]), slide 1 = pulled out ([E+HT, E+2HT]); E = blade end. The plate lies ON the blade (toward -x)."""
    HT = 0.30

    def __init__(self, m):
        self.root = empty("hook_root")
        self.slide_root = empty("hook_slide", parent=self.root)
        self.lip = rbox("hook_lip", (self.HT, BLADE_W + 0.5, 1.9), (self.HT / 2, 0, -0.78), m.metal, bevel=0.06, parent=self.slide_root)
        self.plate = rbox("hook_plate", (2.1, BLADE_W + 0.5, 0.11), (-1.0, 0, 0.12), m.metal, bevel=0.03, parent=self.slide_root)
        self.rivets = []
        for x in (-0.55, -1.65):
            self.rivets.append(cyl("rivet", 0.15, 0.1, (x, 0, 0.22), m.dark_metal, axis="Z", parent=self.root, verts=24))
            rbox("slot", (0.62, 0.26, 0.03), (x, 0, 0.18), m.slot, bevel=0.01, parent=self.slide_root)

    def place(self, end_frame, slide=0.0):
        P, th, U, T = end_frame
        self.root.location = P
        self.root.rotation_euler = (0.0, th, 0.0)
        self.slide_root.location = (self.HT * slide, 0.0, 0.0)


def table(m, x0=-6.0, x1=3.0, y=10.0, z_top=MOUTH_Z - 0.45, thick=1.2):
    t = rbox("table", (x1 - x0, y, thick), ((x0 + x1) / 2, 0, z_top - thick / 2), m.table, bevel=0.3, seg=5)
    return t
