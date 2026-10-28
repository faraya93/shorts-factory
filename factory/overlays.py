"""Editor overlays (reference style): validation and Pillow rendering of scene `data_overlays` and the production `end_card`.

A scene may declare `data_overlays`: a list of specs. Each overlay is rendered as a short RGBA PNG sequence (one ffmpeg input at
the video fps): the animation plays, then its last frame is held by the editor until the overlay's visible window ends.

Timing (exactly one of):
  at_offset_seconds   seconds from the scene's narration start (legacy)
  at_word             a spoken word of the scene (or {"word": ..., "nth": 2}); optional offset_s shifts it. This is the
                      WORD LOCK of the format doctrine: the event starts on the highlighted subtitle word.
Placement: x, y = the graphic's centre as a fraction of the frame (default 0.5, 0.5 = legacy centred overlay).
  keyframes [{"t": seconds_from_overlay_start, "x": .., "y": ..}] move the whole graphic (piecewise linear) so a label can
  follow an object that the camera is moving.

Types (reference style: dark stage, gold = active quantity, teal = annotation, red = error):
  label     legacy: big white centred text. style "tag": tiny ALL-CAPS tracked label, optional leader_to [x, y] hairline
  chip      rounded pill, teal outline, white bold text (multi-line with \\n); text_or_value
  (citation / source chips are NOT rendered on screen: owner decision 2026-10-27; type rejected)
  counter   counts from `from` (default 0) to the number in text_or_value ("DÍA 70"); style "mono" is the reference counter
  bar       fills to a fraction or percentage; style "slim" (gold fill), show_value false hides the figure, marker draws a tick
  bracket   teal measuring bracket from [x, y] to [x, y] (no figure; optional text_or_value tag at its middle)
  ring      dotted teal circle, radius as a fraction of the frame width
  mark      red X (kind "x") or gold ring (kind "ok") that pops in with an overshoot
  cta       acted-out call to action: a generic phone, a FOLLOW tap, a share sheet, a chat bubble and a sent tick
"""

import math
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
TYPES = ("counter", "bar", "label", "chip", "citation", "bracket", "ring", "mark", "cta")
NEEDS_TEXT = ("counter", "bar", "label", "chip", "citation")
DEFAULT_ANIM_S = {"counter": 1.2, "bar": 1.2, "label": 0.25, "chip": 0.3, "citation": 0.3, "bracket": 0.5, "ring": 0.7,
                  "mark": 0.35, "cta": 5.0}
DEFAULT_VISIBLE_S = 3.0

OV_FONT_SIZE, OV_STROKE, OV_MAX_WIDTH = 120, 11, 900
BAR_W, BAR_H, BAR_GAP = 760, 56, 22
NUMBER_RE = re.compile(r"^(?P<pre>[^\d]*?)(?P<num>\d+(?:\.\d+)?)(?P<suf>.*)$", re.DOTALL)

TEAL, RED, GOLD, GREY, PASSIVE, VOID = (103, 205, 190), (190, 74, 74), (245, 192, 74), (150, 150, 155), (81, 85, 90), (18, 15, 16)
TEAL0, RED0, GOLD0, VOID0, PASSIVE0 = TEAL, RED, GOLD, VOID, PASSIVE          # fixed originals (the CTA phone UI is always a dark phone)
INK, INK_STROKE = (255, 255, 255), (0, 0, 0)                # text ink + its outline
CHIP_FILL, CHIP_EDGE, CHIP_TEXT = VOID + (235,), TEAL, (255, 255, 255)
TRACK_EDGE = VOID
THEME = "dark"
THEMES = {   # text/graphics theme for the stage (design system 2026-10-27): "dark" = reference look, "light" = celeste stage
    "dark": dict(INK=(255, 255, 255), INK_STROKE=(0, 0, 0), TEAL=(103, 205, 190), RED=(190, 74, 74), GOLD=(245, 192, 74), GREY=(150, 150, 155),
                 PASSIVE=(81, 85, 90), VOID=(18, 15, 16), CHIP_FILL=(18, 15, 16, 235), CHIP_EDGE=(103, 205, 190), CHIP_TEXT=(255, 255, 255),
                 TRACK_EDGE=(18, 15, 16)),
    "light": dict(INK=(11, 37, 64), INK_STROKE=(255, 255, 255), TEAL=(11, 37, 64), RED=(201, 42, 42), GOLD=(232, 89, 12), GREY=(11, 37, 64),
                  PASSIVE=(120, 150, 178), VOID=(11, 37, 64), CHIP_FILL=(11, 37, 64, 245), CHIP_EDGE=(255, 255, 255), CHIP_TEXT=(255, 255, 255),
                  TRACK_EDGE=(255, 255, 255)),
}


