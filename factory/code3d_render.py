"""code3d renderer: scene script (Blender) -> PNG frames -> clips/scene-NN.mp4, with the exact frame count of the
scene's narration slot, logged to the production's costs.json. No fal spend.

Usage: python factory/code3d_render.py productions/<channel>/<video> <scene id> [--mode draft|final] [--encode-only]
Draft (default) = half resolution + few samples for iteration; render FINAL once, at the end.
"""

import argparse
import json
import math
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 30


def narration_slot_frames(prod: Path, scene_id: int) -> int:
    mp3 = prod / "audio" / f"scene-{scene_id:02d}.mp3"
    if not mp3.exists():
        sys.exit(f"ERROR: {mp3} missing. Run factory/editor.py once (it writes the narration) so the slot is known.")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)],
                               capture_output=True, text=True, check=True).stdout)
    return math.ceil(dur * FPS - 1e-6)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("production", type=Path)
    ap.add_argument("scene", type=int)
    ap.add_argument("--mode", choices=("draft", "final"), default="draft")
    ap.add_argument("--samples", type=int, help="override Cycles samples (final mode)")
    ap.add_argument("--encode-only", action="store_true", help="skip Blender; encode the frames already rendered")
    args = ap.parse_args()
    prod, n = args.production.resolve(), args.scene
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    prefix = cfg.get("scene_script_prefix", "scene")
    extra = list(cfg.get("render_args", []))                     # e.g. ["look=papel"]: stage look/palette, never choreography
    if args.samples:
        extra.append(f"samples={args.samples}")
    script = ROOT / "code3d" / "scenes" / f"{prefix}_{n:02d}.py"       # default 'scene': existing productions unchanged
    frames_dir = prod / "build" / "code3d" / f"{args.mode}-scene-{n:02d}"
    slot = narration_slot_frames(prod, n)

    render_s = None
    if not args.encode_only:
        t0 = time.time()
        r = subprocess.run(["blender", "-b", "--python", str(script), "--", f"production={prod}", f"mode={args.mode}",
                            f"slot={slot}", f"frames=1-{slot}", f"out={frames_dir}", *extra], capture_output=True, text=True)
        render_s = time.time() - t0
        if r.returncode != 0 or "Traceback" in r.stdout + r.stderr:
            print((r.stdout + r.stderr)[-3000:])
            return 1
    n_frames = len(list(frames_dir.glob("f-*.png")))
    if n_frames != slot:
        print(f"ERROR: {n_frames} frames rendered, the narration slot needs {slot}")
        return 1

    out = prod / "clips" / f"scene-{n:02d}.mp4" if args.mode == "final" else prod / "build" / "code3d" / f"scene-{n:02d}-draft.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", str(frames_dir / "f-%04d.png"),
                    "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", str(out)], check=True)

    costs_path = prod / "costs.json"
    costs = json.loads(costs_path.read_text())
    costs["entries"].append({"scene": n, "engine": "code3d", "mode": args.mode, "frames": n_frames, "fal_spend_usd": 0.0,
                             "render_seconds": round(render_s, 1) if render_s is not None else None,
                             "clip": str(out.relative_to(prod)), "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    costs_path.write_text(json.dumps(costs, indent=2) + "\n")
    print(f"scene {n} [{args.mode}]: {n_frames} frames -> {out.relative_to(prod)}"
          + (f" | render {render_s:.1f} s ({render_s / n_frames:.2f} s/frame)" if render_s else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
