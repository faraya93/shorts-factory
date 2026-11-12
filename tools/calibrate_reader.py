"""Calibration replay of a reader prompt on stills the owner has already judged (redesign session 2026-11-11, docs/current/reports/proof-gate-recommendation-2026-11-11.md section 1).

The declaration file (rows: production, owner verdict, aliases, stills; `prompt`: single|multi) is written and committed BEFORE this runs; this tool only fills each row's `readings`.
Readers are the gate's own isolated readers (tools/blind_read.py); the judgment is the gate's own matcher at the live bar (asset_library.judge_guesses). Nothing here records an element,
a proof or an asset: a calibration reading never settles anything in production. A row that already holds readings is never read again (every reading counts, never re-roll).

usage: .venv/bin/python tools/calibrate_reader.py <declaration.json>"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "factory"))
import asset_library as al  # noqa: E402
import blind_read  # noqa: E402


def judge(row: dict) -> bool:
    return al.judge_guesses(row["aliases"], [r["guess"] for r in row["readings"]], [r["confidence"] for r in row["readings"]])


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    path = Path(sys.argv[1])
    spec = json.loads(path.read_text(encoding="utf-8"))
    multi = spec.get("prompt") == "multi"
    todo = [r for r in spec["rows"] if not r.get("readings")]
    with ThreadPoolExecutor(4) as ex:
        results = list(ex.map(lambda r: blind_read.read([str(ROOT / s) for s in r["stills"]], multi, al.MIN_BLIND_GUESSES), todo))
    for row, res in zip(todo, results):
        row["readings"] = res
        row["gate_pass"] = judge(row)
        row["agrees_with_owner"] = row["gate_pass"] == (row["owner"] == "accepted")
    rows = spec["rows"]
    spec["summary"] = {"rejected_passed": [r["production"] for r in rows if r["owner"] == "rejected" and r.get("gate_pass")],
                       "accepted_failed": [r["production"] for r in rows if r["owner"] == "accepted" and r.get("gate_pass") is False],
                       "reader_cost_usd": round(sum(x.get("cost_usd", 0.0) for r in rows for x in r.get("readings") or []), 6)}
    path.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    for r in rows:
        print(r["production"], r["owner"], "PASS" if r.get("gate_pass") else "FAIL", [(x["guess"][:90], x["confidence"]) for x in r["readings"]])
    print(json.dumps(spec["summary"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
