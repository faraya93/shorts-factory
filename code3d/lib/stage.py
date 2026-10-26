"""Shared stage for code3d scenes (runs inside Blender): materials, studio world, camera, key light, and the runner that
poses everything from time `t` via a frame handler and renders stills (iteration) or the animation.
New scenes call `Stage(production, mode)`, build their objects, then `stage.run(update, slot)`."""

import sys
from pathlib import Path

import bpy
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402


class Stage:
    def __init__(self, production: Path, mode: str = "draft", hdri_strength: float = 1.0, key_energy: float = 500.0):
        self.production, self.mode = production, mode
        self.vi = c.identity(production)
        self.pal = c.palette(self.vi)
        self.scene = c.reset_scene()
        c.setup_render(self.scene, mode)
        c.studio_world(self.scene, self.pal["backdrop"], c.ASSETS / "hdri" / "studio_small_08_2k.hdr", hdri_strength)
        self.skin = c.append_material(c.ASSETS / "materials" / "blenderkit-sss-skin-shader.blend", "SSS Skin Shader")
        group = next(n for n in self.skin.node_tree.nodes if n.type == "GROUP")
        group.inputs["Diffuse Color"].default_value = c.linear(self.pal["skin peach"])
        group.inputs["unScatter Color"].default_value = c.linear(self.pal["shaded skin"])
        group.inputs["Medium Scatter Color"].default_value = c.linear(self.pal["tissue red"])
        self.tissue = c.principled("tissue", self.pal["tissue red"], roughness=0.55, subsurface=0.15)
        self.steel = c.principled("steel", self.pal["steel grey"], roughness=0.15, metallic=1.0)
        self.thread_mat = c.principled("thread", "#17171B", roughness=0.55)
        self.cam = c.make_camera(self.scene, lens=50.0)
        c.add_light(self.scene, "AREA", (-4.5, -5.5, 7.5), energy=key_energy, size=5.0, target=Vector((0, 0, 0)))

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
