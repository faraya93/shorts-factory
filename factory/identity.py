"""The channel identity as PARAMETERS: one source of truth, channels/umbrella-es.yaml (blocks `identity` and `render`).
Everything that draws the channel's look reads it through here: the Editor's text themes (overlays.py, editor.py), the end-card mark, the code3d
stage/plinth/accent (via a JSON snapshot, because Blender has no PyYAML), the brand tools and new productions' visual_identity.

CLI (run with the project venv):
  .venv/bin/python factory/identity.py show                      # active preset + the presets available
  .venv/bin/python factory/identity.py export [path] [--preset N] # JSON snapshot for Blender (default build/identity-export.json)
  .venv/bin/python factory/identity.py apply productions/x/scenes.json [--preset N]  # embed the identity into a production's scenes.json
TO SWITCH THE CHANNEL IDENTITY: edit `identity.active` (or one preset's values) in channels/umbrella-es.yaml, then re-render. No code change."""

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "channels" / "umbrella-es.yaml"
EXPORT = ROOT / "build" / "identity-export.json"
HEX = "#"


def load(path: Path | None = None) -> dict:
    return yaml.safe_load(Path(path or CONFIG).read_text(encoding="utf-8"))


def active_name(cfg: dict | None = None) -> str:
    return (cfg or load())["identity"]["active"]


def _flat(name: str, raw: dict, neutrals: dict) -> dict:
    """Flatten one preset into the flat key set the consumers use (top, bottom, plinth, ink, spoken_box, mark_body ...)."""
    sub, mark = raw["subtitle"], raw.get("mark", {})
    return {
        "name": name, "title": raw["title"], "lighting": raw.get("lighting", "studio"),
        "top": raw["stage"]["top"], "bottom": raw["stage"]["bottom"], "plinth": raw["plinth"],
        "board": raw["support"]["board"], "support_board": raw["support"]["board"], "support_plate": raw["support"]["plate"],
        "support_panel": raw["support"]["panel"], "emission_gain": float(raw.get("emission_gain", 1.0)),
        "accent": raw["accent"], "error": raw["error"], "annot": raw["annotation"],
        "mode": sub["mode"], "ink": sub["ink"], "ink_stroke": sub["outline"], "word": sub.get("word", sub["ink"]),
        "spoken_box": sub["spoken_box"], "spoken_text": sub["spoken_text"], "emph": sub["emphasis"],
        "mark_body": mark.get("body", raw["plinth"]), "mark_inner": mark.get("inner", raw["stage"]["top"]), "mark_accent": mark.get("accent", raw["accent"]),
        "halo": raw.get("halo"), "rim": raw.get("rim"), "legacy": bool(raw.get("legacy", False)),
        "passive_dark": neutrals["passive_dark"], "passive": neutrals["passive"], "passive_light": neutrals["passive_light"],
    }


