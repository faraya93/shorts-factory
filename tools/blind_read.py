"""Isolated blind readers (2026-11-08). The audit found 158 of 174 past readers had CLAUDE.md in their context, which names the catalogue's subjects. Each reader here is a fresh headless session
in an empty neutral folder (no CLAUDE.md to discover, no project memory, no settings, no MCP, Read tool only) that sees only neutrally named copies of the stills.
usage: .venv/bin/python tools/blind_read.py [--record element <prod> <scene> <id> | likeness <prod> <slug> | blind <slug>] [--multi] [--readers 3] <still> [...]
Every reading is counted: a low reader is never discarded or re-rolled (report 2026-11-08, flag 9)."""
import argparse
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import asset_library as al  # noqa: E402

MODEL = os.environ.get("SF_READER_MODEL", "haiku")
FORMAT = ' Reply with ONLY one line of JSON: {"guess": "<your answer as text>", "confidence": <0-100>}.'


def read_once(folder: Path, prompt: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_PROJECT"))}
    r = subprocess.run(["claude", "-p", prompt + FORMAT, "--tools", "Read", "--allowedTools", "Read", "--setting-sources", "", "--strict-mcp-config", "--no-session-persistence", "--model", MODEL, "--output-format", "text"],
                       cwd=folder, capture_output=True, text=True, env=env, timeout=240, stdin=subprocess.DEVNULL)
    m = re.search(r"\{.*\}", r.stdout, re.S)
    if not m:
        raise SystemExit(f"reader returned no JSON (exit {r.returncode}): {(r.stdout + r.stderr)[-500:]}")
    d = json.loads(m.group(0))
    return {"guess": str(d["guess"]), "confidence": int(d["confidence"])}


def read(stills: list[str], multi: bool, readers: int) -> list[dict]:
    folder, prompt = al.blind_pack(stills, multi)
    with ThreadPoolExecutor(readers) as ex:
        return list(ex.map(lambda _: read_once(folder, prompt), range(readers)))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", nargs="+")
    ap.add_argument("--multi", action="store_true")
    ap.add_argument("--readers", type=int, default=al.MIN_BLIND_GUESSES)
    ap.add_argument("stills", nargs="+")
    a = ap.parse_args()
    res = read(a.stills, a.multi, a.readers)
    guesses, confs = [r["guess"] for r in res], [r["confidence"] for r in res]
    print(json.dumps(res, ensure_ascii=False))
    if not a.record:
        return 0
    kind, *rest = a.record
    if kind == "element":
        ok = al.record_element(Path(rest[0]).resolve(), int(rest[1]), rest[2], guesses, confs, a.stills, "headless")
    elif kind == "likeness":
        ok = al.record_likeness(Path(rest[0]).resolve(), rest[1], guesses, confs, a.stills, "headless")
    else:
        ok = al.record_blind(rest[0], guesses, confs)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
