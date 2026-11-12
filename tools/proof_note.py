"""Stamp each proof in a unit's proofs.json with the B5 build that produced its still (script and render path), without touching status or readings.
usage: .venv/bin/python tools/proof_note.py <production> P1=proof_51 P2=proof_52 ..."""
import json
import sys
from pathlib import Path

prod = Path(sys.argv[1])
spec = json.loads((prod / "proofs.json").read_text(encoding="utf-8"))
for pair in sys.argv[2:]:
    pid, stem = pair.split("=")
    next(p for p in spec["proofs"] if p["id"] == pid)["built_by_b5"] = {"script": f"code3d/scenes/{stem}.py", "render": "tools/proof_still.py (EEVEE draft path, 1080x1920, frame 10)"}
(prod / "proofs.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
