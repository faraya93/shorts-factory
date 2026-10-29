"""Brand mark generator (pure Pillow, code-rendered): the 'cut-open object' mark, avatar, and a dimmed end card. Proposal only; not wired into the editor.
Run: python tools/brand_mark.py <out_dir> [handle]"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "factory"))
import identity  # noqa: E402  (the colours come from channels/umbrella-es.yaml through factory/identity.py)


def _rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


_P = identity.preset()                                                 # the ACTIVE preset
NAVY, WHITE, EMBER = _rgb(_P["mark_body"]), _rgb(_P["mark_inner"]), _rgb(_P["mark_accent"])   # historical names; values = mark body / inner / accent
CELESTE = SKY = _rgb(_P["top"])
FONT = str(Path(__file__).resolve().parent.parent / "factory" / "assets" / "fonts" / "Montserrat-VF.ttf")


def mark(size=800, body=NAVY, inner=WHITE, accent=EMBER, ss=4, shape="square"):
    """A rounded-square 'object' with its top-right quadrant cut away: the cut face shows the inner layer (white) and the active part
    (ember dot) — the channel's one idea (look inside the object) in three flat shapes."""
    S = size * ss
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(S * 0.22) if shape == "square" else S // 2
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=r, fill=body + (255,))
    cut = Image.new("L", (S, S), 0)
    cd = ImageDraw.Draw(cut)
    cd.rounded_rectangle([int(S * 0.44), -int(S * 0.3), int(S * 1.3), int(S * 0.56)], radius=int(S * 0.10), fill=255)   # the quadrant cut away
    body_mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(body_mask).rounded_rectangle([0, 0, S - 1, S - 1], radius=r, fill=255)
    from PIL import ImageChops
    cut = ImageChops.multiply(cut, body_mask)
    img.paste(Image.new("RGBA", (S, S), inner + (255,)), (0, 0), cut)
    d = ImageDraw.Draw(img)
    cx, cy, rr = int(S * 0.72), int(S * 0.28), int(S * 0.09)
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=accent + (255,))                                                       # active quantity
    return img.resize((size, size), Image.LANCZOS)


def avatar(size=800, bg=CELESTE):
    img = Image.new("RGBA", (size, size), bg + (255,))
    m = mark(int(size * 0.56))
    img.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    return out


def end_card(handle, stage_rgb=SKY, W=1080, H=1920):
    """Dimmed stage (navy veil ~78%) with mark + handle: the reference end card, on the light stage."""
    base = Image.new("RGBA", (W, H), stage_rgb + (255,))
    base.alpha_composite(Image.new("RGBA", (W, H), NAVY + (200,)))
    m = mark(360, body=WHITE, inner=NAVY, accent=EMBER)
    base.alpha_composite(m, ((W - 360) // 2, 760))
    f = ImageFont.truetype(FONT, 64); f.set_variation_by_name("ExtraBold")
    d = ImageDraw.Draw(base)
    tw = d.textlength(handle, font=f)
    d.text(((W - tw) / 2, 1180), handle, font=f, fill=WHITE + (255,))
    return base


def direction_sheet(handle_word="Mecanalia", out=None, names=None):
    """Avatar on each preset's stage colour + wordmark (the name is a placeholder), from the identity presets."""
    P = identity.presets()
    names = names or [n for n in P if P[n]["lighting"] == "studio"]
    f = ImageFont.truetype(FONT, 54); f.set_variation_by_name("ExtraBold")
    W, H = len(names) * 360, 520
    sheet = Image.new("RGB", (W, H), "white")
    for i, k in enumerate(names):
        d = P[k]
        tile = Image.new("RGBA", (360, H), _rgb(d["top"]) + (255,))
        m = mark(200, body=_rgb(d["mark_body"]), inner=_rgb(d["mark_inner"]), accent=_rgb(d["mark_accent"]))
        tile.alpha_composite(m, (80, 120))
        dr = ImageDraw.Draw(tile)
        tw = dr.textlength(handle_word, font=f)
        dr.text(((360 - tw) / 2, 370), handle_word, font=f, fill=_rgb(d["ink"]) + (255,), stroke_width=2 if d["mode"] == "white" else 0, stroke_fill=_rgb(d["ink_stroke"]) + (255,))
        dr.text((10, 10), k.upper(), fill=_rgb(d["ink"]) + (255,))
        sheet.paste(tile.convert("RGB"), (i * 360, 0))
    if out:
        sheet.save(out)
    return sheet


if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    handle = sys.argv[2] if len(sys.argv) > 2 else "@abrelascosas"
    mark(800).save(out / "mark.png"); avatar(800).save(out / "avatar.png"); end_card(handle).convert("RGB").save(out / "endcard.png")
    print("wrote", out)
