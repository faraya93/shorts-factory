"""Isolated blind readers (2026-11-08). The audit found 158 of 174 past readers had CLAUDE.md in their context, which names the catalogue's subjects. Each reader here is a fresh headless session
in an empty neutral folder (no CLAUDE.md to discover, no project memory, no settings, no MCP, Read tool only) that sees only neutrally named copies of the stills.
usage: .venv/bin/python tools/blind_read.py [--record element <prod> <scene> <id> | likeness <prod> <slug> | proof <prod> <proof id> | blind <slug>] [--multi] [--readers 3] <still> [...]
Every reading is counted: a low reader is never discarded or re-rolled (report 2026-11-08, flag 9).
Redesign session 2026-11-11: every reading records which prompt produced it (`single` or `multi`, with a hash of the prompt text) in the reader ledger and, for proofs, in proofs.json; a proof is read
under the single-object prompt only, and only from stills that pass factory/proofs.py require_conforming, checked before any reader runs."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import asset_library as al  # noqa: E402

MODEL = os.environ.get("SF_READER_MODEL", "haiku")
FORMAT = ' Reply with ONLY one line of JSON: {"guess": "<your answer as text>", "confidence": <0-100>}.'


def read_once(folder: Path, prompt: str) -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_PROJECT"))}
    r = subprocess.run(["claude", "-p", prompt + FORMAT, "--tools", "Read", "--allowedTools", "Read", "--setting-sources", "", "--strict-mcp-config", "--no-session-persistence", "--model", MODEL, "--output-format", "json"],
                       cwd=folder, capture_output=True, text=True, env=env, timeout=240, stdin=subprocess.DEVNULL)
    text, cost = unwrap(r.stdout)
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise SystemExit(f"reader returned no JSON (exit {r.returncode}): {(r.stdout + r.stderr)[-500:]}")
    d = json.loads(m.group(0))
    return {"guess": str(d["guess"]), "confidence": int(d["confidence"]), "cost_usd": cost}


def unwrap(stdout: str) -> tuple[str, float]:
    """`--output-format json` wraps the reply in one result object (or a list of events whose last is the result): (reply text, total_cost_usd). Output that is not that wrapper is returned as is, at cost 0."""
    try:
        obj = json.loads(stdout)
    except ValueError:
        return stdout, 0.0
    if isinstance(obj, list):
        obj = next((e for e in reversed(obj) if isinstance(e, dict) and e.get("type") == "result"), {})
    if not isinstance(obj, dict) or "result" not in obj:
        return stdout, 0.0
    return str(obj.get("result", "")), float(obj.get("total_cost_usd") or 0.0)


def prompt_id(multi: bool) -> tuple[str, str]:
    """('single'|'multi', sha256[:16] of the prompt text without its image list): which instrument produced a reading."""
    prompt = al.blind_pack([], multi)[1]
    return ("multi" if multi else "single"), hashlib.sha256(prompt.rsplit("Images: ", 1)[0].encode()).hexdigest()[:16]


def ledger(production: Path, key: str, res: list[dict], multi: bool = False) -> None:
    """Append-only reader cost ledger the runner sums per unit (build/reader-ledger.jsonl): elements.json keeps only the last reading of an element, the ledger keeps every one, with its prompt."""
    path = production / "build" / "reader-ledger.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    kind, sha = prompt_id(multi)
    with path.open("a") as f:
        f.write(json.dumps({"at": datetime.now().isoformat(timespec="seconds"), "key": key, "readers": len(res), "cost_usd": round(sum(r.get("cost_usd", 0.0) for r in res), 6),
                            "prompt": kind, "prompt_sha256": sha}) + "\n")


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
    if a.record and a.record[0] == "proof":                    # settled proofs and non-conforming stills are refused before the readers run; proofs use the single prompt only
        import proofs
        if a.multi:
            raise SystemExit("a proof is read under the single-object prompt only (redesign session 2026-11-11: the multi prompt failed its calibration)")
        proofs.require_conforming(Path(a.record[1]).resolve(), a.record[2], a.stills)
    res = read(a.stills, a.multi, a.readers)
    guesses, confs = [r["guess"] for r in res], [r["confidence"] for r in res]
    cost = round(sum(r["cost_usd"] for r in res), 6)
    print(json.dumps(res, ensure_ascii=False))
    if not a.record:
        return 0
    kind, *rest = a.record
    if kind == "element":
        ok = al.record_element(Path(rest[0]).resolve(), int(rest[1]), rest[2], guesses, confs, a.stills, "headless", reader_cost=cost)
        ledger(Path(rest[0]).resolve(), f"{rest[1]}:{rest[2]}", res, a.multi)
    elif kind == "proof":                                      # block B5: a blind proof in <prod>/proofs.json (factory/proofs.py), same readers, same matcher, same bar
        import proofs
        kind_p, sha = prompt_id(a.multi)
        ok = proofs.record_reading(Path(rest[0]).resolve(), rest[1], guesses, confs, a.stills, reader_cost=cost, prompt=kind_p, prompt_sha256=sha)
        ledger(Path(rest[0]).resolve(), f"proof:{rest[1]}", res, a.multi)
    elif kind == "likeness":
        ok = al.record_likeness(Path(rest[0]).resolve(), rest[1], guesses, confs, a.stills, "headless", reader_cost=cost)
        ledger(Path(rest[0]).resolve(), "hero", res, a.multi)
    else:
        ok = al.record_blind(rest[0], guesses, confs, reader_cost=cost)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
