"""COMPOSITION GATE (design rule, CLAUDE.md "Support colours"): before any full render, tabulate the pairwise colour distances IN FRAME on
representative stills and BLOCK on any pair under its threshold. Run with the project venv:
  .venv/bin/python tools/composition_gate.py <dir with still-NNNN.png + mask-NNNN.png> [--preset coral] [--identity export.json]
Stills come from `blender ... stills=a,b,c mask=1 look=<preset>`. Classes are read from the flat mask (code3d/lib/composition.py)."""
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "factory"))
from palette_metrics import de2000, wcag  # noqa: E402
import identity  # noqa: E402

CLASSES = {"stage": (255, 0, 255), "support_board": (0, 255, 0), "support_plinth": (0, 200, 120), "support_panel": (0, 120, 60), "support_plate": (120, 255, 120),
           "hero_big": (0, 0, 255), "hero_small": (0, 120, 255), "hero_housing": (255, 128, 0), "hero_rubber": (128, 64, 0), "hero_blade": (255, 255, 128),
           "accent": (255, 255, 0), "error": (255, 0, 0)}
T = dict(stage_support=20.0, stage_hero=20.0, support_hero=20.0, accent_stage_de=20.0, accent_stage_contrast=3.0, accent_swatch_family=15.0, min_pixels=400)


def hexof(rgb):
    return "#%02X%02X%02X" % tuple(round(v) for v in rgb)


def class_means(beauty: Image.Image, mask: Image.Image) -> dict:
    out = {}
    bp, mp = beauty.convert("RGB"), mask.convert("RGB")
    W, H = mp.size
    for cls, rgb in CLASSES.items():
        m = Image.eval(mp.convert("L"), lambda v: 0)         # build binary mask by exact class colour
        r, g, b = mp.split()
        sel = Image.composite(Image.new("L", (W, H), 255), Image.new("L", (W, H), 0), r.point(lambda v, t=rgb[0]: 255 if abs(v - t) < 8 else 0))
        for chan, t in ((g, rgb[1]), (b, rgb[2])):
            sel = Image.composite(sel, Image.new("L", (W, H), 0), chan.point(lambda v, t=t: 255 if abs(v - t) < 8 else 0))
        sel = sel.filter(ImageFilter.MinFilter(7))            # erode: drop anti-aliased edges
        n = sum(1 for v in sel.getdata() if v)
        if n < T["min_pixels"]:
            continue
        px_b, px_s = bp.load(), sel.load()
        acc = [0, 0, 0]
        cnt = 0
        for y in range(0, H, 2):
            for x in range(0, W, 2):
                if px_s[x, y]:
                    p = px_b[x, y]
                    acc[0] += p[0]; acc[1] += p[1]; acc[2] += p[2]; cnt += 1
        if cnt:
            out[cls] = (hexof([v / cnt for v in acc]), n)
    return out


def gate(folder: Path, preset: dict) -> tuple[list[str], bool]:
    lines, blocked = [], False
    for beauty in sorted(folder.glob("still-*.png")):
        mask = folder / beauty.name.replace("still-", "mask-")
        if not mask.exists():
            continue
        means = class_means(Image.open(beauty), Image.open(mask))
        lines.append(f"\n### {beauty.name}\n| class | mean rendered colour | pixels |\n|---|---|---|")
        for k, (h, n) in means.items():
            lines.append(f"| {k} | {h} | {n} |")
        lines.append("\n| pair | rule | distance | verdict |\n|---|---|---|---|")
        stage = means.get("stage", (None,))[0]

        def row(a, b, rule, thr, extra=""):
            nonlocal blocked
            d = de2000(means[a][0], means[b][0])
            ok = d >= thr
            blocked |= not ok
            lines.append(f"| {a} vs {b} | {rule} >= {thr:g} | {d:.1f}{extra} | {'PASS' if ok else 'BLOCK'} |")
        sup = [k for k in means if k.startswith("support_")]
        hero = [k for k in means if k.startswith("hero_")]
        if stage:
            for s in sup:
                row("stage", s, "stage-support", T["stage_support"])
            for h in hero:
                row("stage", h, "stage-hero", T["stage_hero"])
        for s in sup:
            for h in hero:
                row(s, h, "support-hero", T["support_hero"])
        if stage and "accent" in means:
            row("accent", "stage", "accent-stage", T["accent_stage_de"])
            c = wcag(means["accent"][0], stage)
            ok = c >= T["accent_stage_contrast"]
            blocked |= not ok
            lines.append(f"| accent vs stage | luminance contrast >= {T['accent_stage_contrast']:g}:1 | {c:.2f}:1 | {'PASS' if ok else 'BLOCK'} |")
            fam = de2000(means["accent"][0], preset["accent"])
            ok = fam <= T["accent_swatch_family"]
            blocked |= not ok
            lines.append(f"| rendered accent {means['accent'][0]} vs swatch {preset['accent']} | family dE <= {T['accent_swatch_family']:g} | {fam:.1f} | {'PASS' if ok else 'BLOCK'} |")
        if "error" in means:
            fam = de2000(means["error"][0], preset["error"])
            ok = fam <= T["accent_swatch_family"]
            blocked |= not ok
            lines.append(f"| rendered error {means['error'][0]} vs swatch {preset['error']} | family dE <= {T['accent_swatch_family']:g} | {fam:.1f} | {'PASS' if ok else 'BLOCK'} |")
    return lines, blocked


if __name__ == "__main__":
    a = sys.argv[1:]
    folder = Path(a[0])
    ident = json.load(open(a[a.index("--identity") + 1])) if "--identity" in a else None
    name = a[a.index("--preset") + 1] if "--preset" in a else (ident or {}).get("active") or identity.active_name()
    preset = (ident["presets"] if ident else identity.presets())[name]
    lines, blocked = gate(folder, preset)
    print(f"# Composition gate: preset {name}  support board {preset['support_board']} plate {preset['support_plate']} panel {preset['support_panel']}")
    print("\n".join(lines))
    print("\nGATE:", "BLOCKED (fix before any full render)" if blocked else "PASS")
    sys.exit(1 if blocked else 0)
