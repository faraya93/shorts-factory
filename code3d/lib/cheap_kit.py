"""Cheap material routes for expensive element classes (playbook: docs/current/specs/render-cost-playbook.md; measured on production 008's heaviest scene).
Each route trades optical fidelity for time; a route changes what the element looks like, so an element under the likeness gate is re-read after switching."""
import bpy
import real_kit as rk

_real_ice = rk.ice      # bound at import, so a caller may swap rk.ice for ice_milky without recursion


def _nodes(m, kind):
    return [n for n in m.node_tree.nodes if n.type == kind]


def _unlink_volume(m):
    out = _nodes(m, "OUTPUT_MATERIAL")[0]
    for l in list(out.inputs["Volume"].links):
        m.node_tree.links.remove(l)


def ice_milky(name="clear_ice", tint="#EAF6FB", core=0.55, seed=0.0, clip=None, strength=0.6):
    """Ice with no volume: the noise gate that drove the volumetric core instead lowers transmission on the surface, so cloudy patches read as milky ice."""
    m = _real_ice(name, tint, core, seed, clip)
    _unlink_volume(m)
    nt, b = m.node_tree, _nodes(m, "BSDF_PRINCIPLED")[0]
    gate = next(n for n in _nodes(m, "MAP_RANGE") if abs(n.inputs["From Min"].default_value - 0.42) < 1e-6)
    inv = nt.nodes.new("ShaderNodeMapRange")
    inv.inputs["To Min"].default_value, inv.inputs["To Max"].default_value = 1.0, 1.0 - strength
    nt.links.new(gate.outputs["Result"], inv.inputs["Value"])
    nt.links.new(inv.outputs["Result"], b.inputs["Transmission Weight"])
    return m


def no_volume(m):
    """Drop a material's volume entirely (context water with a faint absorption, for instance)."""
    _unlink_volume(m)
    return m


def thin_wall(m):
    """One refraction event per surface: a glass shell stops bending what is behind it, and transmission depth falls."""
    b = _nodes(m, "BSDF_PRINCIPLED")[0]
    b.inputs["Thin Wall"].default_value = True if b.inputs["Thin Wall"].type == "BOOLEAN" else 1.0
    return m


def fake_indirect(m):
    """Context glass only: indirect diffuse and glossy rays pass straight through. Camera rays still see glass. Never on an element under test without a re-read."""
    nt = m.node_tree
    out = _nodes(m, "OUTPUT_MATERIAL")[0]
    src = out.inputs["Surface"].links[0].from_socket
    lp, add, mix, tr = nt.nodes.new("ShaderNodeLightPath"), nt.nodes.new("ShaderNodeMath"), nt.nodes.new("ShaderNodeMixShader"), nt.nodes.new("ShaderNodeBsdfTransparent")
    add.operation = "MAXIMUM"
    nt.links.new(lp.outputs["Is Diffuse Ray"], add.inputs[0])
    nt.links.new(lp.outputs["Is Glossy Ray"], add.inputs[1])
    nt.links.new(add.outputs[0], mix.inputs[0])
    nt.links.new(src, mix.inputs[1])
    nt.links.new(tr.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    return m
