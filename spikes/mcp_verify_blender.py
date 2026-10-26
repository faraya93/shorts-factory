"""Blender side of the MCP verification (run: blender -b --python spikes/mcp_verify_blender.py -- <seconds>).
The MCP add-on refuses to start in background mode by design (its commands are drained by a main-thread timer),
so this harness starts the add-on's own socket server manually and calls its drain method in a loop. It exercises
the same command handlers the real MCP server uses; it does NOT prove the live-GUI path."""

import socket
import sys
import threading
import time

import bpy

seconds = float(sys.argv[sys.argv.index("--") + 1])
bpy.ops.preferences.addon_enable(module="blender_mcp")
import blender_mcp as m  # noqa: E402

server = m.BlenderMCPServer(port=9876)
server.running = True
server.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.socket.bind((server.host, server.port))
server.socket.listen(5)
server.server_thread = threading.Thread(target=server._server_loop, daemon=True)
server.server_thread.start()
print("HARNESS ready on", server.port, flush=True)

end = time.time() + seconds
while time.time() < end:
    server._drain_command_queue()
    time.sleep(0.05)
print("HARNESS done", flush=True)
