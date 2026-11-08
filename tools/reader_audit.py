"""One-off audit (2026-11-08): the passed elements of 006/008/009/010 re-read by ISOLATED readers from their stored stills. Writes docs/current/reports/reader-isolation/reread.json. No record is changed."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "factory"))
import blind_read as br      # noqa: E402
import asset_library as al   # noqa: E402

OUT = ROOT / "docs/current/reports/reader-isolation/reread.json"
res = json.loads(OUT.read_text()) if OUT.exists() else {}
for num in sys.argv[1:]:
    prod = next((ROOT / "productions/mecanalia-es").glob(f"{num}-*"))
    cfg = json.loads((prod / "scenes.json").read_text())
    rec = json.loads((prod / "build/gate/elements.json").read_text())
    for sid, els in cfg["scene_elements"].items():
        key = f"{num}:{sid}"
        if key in res:
            continue
        d = prod / "build/gate/likeness" / f"s{int(sid):02d}"
        frames = sorted({f for e in els for f in (e.get("frames") or cfg["gate_stills"][sid])})
        stills = [str(d / f"still-{f:04d}.png") for f in frames if (d / f"still-{f:04d}.png").exists()]
        if not stills:
            res[key] = {"error": "stills missing"}
            continue
        r = br.read(stills, len(els) > 1, 3)
        g, c = [x["guess"] for x in r], [x["confidence"] for x in r]
        res[key] = {"readers": r, "elements": {e["id"]: {"pass_isolated": al.judge_guesses(e["aliases"], g, c), "recorded_confidences": rec.get(f"{sid}:{e['id']}", {}).get("confidences"),
                                                         "recorded_pass": rec.get(f"{sid}:{e['id']}", {}).get("pass")} for e in els}}
        OUT.write_text(json.dumps(res, indent=1, ensure_ascii=False))
        print(key, [x["confidence"] for x in r], g[0][:60], flush=True)
