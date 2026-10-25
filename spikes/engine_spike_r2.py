"""Engine spike R2 (keyframes) on stitches scene 2: 4 fal stills (same style string + seed as v2), animated to the
scene-2 narration slot. Usage: python spikes/engine_spike_r2.py [--animate-only]"""

import json
import math
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "factory"))
from keyframes import animate_keyframes, generate_keyframes  # noqa: E402

load_dotenv()
V2 = Path("productions/pilot/puntos-de-sutura-v2")
OUT = Path("productions/pilot/engine-spike")
cfg = json.loads((V2 / "scenes.json").read_text(encoding="utf-8"))
seed = json.loads((V2 / "costs.json").read_text())["seed"]
style = cfg["style"] + " No text on screen."

FRAMING = ("Same framing in every frame: three-quarter top-down close-up of a smooth cartoon forearm model, the "
           "stylized cut running vertically through the center of the frame, clean pastel lavender background.")
STEPS = [
    "A stylized curved surgical needle with black thread hovers just above the skin beside the LEFT edge of the "
    "cut, its tip about to touch the skin. Never inside the open gap, never blood.",
    "The curved needle is mid-pass: its tip has gone into the skin beside the left edge and travels under the gap, "
    "the curved body half visible above the surface, black thread trailing behind. Never blood.",
    "The curved needle emerges from the skin surface beside the RIGHT edge of the cut, the black thread following "
    "it. Never blood.",
    "The black thread is tightened and the two skin edges meet in one neat zigzag stitch; the cut is closed. "
    "Never blood.",
]

if "--animate-only" not in sys.argv:
    generate_keyframes([f"{FRAMING} {s}" for s in STEPS], style, seed, OUT / "r2-keys", OUT / "costs.json")

narr = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                             str(V2 / "audio" / "scene-02.mp3")], capture_output=True, text=True).stdout)
slot = math.ceil(narr * 30 - 1e-6) / 30
animate_keyframes(sorted((OUT / "r2-keys").glob("key-*.png")), slot, OUT / "r2-keyframes.mp4")
print(f"r2-keyframes.mp4 written, {slot:.2f} s (scene-2 narration slot)")
