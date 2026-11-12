"""Blind proofs before batch eligibility (doctrine-topics-and-scripts.md "Blind proofs before batch eligibility", block B4 of
docs/current/reports/architecture-second-opinion-2026-11-11.md, P8).

A creative session writes <prod>/proofs.json: one proof per element that is not a sealed asset in a sealed pose and not a passed pattern,
plus an asset seal for every declared library asset that is not ready, plus a render-cost measurement for a first `world` environment.
A braked proof unit (block B5) builds each still, reads it with tools/blind_read.py under the unchanged bar and records the result.
A unit whose proofs.json holds any proof not "passed" is not batch-eligible: the runner refuses it and tools/return_topic.py never draws it.
A folder without proofs.json predates the rule (B4, 2026-11-11) and is not refused here.

usage: .venv/bin/python factory/proofs.py check productions/<ch>/<video>"""
import json
import sys
from pathlib import Path

NAME = "proofs.json"
STATUSES = ("pending", "passed", "failed")


def errors(prod: Path) -> list[str]:
    """Empty when the folder has no proofs.json, or every proof in it has passed."""
    f = prod / NAME
    if not f.exists():
        return []
    try:
        spec = json.loads(f.read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"{prod.name}: {NAME} is not JSON: {e}"]
    out = []
    for p in spec.get("proofs") or []:
        st = p.get("status")
        if st not in STATUSES:
            out.append(f"{prod.name}: proof {p.get('id')!r} has status {st!r}, not one of {STATUSES}")
        elif st != "passed":
            out.append(f"{prod.name}: proof {p.get('id')} ({p.get('element_id')}) is {st}: not batch-eligible until every proof has passed")
    return out


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] != "check":
        print(__doc__)
        return 2
    prod = Path(sys.argv[2]).resolve()
    errs = errors(prod)
    print("\n".join(errs) if errs else f"{prod.name}: proofs OK (batch-eligible on proofs)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
