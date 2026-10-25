"""Animated data overlays (counter | bar | label): validation and Pillow rendering.

A scene may declare `data_overlays`: [{type, text_or_value, at_offset_seconds, duration_s?, visible_s?}].
Each overlay is rendered as a short PNG sequence (one ffmpeg input at the video fps): the animation plays,
then its last frame is held by the editor until the overlay's visible window ends. Placement is the frame
centre; the upper band belongs to the subtitles. Style: bold white with a thick black outline.
"""

import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TYPES = ("counter", "bar", "label")
DEFAULT_ANIM_S = {"counter": 1.2, "bar": 1.2, "label": 0.25}
DEFAULT_VISIBLE_S = 3.0

OV_FONT_SIZE, OV_STROKE, OV_MAX_WIDTH = 120, 11, 900
BAR_W, BAR_H, BAR_GAP = 760, 56, 22
NUMBER_RE = re.compile(r"^(?P<pre>[^\d]*?)(?P<num>\d+(?:\.\d+)?)(?P<suf>.*)$", re.DOTALL)


def anim_seconds(spec: dict) -> float:
    return float(spec.get("duration_s", DEFAULT_ANIM_S[spec["type"]]))


def visible_seconds(spec: dict) -> float:
    return float(spec.get("visible_s", DEFAULT_VISIBLE_S))


def ease_out(p: float) -> float:
    return 1 - (1 - p) ** 3


def bar_fraction(value) -> float | None:
    """'75%' -> 0.75, '0.75' -> 0.75; anything outside 0..1 is rejected (None)."""
    s = str(value).strip()
    try:
        x = float(s[:-1]) / 100 if s.endswith("%") else float(s)
    except ValueError:
        return None
    return x if 0 <= x <= 1 else None


def validate_scene_overlays(scene_id, overlays) -> list[str]:
    errors, windows = [], []
    if not isinstance(overlays, list):
        return [f"scene {scene_id}: data_overlays must be a list"]
    for n, spec in enumerate(overlays, 1):
        tag = f"scene {scene_id} overlay {n}"
        if not isinstance(spec, dict) or spec.get("type") not in TYPES:
            errors.append(f"{tag}: type must be one of {TYPES}")
            continue
        value = spec.get("text_or_value")
        if value is None or not str(value).strip():
            errors.append(f"{tag}: missing text_or_value")
        at = spec.get("at_offset_seconds")
        if not isinstance(at, (int, float)) or isinstance(at, bool) or at < 0:
            errors.append(f"{tag}: at_offset_seconds must be a number >= 0")
            continue
        anim, visible = anim_seconds(spec), visible_seconds(spec)
        if anim <= 0 or visible < anim:
            errors.append(f"{tag}: need duration_s > 0 and visible_s >= duration_s")
            continue
        if spec["type"] == "counter" and value is not None and not NUMBER_RE.match(str(value)):
            errors.append(f"{tag}: counter needs a number such as '170 °C' or '10×', got {value!r}")
        if spec["type"] == "bar" and value is not None and bar_fraction(value) is None:
            errors.append(f"{tag}: bar needs a fraction 0..1 or a percentage such as '75%', got {value!r}")
        windows.append((at, at + visible, n))
    for i, (a1, b1, n1) in enumerate(windows):
        for a2, b2, n2 in windows[i + 1:]:
            if a1 < b2 and a2 < b1:
                errors.append(f"scene {scene_id}: overlays {n1} and {n2} overlap in time (both sit at the centre)")
    return errors


def _format_number(x: float, decimals: int) -> str:
    text = f"{x:,.{decimals}f}".replace(",", " ") if abs(x) >= 10000 else f"{x:.{decimals}f}"
    return text


