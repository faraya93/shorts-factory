"""One-call orientation for a production session (block B3, P5 of docs/current/reports/architecture-second-opinion-2026-11-11.md). Read-only; replaces the ~50 ls/grep/sed calls
a session spent finding its bearings (019: 26 ls and 30 grep/sed).
usage: .venv/bin/python tools/status.py productions/<ch>/<video>
Prints: provenance, notes header, the last checkpoint, script/scenes/audio presence, per scene (scene file, audio, stills, element count), gate state (frozen, last record),
queued final, the verifier's verdict, and the unit's uncommitted files. It never starts Blender and never writes."""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
HEADER_LINES = 30
CHECKPOINT_CHARS = 2500


def _json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def notes_header(prod: Path) -> str:
    """The notes.md header: everything before the first ledger line / second-level section beyond HEADER_LINES."""
    try:
        lines = (prod / "notes.md").read_text(encoding="utf-8").splitlines()
    except OSError:
        return "(no notes.md)"
    return "\n".join(lines[:HEADER_LINES]) + (f"\n... ({len(lines)} lines in all; read the rest only if you need it)" if len(lines) > HEADER_LINES else "")


def scene_rows(prod: Path) -> list[str]:
    cfg = _json(prod / "scenes.json")
    if not cfg:
        return ["scenes.json: missing"]
    prefix = cfg.get("scene_script_prefix", "scene")
    els = cfg.get("scene_elements") or {}
    rows = [f"scenes.json: {len(cfg.get('scenes', []))} scenes, gate_version {cfg.get('gate_version')}, hero_rig {cfg.get('hero_rig')}, engine {cfg.get('engine') or cfg.get('primary_engine')}"]
    for sc in cfg.get("scenes", []):
        n = int(sc.get("id", sc.get("n", 0)) or 0)
        code = ROOT / "code3d" / "scenes" / f"{prefix}_{n:02d}.py"
        audio = prod / "audio" / f"scene-{n:02d}.mp3"
        stills = sorted((prod / "build" / "stills" / f"s{n:02d}").glob("still-*.png")) if (prod / "build" / "stills").exists() else []
        rows.append(f"  scene {n:02d}: code {'yes' if code.exists() else 'NO'}  audio {'yes' if audio.exists() else 'NO'}  stills {len(stills)}  elements {len(els.get(str(n), []))}  cost_class {sc.get('render_cost_class', '?')}")
    return rows


def gate_rows(prod: Path) -> list[str]:
    g = prod / "build" / "gate"
    if not g.exists():
        return ["gate: no records yet"]
    rows = []
    fz = _json(g / "freeze.json")
    rows.append(f"gate: {'frozen ' + str(fz.get('date')) if fz else 'hero NOT frozen'}")
    el = _json(g / "elements.json")
    if isinstance(el, dict):
        passed = sum(1 for v in el.values() if isinstance(v, dict) and v.get("passed"))
        rows.append(f"  elements recorded: {len(el)}, passed {passed}")
    md = g / "gate.md"
    if md.exists():
        tail = [l for l in md.read_text(errors="replace").splitlines() if l.strip()][-6:]
        rows += ["  gate.md (tail):"] + [f"    {l[:200]}" for l in tail]
    return rows


def verifier(prod: Path) -> str:
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "verify_production.py"), str(prod)], capture_output=True, text=True)
    out = (r.stdout or r.stderr).strip().splitlines()
    return f"verifier exit {r.returncode}: " + ("\n  ".join([""] + out[:12]) if out else "(no output)")


def git_rows(prod: Path) -> list[str]:
    rel = str(prod.relative_to(ROOT))
    r = subprocess.run(["git", "-C", str(ROOT), "status", "--short", "--", rel], capture_output=True, text=True).stdout.splitlines()
    return [f"git: {len(r)} uncommitted path(s) in the unit"] + [f"  {l}" for l in r[:15]]


def report(prod: Path, run_verifier: bool = True) -> str:
    import provenance
    out = [f"== {prod.name}"]
    prov = provenance.errors(prod)
    out.append("provenance: " + ("OK" if not prov else "; ".join(prov)))
    out += ["-- notes header", notes_header(prod)]
    cp = prod / "build" / "checkpoint.md"
    if cp.exists():
        text = cp.read_text(encoding="utf-8", errors="replace")
        out += ["-- checkpoint (build/checkpoint.md)", text[-CHECKPOINT_CHARS:] if len(text) > CHECKPOINT_CHARS else text]
    out += ["-- scenes"] + scene_rows(prod)
    out += gate_rows(prod)
    q = _json(prod / "build" / "queued.json")
    out.append(f"queued final: {q.get('at') if q else 'no'}")
    if (prod / "returned.json").exists():
        out.append("RETURNED: returned.json exists (" + str((_json(prod / "returned.json") or {}).get("reason", ""))[:160] + ")")
    out += git_rows(prod)
    if run_verifier:
        out.append(verifier(prod))
    return "\n".join(out)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        sys.exit(__doc__)
    p = Path(args[0]).resolve()
    if not p.is_dir() or not re.match(r"\d{3}-", p.name):
        sys.exit(f"not a production folder: {args[0]}")
    print(report(p, "--no-verify" not in sys.argv))
