"""Factory -> orchestrator contract: the PUBLISH PACKAGE of one production, in a known place (the production folder root):
    final.mp4, cover.jpg, publish.json {channel, title, description, music_credit, hashtags, video, cover}
`build` reads the notes.md "Publish package" section + scenes.json (channel, audio.music_credit) and writes publish.json; `check` validates it.
The factory never holds platform credentials and never publishes: the orchestrator reads this package and the owner approves each video.
    .venv/bin/python tools/publish_package.py build|check productions/<channel>/<NNN-slug>"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from factory import channel as channel_cfg  # noqa: E402

REQUIRED = ("channel", "title", "description", "hashtags", "video", "cover")


def _section(notes: str) -> str:
    m = re.search(r"## Publish package[^\n]*\n(.*?)(?=\n## )", notes, re.S)
    if not m:
        raise SystemExit("notes.md has no '## Publish package' section")
    return m.group(1)


def build(prod: Path) -> dict:
    sec = _section((prod / "notes.md").read_text(encoding="utf-8"))
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    title = re.search(r"\*\*Título:\*\*\s*(.+)", sec).group(1).strip()
    tags = re.search(r"\*\*Hashtags[^*]*\*\*\s*(.+)", sec).group(1)
    desc = re.search(r"\*\*Descripción:\*\*\s*(.*?)(?=\n- \*\*Hashtags)", sec, re.S).group(1)
    lines = [ln.strip() for ln in desc.splitlines() if ln.strip() and not ln.strip().startswith("Música:")]
    pkg = {"channel": cfg.get("channel"), "title": title, "description": "\n".join(lines).replace("**", ""),
           "music_credit": (cfg.get("audio") or {}).get("music_credit"), "hashtags": re.findall(r"#\w+", tags), "video": "final.mp4", "cover": "cover.jpg"}
    (prod / "publish.json").write_text(json.dumps(pkg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return pkg


def hashtag_errors(tags: list[str], channel_id: str, family: str) -> list[str]:
    """The channel's hashtag policy (brand.yaml publish.hashtags + the variant's base/family tags): 3-5 tags, topical first,
    then the topic-family tag, then the fixed base LAST; no duplicates."""
    conf = channel_cfg.load(channel_id)["publish"]
    rule, base, fam = conf["hashtags"], conf["hashtags"]["base"], conf["hashtags"]["family"].get(family)
    low = [t.lower() for t in tags]
    errs = [f"hashtag {t!r} is not a single #word" for t in tags if not re.fullmatch(r"#\w+", t)]
    if not rule["min"] <= len(tags) <= rule["max"]:
        errs.append(f"hashtags: {len(tags)} tags, policy is {rule['min']}-{rule['max']}")
    if len(set(low)) != len(low):
        errs.append("hashtags: duplicates")
    if [t.lower() for t in base] != low[len(low) - len(base):]:
        errs.append(f"hashtags: the fixed base {base} must come last")
    if fam is None or fam.lower() not in low:
        errs.append(f"hashtags: the {family} family tag {fam} is missing")
    if low and (low[0] in [b.lower() for b in base] or low[0] == (fam or "").lower()):
        errs.append("hashtags: the first slot must be topical (the object or mechanism), not the base or family tag")
    return errs


def check(prod: Path) -> list[str]:
    f = prod / "publish.json"
    if not f.exists():
        return ["no publish.json"]
    pkg = json.loads(f.read_text(encoding="utf-8"))
    errs = [f"missing {k}" for k in REQUIRED if not pkg.get(k)]
    if pkg.get("title") and len(re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", pkg["title"])) != 1:
        errs.append("title must carry exactly ONE trailing emoji")
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    if (cfg.get("audio") or {}).get("music_credit") and pkg.get("music_credit") != cfg["audio"]["music_credit"]:
        errs.append("music_credit differs from scenes.json audio.music_credit (a music credit still applies if a credited track is ever approved)")
    if re.search(r"\blicencia\b|\bCC[ -]?(BY|0|Attribution)\b|Sketchfab|\bModelo 3D\b", pkg.get("description") or "", re.I):
        errs.append("description carries an asset credit; attribution credits never go in descriptions (owner 2026-11-07)")
    errs += hashtag_errors(pkg.get("hashtags") or [], pkg["channel"], cfg["topic_family"])
    return errs


if __name__ == "__main__":
    cmd, prod = sys.argv[1], Path(sys.argv[2])
    if cmd == "build":
        print(json.dumps(build(prod), ensure_ascii=False, indent=2))
    errs = check(prod)
    print("OK" if not errs else "\n".join(errs))
    sys.exit(1 if errs else 0)