def set_theme(name: str) -> None:
    """Switch the module palette (annotation = TEAL role, accent = GOLD role, error = RED role) for the stage the production uses."""
    global THEME, INK, INK_STROKE, TEAL, RED, GOLD, GREY, PASSIVE, VOID, CHIP_FILL, CHIP_EDGE, CHIP_TEXT, TRACK_EDGE
    t = THEMES[name]
    THEME = name
    INK, INK_STROKE, TEAL, RED, GOLD, GREY, PASSIVE, VOID = (t[k] for k in ("INK", "INK_STROKE", "TEAL", "RED", "GOLD", "GREY", "PASSIVE", "VOID"))
    CHIP_FILL, CHIP_EDGE, CHIP_TEXT, TRACK_EDGE = t["CHIP_FILL"], t["CHIP_EDGE"], t["CHIP_TEXT"], t["TRACK_EDGE"]


MONTSERRAT = str(Path(__file__).resolve().parent / "assets" / "fonts" / "Montserrat-VF.ttf")   # SIL OFL, owner 2026-10-27
VARIANT = {"bold": "ExtraBold", "regular": "SemiBold", "narrow": "ExtraBold", "mono": "ExtraBold"}   # one family everywhere
FONTS = {
    "bold": [MONTSERRAT, "/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/Library/Fonts/Arial Bold.ttf",
             "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"],
    "regular": [MONTSERRAT, "/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
    "narrow": [MONTSERRAT, "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"],
    "mono": [MONTSERRAT, "/System/Library/Fonts/Supplemental/Courier New Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"],
}
TAG_SIZE, TAG_TRACK = 34, 4
CHIP_SIZE, CHIP_PAD_X, CHIP_PAD_Y, CHIP_OUTLINE = 44, 34, 20, 5
CITE_SIZE = 28
MONO_SIZE, MONO_STROKE = 80, 4
SLIM_W, SLIM_H = 520, 30


def font(kind: str, size: int) -> ImageFont.FreeTypeFont:
    for path in FONTS[kind]:
        if Path(path).exists():
            f = ImageFont.truetype(path, size)
            if path == MONTSERRAT:
                f.set_variation_by_name(VARIANT[kind])
            return f
    raise FileNotFoundError(f"no {kind} font found in {FONTS[kind]}")


# ------------------------------------------------------------------------------------------ timing and placement
def norm_word(text: str) -> str:
    return re.sub(r"[¿?¡!.,:;«»\"'()\[\]]", "", str(text)).lower().strip()


def find_word_start(words: list[dict], token: str, nth: int = 1) -> float | None:
    """Start (seconds from the scene's narration start) of the nth spoken word equal to `token`, or None."""
    hits = [w["start"] for w in words if norm_word(w["text"]) == norm_word(token)]
    return hits[nth - 1] if 0 < nth <= len(hits) else None


def start_offset(spec: dict, words: list[dict] | None) -> float:
    """Seconds from the scene's narration start at which the overlay starts (at_word resolved against the scene words)."""
    if "at_word" in spec:
        aw = spec["at_word"]
        token, nth = (aw["word"], aw.get("nth", 1)) if isinstance(aw, dict) else (aw, 1)
        t = find_word_start(words or [], token, nth)
        if t is None:
            raise ValueError(f"at_word {token!r} (nth {nth}) not found in the scene's narration")
        return t + float(spec.get("offset_s", 0.0))
    return float(spec["at_offset_seconds"])


def anim_seconds(spec: dict) -> float:
    return float(spec.get("duration_s", DEFAULT_ANIM_S[spec["type"]]))


def visible_seconds(spec: dict) -> float:
    return float(spec.get("visible_s", max(DEFAULT_VISIBLE_S, anim_seconds(spec)) if spec["type"] == "cta" else DEFAULT_VISIBLE_S))


def ease_out(p: float) -> float:
    return 1 - (1 - p) ** 3


def back_out(p: float, s: float = 1.9) -> float:
    """Ease-out with overshoot (springy pop): 0 -> 1, peaking ~10-15% over 1 near the end."""
    p = min(1.0, max(0.0, p))
    return 1 + (s + 1) * (p - 1) ** 3 + s * (p - 1) ** 2


def bar_fraction(value) -> float | None:
    """'75%' -> 0.75, '0.75' -> 0.75; anything outside 0..1 is rejected (None)."""
    s = str(value).strip()
    try:
        x = float(s[:-1]) / 100 if s.endswith("%") else float(s)
    except ValueError:
        return None
    return x if 0 <= x <= 1 else None


def has_placement(spec: dict) -> bool:
    return any(k in spec for k in ("x", "y", "keyframes", "from", "to", "leader_to"))


def track_expr(points: list[tuple[float, float]], start: float) -> str:
    """ffmpeg expression of t (absolute seconds) for a piecewise-linear track [(t_rel, value), ...] beginning at `start`."""
    pts = sorted(points)
    expr = f"{pts[-1][1]:.2f}"
    for (t0, v0), (t1, v1) in reversed(list(zip(pts, pts[1:]))):
        a, b = start + t0, start + t1
        seg = f"{v0:.2f}+({v1 - v0:.2f})*(t-{a:.3f})/{b - a:.3f}" if b > a else f"{v1:.2f}"
        expr = f"if(lt(t,{b:.3f}),{seg},{expr})"
    return f"if(lt(t,{start + pts[0][0]:.3f}),{pts[0][1]:.2f},{expr})"


# ------------------------------------------------------------------------------------------------- validation
def _frac(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v <= 1


def _point(v) -> bool:
    return isinstance(v, (list, tuple)) and len(v) == 2 and all(_frac(c) for c in v)


def validate_scene_overlays(scene_id, overlays) -> list[str]:
    errors, windows = [], []
    if not isinstance(overlays, list):
        return [f"scene {scene_id}: data_overlays must be a list"]
    for n, spec in enumerate(overlays, 1):
        tag = f"scene {scene_id} overlay {n}"
        if not isinstance(spec, dict) or spec.get("type") not in TYPES:
            errors.append(f"{tag}: type must be one of {TYPES}")
            continue
        kind, value = spec["type"], spec.get("text_or_value")
        if kind == "citation":
            errors.append(f"{tag}: source citations are never rendered on screen (owner rule 2026-10-27)")
            continue
        if kind in NEEDS_TEXT and (value is None or not str(value).strip()):
            errors.append(f"{tag}: missing text_or_value")
        if ("at_word" in spec) == ("at_offset_seconds" in spec):
            errors.append(f"{tag}: give exactly one of at_offset_seconds or at_word")
            continue
        if "at_offset_seconds" in spec:
            at = spec["at_offset_seconds"]
            if not isinstance(at, (int, float)) or isinstance(at, bool) or at < 0:
                errors.append(f"{tag}: at_offset_seconds must be a number >= 0")
                continue
        else:
            aw = spec["at_word"]
            if not (isinstance(aw, str) and aw.strip()) and not (isinstance(aw, dict) and str(aw.get("word", "")).strip()):
                errors.append(f"{tag}: at_word must be a word or {{'word': ..., 'nth': n}}")
                continue
            at = 0.0
        anim, visible = anim_seconds(spec), visible_seconds(spec)
        if anim <= 0 or visible < anim:
            errors.append(f"{tag}: need duration_s > 0 and visible_s >= duration_s")
            continue
        for key in ("x", "y"):
            if key in spec and not _frac(spec[key]):
                errors.append(f"{tag}: {key} must be a fraction 0..1 of the frame")
        for key in ("from", "to", "leader_to"):
            if key in spec and kind != "counter" and not _point(spec[key]):
                errors.append(f"{tag}: {key} must be [x, y] fractions 0..1")
        if "keyframes" in spec:
            kf = spec["keyframes"]
            if not (isinstance(kf, list) and len(kf) >= 2 and all(isinstance(k, dict) and _frac(k.get("x")) and _frac(k.get("y"))
                                                                  and isinstance(k.get("t"), (int, float)) for k in kf)):
                errors.append(f"{tag}: keyframes must be a list of >= 2 {{t, x, y}} with x, y in 0..1")
        if kind == "counter":
            if value is not None and not NUMBER_RE.match(str(value)):
                errors.append(f"{tag}: counter needs a number such as '170 °C' or 'DÍA 70', got {value!r}")
            if "from" in spec and not isinstance(spec["from"], (int, float)):
                errors.append(f"{tag}: counter 'from' must be a number")
        if kind == "bar" and value is not None and bar_fraction(value) is None:
            errors.append(f"{tag}: bar needs a fraction 0..1 or a percentage such as '75%', got {value!r}")
        if kind == "bracket" and not ("from" in spec and "to" in spec):
            errors.append(f"{tag}: bracket needs from and to")
        if kind == "ring" and not (isinstance(spec.get("radius"), (int, float)) and 0 < spec["radius"] <= 0.6):
            errors.append(f"{tag}: ring needs radius in (0, 0.6] (fraction of the frame width)")
        if kind == "mark" and spec.get("kind") not in ("x", "ok"):
            errors.append(f"{tag}: mark needs kind 'x' or 'ok'")
        if kind == "cta" and not str(spec.get("message", "")).strip():
            errors.append(f"{tag}: cta needs a message (the chat bubble text)")
        if kind == "label" and spec.get("style", "title") not in ("title", "tag"):
            errors.append(f"{tag}: label style must be 'title' or 'tag'")
        if not has_placement(spec):    # only legacy centred overlays share one spot, so only they may not overlap
            windows.append((at, at + visible, n))
    for i, (a1, b1, n1) in enumerate(windows):
        for a2, b2, n2 in windows[i + 1:]:
            if a1 < b2 and a2 < b1:
                errors.append(f"scene {scene_id}: overlays {n1} and {n2} overlap in time (both sit at the centre)")
    return errors


def validate_end_card(card) -> list[str]:
    if card is None:
        return []
    if not isinstance(card, dict):
        return ["end_card must be an object"]
    errors = []
    d = card.get("duration_s", 4.0)
    if not isinstance(d, (int, float)) or not 1 <= d <= 10:
        errors.append("end_card.duration_s must be a number in [1, 10]")
    if not str(card.get("handle", "")).strip():
        errors.append("end_card.handle is required (use the placeholder '@[CANAL]' until the channel handle exists)")
    dim = card.get("dim", 0.25)
    if not isinstance(dim, (int, float)) or not 0 <= dim <= 0.9:
        errors.append("end_card.dim must be a number in [0, 0.9] (the brightness left behind the card)")
    return errors


# ----------------------------------------------------------------------------------------------------- drawing
def _format_number(x: float, decimals: int) -> str:
    return f"{x:,.{decimals}f}".replace(",", "\u00a0") if abs(x) >= 10000 else f"{x:.{decimals}f}"


def counter_text(spec: dict, progress: float) -> str:
    """The counter's text at animation progress 0..1 (eased); the last frame is exactly the target."""
    m = NUMBER_RE.match(str(spec["text_or_value"]))
    target = float(m["num"])
    start = float(spec.get("from", 0))
    decimals = len(m["num"].split(".")[1]) if "." in m["num"] else 0
    value = target if progress >= 1 else start + (target - start) * ease_out(progress)
    return f"{m['pre']}{_format_number(value, decimals)}{m['suf']}"


def _wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> str:
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if line and draw.textlength(trial, font=fnt) > OV_MAX_WIDTH:
            lines.append(line)
            line = word
        else:
            line = trial
    lines.append(line)
    return "\n".join(lines)


def _text_image(text: str, fnt: ImageFont.FreeTypeFont, size: tuple[int, int] | None = None, stroke: int = OV_STROKE,
                fill=None) -> Image.Image:
    """Text with an outline (theme ink / ink stroke), centred on a transparent canvas (of `size` if given)."""
    fill = fill or INK + (255,)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    block = _wrap(probe, text, fnt)
    box = probe.multiline_textbbox((0, 0), block, font=fnt, stroke_width=stroke, align="center", spacing=10)
    tw, th = math.ceil(box[2] - box[0]), math.ceil(box[3] - box[1])
    w, h = size or (tw + 2 * stroke, th + 2 * stroke)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(img).multiline_text(((w - tw) / 2 - box[0], (h - th) / 2 - box[1]), block, font=fnt, fill=fill,
                                       stroke_width=stroke, stroke_fill=INK_STROKE, align="center", spacing=10)
    return img


def _bar_image(label: str, fraction: float, fnt: ImageFont.FreeTypeFont, text_size: tuple[int, int]) -> Image.Image:
    img = Image.new("RGBA", (max(BAR_W + 2 * OV_STROKE, text_size[0]), text_size[1] + BAR_GAP + BAR_H + 2 * OV_STROKE),
                    (0, 0, 0, 0))
    text = _text_image(label, fnt, (img.width, text_size[1]))
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


def _slim_bar(fraction: float, marker: float | None, label: str | None) -> Image.Image:
    pad = 8
    lab = None
    if label:
        lab = _text_image(label, font("bold", 34), stroke=3, fill=GREY + (255,))
    top = (lab.height + 10) if lab else 0
    img = Image.new("RGBA", (max(SLIM_W + 2 * pad, lab.width if lab else 0), top + SLIM_H + 2 * pad), (0, 0, 0, 0))
    if lab:
        img.alpha_composite(lab, ((img.width - lab.width) // 2, 0))
    d = ImageDraw.Draw(img)
    x0, y0 = (img.width - SLIM_W) // 2, top + pad
    d.rounded_rectangle([x0 - 3, y0 - 3, x0 + SLIM_W + 3, y0 + SLIM_H + 3], radius=SLIM_H // 2 + 3, fill=TRACK_EDGE + (235,))
    d.rounded_rectangle([x0, y0, x0 + SLIM_W, y0 + SLIM_H], radius=SLIM_H // 2, fill=PASSIVE + (255,))
    if fraction > 0:
        d.rounded_rectangle([x0, y0, x0 + max(SLIM_H, round(SLIM_W * fraction)), y0 + SLIM_H], radius=SLIM_H // 2, fill=GOLD + (255,))
    if marker is not None:
        mx = x0 + round(SLIM_W * marker)
        d.rectangle([mx - 2, y0 - 8, mx + 2, y0 + SLIM_H + 8], fill=INK + (255,))
    return img


def _tracked_text(text: str, fnt: ImageFont.FreeTypeFont, tracking: int, fill) -> Image.Image:
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    widths = [probe.textlength(ch, font=fnt) for ch in text]
    w = math.ceil(sum(widths) + tracking * (len(text) - 1)) + 8
    asc, desc = fnt.getmetrics()
    img = Image.new("RGBA", (w, asc + desc + 8), (0, 0, 0, 0))
    d, x = ImageDraw.Draw(img), 4.0
    for ch, cw in zip(text, widths):
        d.text((x, 4), ch, font=fnt, fill=fill, stroke_width=2, stroke_fill=INK_STROKE + (255,))
        x += cw + tracking
    return img


def _px(spec: dict, key: str, default):
    v = spec.get(key)
    return (v[0] * W, v[1] * H) if v else default


def _center(spec: dict) -> tuple[float, float]:
    return spec.get("x", 0.5) * W, spec.get("y", 0.5) * H


def _pop_frames(img: Image.Image, n: int) -> list[Image.Image]:
    """The same graphic scaled in with an overshoot (anticipation-free pop), on a canvas a bit larger than itself."""
    cw, ch = round(img.width * 1.25), round(img.height * 1.25)
    out = []
    for i in range(n):
        s = max(0.01, back_out((i + 1) / n))
        scaled = img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))), Image.LANCZOS)
        canvas = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
        canvas.alpha_composite(scaled, ((cw - scaled.width) // 2, (ch - scaled.height) // 2))
        out.append(canvas)
    return out


def _fade_frames(img: Image.Image, n: int) -> list[Image.Image]:
    frames = []
    for i in range(n):
        f = img.copy()
        f.putalpha(f.getchannel("A").point(lambda a, k=(i + 1) / n: round(a * k)))
        frames.append(f)
    return frames


def _chip_image(text: str) -> Image.Image:
    fnt = font("bold", CHIP_SIZE)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines = text.split("\n")
    widths = [probe.textlength(l, font=fnt) for l in lines]
    asc, desc = fnt.getmetrics()
    lh = asc + desc
    w, h = math.ceil(max(widths)) + 2 * CHIP_PAD_X, lh * len(lines) + 2 * CHIP_PAD_Y
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=min(h // 2, 46), fill=CHIP_FILL, outline=CHIP_EDGE + (255,), width=CHIP_OUTLINE)
    for i, l in enumerate(lines):
        d.text(((w - widths[i]) / 2, CHIP_PAD_Y + i * lh), l, font=fnt, fill=CHIP_TEXT + (255,))
    return img


def _label_tag(spec: dict, n: int):
    """Tiny ALL-CAPS tracked label; with leader_to, a hairline leader grows from the text to the target point (dot at the end).
    Returns (frames, (left, top)) in frame pixels."""
    text = str(spec["text_or_value"]).upper()
    tag = _tracked_text(text, font("narrow", TAG_SIZE), TAG_TRACK, INK + (255,))
    cx, cy = _center(spec)
    tx0, ty0 = cx - tag.width / 2, cy - tag.height / 2
    target = _px(spec, "leader_to", None)
    if not target:
        return _fade_frames(tag, n), (round(tx0), round(ty0))
    tx, ty = target
    # leader leaves from the text edge nearest the target
    sx = min(max(tx, tx0), tx0 + tag.width)
    sy = ty0 + tag.height if ty > cy else ty0
    m = 10
    left, top = math.floor(min(tx0, tx, sx) - m), math.floor(min(ty0, ty, sy) - m)
    right, bottom = math.ceil(max(tx0 + tag.width, tx, sx) + m), math.ceil(max(ty0 + tag.height, ty, sy) + m)
    frames = []
    for i in range(n):
        p = ease_out((i + 1) / n)
        img = Image.new("RGBA", (right - left, bottom - top), (0, 0, 0, 0))
        base = tag.copy()
        base.putalpha(base.getchannel("A").point(lambda a, k=min(1.0, (i + 1) * 3 / n): round(a * k)))
        img.alpha_composite(base, (round(tx0 - left), round(ty0 - top)))
        d = ImageDraw.Draw(img)
        ex, ey = sx + (tx - sx) * p, sy + (ty - sy) * p
        d.line([(sx - left, sy - top), (ex - left, ey - top)], fill=INK + (255,), width=3)
        if p >= 1.0:
            d.ellipse([tx - left - 6, ty - top - 6, tx - left + 6, ty - top + 6], fill=INK + (255,))
        frames.append(img)
    return frames, (left, top)


def _bracket(spec: dict, n: int):
    (x0, y0), (x1, y1) = _px(spec, "from", (0, 0)), _px(spec, "to", (0, 0))
    tick, m, wd = 30, 40, 6
    extra = 70 if spec.get("text_or_value") else 0           # room above the bracket for its tag
    left, top = math.floor(min(x0, x1) - m), math.floor(min(y0, y1) - m - extra)
    right, bottom = math.ceil(max(x0, x1) + m), math.ceil(max(y0, y1) + m)
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / length * tick, dx / length * tick
    tag = None
    if spec.get("text_or_value"):
        tag = _tracked_text(str(spec["text_or_value"]).upper(), font("narrow", TAG_SIZE), TAG_TRACK, TEAL + (255,))
    frames = []
    for i in range(n):
        p = ease_out((i + 1) / n)
        img = Image.new("RGBA", (right - left, bottom - top), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        ax, ay, bx, by = mx + (x0 - mx) * p, my + (y0 - my) * p, mx + (x1 - mx) * p, my + (y1 - my) * p    # grows from the middle
        d.line([(ax - left, ay - top), (bx - left, by - top)], fill=TEAL + (255,), width=wd)
        for (px_, py_) in ((ax, ay), (bx, by)):
            d.line([(px_ - nx - left, py_ - ny - top), (px_ + nx - left, py_ + ny - top)], fill=TEAL + (255,), width=wd)
        if tag is not None and p > 0.6:
            img.alpha_composite(tag, (round(mx - tag.width / 2 - left), round(my - tag.height - 14 - top)))
        frames.append(img)
    return frames, (left, top)


def _ring(spec: dict, n: int):
    cx, cy = _center(spec)
    r = spec["radius"] * W
    wd, m = 7, 14
    size = math.ceil(2 * (r + wd + m))
    frames = []
    dashes = 48
    for i in range(n):
        p = ease_out((i + 1) / n)
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        box = [m + wd, m + wd, size - m - wd, size - m - wd]
        for k in range(int(dashes * p)):
            a0 = -90 + k * 360 / dashes
            d.arc(box, a0, a0 + 360 / dashes * 0.55, fill=TEAL + (255,), width=wd)
        frames.append(img)
    return frames, (round(cx - size / 2), round(cy - size / 2))


def _mark(spec: dict, n: int):
    cx, cy = _center(spec)
    size = 120
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if spec["kind"] == "x":
        d.line([(18, 18), (size - 18, size - 18)], fill=RED + (255,), width=18)
        d.line([(size - 18, 18), (18, size - 18)], fill=RED + (255,), width=18)
        for a, b in (((18, 18), (size - 18, size - 18)), ((size - 18, 18), (18, size - 18))):
            for p in (a, b):
                d.ellipse([p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9], fill=RED + (255,))
    else:
        d.ellipse([14, 14, size - 14, size - 14], outline=GOLD + (255,), width=14)
    frames = _pop_frames(img, n)
    cw = frames[0].width
    return frames, (round(cx - cw / 2), round(cy - cw / 2))


def _cta(spec: dict, n: int, fps: int):
    """Phone mock: phase A taps FOLLOW, phase B opens a share sheet and picks a friend, phase C shows the chat bubble and a sent tick."""
    pw, ph = 640, 1180
    cx, cy = _center(spec)
    follow = str(spec.get("follow_text", "SEGUIR")).upper()
    following = str(spec.get("following_text", "SIGUIENDO")).upper()
    message, sent = str(spec["message"]), str(spec.get("sent_text", "Enviado"))
    f_btn, f_msg, f_small = font("bold", 40), font("regular", 36), font("regular", 28)
    frames = []
    for i in range(n):
        u = (i + 1) / n
        img = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=70, fill=(28, 26, 27, 250), outline=(95, 95, 100, 255), width=6)
        d.rounded_rectangle([pw // 2 - 70, 22, pw // 2 + 70, 48], radius=13, fill=VOID0 + (255,))
        if u < 0.62:                                   # profile screen with the FOLLOW button
            d.ellipse([60, 110, 190, 240], fill=PASSIVE + (255,))
            d.rounded_rectangle([220, 130, 520, 160], radius=14, fill=(110, 110, 116, 255))
            d.rounded_rectangle([220, 185, 420, 210], radius=12, fill=(70, 70, 76, 255))
            tapped = u > 0.18
            bx0, by0, bx1, by1 = 60, 290, pw - 60, 370
            d.rounded_rectangle([bx0, by0, bx1, by1], radius=22, fill=(PASSIVE0 + (255,)) if tapped else (GOLD0 + (255,)))
            label = following if tapped else follow
            tw = d.textlength(label, font=f_btn)
            d.text(((pw - tw) / 2, by0 + 17), label, font=f_btn, fill=(255, 255, 255, 255) if tapped else VOID0 + (255,))
            if 0.10 < u < 0.26:                         # tap ripple
                k = (u - 0.10) / 0.16
                r = 20 + 60 * k
                d.ellipse([pw / 2 - r, 330 - r, pw / 2 + r, 330 + r], outline=(255, 255, 255, round(255 * (1 - k))), width=5)
            for row in range(3):
                for col in range(3):
                    d.rounded_rectangle([60 + col * 185, 470 + row * 185, 60 + col * 185 + 170, 470 + row * 185 + 170],
                                        radius=14, fill=(48, 46, 48, 255))
            if u > 0.30:                                # share sheet slides up
                k = ease_out(min(1.0, (u - 0.30) / 0.14))
                top = ph - round(560 * k)
                d.rounded_rectangle([0, top, pw - 1, ph - 1], radius=60, fill=(40, 38, 40, 255), outline=(95, 95, 100, 255), width=4)
                d.rounded_rectangle([pw // 2 - 50, top + 18, pw // 2 + 50, top + 28], radius=5, fill=(120, 120, 126, 255))
                d.rounded_rectangle([50, top + 60, pw - 50, top + 110], radius=24, fill=(60, 58, 60, 255))
                shades = [(120, 100, 90), (90, 110, 120), (130, 120, 100), (100, 100, 125)]
                for a in range(4):
                    ax = 70 + a * 140
                    d.ellipse([ax, top + 160, ax + 110, top + 270], fill=shades[a] + (255,))
                    if a == 0 and u > 0.42:
                        k2 = min(1.0, (u - 0.42) / 0.10)
                        d.ellipse([ax - 8, top + 152, ax + 118, top + 278], outline=GOLD0 + (255,), width=int(2 + 8 * k2))
                if u > 0.50:
                    k3 = ease_out(min(1.0, (u - 0.50) / 0.10))
                    d.rounded_rectangle([50, top + 350, pw - 50, top + 430], radius=26, fill=GOLD0 + (round(255 * k3),))
                    d.text((pw // 2 - d.textlength("ENVIAR", font=f_btn) / 2, top + 368), "ENVIAR", font=f_btn, fill=VOID0 + (round(255 * k3),))
        else:                                           # chat: the friend's bubble and the sent tick
            d.ellipse([50, 100, 130, 180], fill=(120, 100, 90, 255))
            d.rounded_rectangle([150, 125, 400, 155], radius=14, fill=(110, 110, 116, 255))
            k = back_out(min(1.0, (u - 0.62) / 0.12))
            words, lines, line = message.split(), [], ""
            for wd_ in words:
                trial = f"{line} {wd_}".strip()
                if line and d.textlength(trial, font=f_msg) > pw - 200:
                    lines.append(line)
                    line = wd_
                else:
                    line = trial
            lines.append(line)
            bh = 40 + 48 * len(lines)
            by = 300
            bx1 = 70 + round((pw - 140) * min(1.0, k))
            d.rounded_rectangle([70, by, max(bx1, 120), by + bh], radius=34, fill=(60, 58, 60, 255))
            if k >= 1.0:
                for j, l in enumerate(lines):
                    d.text((100, by + 22 + 48 * j), l, font=f_msg, fill=(255, 255, 255, 255))
            if u > 0.82:
                a = round(255 * min(1.0, (u - 0.82) / 0.08))
                d.text((70, by + bh + 20), sent, font=f_small, fill=TEAL0 + (a,))
                d.ellipse([70 + d.textlength(sent, font=f_small) + 14, by + bh + 28, 70 + d.textlength(sent, font=f_small) + 38, by + bh + 52],
                          fill=TEAL0 + (a,))
        frames.append(img)
    return frames, (round(cx - pw / 2), round(cy - ph / 2))


def render_overlay(spec: dict, out_dir: Path, prefix: str, font_path: str, fps: int) -> dict:
    """Write the PNG sequence <out_dir>/<prefix>-%03d.png; the last frame is the final state.
    Returns pattern, w, h, frames, anim_s and, when the overlay is positioned, left/top (frame pixels) and an optional track."""
    out_dir.mkdir(parents=True, exist_ok=True)
    kind = spec["type"]
    n = max(1, round(anim_seconds(spec) * fps))
    value = str(spec.get("text_or_value", ""))
    origin = None
    if kind == "label" and spec.get("style") == "tag":
        frames, origin = _label_tag(spec, n)
    elif kind == "label":
        base = _text_image(value, ImageFont.truetype(font_path, OV_FONT_SIZE))
        frames = _fade_frames(base, n)
    elif kind == "chip":
        frames = _pop_frames(_chip_image(value), n)
        cx, cy = _center(spec)
        origin = (round(cx - frames[0].width / 2), round(cy - frames[0].height / 2))
    elif kind == "citation":
        img = _text_image(value, font("regular", CITE_SIZE), stroke=2, fill=GREY + (255,))
        cx, cy = _center(spec)
        frames, origin = _fade_frames(img, n), (round(cx - img.width / 2), round(cy - img.height / 2))
    elif kind == "counter":
        mono = spec.get("style") == "mono"
        fnt = font("mono", MONO_SIZE) if mono else ImageFont.truetype(font_path, OV_FONT_SIZE)
        stroke = MONO_STROKE if mono else OV_STROKE
        size = _text_image(counter_text(spec, 1.0), fnt, stroke=stroke).size
        frames = [_text_image(counter_text(spec, (i + 1) / n), fnt, size, stroke=stroke) for i in range(n)]
        if mono or has_placement(spec):
            cx, cy = _center(spec)
            origin = (round(cx - size[0] / 2), round(cy - size[1] / 2))
    elif kind == "bar":
        target = bar_fraction(value)
        if spec.get("style") == "slim":
            frames = [_slim_bar(target * (ease_out((i + 1) / n) if i + 1 < n else 1.0), spec.get("marker"), spec.get("label"))
                      for i in range(n)]
            cx, cy = _center(spec)
            origin = (round(cx - frames[0].width / 2), round(cy - frames[0].height / 2))
        else:
            fnt = ImageFont.truetype(font_path, OV_FONT_SIZE)
            text_size = _text_image("100%", fnt).size
            frames = []
            for i in range(n):
                p = ease_out((i + 1) / n) if i + 1 < n else 1.0
                label = f"{round(target * p * 100)}%" if spec.get("show_value", True) else " "
                frames.append(_bar_image(label, target * p, fnt, text_size))
            if has_placement(spec):
                cx, cy = _center(spec)
                origin = (round(cx - frames[0].width / 2), round(cy - frames[0].height / 2))
    elif kind == "bracket":
        frames, origin = _bracket(spec, n)
    elif kind == "ring":
        frames, origin = _ring(spec, n)
    elif kind == "mark":
        frames, origin = _mark(spec, n)
    else:  # cta
        frames, origin = _cta(spec, n, fps)
    for i, frame in enumerate(frames):
        frame.save(out_dir / f"{prefix}-{i:03d}.png")
    meta = {"pattern": str(out_dir / f"{prefix}-%03d.png"), "w": frames[0].width, "h": frames[0].height,
            "frames": len(frames), "anim_s": n / fps}
    if origin is not None:
        meta["left"], meta["top"] = origin
        if "keyframes" in spec:   # keyframes give the graphic's CENTRE over time; convert to a top-left track for ffmpeg
            kf = sorted(spec["keyframes"], key=lambda k: k["t"])
            meta["track"] = [(k["t"], k["x"] * W - meta["w"] / 2, k["y"] * H - meta["h"] / 2) for k in kf]
    return meta


# ------------------------------------------------------------------------------------------------- end card
def render_end_card(card: dict, out_dir: Path, prefix: str, fps: int) -> dict:
    """Full-frame sequence: the scene dims to `dim` brightness, then a placeholder logo and the handle fade in (~0.6 s)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    dim = float(card.get("dim", 0.25))
    handle = str(card["handle"]).upper()
    n = max(2, round(0.6 * fps))
    logo = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    ld = ImageDraw.Draw(logo)
    ld.rounded_rectangle([6, 6, 193, 193], radius=52, outline=(255, 255, 255, 255), width=12)
    ld.polygon([(78, 60), (78, 140), (146, 100)], fill=(255, 255, 255, 255))     # generic play glyph: a PLACEHOLDER
    tag = _tracked_text(handle, font("narrow", 56), 3, (255, 255, 255, 255))
    frames = []
    for i in range(n):
        p = ease_out((i + 1) / n)
        img = Image.new("RGBA", (W, H), (0, 0, 0, round(255 * (1 - dim) * p)))
        a = lambda im: im.putalpha(im.getchannel("A").point(lambda v: round(v * p))) or im
        img.alpha_composite(a(logo.copy()), ((W - 200) // 2, round(H * 0.5) - 140))
        img.alpha_composite(a(tag.copy()), ((W - tag.width) // 2, round(H * 0.5) + 90))
        frames.append(img)
    for i, f in enumerate(frames):
        f.save(out_dir / f"{prefix}-{i:03d}.png")
    return {"pattern": str(out_dir / f"{prefix}-%03d.png"), "w": W, "h": H, "frames": n, "anim_s": n / fps}
