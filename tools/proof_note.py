"""Proof build notes in a unit's proofs.json, without touching status or readings.
usage: .venv/bin/python tools/proof_note.py <production> P1=proof_51 P2=proof_52 ...        (block B5: stamp `built_by_b5`, kept for the B5 record)
       .venv/bin/python tools/proof_note.py <production> --conform <proof id> <script stem> [--deviation "<what differs from the staging spec>" ...]
--conform (redesign session 2026-11-11) writes the builder's `conformance` note against the proof's staging spec: with no --deviation, matches_staging is true and the still may be read
(factory/proofs.py require_conforming also checks the reader-still sidecar); with any --deviation the reading is deferred until the still is rebuilt to the spec. Never edit a staging to fit a build."""
import json
import sys
from datetime import date
from pathlib import Path

prod = Path(sys.argv[1])
spec = json.loads((prod / "proofs.json").read_text(encoding="utf-8"))
args = sys.argv[2:]
if args and args[0] == "--conform":
    pid, stem = args[1], args[2]
    devs = [args[i + 1] for i, a in enumerate(args) if a == "--deviation"]
    next(p for p in spec["proofs"] if p["id"] == pid)["conformance"] = {
        "by": "braked proof unit", "at": date.today().isoformat(), "script": f"code3d/scenes/{stem}.py",
        "render": "tools/proof_still.py --reader (reader-still policy)", "matches_staging": not devs, "deviations": devs}
else:
    for pair in args:
        pid, stem = pair.split("=")
        next(p for p in spec["proofs"] if p["id"] == pid)["built_by_b5"] = {"script": f"code3d/scenes/{stem}.py", "render": "tools/proof_still.py (EEVEE draft path, 1080x1920, frame 10)"}
(prod / "proofs.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
