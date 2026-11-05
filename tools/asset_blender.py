#!/usr/bin/env python3
"""Connect the asset sources for an asset job (docs/current/specs/asset-system.md).

    .venv/bin/python tools/asset_blender.py open                      open Blender with its MCP server and every connected library switched on
    .venv/bin/python tools/asset_blender.py connect-sketchfab         after the owner put SKETCHFAB_API_TOKEN in .env: verify it and mark the source connected
    .venv/bin/python tools/asset_blender.py blenderkit-search <words>  anonymous search, free assets only, allowed licences only
    .venv/bin/python tools/asset_blender.py blenderkit-get <asset-base-id> <folder>   anonymous download of one asset's .blend into a new, empty folder

Secrets: the token lives only in .env (gitignored) and in the environment of the Blender this tool starts. It is never printed, passed on a command line or written anywhere else.
Downloaded .blend files are untrusted: open them only without -y (scripts stay off) and take data with bpy.data.libraries.load.
"""
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
REGISTRY = ROOT / "assets" / "registry.yaml"
START_SCRIPT = Path.home() / ".claude" / "skills" / "blender-kiln" / "tools" / "blender_mcp_start.py"
BLENDER_BIN = Path("/Applications/Blender.app/Contents/MacOS/Blender")
PORT = 9876
BLENDERKIT = "https://www.blendkit.com/api/v1/search/"
BK_LICENCES = {"cc_zero": "CC0-1.0", "royalty_free": "Royalty-Free"}
BK_TERMS = "https://www.blendkit.com/docs/licenses/"
TOKEN_NAME = "SKETCHFAB_API_TOKEN"

OWNER_STEPS = f"""Sketchfab is approved but not connected yet. Owner steps:
  1. Create a free account at https://sketchfab.com
  2. Copy the 32-character token from My Settings > Password & API (https://sketchfab.com/settings/password)
  3. Add this line to {ENV_FILE}, in your editor: {TOKEN_NAME}=<the token>
     Never paste the token into the chat or the repo.
  4. Tell any session "the Sketchfab token is in .env". It runs: .venv/bin/python tools/asset_blender.py connect-sketchfab"""


def read_token(env_file: Path = ENV_FILE) -> str:
    if not env_file.exists():
        return ""
    for line in env_file.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith(f"{TOKEN_NAME}="):
            return line.split("=", 1)[1].strip().strip("'\"")
    return ""


