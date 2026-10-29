"""Reads the channel config snapshot inside Blender (which has no PyYAML). The ONE source is channels/umbrella-es.yaml; factory/identity.py exports it
as JSON (build/identity-export.json) and the render driver passes `identity=<path>`. Direct runs: `.venv/bin/python factory/identity.py export`.
Holds no colour and no render number of its own."""
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EXPORT = ROOT / "build" / "identity-export.json"
_cache: dict = {}


def data(args: dict | None = None) -> dict:
    path = (args or {}).get("identity") or os.environ.get("SHORTS_IDENTITY") or str(DEFAULT_EXPORT)
    if path not in _cache:
        if not Path(path).exists():
            raise FileNotFoundError(f"identity export {path} missing: run `.venv/bin/python factory/identity.py export` (the render driver does it automatically)")
        _cache[path] = json.loads(Path(path).read_text(encoding="utf-8"))
    return _cache[path]


def preset(name: str | None = None, args: dict | None = None) -> dict:
    d = data(args)
    return d["presets"][name or d["active"]]


def script_stem() -> str:
    """Basename of the scene script Blender was started with (tape_02, gear_05 ...), used to look up its scene type."""
    argv = sys.argv
    for i, a in enumerate(argv):
        if a == "--python" and i + 1 < len(argv):
            return Path(argv[i + 1]).stem
    return ""


def render_profile(args: dict | None = None) -> tuple[str, dict]:
    """(profile name, its settings): explicit `profile=` arg > the scene type's profile > the default profile (all from the config)."""
    r = data(args)["render"]
    name = (args or {}).get("profile")
    if not name:
        stype = r.get("scene_types", {}).get(script_stem())
        name = r.get("scene_type_profiles", {}).get(stype) if stype else None
    name = name or r["default_profile"]
    return name, r["profiles"][name]