def counter_text(spec: dict, progress: float) -> str:
    """The counter's text at animation progress 0..1 (eased); the last frame is exactly the target."""
    m = NUMBER_RE.match(str(spec["text_or_value"]))
    target = float(m["num"])
    decimals = len(m["num"].split(".")[1]) if "." in m["num"] else 0
    value = target if progress >= 1 else target * ease_out(progress)
    return f"{m['pre']}{_format_number(value, decimals)}{m['suf']}"


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> str:
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if line and draw.textlength(trial, font=font) > OV_MAX_WIDTH:
            lines.append(line)
            line = word
        else:
            line = trial
    lines.append(line)
    return "\n".join(lines)


def _text_image(text: str, font: ImageFont.FreeTypeFont, size: tuple[int, int] | None = None) -> Image.Image:
    """White text with a thick black outline, centred on a transparent canvas (of `size` if given)."""
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    block = _wrap(probe, text, font)
    box = probe.multiline_textbbox((0, 0), block, font=font, stroke_width=OV_STROKE, align="center", spacing=10)
    tw, th = math.ceil(box[2] - box[0]), math.ceil(box[3] - box[1])
    w, h = size or (tw + 2 * OV_STROKE, th + 2 * OV_STROKE)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).multiline_text(((w - tw) / 2 - box[0], (h - th) / 2 - box[1]), block, font=font, fill="white",
                                       stroke_width=OV_STROKE, stroke_fill="black", align="center", spacing=10)
    return img


def _bar_image(label: str, fraction: float, font: ImageFont.FreeTypeFont, text_size: tuple[int, int]) -> Image.Image:
    img = Image.new("RGBA", (max(BAR_W + 2 * OV_STROKE, text_size[0]), text_size[1] + BAR_GAP + BAR_H + 2 * OV_STROKE),
                    (0, 0, 0, 0))
    text = _text_image(label, font, (img.width, text_size[1]))
    img.alpha_composite(text, (0, 0))
    d = ImageDraw.Draw(img)
    x0, y0 = (img.width - BAR_W) // 2, text_size[1] + BAR_GAP + OV_STROKE
    d.rounded_rectangle([x0 - OV_STROKE, y0 - OV_STROKE, x0 + BAR_W + OV_STROKE, y0 + BAR_H + OV_STROKE],
                        radius=BAR_H // 2 + OV_STROKE, fill=(0, 0, 0, 255))
    d.rounded_rectangle([x0, y0, x0 + BAR_W, y0 + BAR_H], radius=BAR_H // 2, fill=(70, 70, 76, 255))
    if fraction > 0:
        d.rounded_rectangle([x0, y0, x0 + max(BAR_H, round(BAR_W * fraction)), y0 + BAR_H], radius=BAR_H // 2,
                            fill=(255, 255, 255, 255))
    return img


def render_overlay(spec: dict, out_dir: Path, prefix: str, font_path: str, fps: int) -> dict:
    """Write the PNG sequence <out_dir>/<prefix>-%03d.png; the last frame is the final state."""
    out_dir.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype(font_path, OV_FONT_SIZE)
    n = max(1, round(anim_seconds(spec) * fps))
    kind, value = spec["type"], str(spec["text_or_value"])
    frames = []
    if kind == "label":
        base = _text_image(value, font)
        for i in range(n):
            frame = base.copy()
            frame.putalpha(frame.getchannel("A").point(lambda a, k=(i + 1) / n: round(a * k)))
            frames.append(frame)
    elif kind == "counter":
        size = _text_image(counter_text(spec, 1.0), font).size
        frames = [_text_image(counter_text(spec, (i + 1) / n), font, size) for i in range(n)]
    else:  # bar: the percentage counts up while the fill grows
        target = bar_fraction(value)
        text_size = _text_image("100%", font).size
        for i in range(n):
            p = ease_out((i + 1) / n) if i + 1 < n else 1.0
            frames.append(_bar_image(f"{round(target * p * 100)}%", target * p, font, text_size))
    for i, frame in enumerate(frames):
        frame.save(out_dir / f"{prefix}-{i:03d}.png")
    return {"pattern": str(out_dir / f"{prefix}-%03d.png"), "w": frames[0].width, "h": frames[0].height,
            "frames": len(frames), "anim_s": n / fps}
