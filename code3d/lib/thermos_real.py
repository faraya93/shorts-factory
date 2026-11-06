"""Real thermos for 009 (every-element remake 2026-11-05). Runs inside Blender (Cycles, `transparent` profile).

thermos(S, ...) builds a hollow DOUBLE-WALLED flask from real lathes: an outer enamel shell with a steel base band, a polished inner steel flask, and the coffee inside it as a clear amber refracting
liquid with a meniscus. A SWEEPING CUT PLANE (a Value node per material: world y) makes the front of the shells transparent between two heights, so the wall structure, the vacuum gap and
the coffee are revealed by a moving cut instead of a static diagram. Heat is drawn in the same physical language: the inner wall GLOWS (emission driven by a node), the air in the gap is a
swarm of tiny glass spheres that jitter (convection) and fly out when the air is pumped out, infrared is a bundle of thin emissive rays that cross the gap and bounce off the mirror wall."""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import real_kit as rk  # noqa: E402

RO, T, GAP, H = 4.2, 0.4, 0.9, 28.0
RI_O = RO - T - GAP                 # outer radius of the inner flask
T2 = 0.35
H2 = 26.5
LEVEL = 21.0                        # coffee level


def _shell(name, ro, wall, h, base, mat, loc, seg=96):
    ri = ro - wall
    prof = [(0.0, 0.0), (ro - 0.5, 0.0), (ro - 0.15, 0.12), (ro, 0.7), (ro, h), (ro - wall * 0.5, h + 0.05), (ri, h), (ri, base + 0.15), (ri - 0.7, base), (0.0, base)]
    return rk.lathe(name, prof, mat, loc=loc, seg=seg)


def add_cut(mat, z0=3.2, z1=24.5):
    """Make `mat` transparent in a front window: where world y < the 'cut' Value and z0 < z < z1. Returns the Value node (set outputs[0].default_value per frame)."""
    nt = mat.node_tree
    out = next(n for n in nt.nodes if n.type == "OUTPUT_MATERIAL")
    src = out.inputs["Surface"].links[0].from_node
    cut = nt.nodes.new("ShaderNodeValue")
    cut.outputs[0].default_value = -99.0
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(geo.outputs["Position"], sep.inputs["Vector"])
    ly = nt.nodes.new("ShaderNodeMath")
    ly.operation = "LESS_THAN"
    nt.links.new(sep.outputs["Y"], ly.inputs[0])
    nt.links.new(cut.outputs[0], ly.inputs[1])
    gz = nt.nodes.new("ShaderNodeMath")
    gz.operation = "GREATER_THAN"
    gz.inputs[1].default_value = z0
    nt.links.new(sep.outputs["Z"], gz.inputs[0])
    lz = nt.nodes.new("ShaderNodeMath")
    lz.operation = "LESS_THAN"
    lz.inputs[1].default_value = z1
    nt.links.new(sep.outputs["Z"], lz.inputs[0])
    a = nt.nodes.new("ShaderNodeMath")
    a.operation = "MULTIPLY"
    nt.links.new(ly.outputs[0], a.inputs[0])
    nt.links.new(gz.outputs[0], a.inputs[1])
    b = nt.nodes.new("ShaderNodeMath")
    b.operation = "MULTIPLY"
    nt.links.new(a.outputs[0], b.inputs[0])
    nt.links.new(lz.outputs[0], b.inputs[1])
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(b.outputs[0], mix.inputs["Fac"])
    nt.links.new(src.outputs[0] if src.type != "BSDF_PRINCIPLED" else src.outputs["BSDF"], mix.inputs[1])
    nt.links.new(tr.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return cut


def hot_steel(name="g_pin", hex_color="#B8C0CA"):
    """Polished steel whose emission can be raised (the wall warming up): returns (material, emission strength input)."""
    m = rk.steel(name, hex_color, rough=0.18, brushed=False)
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Emission Color"].default_value = rk.lin("#FF5A1A")
    b.inputs["Emission Strength"].default_value = 0.0
    return m, b.inputs["Emission Strength"]


def thermos(S, loc=(0, 0, 0), enamel="#2D6FB7"):
    """Build the cut-away thermos. Returns a dict: cuts (list of Value nodes to animate together), hot (emission input of the inner wall), parts."""
    P = {}
    enam = rk.wet_tissue("g_big", enamel, sss=0.0, rough=0.28, coat=0.5)
    P["outer"] = _shell("outer", RO, T, H, 1.0, enam, loc)
    band_m = rk.steel("g_pin", "#9AA3AD", rough=0.3)
    P["band_lo"] = S.torus("band_lo", RO + 0.02, 0.32, (loc[0], loc[1], loc[2] + 2.0), band_m)
    P["band_hi"] = S.torus("band_hi", RO + 0.02, 0.32, (loc[0], loc[1], loc[2] + 26.2), band_m)
    handle_m = rk.wet_tissue("rubber_k", "#2B2B33", sss=0.0, rough=0.5, coat=0.1)
    P["handle"] = S.torus("handle", 3.3, 0.5, (loc[0] + RO + 0.4, loc[1], loc[2] + 14.0), handle_m, rot=(math.pi / 2, 0, 0))             # the side handle: what makes a flask a flask
    inner_m, hot = hot_steel()
    inner_m.name = "g_pin"
    P["inner"] = _shell("inner", RI_O, T2, H2, 2.0, inner_m, loc)
    lip = rk.lathe("liq", [(0.0, 2.0 + T2 + 0.04), (RI_O - T2 - 0.1, 2.0 + T2 + 0.04), (RI_O - T2 - 0.04, 2.0 + T2 + 0.2), (RI_O - T2 - 0.04, LEVEL - 0.15), (RI_O - T2 - 0.2, LEVEL), (0.0, LEVEL - 0.02)],
                   rk.water("clear_coffee", "#7A5430", density=0.1, absorb="#B5792F"), loc=loc, seg=96)
    rk.noshadow(lip)
    P["coffee"] = lip
    cuts = [add_cut(enam), add_cut(inner_m)]
    for o in (P["outer"], P["inner"]):
        S.reg(o)
    S.reg(lip)
    P["cuts"], P["hot"] = cuts, hot
    return P


def set_cut(P, y):
    for c in P["cuts"]:
        c.outputs[0].default_value = y


def cap(S, mat, loc=(0, 0, H + 3.2)):
    root = S.empty("cap", loc)
    S.cyl("cap_cup", 4.6, 6.2, (0, 0, 0), mat, axis="Z", verts=64, bevel=0.5, parent=root)
    for i, dz in enumerate((-1.8, 0.0, 1.8)):
        S.torus(f"cap_rib{i}", 4.65, 0.22, (0, 0, dz), mat, parent=root)
    S.cyl("cap_knob", 1.1, 1.2, (0, 0, 3.6), rk.steel("g_pin", "#9AA3AD"), axis="Z", verts=32, bevel=0.2, parent=root)
    return root


def front_light(strength=3.5):
    """A big emissive panel in front of the camera side, invisible to the camera: lights the inside of the cut-away (reflections and refraction), like a softbox."""
    m = rk.emissive("softbox", "#FFFFFF", strength)
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=(0, -70, 16), rotation=(-math.pi / 2, 0, 0))
    o = bpy.context.object
    o.name = "front_panel"
    o.scale = (70, 60, 1)
    o.data.materials.append(m)
    o.visible_camera = False
    o.visible_shadow = False
    return o