def _de(a: str, b: str) -> float:
    """CIEDE2000 between two #RRGGBB colours (self-contained so the Editor does not depend on tools/)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("palette_metrics", ROOT / "tools" / "palette_metrics.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.de2000(a, b)


SUPPORT_MIN_DE = 20.0       # design rule (CLAUDE.md "Support colours"): every support colour >= 20 CIEDE2000 from BOTH ends of the stage gradient


def support_errors(p: dict) -> list[str]:
    """Rule 1 (SEPARATION) for the support colours of a flat preset: board, plate, panel and plinth must not default to, or sit close to, the stage."""
    errs = []
    for key in ("support_board", "support_plate", "support_panel", "plinth"):
        for end in ("top", "bottom"):
            d = _de(p[key], p[end])
            if d < SUPPORT_MIN_DE:
                errs.append(f"{p['name']}.{key} {p[key]} is only dE {d:.1f} from the stage {end} {p[end]} (needs >= {SUPPORT_MIN_DE:g})")
    return errs


def apply_production_support(p: dict, scenes: dict | None) -> dict:
    """A production may carry its own support colours (chosen by the design lens, with the reasons in scenes.json `support_colours.reason`)."""
    sc = (scenes or {}).get("support_colours") or {}
    q = dict(p)
    for key, field in (("board", "support_board"), ("plate", "support_plate"), ("panel", "support_panel")):
        if sc.get(key):
            q[field] = sc[key]
    q["board"] = q["support_board"]
    return q


def presets(cfg: dict | None = None) -> dict:
    cfg = cfg or load()
    ident = cfg["identity"]
    return {k: _flat(k, v, ident["neutrals"]) for k, v in ident["presets"].items()}


def preset(name: str | None = None, cfg: dict | None = None) -> dict:
    cfg = cfg or load()
    return presets(cfg)[name or active_name(cfg)]


def render_config(cfg: dict | None = None) -> dict:
    return (cfg or load())["render"]


def visual_identity_block(name: str | None = None, cfg: dict | None = None) -> dict:
    """The `visual_identity` block a production embeds: colours come from the preset, the rest (lighting, materials, unify, qa) from the yaml."""
    cfg = cfg or load()
    p = preset(name, cfg)
    base = dict(cfg["visual_identity"])
    palette = [
        {"hex": p["top"], "name": "stage top"}, {"hex": p["bottom"], "name": "stage bottom"}, {"hex": p["plinth"], "name": "plinth"},
        {"hex": p["passive_dark"], "name": "passive dark grey"}, {"hex": p["passive"], "name": "passive grey"},
        {"hex": p["passive_light"], "name": "passive light grey"},
        {"hex": p["accent"], "name": "accent gold"}, {"hex": p["accent"], "name": "accent amber"},       # names the rigs look up: they hold the ACCENT
        {"hex": p["annot"], "name": "annotation teal"}, {"hex": p["error"], "name": "error red"},
    ]
    return {"background": {"hex": p["top"], "description": f"{p['title']} studio seamless: stage gradient {p['top']} to {p['bottom']}, plinth {p['plinth']}, soft contact shadow, no vignette"},
            "palette": palette, "lighting": base["lighting"], "materials": base["materials"], "unify": dict(base["unify"]),
            "qa_tolerance_de": base["qa_tolerance_de"], "text_theme": p["name"]}


def export_json(path: Path | None = None, name: str | None = None, production: Path | None = None) -> Path:
    """Snapshot for Blender. With `production`, that production's scenes.json `support_colours` override the preset's support colours."""
    cfg = load()
    out = Path(path or EXPORT)
    out.parent.mkdir(parents=True, exist_ok=True)
    P = presets(cfg)
    if production:
        scenes = json.loads((Path(production) / "scenes.json").read_text(encoding="utf-8"))
        P = {k: apply_production_support(v, scenes) for k, v in P.items()}
    out.write_text(json.dumps({"active": name or active_name(cfg), "presets": P, "render": render_config(cfg)}, indent=1), encoding="utf-8")
    return out


def apply_to_scenes(scenes_path: Path, name: str | None = None) -> None:
    """Embed the identity into a production's scenes.json (what a new production must carry; render_args select the look and the tuned stack)."""
    cfg = load()
    p = Path(scenes_path)
    d = json.loads(p.read_text(encoding="utf-8"))
    pr = preset(name, cfg)
    d["visual_identity"] = visual_identity_block(pr["name"], cfg)
    d["identity_preset"] = pr["name"]
    d["render_args"] = [f"look={pr['name']}"]
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    args = sys.argv[1:]
    name = args[args.index("--preset") + 1] if "--preset" in args else None
    if args and args[0] == "export":
        prod = args[args.index("--production") + 1] if "--production" in args else None
        pos = [a for a in args[1:] if not a.startswith("--") and a not in (name, prod)]
        print(export_json(Path(pos[0]) if pos else None, name, Path(prod) if prod else None))
    elif args and args[0] == "apply":
        apply_to_scenes(Path(args[1]), name)
        print("identity embedded in", args[1])
    else:
        cfg = load()
        print("active:", active_name(cfg))
        for k, v in presets(cfg).items():
            print(f"  {k:15s} stage {v['top']}->{v['bottom']}  plinth {v['plinth']}  accent {v['accent']}  subtitle {v['mode']}")
