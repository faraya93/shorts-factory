"""Real-material kit (2026-11-05, every-element rule): physically based materials and organic builders for the substances that used to be flat-colour stand-ins.
Runs inside Blender (Cycles). Scene units are centimetres-ish "BU" as in the set-piece kit. Scenes that use transmission or volumes must run under the `transparent`
render profile (channels/mecanalia/brand.yaml render.scene_types).

Materials (all node based, Principled): water, glass, ice, coffee, steel, wet_tissue (vessels, skin, pulp), stone, droplets.
Builders: lathe (closed profile -> solid of revolution), tumbler + liquid, ice_cube (irregular, cloudy core), vessel tree (branching tubes with tapering radii),
heat_volume (noise-driven emissive volume), ray (thin emissive tube).
Gate roles: the composition gate classifies by material name. Opaque materials keep its role names (g_big, g_pin, g_mark, shell_y ...). CLEAR materials (glass, water, ice) are named clear_* so
they fall in the gate's unmeasured `other` class: they inherit the stage colour by refraction by definition, so the stage-hero colour rule cannot apply; they are guarded by the
extended likeness gate (lens decision 2026-11-05)."""
import math
import random
import sys
from pathlib import Path

import bpy
import bmesh
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402

lin = c.linear


def _principled(name):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    return m, nt, next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")


def _volume(nt, out, node_type, **vals):
    v = nt.nodes.new(node_type)
    for k, x in vals.items():
        v.inputs[k].default_value = x
    nt.links.new(v.outputs[0], out.inputs["Volume"])
    return v


