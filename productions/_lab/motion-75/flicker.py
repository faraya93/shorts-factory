"""Temporal stability of the 75% render (editor-upscaled) vs the 100% render of the same shot. Run with Blender's bundled python (numpy).
Both frame sets are encoded the way code3d_render.py encodes clips (libx264 crf16), the 75% clip is then scaled with the editor's filter
(scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920), both are decoded to 8-bit gray and compared.
Measures (all in gray levels 0-255):
  still   = pixels whose 100% render never changes by more than 2 levels between consecutive frames (the truly still region of the reference)
  edge    = thin-structure region: Sobel edges of the 100% frames, dilated 3 px, excluding the still set
  F1(m)   = mean |f[t+1]-f[t]| over mask m           (frame-to-frame flicker; the literal measure in the still region)
  F2(m)   = mean |f[t+1]-2f[t]+f[t-1]| over mask m   (motion-robust shimmer: smooth camera/object motion cancels, flicker does not)
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
lab = Path(__file__).parent
W, H = 1080, 1920
EDIT = f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}"

def clip(tag):
    out = lab / f"{tag}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", str(lab / tag / "f-%04d.png"), "-c:v", "libx264", "-crf", "16",
                    "-preset", "medium", "-pix_fmt", "yuv420p", "-an", str(out)], check=True)
    return out

def gray(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", EDIT + ",format=gray", "-f", "rawvideo", "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, H, W).astype(np.int16)

def dilate(m, k):
    out = m.copy()
    for dy in range(-k, k + 1):
        for dx in range(-k, k + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out

a, b = gray(clip("r75")), gray(clip("r100"))
assert a.shape == b.shape, (a.shape, b.shape)
n = len(a)
d100 = np.abs(np.diff(b, axis=0))
still = (d100 <= 2).all(axis=0)
f = b[n // 2].astype(np.float32)
gx = np.abs(np.roll(f, -1, 1) - np.roll(f, 1, 1)); gy = np.abs(np.roll(f, -1, 0) - np.roll(f, 1, 0))
edge = dilate((gx + gy) > 40, 3) & ~still
# also union of edge masks over a few frames so moving edges are covered
for i in (n // 6, n // 3, 2 * n // 3, 5 * n // 6):
    f = b[i].astype(np.float32); gx = np.abs(np.roll(f, -1, 1) - np.roll(f, 1, 1)); gy = np.abs(np.roll(f, -1, 0) - np.roll(f, 1, 0))
    edge |= dilate((gx + gy) > 40, 3) & ~still
res = {"frames": n, "still_px_pct": round(100 * still.mean(), 2), "edge_px_pct": round(100 * edge.mean(), 2)}
for name, v in (("r75_upscaled", a), ("r100", b)):
    d1 = np.abs(np.diff(v, axis=0)); d2 = np.abs(v[2:] - 2 * v[1:-1] + v[:-2])
    res[name] = {"F1_still": round(float(d1[:, still].mean()), 4), "F2_still": round(float(d2[:, still].mean()), 4),
                 "F1_edge": round(float(d1[:, edge].mean()), 4), "F2_edge": round(float(d2[:, edge].mean()), 4),
                 "F2_edge_p99": round(float(np.percentile(d2[:, edge], 99)), 2)}
res["pixel_diff_75_vs_100_mean_edge"] = round(float(np.abs(a - b)[:, edge].mean()), 3)
res["ratio_F2_edge_75_over_100"] = round(res["r75_upscaled"]["F2_edge"] / res["r100"]["F2_edge"], 3)
res["ratio_F1_still_75_over_100"] = round(res["r75_upscaled"]["F1_still"] / max(res["r100"]["F1_still"], 1e-9), 3)
(lab / "flicker.json").write_text(json.dumps(res, indent=2) + "\n")
print(json.dumps(res, indent=2))
