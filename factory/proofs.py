"""Blind proofs before batch eligibility (doctrine-topics-and-scripts.md "Blind proofs before batch eligibility", block B4 of
docs/current/reports/architecture-second-opinion-2026-11-11.md, P8).

A creative session writes <prod>/proofs.json: one proof per element that is not a sealed asset in a sealed pose and not a passed pattern,
plus an asset seal for every declared library asset that is not ready, plus a render-cost measurement for a first `world` environment.
A braked proof unit (block B5) builds each still, reads it with tools/blind_read.py under the unchanged bar and records the result.
A unit whose proofs.json holds any proof not "passed" is not batch-eligible: the runner refuses it and tools/return_topic.py never draws it.
A folder without proofs.json predates the rule (B4, 2026-11-11) and is not refused here.

Redesign session 2026-11-11 (docs/current/reports/redesign-2026-11-11.md; doctrine-topics-and-scripts.md "Blind proofs before batch eligibility"):
- STILL CONFORMANCE: a proof still is read only when it was rendered under the reader-still policy (factory/gate.py STILL_POLICY, half-resolution Cycles; tools/proof_still.py --reader writes the
  sidecar) and the builder recorded a `conformance` note against the staging spec with no deviation. `require_conforming` runs BEFORE the readers: a non-conforming still is not read, so no reading is spent.
- ONE PROMPT: proofs are read under the single-object prompt only (the `multi` prompt failed its calibration, docs/current/reports/multi-calibration-2026-11-11.json); every reading records its prompt and hash.
- ONE ALIAS SET PER PHYSICAL ELEMENT: `alias_sets` {name: [aliases]} at the top of proofs.json; a proof that names `alias_sets` must declare `aliases` == the union of those sets (in order) + its own
  `event_aliases`, and a script element with the same id must declare the same list. Sets hold only words declared before any reading of that element.
- STOP-LOSS: a proof is designed at most twice (`round` 1 or 2). A round-2 proof that fails is that element's boundary: the unit is returned, there is no third design round.

usage: .venv/bin/python factory/proofs.py check productions/<ch>/<video>"""
import json
import shutil
import sys
from datetime import date
from pathlib import Path

NAME = "proofs.json"
STATUSES = ("pending", "passed", "failed")
MAX_ROUNDS = 2
READER_RES = (540, 960)            # 50% of the 1080x1920 frame: factory/gate.py STILL_POLICY["res"]


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
    return out + lint(prod, spec)


def union(spec: dict, p: dict) -> list[str]:
    """The alias list a proof that names `alias_sets` must declare: its sets in order, then its own event words, first occurrence kept."""
    sets = spec.get("alias_sets") or {}
    seen, out = set(), []
    for a in [x for name in p.get("alias_sets") or [] for x in sets.get(name, [])] + list(p.get("event_aliases") or []):
        if a not in seen:
            seen.add(a)
            out.append(a)
    return out


def lint(prod: Path, spec: dict) -> list[str]:
    """Alias-set consistency (proofs and the script's elements) and the stop-loss. Proofs without `alias_sets` predate the rule and are not linted for aliases."""
    out = []
    sets = spec.get("alias_sets") or {}
    script = prod / "script.json"
    elements = {}
    if script.exists():
        try:
            for sc in json.loads(script.read_text(encoding="utf-8")).get("scenes") or []:
                for e in sc.get("elements") or []:
                    elements.setdefault(e.get("id"), e)
        except ValueError:
            pass
    for p in spec.get("proofs") or []:
        pid = p.get("id")
        if int(p.get("round", 1)) > MAX_ROUNDS:
            out.append(f"{prod.name}: proof {pid} is at design round {p.get('round')}: the stop-loss allows {MAX_ROUNDS}; the element is a boundary and the unit is returned")
        if not p.get("alias_sets"):
            continue
        missing = [n for n in p["alias_sets"] if n not in sets]
        if missing:
            out.append(f"{prod.name}: proof {pid} names alias sets {missing} that proofs.json does not declare")
            continue
        want = union(spec, p)
        if p.get("aliases") != want:
            out.append(f"{prod.name}: proof {pid} aliases differ from its alias sets {p['alias_sets']} + event_aliases (one alias set per physical element per unit)")
        el = elements.get(p.get("element_id"))
        if el is not None and el.get("aliases") != want:
            out.append(f"{prod.name}: script element {p.get('element_id')!r} aliases differ from proof {pid}'s (one alias set per physical element per unit)")
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


def png_size(path: Path) -> tuple[int, int]:
    head = path.read_bytes()[:24]
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG")
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


def conformance_errors(p: dict, stills: list[str]) -> list[str]:
    """Why these stills may not be read for this proof (empty = conforming): the reader-still policy sidecar (tools/proof_still.py --reader), the half-resolution size, and the builder's
    conformance note against the staging spec with no deviation (a deviation defers the reading, it never spends it)."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    out = []
    note = p.get("conformance") or {}
    if note.get("matches_staging") is not True:
        out.append(f"proof {p.get('id')}: no builder conformance note with matches_staging true (write it against the staging spec before any reader runs)")
    if note.get("deviations"):
        out.append(f"proof {p.get('id')}: the builder recorded deviations from the staging spec {note['deviations']}: the reading is deferred until the still matches the spec")
    for s in stills:
        f = Path(s)
        side = f.with_suffix(".render.json")
        try:
            pol = json.loads(side.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            out.append(f"{s}: no reader-still sidecar {side.name}: render it with tools/proof_still.py --reader (half-resolution Cycles)")
            continue
        if pol.get("engine") != "CYCLES" or pol.get("res") != 50:
            out.append(f"{s}: rendered {pol}, not the reader-still policy (CYCLES, res 50)")
        try:
            if png_size(f) != READER_RES:
                out.append(f"{s}: {png_size(f)}, not the reader-still size {READER_RES}")
        except (OSError, ValueError) as e:
            out.append(str(e))
    return out


def require_conforming(prod: Path, proof_id: str, stills: list[str]) -> dict:
    """Called by tools/blind_read.py --record proof BEFORE the readers run (redesign session 2026-11-11): a settled proof or a non-conforming still is refused without spending a reading."""
    p = require_pending(prod, proof_id)
    errs = conformance_errors(p, stills)
    if errs:
        raise SystemExit("not read (no reading spent):\n" + "\n".join(errs))
    return p


def record_reading(prod: Path, proof_id: str, guesses: list[str], confidences: list[int], stills: list[str] | None = None, reader_cost: float | None = None,
                   prompt: str | None = None, prompt_sha256: str | None = None) -> bool:
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
                                          "mean_confidence": round(sum(confidences) / max(1, len(confidences)), 1), "stills": kept, "round": int(p.get("round", 1)),
                                          **({"prompt": prompt, "prompt_sha256": prompt_sha256} if prompt else {}),
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
    named = (al.read_meta(slug).get("checks") or {}).get("blind_naming") or {}
    p["status"] = "passed" if ready else ("failed" if named.get("pass") is False and named.get("guesses") else p.get("status", "pending"))   # a failed isolated naming settles the seal: no re-roll
    if not ready and named.get("guesses"):
        p.setdefault("readings", []).append({"date": date.today().isoformat(), "asset_blind_naming": named})
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