def sketchfab_account(token: str) -> tuple[int, str]:
    """(http status, username). The token goes only in the header of this one request to Sketchfab."""
    req = urllib.request.Request("https://api.sketchfab.com/v3/me", headers={"Authorization": f"Token {token}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.load(r).get("username", "")
    except urllib.error.HTTPError as e:
        return e.code, ""


def mark_connected(today: str, registry: Path = REGISTRY) -> None:
    """Flip only the sketchfab block's status, keeping the file's comments and layout."""
    text = registry.read_text(encoding="utf-8")
    m = re.search(r"(- id: sketchfab\n.*?)(?=\n  - id: )", text, re.S)
    if not m:
        raise SystemExit("no sketchfab block in the registry")
    block = re.sub(r"status: \S+", "status: connected", m.group(1), count=1)
    block = re.sub(r"verified: \S+", f"verified: {today}", block, count=1)
    registry.write_text(text[:m.start(1)] + block + text[m.end(1):], encoding="utf-8")


def connect_sketchfab() -> int:
    token = read_token()
    if not token:
        print(OWNER_STEPS)
        return 1
    status, user = sketchfab_account(token)
    if status != 200:
        print(f"Sketchfab refused the token in .env (HTTP {status}). Copy it again from https://sketchfab.com/settings/password")
        return 1
    mark_connected(time.strftime("%Y-%m-%d"))
    print(f"Sketchfab connected, account '{user}'. Registry status is connected: commit any change. `open` switches the library on.")
    return 0


def port_open() -> bool:
    with socket.socket() as s:
        s.settimeout(1)
        return s.connect_ex(("127.0.0.1", PORT)) == 0


def blender_running() -> bool:
    return subprocess.run(["pgrep", "-x", "Blender"], capture_output=True).returncode == 0


def open_blender() -> int:
    if port_open():
        print(f"Blender already answers on port {PORT}. Library switches and the token are set at launch: close it and re-run if they are off.")
        return 0
    if blender_running():
        print("A Blender is open without its MCP server (after a crash it relaunches itself). Quit it, then run this again.")
        return 1
    token = read_token()
    env = dict(os.environ)
    if token:
        env["BLENDERMCP_SKETCHFAB_API_KEY"] = token     # macOS `open` would drop the environment, hence the direct launch below
    switches = "import bpy, os; s = bpy.context.scene; s.blendermcp_use_polyhaven = True; s.blendermcp_use_sketchfab = bool(os.environ.get('BLENDERMCP_SKETCHFAB_API_KEY'))"
    subprocess.Popen([str(BLENDER_BIN), "--python", str(START_SCRIPT), "--python-expr", switches], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    for _ in range(90):
        if port_open():
            print(f"Blender open, MCP on port {PORT}. Libraries on: polyhaven{', sketchfab' if token else ''}.")
            return 0
        time.sleep(1)
    print("Blender did not answer in 90 s.")
    return 1


def curl_json(url: str) -> dict:
    """BlenderKit answers 403 to Python's urllib and 200 to curl (code3d/TOOLING.md; search too, 2026-11-04)."""
    out = subprocess.run([shutil.which("curl"), "-sL", "--fail", "--max-time", "60", url], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def bk_results(words: str) -> list[dict]:
    query = "+".join(["asset_type:model", "is_free:true"] + [urllib.parse.quote(w) for w in words.split()])
    return curl_json(f"{BLENDERKIT}?query={query}").get("results", [])


def bk_allowed(results: list[dict]) -> list[dict]:
    return [r for r in results if r.get("license") in BK_LICENCES]


def blenderkit_search(words: str) -> int:
    results = bk_results(words)
    keep = sorted(bk_allowed(results), key=lambda r: r["license"] != "cc_zero")     # CC0 first: best licence wins
    for r in keep:
        print(f"{r.get('assetBaseId')}  {BK_LICENCES[r['license']]:12} {(r.get('filesSize') or 0) / 1e6:7.1f} MB  {r.get('name')}  by {(r.get('author') or {}).get('fullName')}  thumb: {r.get('thumbnailMiddleUrl') or r.get('thumbnailSmallUrl')}")
    print(f"{len(keep)} usable of {len(results)} returned. A hit is not a match: look at it before taking it.")
    return 0


def blenderkit_get(base_id: str, folder: str) -> int:
    out = Path(folder)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"{out} is not empty: downloads go in a new, empty folder")
    results = curl_json(f"{BLENDERKIT}?query=asset_base_id:{urllib.parse.quote(base_id)}").get("results", [])
    if not results:
        raise SystemExit(f"no asset {base_id}")
    a = results[0]
    if a.get("license") not in BK_LICENCES:
        raise SystemExit(f"licence {a.get('license')!r} is not allowed")
    blend = next((f for f in a.get("files", []) if f.get("fileType") == "blend"), None)
    if not blend:
        raise SystemExit("this asset has no .blend file")
    signed_req = f"{blend['downloadUrl']}?scene_uuid={uuid.uuid4()}"
    signed = curl_json(signed_req)["filePath"]
    curl = shutil.which("curl")
    out.mkdir(parents=True, exist_ok=True)
    target = out / "source.blend"
    subprocess.run([curl, "-sL", "--fail", "--max-time", "600", "-o", str(target), signed], check=True)
    print(json.dumps({"file": str(target), "bytes": target.stat().st_size,
                      "for asset.json": {"source": {"registry_id": "blenderkit", "url": f"https://www.blendkit.com/asset-gallery-detail/{a.get('id')}/", "asset_id": base_id,
                                                    "author": (a.get("author") or {}).get("fullName"), "retrieved": time.strftime("%Y-%m-%d")},
                                         "licence": {"id": BK_LICENCES[a["license"]], "url": BK_TERMS}}}, indent=2, ensure_ascii=False))
    return 0


def main() -> int:
    args = sys.argv[1:]
    if args[:1] == ["open"]:
        return open_blender()
    if args[:1] == ["connect-sketchfab"]:
        return connect_sketchfab()
    if args[:1] == ["blenderkit-search"] and len(args) > 1:
        return blenderkit_search(" ".join(args[1:]))
    if args[:1] == ["blenderkit-get"] and len(args) == 3:
        return blenderkit_get(args[1], args[2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
