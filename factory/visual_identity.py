"""Visual identity: one block that every engine consumes literally.

The block is defined once in the channel config; each production embeds a verbatim copy in its scenes.json
(`visual_identity`) so it stays reproducible if the channel config changes later. It carries:
  background {hex, description}   exact background colour / shared backdrop
  palette [{hex, name?}]          the palette, as hex values
  lighting, materials             wording injected into every t2v / image prompt
  unify {...}                     the Editor's shared pass for EVERY scene: colour grade + film grain + vignette
  qa_tolerance_de                 max CIE76 delta-E between a scene's sampled background and the spec hex

code3d scenes use the exact hex values in code and render on the spec background.
"""

import math
import re
import statistics
import subprocess
from pathlib import Path

from PIL import Image, ImageStat

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
DEFAULT_UNIFY = {"saturation": 1.04, "contrast": 1.03, "warmth": 0.0, "grain": 5, "vignette_angle": 0.9}
DEFAULT_TOLERANCE_DE = 15.0


def validate(vi) -> list[str]:
    if not isinstance(vi, dict):
        return ["visual_identity must be an object"]
    errors = []
    bg = vi.get("background")
    if not isinstance(bg, dict) or not HEX_RE.match(str(bg.get("hex", ""))):
        errors.append("visual_identity.background.hex must be a #RRGGBB value")
    elif not str(bg.get("description", "")).strip():
        errors.append("visual_identity.background.description is required (it is injected into prompts)")
    palette = vi.get("palette")
    if not isinstance(palette, list) or not palette:
        errors.append("visual_identity.palette must be a non-empty list of {hex, name?}")
    else:
        errors += [f"visual_identity.palette[{i}].hex must be #RRGGBB" for i, c in enumerate(palette)
                   if not isinstance(c, dict) or not HEX_RE.match(str(c.get("hex", "")))]
    for field in ("lighting", "materials"):
        if not str(vi.get(field, "")).strip():
            errors.append(f"visual_identity.{field} is required")
    unify = {**DEFAULT_UNIFY, **(vi.get("unify") or {})}
    for key, (lo, hi) in {"saturation": (0.5, 1.5), "contrast": (0.5, 1.5), "warmth": (-0.3, 0.3),
                          "grain": (0, 30), "vignette_angle": (0, 1.5)}.items():
        if not isinstance(unify[key], (int, float)) or not lo <= unify[key] <= hi:
            errors.append(f"visual_identity.unify.{key} must be a number in [{lo}, {hi}]")
    tol = vi.get("qa_tolerance_de", DEFAULT_TOLERANCE_DE)
    if not isinstance(tol, (int, float)) or tol <= 0:
        errors.append("visual_identity.qa_tolerance_de must be a number > 0")
    return errors


def identity_clause(vi: dict) -> str:
    """The wording injected right after the style string in every t2v and image prompt."""
    bg = vi["background"]
    palette = ", ".join(f"{c['name']} {c['hex']}" if c.get("name") else c["hex"] for c in vi["palette"])
    return (f"Background: {bg['description'].strip().rstrip('.')} (exactly {bg['hex']}). "
            f"Palette: {palette}. Lighting: {vi['lighting'].strip().rstrip('.')}. "
            f"Materials: {vi['materials'].strip().rstrip('.')}.")


def unify_filter(vi: dict | None) -> str:
    """ffmpeg filter fragment for the shared pass (same parameters for every scene, whatever its engine)."""
    if not vi:
        return ""
    u = {**DEFAULT_UNIFY, **(vi.get("unify") or {})}
    parts = [f"eq=saturation={u['saturation']}:contrast={u['contrast']}"]
    if u["warmth"]:  # warm = more red, less blue in the midtones
        parts.append(f"colorbalance=rm={u['warmth']}:bm={-u['warmth']}")
    if u["grain"]:
        parts.append(f"noise=alls={u['grain']}:allf=t+u:all_seed=1")
    if u["vignette_angle"]:
        parts.append(f"vignette=angle={u['vignette_angle']}")
    return ",".join(parts)


# --- QA: sampled background colour vs the spec hex ---------------------------------------

def hex_to_rgb(h: str) -> tuple[int, int, int]:
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def rgb_to_hex(rgb) -> str:
    return "#{:02X}{:02X}{:02X}".format(*(round(c) for c in rgb))


def rgb_to_lab(rgb) -> tuple[float, float, float]:
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e(rgb1, rgb2) -> float:
    """CIE76 colour difference (~2.3 is a just-noticeable difference)."""
    return math.dist(rgb_to_lab(rgb1), rgb_to_lab(rgb2))


def sample_background(frame: Path) -> tuple[int, int, int]:
    """Background colour of a frame: channel-wise median of 8 border patches (4 corners + 4 edge midpoints).
    The median tolerates a foreground object covering a few of the patches."""
    img = Image.open(frame).convert("RGB")
    w, h = img.size
    pw, ph = max(2, round(w * 0.05)), max(2, round(h * 0.05))
    mx, my = round(w * 0.03), round(h * 0.03)
    anchors = [(mx, my), (w - mx - pw, my), (mx, h - my - ph), (w - mx - pw, h - my - ph),
               ((w - pw) // 2, my), ((w - pw) // 2, h - my - ph), (mx, (h - ph) // 2), (w - mx - pw, (h - ph) // 2)]
    means = [tuple(ImageStat.Stat(img.crop((x, y, x + pw, y + ph))).mean) for x, y in anchors]
    return tuple(statistics.median(m[i] for m in means) for i in range(3))


def qa_clip(clip: Path, vi: dict, work: Path, duration: float) -> dict:
    """Sample 3 frames (20/50/80% of the clip), take the median background colour, compare with the spec."""
    work.mkdir(parents=True, exist_ok=True)
    samples = []
    for k, frac in enumerate((0.2, 0.5, 0.8)):
        png = work / f"{clip.stem}-{k}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{duration * frac:.3f}", "-i", str(clip),
                        "-frames:v", "1", str(png)], check=True)
        samples.append(sample_background(png))
    median = tuple(statistics.median(s[i] for s in samples) for i in range(3))
    spec = hex_to_rgb(vi["background"]["hex"])
    tol = vi.get("qa_tolerance_de", DEFAULT_TOLERANCE_DE)
    de = delta_e(median, spec)
    return {"hex": rgb_to_hex(median), "spec_hex": vi["background"]["hex"], "delta_e": round(de, 1),
            "tolerance_de": tol, "ok": de <= tol}