def _clip_surface(nt, bsdf, out, mode, vol_nodes=()):
    """Show this material only below ('below') or above ('above') a world-space height held in a Value node (the freezing front). Elsewhere the surface is Transparent and
    the volume density is zero, so a liquid and its ice can occupy the same space and swap along a moving front. Returns the Value node: set its default_value per frame."""
    front = nt.nodes.new("ShaderNodeValue")
    front.label = "front"
    front.outputs[0].default_value = 1e6 if mode == "below" else -1e6
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
    cmp_ = nt.nodes.new("ShaderNodeMath")
    cmp_.operation = "LESS_THAN" if mode == "below" else "GREATER_THAN"
    nt.links.new(sep.outputs["Z"], cmp_.inputs[0])
    nt.links.new(front.outputs[0], cmp_.inputs[1])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(cmp_.outputs[0], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(bsdf.outputs["BSDF"], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    for vn in vol_nodes:                                   # multiply the scatter density by the same factor
        src = vn.inputs[0].links[0].from_node if vn.inputs[0].links else None
        m2 = nt.nodes.new("ShaderNodeMath")
        m2.operation = "MULTIPLY"
        nt.links.new(cmp_.outputs[0], m2.inputs[1])
        nt.links.new(vn.outputs[0], m2.inputs[0])
        vs = [l.to_node for l in vn.outputs[0].links if l.to_node.type == "VOLUME_SCATTER"][0]
        nt.links.new(m2.outputs[0], vs.inputs["Density"])
    return front


def water(name="clear_water", tint="#DFF3F6", density=0.0, absorb="#9FD8E6", clip=None):
    """Physically based water: IOR 1.333, full transmission. density > 0 adds depth absorption in `absorb` (per BU)."""
    m, nt, b, out = _principled(name)
    b.inputs["Base Color"].default_value = lin(tint)
    b.inputs["Roughness"].default_value = 0.0
    b.inputs["IOR"].default_value = 1.333
    b.inputs["Transmission Weight"].default_value = 1.0
    if density:
        _volume(nt, out, "ShaderNodeVolumeAbsorption", Density=density, Color=lin(absorb))
    if clip:
        front = _clip_surface(nt, b, out, clip)
        m["front_node"] = front.name
    return m


def glass(name="clear_glass", tint="#F2FAF8", rough=0.01):
    m, nt, b, out = _principled(name)
    b.inputs["Base Color"].default_value = lin(tint)
    b.inputs["Roughness"].default_value = rough
    b.inputs["IOR"].default_value = 1.5
    b.inputs["Transmission Weight"].default_value = 1.0
    return m


def ice(name="clear_ice", tint="#EAF6FB", core=0.55, seed=0.0, clip=None):
    """Ice: IOR 1.31, frosted patches (noise-driven roughness), a fine melted-surface bump, and a cloudy core (noise-gated volume scatter that fades toward the faces),
    with a faint blue absorption. This is what a real cube looks like: clear skin, white cloudy centre, internal fractures read through refraction."""
    m, nt, b, out = _principled(name)
    b.inputs["Base Color"].default_value = lin(tint)
    b.inputs["IOR"].default_value = 1.31
    b.inputs["Transmission Weight"].default_value = 1.0
    tc = nt.nodes.new("ShaderNodeTexCoord")
    mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Location"].default_value = (seed, seed * 0.7, seed * 1.3)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    # frosting: roughness 0.04 .. 0.38
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 2.2
    nz.inputs["Detail"].default_value = 6.0
    nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    rr = nt.nodes.new("ShaderNodeMapRange")
    rr.inputs["From Min"].default_value, rr.inputs["From Max"].default_value = 0.35, 0.7
    rr.inputs["To Min"].default_value, rr.inputs["To Max"].default_value = 0.04, 0.38
    nt.links.new(nz.outputs["Fac"], rr.inputs["Value"])
    nt.links.new(rr.outputs["Result"], b.inputs["Roughness"])
    # fine bump: melted ripples
    nb = nt.nodes.new("ShaderNodeTexNoise")
    nb.inputs["Scale"].default_value = 9.0
    nb.inputs["Detail"].default_value = 3.0
    nt.links.new(mp.outputs["Vector"], nb.inputs["Vector"])
    bm = nt.nodes.new("ShaderNodeBump")
    bm.inputs["Strength"].default_value = 0.18
    bm.inputs["Distance"].default_value = 0.2
    nt.links.new(nb.outputs["Fac"], bm.inputs["Height"])
    nt.links.new(bm.outputs["Normal"], b.inputs["Normal"])
    # cloudy core: scatter density = noise gate x radial falloff (object space, cube half size ~ 1)
    nv = nt.nodes.new("ShaderNodeTexNoise")
    nv.inputs["Scale"].default_value = 1.6
    nv.inputs["Detail"].default_value = 4.0
    nt.links.new(mp.outputs["Vector"], nv.inputs["Vector"])
    gate = nt.nodes.new("ShaderNodeMapRange")
    gate.inputs["From Min"].default_value, gate.inputs["From Max"].default_value = 0.42, 0.62
    nt.links.new(nv.outputs["Fac"], gate.inputs["Value"])
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
    vl = nt.nodes.new("ShaderNodeVectorMath")
    vl.operation = "LENGTH"
    nt.links.new(tc.outputs["Object"], vl.inputs[0])
    fall = nt.nodes.new("ShaderNodeMapRange")
    fall.inputs["From Min"].default_value, fall.inputs["From Max"].default_value = 0.35, 1.0     # inner part dense, faces clear (cube local size 1 after scale)
    fall.inputs["To Min"].default_value, fall.inputs["To Max"].default_value = 1.0, 0.0
    nt.links.new(vl.outputs["Value"], fall.inputs["Value"])
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    nt.links.new(gate.outputs["Result"], mul.inputs[0])
    nt.links.new(fall.outputs["Result"], mul.inputs[1])
    dens = nt.nodes.new("ShaderNodeMath")
    dens.operation = "MULTIPLY"
    dens.inputs[1].default_value = core
    nt.links.new(mul.outputs["Value"], dens.inputs[0])
    vs = nt.nodes.new("ShaderNodeVolumeScatter")
    vs.inputs["Color"].default_value = lin("#F4FBFF")
    vs.inputs["Anisotropy"].default_value = 0.3
    nt.links.new(dens.outputs["Value"], vs.inputs["Density"])
    va = nt.nodes.new("ShaderNodeVolumeAbsorption")
    va.inputs["Color"].default_value = lin("#9CD3EA")
    va.inputs["Density"].default_value = 0.05
    ad = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(vs.outputs[0], ad.inputs[0])
    nt.links.new(va.outputs[0], ad.inputs[1])
    nt.links.new(ad.outputs[0], out.inputs["Volume"])
    if clip:
        front = _clip_surface(nt, b, out, clip, vol_nodes=(dens,))
        m["front_node"] = front.name
    return m


def coffee(name="shell_y", base="#2B1608", edge="#7A4A27"):
    """Brewed coffee: dark, very glossy surface with a lighter, warm, thin-edge subsurface glow (a liquid, not a block)."""
    m, nt, b, out = _principled(name)
    b.inputs["Base Color"].default_value = lin(base)
    b.inputs["Roughness"].default_value = 0.03
    b.inputs["Specular IOR Level"].default_value = 0.8
    b.inputs["Subsurface Weight"].default_value = 0.35
    b.inputs["Subsurface Radius"].default_value = (1.0, 0.45, 0.2)
    b.inputs["Subsurface Scale"].default_value = 0.6
    try:
        b.inputs["Subsurface Radius"].default_value = (1.2, 0.5, 0.25)
    except Exception:
        pass
    # a pale warm rim of crema toward the edge, driven by Fresnel-like layer weight
    lw = nt.nodes.new("ShaderNodeLayerWeight")
    lw.inputs["Blend"].default_value = 0.55
    mix = nt.nodes.new("ShaderNodeMix")
    mix.data_type = "RGBA"
    mix.inputs["A"].default_value = lin(base)
    mix.inputs["B"].default_value = lin(edge)
    nt.links.new(lw.outputs["Facing"], mix.inputs["Factor"])
    nt.links.new(mix.outputs["Result"], b.inputs["Base Color"])
    return m


def steel(name="g_pin", hex_color="#9AA3AD", rough=0.28, brushed=True):
    m, nt, b, out = _principled(name)
    b.inputs["Base Color"].default_value = lin(hex_color)
    b.inputs["Metallic"].default_value = 1.0
    b.inputs["Roughness"].default_value = rough
    if brushed:
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 60.0
        nz.inputs["Detail"].default_value = 8.0
        bm = nt.nodes.new("ShaderNodeBump")
        bm.inputs["Strength"].default_value = 0.05
        nt.links.new(nz.outputs["Fac"], bm.inputs["Height"])
        nt.links.new(bm.outputs["Normal"], b.inputs["Normal"])
    return m


def wet_tissue(name="g_mark", hex_color="#C4575A", sss=0.5, rough=0.3, coat=0.9, trans=0.0):
    """Soft biological surface: subsurface scattering, a glossy wet coat. Vessels, pulp, the pad of a fingertip."""
    m, nt, b, out = _principled(name)
    b.inputs["Base Color"].default_value = lin(hex_color)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Subsurface Weight"].default_value = sss
    b.inputs["Subsurface Radius"].default_value = (1.0, 0.35, 0.22)
    b.inputs["Subsurface Scale"].default_value = 0.4
    b.inputs["Coat Weight"].default_value = coat
    b.inputs["Coat Roughness"].default_value = 0.06
    if trans:
        b.inputs["Transmission Weight"].default_value = trans
    return m


def stone(name="g_pin", base="#5C6670", seed=0.0, dark="#3C434B"):
    """Wet river stone: glossy coat over a mottled mineral base."""
    m, nt, b, out = _principled(name)
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.inputs["Scale"].default_value = 6.0
    nz.inputs["Detail"].default_value = 8.0
    mp_ = nt.nodes.new("ShaderNodeMapping")
    mp_.inputs["Location"].default_value = (seed, seed * 0.5, seed * 0.3)
    cr = nt.nodes.new("ShaderNodeValToRGB")
    cr.color_ramp.elements[0].color = lin(dark)
    cr.color_ramp.elements[1].color = lin(base)
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], mp_.inputs["Vector"])
    nt.links.new(mp_.outputs["Vector"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"])
    nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.55
    b.inputs["Coat Weight"].default_value = 1.0
    b.inputs["Coat Roughness"].default_value = 0.03
    return m


def emissive(name, hex_color, strength=4.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    e = nt.nodes.new("ShaderNodeEmission")
    e.inputs["Color"].default_value = lin(hex_color)
    e.inputs["Strength"].default_value = strength
    nt.links.new(e.outputs["Emission"], out.inputs["Surface"])
    return m


# ------------------------------------------------------------------------------------------------------ geometry
def smooth(o):
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def _runs(profile, sharp_deg=40.0, max_len=1.2):
    """Split a (r, z) profile into smooth runs at sharp corners and densify long segments, so smooth shading never averages normals across a corner or a tall flat quad
    (that gave streaky refraction on the first glass). Each run is a list of points."""
    pts = list(profile)
    runs, cur = [], [pts[0]]
    for i in range(1, len(pts)):
        a, b = Vector(pts[i - 1]), Vector(pts[i])
        L = (b - a).length
        n = max(1, int(math.ceil(L / max_len)))
        for k in range(1, n):
            cur.append(tuple(a + (b - a) * (k / n)))
        cur.append(pts[i])
        if i < len(pts) - 1:
            d0, d1 = (b - a), (Vector(pts[i + 1]) - b)
            if d0.length > 1e-9 and d1.length > 1e-9 and math.degrees(d0.angle(d1)) > sharp_deg:
                runs.append(cur)
                cur = [pts[i]]
    runs.append(cur)
    return runs


def lathe(name, profile, mat, loc=(0, 0, 0), seg=64, squash=(1.0, 1.0), closed=False, sharp_deg=40.0, max_len=1.2):
    """Solid of revolution about z from a (radius, z) profile that starts and ends on the axis (poles): a manifold solid, needed for transmission and volumes.
    Sharp corners get their own vertices (crisp edges), gentle curves stay smooth."""
    verts, faces = [], []
    for run in _runs(profile, sharp_deg, max_len):
        rings = []
        for r, z in run:
            rings.append(len(verts))
            for i in range(seg):
                a = 2 * math.pi * i / seg
                verts.append((r * math.cos(a) * squash[0], r * math.sin(a) * squash[1], z))
        for k in range(len(run) - 1):
            r0, r1 = rings[k], rings[k + 1]
            for i in range(seg):
                j = (i + 1) % seg
                faces.append((r0 + i, r0 + j, r1 + j, r1 + i))
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.remove_doubles(bm, verts=[v for v in bm.verts if abs(v.co.x) < 1e-6 and abs(v.co.y) < 1e-6], dist=1e-5)     # merge only the pole points
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    o = bpy.data.objects.new(name, mesh)
    bpy.context.scene.collection.objects.link(o)
    o.location = loc
    mesh.materials.append(mat)
    return smooth(o)


def tumbler(S, name, mat_glass, mat_liquid, r=5.0, h=12.0, wall=0.32, base=1.1, level=9.0, loc=(0, 0, 0), meniscus=0.18):
    """A drinking glass (solid wall and thick base, profile revolved) and the liquid inside it, with a meniscus that climbs the wall. Returns (glass, liquid)."""
    ro, ri = r, r - wall
    prof = [(0.0, 0.0), (ro - 0.5, 0.0), (ro - 0.15, 0.12), (ro, 0.7), (ro, h), (ro - wall * 0.5, h + 0.05), (ri, h), (ri, base + 0.15), (ri - 0.7, base), (0.0, base)]
    g = lathe(name, prof, mat_glass, loc=loc, seg=96, closed=False)
    gap = 0.04
    lp = [(0.0, base + gap), (ri - 0.7 - gap, base + gap), (ri - gap, base + gap + 0.15), (ri - gap, level - meniscus), (ri - gap - 0.1, level), (0.0, level - 0.02)]
    lq = lathe(name + "_liquid", lp, mat_liquid, loc=loc, seg=96, closed=False)
    S.reg(g)
    S.reg(lq)
    noshadow(g, lq)
    contact_shadow(S, loc, r * 1.25)
    return g, lq


def ice_cube(S, name, mat, size=2.6, loc=(0, 0, 0), rot=(0, 0, 0), seed=1, bevel=0.35, **tk):
    """A cube of ice: bevelled, then subdivided and noise-displaced so no face is flat, with the cloudy-core material. The object scale carries the size, so the material's
    object-space falloff stays correct."""
    rng = random.Random(seed)
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    mod = o.modifiers.new("bevel", "BEVEL")
    mod.width, mod.segments = 0.22, 4
    sub = o.modifiers.new("sub", "SUBSURF")
    sub.levels = sub.render_levels = 2
    tex = bpy.data.textures.new(name + "_tex", "CLOUDS")
    tex.noise_scale = 0.9 + 0.4 * rng.random()
    dis = o.modifiers.new("melt", "DISPLACE")
    dis.texture, dis.strength, dis.mid_level = tex, 0.07, 0.5
    o.scale = (size / 2, size / 2, size / 2)
    o.data.materials.append(mat)
    smooth(o)
    noshadow(o)
    return S.reg(o, **tk)


def tube(S, name, pts, radii, mat, grow=None, smooth_curve=True):
    """Tube along 3D points with a radius per point (tapering vessels, nerves). grow=(t0, t1) draws it from the first point to the last. Returns (object, curve)."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth, cu.bevel_resolution, cu.use_fill_caps = 1.0, 4, True
    sp = cu.splines.new("NURBS" if smooth_curve else "POLY")
    sp.points.add(len(pts) - 1)
    for p, q, r in zip(sp.points, pts, radii):
        p.co = (q[0], q[1], q[2], 1.0)
        p.radius = r
    if smooth_curve:
        sp.order_u, sp.use_endpoint_u = min(4, len(pts)), True
    o = bpy.data.objects.new(name, cu)
    bpy.context.scene.collection.objects.link(o)
    cu.materials.append(mat)
    if grow:
        cu.bevel_factor_end = 0.0
        S.lines.append((cu, grow))
    return o, cu


def vessel_tree(S, name, root, direction, length, radius, mat, depth=3, spread=0.55, seed=3, plane=None, grow=None, out=None, xlim=None, zmin=None, rlim=None):
    """Branching vessels by a recursive random walk: every branch is a tapering tube that wanders, and splits into two thinner ones. `plane` = (axis index to keep flat, value)
    keeps the network on a cut face. Returns the list of (object, curve, base radius) for animation (constriction scales curve.bevel_depth)."""
    rng = random.Random(seed)
    made = out if out is not None else []

    def branch(p0, d, L, r, lvl, t0):
        pts, radii = [Vector(p0)], [r]
        p = Vector(p0)
        steps = 5
        for k in range(steps):
            jitter = Vector((rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1))) * 0.35
            d = (d + jitter).normalized()
            if plane:
                d[plane[0]] = 0.0
                d = d.normalized()
            p = p + d * (L / steps)
            if plane:
                p[plane[0]] = plane[1]
            if xlim:                                                           # keep |x| inside the tissue band (between the bone and the skin)
                p.x = math.copysign(min(max(abs(p.x), xlim[0]), xlim[1]), p.x if abs(p.x) > 1e-6 else root[0])
            if rlim:                                                           # keep the point inside an annulus around the axis (inside a translucent finger)
                rr = math.hypot(p.x, p.y / 0.84)
                if rr > 1e-6:
                    k = min(max(rr, rlim[0]), rlim[1]) / rr
                    p.x, p.y = p.x * k, p.y * k
            if zmin is not None:
                p.z = max(p.z, zmin)
            pts.append(p.copy())
            radii.append(r * (1.0 - 0.28 * (k + 1) / steps))
        g = None if not grow else (grow[0] + (grow[1] - grow[0]) * 0.12 * (3 - lvl), grow[1])
        o, cu = tube(S, f"{name}_{lvl}_{len(made)}", pts, radii, mat, grow=g)
        made.append((o, cu, 1.0))
        if lvl > 0:
            for sgn in (-1, 1):
                ang = spread * sgn * (0.7 + 0.6 * rng.random())
                ax = Vector((0, 1, 0)) if not plane else Vector((0, 0, 0))
                if plane:
                    ax[plane[0]] = 1.0
                rot = Vector(d).copy()
                rot.rotate(__import__("mathutils").Quaternion(ax if ax.length else Vector((0, 1, 0)), ang))
                branch(pts[-1], rot, L * 0.62, r * 0.66, lvl - 1, t0)
    branch(root, Vector(direction).normalized(), length, radius, depth, 0)
    return made


def heat_volume(S, name, size, loc, hex_color="#FF6A1F", density=0.06, strength=2.0, scale=0.9):
    """A box of emissive, noise-modulated volume: a thermal plume / glow in the same physical language as the rest of the scene. Returns (object, w_input) - animate the noise
    in time by setting w_input.default_value (S.every_frame)."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = size
    m = bpy.data.materials.new(name + "_mat")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nz = nt.nodes.new("ShaderNodeTexNoise")
    nz.noise_dimensions = "4D"
    nz.inputs["Scale"].default_value = scale
    nz.inputs["Detail"].default_value = 3.0
    nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
    cr = nt.nodes.new("ShaderNodeMapRange")
    cr.inputs["From Min"].default_value, cr.inputs["From Max"].default_value = 0.4, 0.75
    nt.links.new(nz.outputs["Fac"], cr.inputs["Value"])
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
    edge = nt.nodes.new("ShaderNodeVectorMath")
    edge.operation = "LENGTH"
    nt.links.new(tc.outputs["Object"], edge.inputs[0])
    fall = nt.nodes.new("ShaderNodeMapRange")
    fall.inputs["From Min"].default_value, fall.inputs["From Max"].default_value = 0.1, 0.75
    fall.inputs["To Min"].default_value, fall.inputs["To Max"].default_value = 1.0, 0.0
    nt.links.new(edge.outputs["Value"], fall.inputs["Value"])
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    nt.links.new(cr.outputs["Result"], mul.inputs[0])
    nt.links.new(fall.outputs["Result"], mul.inputs[1])
    pv = nt.nodes.new("ShaderNodeVolumePrincipled")
    pv.inputs["Color"].default_value = lin(hex_color)
    pv.inputs["Emission Color"].default_value = lin(hex_color)
    pv.inputs["Emission Strength"].default_value = strength
    pv.inputs["Density"].default_value = density
    pv.inputs["Blackbody Intensity"].default_value = 0.0
    nt.links.new(mul.outputs["Value"], pv.inputs["Emission Strength"])
    nt.links.new(pv.outputs[0], out.inputs["Volume"])
    mul2 = nt.nodes.new("ShaderNodeMath")
    mul2.operation = "MULTIPLY"
    mul2.inputs[1].default_value = strength
    nt.links.remove(pv.inputs["Emission Strength"].links[0])
    nt.links.new(mul.outputs["Value"], mul2.inputs[0])
    nt.links.new(mul2.outputs["Value"], pv.inputs["Emission Strength"])
    o.data.materials.append(m)
    o.visible_shadow = False
    return S.reg(o), nz.inputs["W"]


def ray(S, name, p0, p1, r, mat, **tk):
    """A thin emissive tube from p0 to p1 (a ray of infrared light). Returns the registered object (scale it along its length to grow)."""
    a, b = Vector(p0), Vector(p1)
    d = b - a
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=r, depth=d.length, location=(a + b) / 2)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
    o.data.materials.append(mat)
    smooth(o)
    o.visible_shadow = False
    return S.reg(o, **tk)


def droplet(S, name, mat, r, loc, **tk):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=32, ring_count=20)
    o = bpy.context.object
    o.name = name
    o.data.materials.append(mat)
    smooth(o)
    o.visible_shadow = False
    return S.reg(o, **tk)


def softboxes(strength=5.0, tint="#FFFFFF", top=True, sides=True, centre=(0, 0, 7)):
    """Large emissive panels outside the frame, invisible to the camera but seen by reflections and refractions: what makes glass, water and ice sparkle instead of
    reflecting a black room. Not a light-rig change: the production lights from looks.py are untouched."""
    made = []
    m = emissive("softbox", tint, strength)
    specs = []
    if top:
        specs.append(((0, -4, 46), (math.pi, 0, 0), (70, 40)))
    if sides:
        specs += [((-38, -6, 12), (0, math.radians(-90), 0), (30, 50)), ((38, -6, 12), (0, math.radians(90), 0), (30, 50))]
    for i, (loc, rot, sz) in enumerate(specs):
        bpy.ops.mesh.primitive_plane_add(size=1.0, location=(loc[0] + centre[0], loc[1] + centre[1], loc[2] + centre[2] - 7), rotation=rot)
        o = bpy.context.object
        o.name = f"softbox{i}"
        o.scale = (sz[0], sz[1], 1)
        o.data.materials.append(m)
        o.visible_camera = False
        o.visible_shadow = False
        made.append(o)
    return made


def noshadow(*objs):
    """Glass, water and ice must not block shadow rays (Cycles treats refractive surfaces as opaque for light: the contents of a glass go black, measured 2026-11-05 on the
    hand-in-water tray). Pair with contact_shadow() so the object is still grounded."""
    for o in objs:
        o.visible_shadow = False
    return objs


def contact_shadow(S, loc, radius, strength=0.5, squash=(1.0, 0.7)):
    """A soft elliptical dark gradient lying on the floor under a see-through object (its real shadow is switched off by noshadow)."""
    bpy.ops.mesh.primitive_plane_add(size=2.0, location=(loc[0], loc[1], loc[2] + 0.02))
    o = bpy.context.object
    o.name = "contact_shadow"
    o.scale = (radius * squash[0], radius * squash[1], 1)
    m = bpy.data.materials.new("contact_shadow")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    vm = nt.nodes.new("ShaderNodeVectorMath")
    vm.operation = "LENGTH"
    sub = nt.nodes.new("ShaderNodeVectorMath")
    sub.operation = "SUBTRACT"
    sub.inputs[1].default_value = (0.5, 0.5, 0.0)
    nt.links.new(tc.outputs["UV"], sub.inputs[0])
    nt.links.new(sub.outputs["Vector"], vm.inputs[0])
    rr = nt.nodes.new("ShaderNodeMapRange")
    rr.inputs["From Min"].default_value, rr.inputs["From Max"].default_value = 0.0, 0.5
    rr.inputs["To Min"].default_value, rr.inputs["To Max"].default_value = strength, 0.0
    rr.interpolation_type = "SMOOTHSTEP"
    nt.links.new(vm.outputs["Value"], rr.inputs["Value"])
    tr_ = nt.nodes.new("ShaderNodeBsdfTransparent")
    bk = nt.nodes.new("ShaderNodeBsdfDiffuse")
    bk.inputs["Color"].default_value = (0.01, 0.0, 0.02, 1)
    mx = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(rr.outputs["Result"], mx.inputs["Fac"])
    nt.links.new(tr_.outputs[0], mx.inputs[1])
    nt.links.new(bk.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs["Surface"])
    o.data.materials.append(m)
    o.visible_shadow = False
    return o


def pebble(S, name, mat, r=2.6, loc=(0, 0, 0), seed=2, lump=0.22, **tk):
    """A river stone: a squashed sphere pushed around by noise, so it has no symmetric silhouette."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=64, ring_count=40)
    o = bpy.context.object
    o.name = name
    o.scale = (1.0, 0.86, 0.74)
    tex = bpy.data.textures.new(name + "_t", "CLOUDS")
    tex.noise_scale = 0.8 + 0.3 * random.Random(seed).random()
    d = o.modifiers.new("lump", "DISPLACE")
    d.texture, d.strength, d.mid_level = tex, r * lump, 0.5
    o.data.materials.append(mat)
    smooth(o)
    return S.reg(o, **tk)


def set_front(mat, z):
    """Move a clipped material's freezing front to world height z."""
    mat.node_tree.nodes[mat["front_node"]].outputs[0].default_value = z


def slab(S, name, size, loc, mat, bevel=0.25, **tk):
    """A closed bevelled box of see-through material (ice slab, water body)."""
    o = S.box(name, size, loc, mat, bevel=bevel, **tk)
    o.visible_shadow = False
    return o


def disc(S, name, radius, thick, loc, mat, **tk):
    """A thin round slab (an ice lid), with a bevelled edge and a slightly uneven rim."""
    r, t = radius, thick
    prof = [(0.0, 0.0), (r - 0.3, 0.0), (r - 0.05, t * 0.2), (r, t * 0.5), (r - 0.05, t * 0.8), (r - 0.3, t), (0.0, t)]
    o = lathe(name, prof, mat, loc=loc, seg=96)
    noshadow(o)
    return S.reg(o, **tk)
