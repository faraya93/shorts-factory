"""Check that every at_word of every overlay resolves in the scene's narration timings. .venv/bin/python tools/check_overlays.py productions/<ch>/<video>"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "factory"))
import overlays  # noqa: E402
prod = Path(sys.argv[1]); cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8")); bad = 0
for s in cfg["scenes"]:
    f = prod / "audio" / f"scene-{s['id']:02d}.words.json"
    words = [w for ph in json.load(open(f)) for w in ph["words"]]
    for o in s.get("data_overlays", []):
        try: overlays.start_offset(o, words)
        except ValueError as e: print(f"scene {s['id']}: {e}"); bad += 1
print("overlays OK" if not bad else f"{bad} unresolved")
sys.exit(1 if bad else 0)
