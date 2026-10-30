"""Print per-scene word start times: .venv/bin/python tools/wordtimes.py productions/<ch>/<video> [scene ids]"""
import json, sys
from pathlib import Path
prod = Path(sys.argv[1]); ids = [int(x) for x in sys.argv[2:]] or range(1, 20)
for i in ids:
    f = prod / "audio" / f"scene-{i:02d}.words.json"
    if not f.exists(): continue
    out = []
    for ph in json.load(open(f)):
        for w in ph["words"]: out.append(f"{w['text']}@{w['start']:.1f}")
    print(f"S{i}:", " ".join(out))
