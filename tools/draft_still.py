"""Draft stills of one scene (EEVEE, half-resolution), under caffeinate -dimsu. NEVER run while a final render is using the GPU.
usage: .venv/bin/python tools/draft_still.py productions/<ch>/<video> <scene id> <frame>[,<frame>...] [--cpu]   -> productions/.../build/stills/s<id>-f<frame>.png"""
import json, math, shutil, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import identity  # noqa: E402
prod = Path(sys.argv[1]).resolve(); n = int(sys.argv[2]); frames = sys.argv[3]
cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
prefix = cfg.get("scene_script_prefix", "scene")
mp3 = prod / "audio" / f"scene-{n:02d}.mp3"
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)], capture_output=True, text=True).stdout) if mp3.exists() else 10.0
slot = math.ceil(dur * 30 - 1e-6)
out = prod / "build" / "stills" / f"s{n:02d}"
extra = list(cfg.get("render_args", [])) + [f"identity={identity.export_json(production=prod)}"]
cmd = ["caffeinate", "-dimsu", "blender", "-b", "--python", str(ROOT / "code3d" / "scenes" / f"{prefix}_{n:02d}.py"), "--", f"production={prod}", "mode=draft", f"slot={slot}", f"stills={frames}", f"out={out}", *extra]
if "--mask" in sys.argv: cmd.append("mask=1")
if "--cpu" in sys.argv: cmd.append("cpu=1")
r = subprocess.run(cmd, capture_output=True, text=True)
if "--debug" in sys.argv: print(r.stdout[-3000:])
if r.returncode != 0 or "Traceback" in r.stdout + r.stderr: print((r.stdout + r.stderr)[-3500:]); sys.exit(1)
print("ok", out, sorted(p.name for p in out.glob("still-*.png")))
