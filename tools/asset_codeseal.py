"""Land a code-primitive asset job and seal it (block B5): set route/licence/rig module/built states in assets/library/<slug>/asset.json, run isolated blind naming on the given stills
(tools/blind_read.py, the library's own judge and bar), and only when the naming passes mark the asset `ready` and seal it. Never touches thresholds or aliases.
usage: .venv/bin/python tools/asset_codeseal.py <slug> <rig_module> "<state>" [--state "<state>"...] -- <still> [<still>...]"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import asset_library as al  # noqa: E402


def main() -> int:
    argv = sys.argv[1:]
    cut = argv.index("--")
    head, stills = argv[:cut], argv[cut + 1:]
    slug, rig, states = head[0], head[1], [h for h in head[2:] if h != "--state"]
    m = al.read_meta(slug)
    m.update(route="code-primitive")
    m["licence"] = {"id": "own-work", "url": None, "attribution": None, "note": f"built in this factory ({rig})", "decision": None}
    m["files"].update(rig_module=rig, blend=None)
    m["brief"]["states"] = states
    m["source"] = {k: None for k in m.get("source", {"registry_id": None})}
    al.write_meta(m)
    r = subprocess.run([str(ROOT / ".venv/bin/python"), str(ROOT / "tools/blind_read.py"), *stills, "--record", "blind", slug], capture_output=True, text=True)
    print(r.stdout[-1500:])
    if r.returncode != 0:
        print(f"{slug}: blind naming FAILED; the asset stays in_progress")
        return 1
    m = al.read_meta(slug)
    m["status"] = "ready"
    al.write_meta(m)
    al.seal(slug)
    errs, warns = al.validate(slug, al.source_ids())
    print(f"{slug}: {'OK' if not errs else errs}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
