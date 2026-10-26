"""MCP side of the verification: speaks the MCP stdio protocol to `uvx mcp-for-blender` (the same server Claude Code
launches), lists its tools, then queries the scene, imports an HDRI and triggers one test render.
Usage: python spikes/mcp_verify_client.py <hdri.hdr> <out.png>"""

import json
import subprocess
import sys

hdri, out = sys.argv[1], sys.argv[2]
proc = subprocess.Popen(["uvx", "mcp-for-blender"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL, text=True)
_id = 0


def rpc(method, params=None, notify=False):
    global _id
    msg = {"jsonrpc": "2.0", "method": method, **({"params": params} if params is not None else {})}
    if not notify:
        _id += 1
        msg["id"] = _id
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()
    if notify:
        return None
    while True:
        line = json.loads(proc.stdout.readline())
        if line.get("id") == _id:
            return line


def call(tool, args):
    r = rpc("tools/call", {"name": tool, "arguments": args})
    if "error" in r:
        return f"ERROR {r['error']}"
    return "".join(c.get("text", "") for c in r["result"]["content"])


init = rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                          "clientInfo": {"name": "verify", "version": "0"}})
print("MCP server:", init["result"]["serverInfo"])
rpc("notifications/initialized", notify=True)
tools = [t["name"] for t in rpc("tools/list")["result"]["tools"]]
print("tools:", len(tools), tools[:14])

print("\n1) get_scene_info ->", call("get_scene_info", {})[:400])
code = f'''
import bpy
w = bpy.context.scene.world or bpy.data.worlds.new("w"); bpy.context.scene.world = w; w.use_nodes = True
nt = w.node_tree; env = nt.nodes.new("ShaderNodeTexEnvironment")
env.image = bpy.data.images.load(r"{hdri}")
nt.links.new(env.outputs["Color"], nt.nodes["Background"].inputs["Color"])
bpy.context.scene.view_settings.view_transform = "Standard"
print("HDRI imported:", env.image.name, tuple(env.image.size))
'''
print("\n2) import HDRI ->", call("execute_blender_code", {"code": code})[:300])
code = f'''
import bpy
s = bpy.context.scene
s.render.engine = "BLENDER_EEVEE"; s.render.resolution_x, s.render.resolution_y = 270, 480
s.render.filepath = r"{out}"
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0)); bpy.ops.object.shade_smooth()
bpy.ops.object.camera_add(location=(0, -5, 0), rotation=(1.5708, 0, 0)); s.camera = bpy.context.object
bpy.ops.render.render(write_still=True)
print("rendered ->", s.render.filepath)
'''
print("\n3) test render ->", call("execute_blender_code", {"code": code})[:300])
proc.terminate()
