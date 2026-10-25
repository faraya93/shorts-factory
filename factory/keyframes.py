"""Keyframes engine: fal image stills, animated into a clip by the Editor (crossfades + slow zoom).

generate_keyframes() calls a fal IMAGE model (same style string and fixed seed for every still) and logs each
generation to the production's costs.json; animate_keyframes() turns the stills into one clip of an exact
duration with local ffmpeg only (no spend).
"""

import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import fal_client

IMAGE_MODEL = "fal-ai/flux-2"
PRICE_PER_MP = 0.012          # USD per megapixel (fal model page, verified 2026-10-25); rounding is not stated
IMAGE_SIZE = "portrait_16_9"  # vertical stills, upscaled to 1080x1920 by the animation step
CROSSFADE_S = 0.7
ZOOM_END = 1.10               # slow push from 1.0x to 1.10x over each still


def generate_keyframes(prompts: list[str], style: str, seed: int, out_dir: Path, costs_path: Path) -> list[dict]:
    """One fal call per still: prompt = style string verbatim + the keyframe prompt; fixed seed; no prompt expansion."""
    out_dir.mkdir(parents=True, exist_ok=True)
    costs = json.loads(costs_path.read_text()) if costs_path.exists() else {"model": IMAGE_MODEL, "seed": seed, "entries": []}
    results = []
    for i, text in enumerate(prompts, 1):
        path = out_dir / f"key-{i:02d}.png"
        if path.exists() and any(e.get("keyframe") == i and "url" in e for e in costs["entries"]):
            print(f"keyframe {i}: already generated, skipped (never pay twice)")
            results.append({"path": path, "width": None, "height": None})
            continue
        args = {"prompt": f"{style} {text}", "image_size": IMAGE_SIZE, "seed": seed, "num_images": 1,
                "enable_prompt_expansion": False, "output_format": "png"}
        try:
            result = fal_client.subscribe(IMAGE_MODEL, arguments=args)
        except Exception as e:  # e.g. content_policy_violation: log it and stop, the caller decides what to do
            costs["entries"].append({"keyframe": i, "model": IMAGE_MODEL, "status": "rejected", "error": str(e)[:300],
                                     "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")})
            costs_path.write_text(json.dumps(costs, indent=2, ensure_ascii=False) + "\n")
            raise
        img = result["images"][0]
        urllib.request.urlretrieve(img["url"], path)
        mp = max(1, -(-(img.get("width", 1024) * img.get("height", 1024)) // 1_000_000))  # billed megapixels, rounded up
        costs["entries"].append({"keyframe": i, "model": IMAGE_MODEL, "seed": seed, "width": img.get("width"),
                                 "height": img.get("height"), "billed_mp_assumed": mp,
                                 "estimated_cost_usd": round(mp * PRICE_PER_MP, 5), "url": img["url"],
                                 "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        costs_path.write_text(json.dumps(costs, indent=2, ensure_ascii=False) + "\n")
        results.append({"path": path, **{k: img.get(k) for k in ("width", "height")}})
        print(f"keyframe {i}: {img.get('width')}x{img.get('height')} -> {path.name}")
    return results


def animate_keyframes(images: list[Path], duration: float, out: Path, fps: int = 30, w: int = 1080, h: int = 1920) -> None:
    """Stills -> one clip of exactly `duration` seconds: slow zoom on each still, crossfade between stills."""
    n = len(images)
    # n stills of length d overlapping by CROSSFADE_S: total = n*d - (n-1)*CROSSFADE_S
    d = (duration + (n - 1) * CROSSFADE_S) / n
    frames = max(2, round(d * fps))
    parts, cmd = [], ["ffmpeg", "-y", "-v", "error"]
    for i, img in enumerate(images):
        cmd += ["-loop", "1", "-framerate", str(fps), "-t", f"{d:.4f}", "-i", str(img)]
        zoom = f"1+{ZOOM_END - 1}*on/{frames - 1}"
        parts.append(f"[{i}:v]scale={w * 3 // 2}:{h * 3 // 2}:force_original_aspect_ratio=increase:flags=lanczos,"
                     f"crop={w * 3 // 2}:{h * 3 // 2},zoompan=z='{zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                     f"d=1:s={w}x{h}:fps={fps},setsar=1,format=yuv420p[k{i}]")
    last = "k0"
    for i in range(1, n):
        offset = i * (d - CROSSFADE_S)
        parts.append(f"[{last}][k{i}]xfade=transition=fade:duration={CROSSFADE_S}:offset={offset:.4f}[x{i}]")
        last = f"x{i}"
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{last}]", "-t", f"{duration:.4f}", "-r", str(fps),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-an", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{r.stderr[-2000:]}")
