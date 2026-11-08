"""Render-cost bench: one scene, one frame, many variants, one at a time through the launcher. s/frame from Blender's own timer; RMSE against a high-sample reference.
usage: .venv/bin/python tools/cost_bench.py <production> <scene> <frame[,frame...]> <variants.json> <out dir>    (variants.json = {name: {"cy":{}, "res":n, "mat":[], "samples":n}}; results.json in <out dir>)"""
import json
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(ROOT / "tools"))
import blender_run  # noqa: E402
import identity     # noqa: E402


def load(p: Path, size=(540, 960)) -> Image.Image:
    return Image.open(p).convert("RGB").resize(size, Image.LANCZOS)


def rmse(a: Image.Image, b: Image.Image) -> float:
    return math.sqrt(sum(x * x for x in ImageStat.Stat(ImageChops.difference(a, b)).rms) / 3)


def main() -> int:
    prod, sid, frames, variants, out = Path(sys.argv[1]).resolve(), int(sys.argv[2]), sys.argv[3], json.loads(Path(sys.argv[4]).read_text()), Path(sys.argv[5]).resolve()
    frame = int(frames.split(",")[0])
    out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads((prod / "scenes.json").read_text())
    prefix = cfg.get("scene_script_prefix", "scene")
    mp3 = prod / "audio" / f"scene-{sid:02d}.mp3"
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp3)], capture_output=True, text=True).stdout)
    slot = math.ceil(dur * 30 - 1e-6)
    extra = [*cfg.get("render_args", []), f"identity={identity.export_json(production=prod)}"]
    res_path = out / "results.json"
    results = json.loads(res_path.read_text()) if res_path.exists() else {}
    for name, v in variants.items():
        if name in results:
            continue
        d = out / name
        png = d / f"still-{frame:04d}.png"
        png.unlink(missing_ok=True)
        t0 = time.time()
        r = blender_run.blender(["-b", "--python", str(ROOT / "tools" / "bench_prelude.py"), "--python", str(ROOT / "code3d" / "scenes" / f"{prefix}_{sid:02d}.py"), "--", f"production={prod}", "mode=final",
                                 f"slot={slot}", f"samples={v.get('samples', 64)}", f"stills={frames}", f"out={d}", *extra], capture_output=True, text=True, env={**os.environ, "SF_BENCH": json.dumps(v), "SF_BENCH_SCENE": f"{prefix}_{sid:02d}"})
        wall = time.time() - t0
        times = re.findall(r"Time: (\d+):(\d+\.\d+)", r.stdout)
        rs = int(times[-1][0]) * 60 + float(times[-1][1]) if times else None
        ok = png.exists() and "Traceback" not in r.stdout + r.stderr
        results[name] = {"render_s": rs, "wall_s": round(wall, 1), "ok": ok, "variant": v}
        if not ok:
            (d / "error.log").parent.mkdir(parents=True, exist_ok=True); (d / "error.log").write_text((r.stdout + r.stderr)[-4000:])
        print(name, results[name]["render_s"], results[name]["wall_s"], ok, flush=True)
        res_path.write_text(json.dumps(results, indent=1))
    ref = out / "reference" / f"still-{frame:04d}.png"
    if ref.exists():
        R = load(ref)
        for name in results:
            p = out / name / f"still-{frame:04d}.png"
            if p.exists():
                results[name]["rmse_vs_ref"] = round(rmse(load(p), R), 2)
    res_path.write_text(json.dumps(results, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
