"""Script provenance stamp (doctrine-topics-and-scripts.md "Who writes the script", lens decision 2026-11-11, block B2 of
docs/current/reports/architecture-second-opinion-2026-11-11.md).

Every script is written by an Opus creative session, which stamps the production folder with <prod>/provenance.json. A production
session never writes a script and never writes the stamp (tools/runner-settings.json denies it). The runner refuses an unstamped unit;
scenes_schema.py and the final-render paths refuse an unstamped production numbered PROVENANCE_FROM or later.

usage: .venv/bin/python factory/provenance.py stamp productions/<ch>/<video> --model <model id> --record "<report or lens-decision row>" [--evidence "..."] [--script-rev <commit>]
       .venv/bin/python factory/provenance.py check productions/<ch>/<video>
--script-rev hashes script.json as it stood in that commit (a stamp written after the fact, from the repo's own records); otherwise the file on disk."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "provenance.json"
WRITER = "creative-session"
PROVENANCE_FROM = 25          # productions numbered from 025 need a stamp before a final render; the runner needs one for every unit
HEX64 = re.compile(r"^[0-9a-f]{64}$")


def errors(prod: Path) -> list[str]:
    """Empty when the folder carries a well-formed stamp from an Opus creative session for a script that exists."""
    f = prod / NAME
    if not f.exists():
        return [f"{prod.name}: no {NAME}: its script has no recorded Opus creative session (a production session never writes a script)"]
    try:
        s = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"{prod.name}: {NAME} is not JSON: {e}"]
    out = []
    if s.get("script_by") != WRITER:
        out.append(f"{prod.name}: {NAME} script_by must be {WRITER!r}")
    if "opus" not in str(s.get("model", "")).lower():
        out.append(f"{prod.name}: {NAME} model must be an Opus model, got {s.get('model')!r}")
    if not str(s.get("record", "")).strip():
        out.append(f"{prod.name}: {NAME} needs the record that proves it (report or lens-decision row)")
    if not HEX64.match(str(s.get("script_sha256", ""))):
        out.append(f"{prod.name}: {NAME} script_sha256 missing or malformed")
    if not (prod / "script.json").exists():
        out.append(f"{prod.name}: stamped but no script.json on file")
    return out


def required(prod: Path) -> bool:
    m = re.match(r"(\d{3})-", prod.name)
    return bool(m) and int(m.group(1)) >= PROVENANCE_FROM


def gate_errors(prod: Path) -> list[str]:
    """What a final render or a spend refuses on: a stamp is required from PROVENANCE_FROM on."""
    return errors(prod) if required(prod) else []


def script_hash(prod: Path, rev: str | None = None) -> str:
    if rev:
        rel = (prod / "script.json").resolve().relative_to(ROOT)
        data = subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=ROOT, capture_output=True, check=True).stdout
    else:
        data = (prod / "script.json").read_bytes()
    return hashlib.sha256(data).hexdigest()


def stamp(prod: Path, model: str, record: str, evidence: str = "", rev: str | None = None) -> dict:
    if "opus" not in model.lower():
        raise SystemExit(f"refused: the stamp records an Opus creative session, got model {model!r}")
    if not record.strip():
        raise SystemExit("refused: --record must name the report or lens-decision row that proves the script's origin")
    if not (prod / "script.json").exists():
        raise SystemExit(f"refused: {prod} has no script.json")
    f = prod / NAME
    prev = json.loads(f.read_text(encoding="utf-8")) if f.exists() else None
    s = {"script_by": WRITER, "model": model, "at": date.today().isoformat(), "record": record.strip(), "evidence": evidence.strip(),
         "script_sha256": script_hash(prod, rev), "script_rev": rev or "working tree"}
    if prev:
        s["history"] = prev.pop("history", []) + [prev]
    f.write_text(json.dumps(s, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return s


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("stamp"); p.add_argument("production", type=Path); p.add_argument("--model", required=True); p.add_argument("--record", required=True)
    p.add_argument("--evidence", default=""); p.add_argument("--script-rev")
    p = sub.add_parser("check"); p.add_argument("production", type=Path)
    a = ap.parse_args()
    prod = a.production.resolve()
    if a.cmd == "stamp":
        print(json.dumps(stamp(prod, a.model, a.record, a.evidence, a.script_rev), ensure_ascii=False))
        return 0
    errs = errors(prod)
    print("\n".join(errs) if errs else f"{prod.name}: provenance OK")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
