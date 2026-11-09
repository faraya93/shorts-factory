"""Shared helpers for the termo2 scenes (not a scene: no number suffix)."""
import math
import bpy
from mathutils import Vector


def grow_ray(o, p0, p1, t0, t1, t_off=None, t_off1=None):
    """Return an update fn(t): the ray grows from p0 to p1 between t0 and t1 (and, if t_off given, shrinks away from p0 toward p1 between t_off and t_off1)."""
    a, b = Vector(p0), Vector(p1)
    d = b - a
    L = d.length

    def upd(t):
        u = min(max((t - t0) / (t1 - t0), 0.0), 1.0)
        v = 0.0 if t_off is None else min(max((t - t_off) / (t_off1 - t_off), 0.0), 1.0)
        n = max(u - v, 1e-3)
        o.scale = (1, 1, n)
        o.location = a + d * (v + (u - v) / 2)
    return upd


def window(P, z0, z1):
    """Narrow (or move) the cut window of a built thermos: the shells' cut materials hold two Math nodes with the window heights (defaults 3.2 and 24.5)."""
    for key in ("outer", "inner"):
        for slot in P[key].material_slots:
            for n in slot.material.node_tree.nodes:
                if n.type == "MATH" and n.operation == "GREATER_THAN" and abs(n.inputs[1].default_value - 3.2) < 1e-6:
                    n.inputs[1].default_value = z0
                if n.type == "MATH" and n.operation == "LESS_THAN" and abs(n.inputs[1].default_value - 24.5) < 1e-6:
                    n.inputs[1].default_value = z1


def even_light(vol, gain=1.2, colour=(1.0, 1.0, 1.0, 1.0)):
    """Adds emission proportional to the steam's own density, so a light cut off by the flask cannot draw a hard horizontal break across the column (visibility fix 2026-11-08)."""
    nt = vol.active_material.node_tree
    sc = next(n for n in nt.nodes if n.type == "VOLUME_SCATTER")
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    mul = nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    mul.inputs[1].default_value = gain
    nt.links.new(sc.inputs["Density"].links[0].from_socket, mul.inputs[0])
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = colour
    nt.links.new(mul.outputs[0], em.inputs["Strength"])
    add = nt.nodes.new("ShaderNodeAddShader")
    nt.links.new(sc.outputs[0], add.inputs[0])
    nt.links.new(em.outputs[0], add.inputs[1])
    nt.links.new(add.outputs[0], out.inputs["Volume"])


def wisp_steam(S, name, size, loc, density=2.0, warp=0.28, gain=0.7, scatter=(1.0, 1.0, 1.0, 1.0), emit=(1.0, 1.0, 1.0, 1.0), seed=0.0):
    """Steam that reads as steam: a column whose axis curls more the higher it rises and whose density breaks into wisps. A straight, even, tapered column read as a flashlight beam to three of three blind readers
    (2026-11-08). Returns (object, time value socket); the time socket feeds every noise, set default_value per frame. Density-proportional emission: no light can draw a step across it."""
    import bpy
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
    o = bpy.context.object
    o.name, o.scale = name, size
    m = bpy.data.materials.new(name + "_mat")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    N, L = nt.nodes.new, nt.links.new

    def maprange(src, a, b, c=0.0, d=1.0):
        n = N("ShaderNodeMapRange")
        n.inputs["From Min"].default_value, n.inputs["From Max"].default_value, n.inputs["To Min"].default_value, n.inputs["To Max"].default_value = a, b, c, d
        L(src, n.inputs["Value"])
        return n.outputs["Result"]

    def math(op, x, y=None):
        n = N("ShaderNodeMath")
        n.operation = op
        for i, v in enumerate((x, y)):
            if v is None:
                continue
            if isinstance(v, (int, float)):
                n.inputs[i].default_value = v
            else:
                L(v, n.inputs[i])
        return n.outputs[0]

    out, tc, sep = N("ShaderNodeOutputMaterial"), N("ShaderNodeTexCoord"), N("ShaderNodeSeparateXYZ")
    L(tc.outputs["Object"], sep.inputs["Vector"])
    time = N("ShaderNodeValue")
    x, y, z = sep.outputs["X"], sep.outputs["Y"], sep.outputs["Z"]
    h = maprange(z, -0.5, 0.5)                                               # 0 at the mouth, 1 at the top

    def curl(off):
        cz = N("ShaderNodeCombineXYZ")
        L(math("MULTIPLY", z, 2.2), cz.inputs["Z"])
        cz.inputs["X"].default_value = off + seed
        nz = N("ShaderNodeTexNoise")
        nz.noise_dimensions = "4D"
        nz.inputs["Scale"].default_value = 1.0
        nz.inputs["Detail"].default_value = 1.0
        L(cz.outputs[0], nz.inputs["Vector"])
        L(time.outputs[0], nz.inputs["W"])
        return math("MULTIPLY", maprange(nz.outputs["Fac"], 0.3, 0.7, -1.0, 1.0), math("MULTIPLY", h, warp))

    xw, yw = math("SUBTRACT", x, curl(0.0)), math("SUBTRACT", y, curl(7.3))
    r = math("SQRT", math("ADD", math("MULTIPLY", xw, xw), math("MULTIPLY", yw, yw)))
    edge = maprange(h, 0.0, 1.0, 0.07, 0.30)
    radial = math("POWER", maprange(math("DIVIDE", r, edge), 0.0, 1.0, 1.0, 0.0), 1.4)
    ends = math("SINE", math("MULTIPLY", math("POWER", h, 0.55), 3.14159))     # peaks low, no flat cap at either end
    wn = N("ShaderNodeTexNoise")
    wn.noise_dimensions = "4D"
    wn.inputs["Scale"].default_value = 5.0
    wn.inputs["Detail"].default_value = 5.0
    wn.inputs["Roughness"].default_value = 0.6
    L(tc.outputs["Object"], wn.inputs["Vector"])
    L(time.outputs[0], wn.inputs["W"])
    wisps = maprange(wn.outputs["Fac"], 0.38, 0.62)
    dens = math("MULTIPLY", math("MULTIPLY", math("MULTIPLY", radial, ends), wisps), density)
    sc, em, add = N("ShaderNodeVolumeScatter"), N("ShaderNodeEmission"), N("ShaderNodeAddShader")
    sc.inputs["Color"].default_value, em.inputs["Color"].default_value = scatter, emit
    L(dens, sc.inputs["Density"])
    L(math("MULTIPLY", dens, gain), em.inputs["Strength"])
    L(sc.outputs[0], add.inputs[0])
    L(em.outputs[0], add.inputs[1])
    L(add.outputs[0], out.inputs["Volume"])
    o.data.materials.append(m)
    S.reg(o)
    return o, time.outputs[0]
