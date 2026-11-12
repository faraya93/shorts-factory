"""Blind proofs before batch eligibility (doctrine-topics-and-scripts.md "Blind proofs before batch eligibility", block B4 of
docs/current/reports/architecture-second-opinion-2026-11-11.md, P8).

A creative session writes <prod>/proofs.json: one proof per element that is not a sealed asset in a sealed pose and not a passed pattern,
plus an asset seal for every declared library asset that is not ready, plus a render-cost measurement for a first `world` environment.
A braked proof unit (block B5) builds each still, reads it with tools/blind_read.py under the unchanged bar and records the result.
A unit whose proofs.json holds any proof not "passed" is not batch-eligible: the runner refuses it and tools/return_topic.py never draws it.
A folder without proofs.json predates the rule (B4, 2026-11-11) and is not refused here.

usage: .venv/bin/python factory/proofs.py check productions/<ch>/<video>"""
import json
import shutil
import sys
from datetime import date
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


def _load(prod: Path) -> dict:
    return json.loads((prod / NAME).read_text(encoding="utf-8"))


def _save(prod: Path, spec: dict) -> None:
    (prod / NAME).write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def find(spec: dict, proof_id: str) -> dict:
    p = next((x for x in spec.get("proofs") or [] if x.get("id") == proof_id), None)
    if p is None:
        raise SystemExit(f"{NAME} declares no proof {proof_id!r}")
    return p


def require_pending(prod: Path, proof_id: str) -> dict:
    """Called BEFORE the readers run, so a settled proof is never read again (every reading counts, never re-roll): a failed proof goes back to a creative session, which resets it with a redesigned staging."""
    p = find(_load(prod), proof_id)
    if p.get("status") != "pending":
        raise SystemExit(f"proof {proof_id} is {p.get('status')}, not pending: it is settled (a failed proof goes back to a creative session, which redesigns it)")
    return p


def record_reading(prod: Path, proof_id: str, guesses: list[str], confidences: list[int], stills: list[str] | None = None, reader_cost: float | None = None) -> bool:
    """Judge one element reading with the gate's own matcher and bar (asset_library.judge_guesses, aliases exactly as declared in proofs.json), append it to the proof's readings and settle the
    proof from it. The stills the readers judged are kept under build/proofs/<id>/."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import asset_library as al
    spec = _load(prod)
    p = find(spec, proof_id)
    if p.get("status") != "pending":
        raise SystemExit(f"proof {proof_id} is {p.get('status')}, not pending")
    if not p.get("aliases"):
        raise SystemExit(f"proof {proof_id} declares no aliases: it is not an element reading (asset seals settle through asset_library.py, costs through record-cost)")
    ok = al.judge_guesses(p["aliases"], guesses, confidences)
    kept = []
    if stills:
        keep = prod / "build" / "proofs" / proof_id
        keep.mkdir(parents=True, exist_ok=True)
        for s in stills:
            dst = keep / f"{date.today().isoformat()}-{len(p.get('readings') or []) + 1}-{Path(s).name}"
            shutil.copyfile(s, dst)
            kept.append(str(dst.relative_to(prod)))
    p.setdefault("readings", []).append({"date": date.today().isoformat(), "pass": ok, "guesses": guesses, "confidences": confidences,
                                          "mean_confidence": round(sum(confidences) / max(1, len(confidences)), 1), "stills": kept,
                                          **({"reader_cost_usd": reader_cost} if reader_cost is not None else {})})
    p["status"] = "passed" if ok else "failed"
    _save(prod, spec)
    return ok


def settle_asset(prod: Path, proof_id: str) -> bool:
    """An asset-seal proof passes when the asset it names validates as `ready` (the library's own blind naming and seal checks)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import asset_library as al
    spec = _load(prod)
    p = find(spec, proof_id)
    slug = p.get("element_id")
    errs, _ = al.validate(slug, al.source_ids())
    ready = not errs and al.read_meta(slug).get("status") == "ready"
    p["status"] = "passed" if ready else p.get("status", "pending")
    p.setdefault("readings", []).append({"date": date.today().isoformat(), "asset": slug, "ready": ready, "errors": errs})
    _save(prod, spec)
    return ready


def record_cost(prod: Path, proof_id: str, seconds_per_frame: float, cost_class: str, note: str = "") -> bool:
    """A render-cost proof is settled by a measurement: it passes at or under 15 s/frame (the playbook's cost_restage threshold); above that it fails and goes back to a creative session."""
    spec = _load(prod)
    p = find(spec, proof_id)
    ok = seconds_per_frame <= 15.0
    p.setdefault("readings", []).append({"date": date.today().isoformat(), "seconds_per_frame": seconds_per_frame, "render_cost_class": cost_class, "pass": ok, **({"note": note} if note else {})})
    p["status"] = "passed" if ok else "failed"
    _save(prod, spec)
    return ok


def main() -> int:
    if len(sys.argv) >= 3 and sys.argv[1] == "settle-asset" and len(sys.argv) == 4:
        ok = settle_asset(Path(sys.argv[2]).resolve(), sys.argv[3])
        print("PASS" if ok else "NOT READY")
        return 0 if ok else 1
    if len(sys.argv) == 7 and sys.argv[1] == "record-cost":
        ok = record_cost(Path(sys.argv[2]).resolve(), sys.argv[3], float(sys.argv[4]), sys.argv[5], sys.argv[6])
        print("PASS" if ok else "FAIL")
        return 0 if ok else 1
    if len(sys.argv) != 3 or sys.argv[1] != "check":
        print(__doc__ + "\n       factory/proofs.py settle-asset <prod> <proof id>\n       factory/proofs.py record-cost <prod> <proof id> <s/frame> <class> <note>")
        return 2
    prod = Path(sys.argv[2]).resolve()
    errs = errors(prod)
    print("\n".join(errs) if errs else f"{prod.name}: proofs OK (batch-eligible on proofs)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
