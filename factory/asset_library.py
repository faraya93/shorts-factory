#!/usr/bin/env python3
"""The factory asset library: every hero object, stored once, reused forever (docs/current/specs/asset-system.md).

    .venv/bin/python factory/asset_library.py find <words>                 is this object already solved? (no words: list everything)
    .venv/bin/python factory/asset_library.py new <slug> --name "..." --alias a --alias b --family objects
    .venv/bin/python factory/asset_library.py seal <slug>                  hash the .blend, rewrite the README, validate
    .venv/bin/python factory/asset_library.py check [slug]                 validate one asset or the whole library
    .venv/bin/python factory/asset_library.py blind-pack <still> [...]     copy stills to a neutral folder and print the blind-naming prompt
    .venv/bin/python factory/asset_library.py blind <slug> --guess "..." --confidence 80 --guess "..." --confidence 75     record the asset's blind naming
    .venv/bin/python factory/asset_library.py likeness <production> <slug> --guess "..." --confidence 80 --guess "..." --confidence 75     same, for the production's own stills
    .venv/bin/python factory/asset_library.py use <slug> <production>      record a production that used the asset

Inside Blender (no third-party imports at module level, so this file also loads under Blender's Python):
    import asset_library as al
    al.save_collection("heart", "asset")     # MCP session: packs textures and writes assets/library/heart/heart.blend
    hero = al.load_hero("heart")             # scene script: appends the asset's collection into the scene

Binaries are gitignored (media); asset.json, README.md, build.py and job/report.md are committed.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIBRARY = Path(os.environ.get("ASSET_LIBRARY") or ROOT / "assets" / "library")
REGISTRY = ROOT / "assets" / "registry.yaml"
SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ROUTES = {"library", "generator", "modelled", "code-primitive"}
STATUSES = {"in_progress", "ready", "rejected"}
FAMILIES = {"objects", "body", "numbers", "whatif"}
MIN_BLIND_GUESSES = 2
MIN_BLIND_CONFIDENCE = 60

# The global licence rule. Anything not listed here is unclear, and unclear is not used.
LICENCES = {
    "CC0-1.0": {},
    "own-work": {},                                # built in this factory (scripted, sculpted); no third-party source
    "Royalty-Free": {"needs_url": True},           # a named platform licence: the url of its terms is recorded
    "CC-BY-4.0": {"needs_attribution": True},
    "CC-BY-3.0": {"needs_attribution": True},
    "AGPL-3.0": {"needs_decision": True},          # MB-Lab output: see its registry note; each use needs a recorded lens decision
}


def asset_dir(slug: str) -> Path:
    return LIBRARY / slug


def read_meta(slug: str) -> dict:
    return json.loads((asset_dir(slug) / "asset.json").read_text(encoding="utf-8"))


def write_meta(meta: dict) -> None:
    (asset_dir(meta["slug"]) / "asset.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slugs() -> list[str]:
    return sorted(p.parent.name for p in LIBRARY.glob("*/asset.json")) if LIBRARY.exists() else []


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(text: str) -> str:
    """Lowercase without Spanish accents, so "corazón" matches "corazon"."""
    table = str.maketrans("áéíóúüñ", "aeiouun")
    return text.casefold().translate(table).strip()


def source_ids() -> set[str]:
    import yaml                                     # not available under Blender's Python; the registry is only read from the venv
    return {s["id"] for s in yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))["sources"]}


def find(words: str = "") -> list[dict]:
    q = norm(words)
    terms = q.split()
    hits = []
    for slug in slugs():
        m = read_meta(slug)
        names = [norm(x) for x in [m["slug"], m.get("name", "")] + list(m.get("aliases", []))]
        blob = " ".join(names)
        if all(t in blob for t in terms):
            hits.append(m)
    return hits


def new(slug: str, name: str, aliases: list[str], family: str) -> Path:
    if not SLUG.match(slug):
        raise SystemExit("slug: lowercase ascii words joined by '-', e.g. human-heart")
    if family not in FAMILIES:
        raise SystemExit(f"family must be one of {sorted(FAMILIES)}")
    if not aliases:
        raise SystemExit("give at least one --alias: the names a viewer would use for this object (blind naming is checked against them)")
    d = asset_dir(slug)
    if d.exists():
        raise SystemExit(f"{slug} already exists: reuse or update it, never solve the same object twice")
    for alias in [name] + aliases:
        for hit in find(alias):
            raise SystemExit(f"'{alias}' already matches library asset '{hit['slug']}' (status {hit['status']}): reuse or update it")
    (d / "job" / "stills").mkdir(parents=True)
    meta = {
        "slug": slug, "name": name, "aliases": aliases, "family": family, "created": date.today().isoformat(), "status": "in_progress",
        "route": None,
        "brief": {"must_read_as": "", "seen_at": "", "moving_parts": [], "states": [], "style_notes": ""},
        "source": {"registry_id": None, "url": None, "asset_id": None, "author": None, "retrieved": None},
        "licence": {"id": None, "url": None, "attribution": None, "note": None, "decision": None},
        "files": {"blend": f"{slug}.blend", "sha256": None, "collection": "asset", "rig_module": None, "build_script": None},
        "real_size_m": None,
        "checks": {"qa": {"pass": None, "date": None}, "blind_naming": {"pass": None, "date": None, "guesses": []}, "fidelity": None},
        "owner_verdict": "pending",
        "rejected_candidates": [],
        "productions": [],
    }
    write_meta(meta)
    (d / "job" / "report.md").write_text(
        f"# Asset job: {name} ({slug})\n\nStarted {meta['created']}.\n\n## Brief\n\n## Sources searched (query, result, why taken or refused)\n\n"
        "## Steps and visual checks\n\n## Checks (QA, blind naming, fidelity)\n\n## Wall time, spend ($0 expected), anything skipped\n", encoding="utf-8")
    write_readme(meta)
    return d


NOTES_MARKER = "## Notes"


def write_readme(meta: dict) -> None:
    path = asset_dir(meta["slug"]) / "README.md"
    notes = ""
    if path.exists() and NOTES_MARKER in (old := path.read_text(encoding="utf-8")):
        notes = old.split(NOTES_MARKER, 1)[1].strip()
    src, lic, chk = meta["source"], meta["licence"], meta["checks"]
    lines = [
        f"# {meta['name']} (`{meta['slug']}`)", "",
        "Generated from `asset.json` by `factory/asset_library.py`; edit `asset.json` and run `seal`. Only the Notes section below is hand-written.", "",
        f"- **Status:** {meta['status']}",
        f"- **Route:** {meta['route']}",
        f"- **Source:** {src.get('registry_id')}, {src.get('url')} (asset {src.get('asset_id')}, by {src.get('author')})",
        f"- **Licence:** {lic.get('id')} {lic.get('url') or ''}".rstrip(),
        f"- **Attribution required:** {lic.get('attribution') or 'none'}",
        f"- **Date retrieved or built:** {src.get('retrieved') or meta['created']}",
        f"- **Productions that used it:** {', '.join(meta['productions']) or 'none yet'}",
        f"- **Reads as:** {', '.join(meta['aliases'])}",
        f"- **Checks:** QA {chk['qa']['pass']}; blind naming {chk['blind_naming']['pass']} ({'; '.join(chk['blind_naming']['guesses']) or 'no guesses yet'}); owner verdict {meta['owner_verdict']}",
        f"- **Job record:** `job/report.md`; stills in `job/stills/` (local, gitignored)",
        "", NOTES_MARKER, "", notes, "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def validate(slug: str, known_sources: set[str] | None = None) -> tuple[list[str], list[str]]:
    """Returns (errors, warnings). An in_progress or rejected asset only has to be well formed; a ready one must satisfy everything."""
    e: list[str] = []
    w: list[str] = []
    try:
        m = read_meta(slug)
    except (OSError, ValueError) as x:
        return [f"{slug}: unreadable asset.json ({x})"], []
    if m.get("slug") != slug or not SLUG.match(slug):
        e.append(f"{slug}: slug does not match its folder")
    if m.get("status") not in STATUSES:
        e.append(f"{slug}: status must be one of {sorted(STATUSES)}")
    if m.get("route") is not None and m.get("route") not in ROUTES:
        e.append(f"{slug}: route must be one of {sorted(ROUTES)}")
    lic = m.get("licence") or {}
    lic_id = lic.get("id")
    if lic_id is not None and lic_id not in LICENCES:
        e.append(f"{slug}: licence '{lic_id}' is not allowed (allowed: {sorted(LICENCES)}); anything unclear is not used")
    if m.get("status") != "ready":
        return e, w

    rule = LICENCES.get(lic_id or "", None)
    if rule is None and lic_id is None:
        e.append(f"{slug}: a ready asset needs a licence")
    if rule:
        if rule.get("needs_attribution") and not lic.get("attribution"):
            e.append(f"{slug}: {lic_id} needs the attribution text in licence.attribution")
        if rule.get("needs_url") and not lic.get("url"):
            e.append(f"{slug}: {lic_id} needs the url of the licence terms")
        if rule.get("needs_decision") and not lic.get("decision"):
            e.append(f"{slug}: {lic_id} needs licence.decision pointing to its entry in docs/current/reports/lens-decisions.md")
    route = m.get("route")
    src = m.get("source") or {}
    if route is None:
        e.append(f"{slug}: a ready asset needs a route")
    if route in ("library", "generator"):
        for key in ("registry_id", "url", "author", "retrieved"):
            if not src.get(key):
                e.append(f"{slug}: route {route} needs source.{key}")
        if known_sources is not None and src.get("registry_id") and src["registry_id"] not in known_sources:
            e.append(f"{slug}: source '{src['registry_id']}' is not in assets/registry.yaml")
    if route in ("modelled", "code-primitive") and lic_id not in ("own-work", None):
        w.append(f"{slug}: route {route} normally carries licence own-work, found {lic_id}")
    files = m.get("files") or {}
    if route == "code-primitive":
        mod = files.get("rig_module")
        if not mod or not (ROOT / "code3d" / "lib" / f"{mod}.py").exists():
            e.append(f"{slug}: route code-primitive needs files.rig_module naming a code3d/lib module")
    elif route:
        blend = asset_dir(slug) / (files.get("blend") or "")
        if not files.get("sha256"):
            e.append(f"{slug}: not sealed (run: asset_library.py seal {slug})")
        elif not blend.is_file():
            w.append(f"{slug}: {blend.name} is not on this machine (binaries are gitignored); rebuild it from the recorded source or build.py")
        elif sha256(blend) != files["sha256"]:
            e.append(f"{slug}: {blend.name} changed since it was sealed; re-run the checks, then seal")
    chk = m.get("checks") or {}
    if (chk.get("qa") or {}).get("pass") is not True and route != "code-primitive":
        e.append(f"{slug}: a ready asset needs checks.qa.pass = true (blender-asset-qa)")
    if (chk.get("blind_naming") or {}).get("pass") is not True:
        e.append(f"{slug}: a ready asset needs a passing blind naming (asset_library.py blind)")
    if not (m.get("brief") or {}).get("must_read_as"):
        e.append(f"{slug}: brief.must_read_as is empty")
    readme = asset_dir(slug) / "README.md"
    if not readme.exists() or "**Licence:**" not in readme.read_text(encoding="utf-8"):
        e.append(f"{slug}: README.md missing or not generated (run seal)")
    # A CC-BY credit has to reach the viewer: the description of every published package that used the asset must carry it.
    if rule and rule.get("needs_attribution") and lic.get("attribution"):
        for prod in m.get("productions") or []:
            pub = ROOT / "productions" / prod / "publish.json"
            if pub.exists() and lic["attribution"] not in pub.read_text(encoding="utf-8"):
                e.append(f"{slug}: {prod}/publish.json does not carry the attribution '{lic['attribution']}'")
    return e, w


def seal(slug: str) -> None:
    m = read_meta(slug)
    if m.get("route") != "code-primitive":
        blend = asset_dir(slug) / m["files"]["blend"]
        if not blend.is_file():
            raise SystemExit(f"{blend} does not exist: save the asset first (al.save_collection in the MCP session)")
        m["files"]["sha256"] = sha256(blend)
    write_meta(m)
    write_readme(m)


def judge_guesses(aliases: list[str], guesses: list[str], confidences: list[int]) -> bool:
    """Pass only when at least MIN_BLIND_GUESSES independent first guesses each name the object by an alias AND each reader is at least MIN_BLIND_CONFIDENCE sure.
    The floor comes from the 2026-11-04 calibration (docs/current/reports/likeness-calibration.md): naming alone passed 008, carried by one strong frame."""
    patterns = [re.compile(rf"\b{re.escape(norm(a))}(s|es)?\b") for a in aliases]        # whole words: "ice" must not match "device", plurals count
    return (len(guesses) >= MIN_BLIND_GUESSES and len(confidences) == len(guesses)
            and all(any(p.search(norm(g)) for p in patterns) for g in guesses)
            and all(c >= MIN_BLIND_CONFIDENCE for c in confidences))


def blind_pack(stills: list[str]) -> tuple[Path, str]:
    """Neutral copies: a path or filename that names the object would spoil the test."""
    out = Path(tempfile.mkdtemp(prefix="blind-"))
    copies = []
    for i, s in enumerate(stills):
        p = Path(s)
        if not p.is_file():
            raise SystemExit(f"{s}: not a file")
        dst = out / f"view-{i + 1}{p.suffix.lower()}"
        shutil.copyfile(p, dst)
        copies.append(str(dst))
    prompt = ("Look at these images and name the single object they show, as a person scrolling past on a phone would. Answer with your first guess in one "
              "short noun phrase, then two alternatives, then a confidence from 0 to 100. If it does not resemble anything specific, say so plainly; do not "
              "try to be polite. Images: " + ", ".join(copies))
    return out, prompt


def record_blind(slug: str, guesses: list[str], confidences: list[int]) -> bool:
    m = read_meta(slug)
    ok = judge_guesses(m["aliases"], guesses, confidences)
    m["checks"]["blind_naming"] = {"pass": ok, "date": date.today().isoformat(), "guesses": guesses, "confidences": confidences}
    write_meta(m)
    write_readme(m)
    return ok


def record_likeness(production: Path, slug: str, guesses: list[str], confidences: list[int]) -> bool:
    """The production-side twin of the blind naming: the hero as it appears in this video's own stills, written next to the gate record."""
    sys.path.insert(0, str(ROOT / "factory"))
    import gate
    ok = judge_guesses(read_meta(slug)["aliases"], guesses, confidences)
    rec = production / "build" / "gate"
    rec.mkdir(parents=True, exist_ok=True)
    (rec / "likeness.json").write_text(json.dumps({"pass": ok, "date": date.today().isoformat(), "asset": slug, "guesses": guesses, "confidences": confidences,
                                                   "fingerprint": gate.fingerprint(production)}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return ok


def use(slug: str, production: str) -> None:
    prod = production.split("productions/", 1)[-1].strip("/")
    if not (ROOT / "productions" / prod).is_dir():
        raise SystemExit(f"no production at productions/{prod}")
    m = read_meta(slug)
    if m["status"] != "ready":
        raise SystemExit(f"{slug} is {m['status']}, not ready")
    if prod not in m["productions"]:
        m["productions"].append(prod)
    write_meta(m)
    write_readme(m)
    if m["licence"].get("attribution"):
        print(f"ATTRIBUTION REQUIRED in the description of {prod}: {m['licence']['attribution']}")


def fingerprint(slug: str) -> str:
    """What a production's gate record depends on: the asset's status and the exact file or rig."""
    m = read_meta(slug)
    return json.dumps({"status": m.get("status"), "sha": (m.get("files") or {}).get("sha256"), "rig": (m.get("files") or {}).get("rig_module")}, sort_keys=True)


# ---- inside Blender ----

def save_collection(slug: str, collection: str = "asset") -> Path:
    """Write ONE collection (and only what it uses) as the asset's .blend, textures packed so the file stands alone."""
    import bpy
    col = bpy.data.collections[collection]
    bpy.ops.file.pack_all()
    path = asset_dir(slug) / read_meta(slug)["files"]["blend"]
    bpy.data.libraries.write(str(path), {col}, fake_user=True, compress=True)
    # The check tools (QA, fidelity) only see meshes in a scene, but a Scene cannot go through libraries.write: Blender 5.2 segfaults copying it (found 2026-11-04).
    # So a separate background Blender links the collection into the saved file's own scene.
    link = f"import bpy; bpy.context.scene.collection.children.link(bpy.data.collections[{collection!r}]); bpy.ops.wm.save_mainfile(compress=True)"
    subprocess.run([bpy.app.binary_path, "-b", str(path), "--python-exit-code", "1", "--python-expr", link], check=True, capture_output=True)
    return path


def load_hero(slug: str, scene=None):
    """Append a ready asset's collection into the scene; refuses anything not ready or changed since it was sealed."""
    import bpy
    m = read_meta(slug)
    if m["status"] != "ready":
        raise RuntimeError(f"asset {slug} is {m['status']}, not ready")
    blend = asset_dir(slug) / m["files"]["blend"]
    if sha256(blend) != m["files"]["sha256"]:
        raise RuntimeError(f"asset {slug}: {blend.name} changed since it was sealed")
    with bpy.data.libraries.load(str(blend), link=False) as (src, dst):
        if m["files"]["collection"] not in src.collections:
            raise RuntimeError(f"asset {slug}: no collection '{m['files']['collection']}' in {blend.name}")
        dst.collections = [m["files"]["collection"]]
    col = dst.collections[0]
    (scene or bpy.context.scene).collection.children.link(col)
    return col


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("find"); p.add_argument("words", nargs="*")
    p = sub.add_parser("new"); p.add_argument("slug"); p.add_argument("--name", required=True); p.add_argument("--alias", action="append", default=[]); p.add_argument("--family", required=True)
    p = sub.add_parser("seal"); p.add_argument("slug")
    p = sub.add_parser("check"); p.add_argument("slug", nargs="?")
    p = sub.add_parser("blind-pack"); p.add_argument("stills", nargs="+")
    p = sub.add_parser("blind"); p.add_argument("slug"); p.add_argument("--guess", action="append", default=[]); p.add_argument("--confidence", action="append", type=int, default=[])
    p = sub.add_parser("likeness"); p.add_argument("production"); p.add_argument("slug"); p.add_argument("--guess", action="append", default=[]); p.add_argument("--confidence", action="append", type=int, default=[])
    p = sub.add_parser("use"); p.add_argument("slug"); p.add_argument("production")
    a = ap.parse_args()

    if a.cmd == "find":
        hits = find(" ".join(a.words))
        for m in hits:
            print(f"{m['slug']}  [{m['status']}]  route={m['route']}  licence={m['licence']['id']}  aliases={', '.join(m['aliases'])}")
        if not hits:
            print("no match in the library: run an asset job (docs/current/specs/asset-system.md)")
    elif a.cmd == "new":
        print(new(a.slug, a.name, a.alias, a.family))
    elif a.cmd in ("seal", "check"):
        if a.cmd == "seal":
            seal(a.slug)
        known = source_ids()
        errors, warnings = [], []
        for s in ([a.slug] if a.slug else slugs()):
            er, wa = validate(s, known)
            errors += er
            warnings += wa
        for x in warnings:
            print(f"WARNING {x}")
        for x in errors:
            print(f"ERROR {x}")
        print(f"{'FAIL' if errors else 'OK'}: {len(errors)} errors, {len(warnings)} warnings")
        return 1 if errors else 0
    elif a.cmd == "blind-pack":
        out, prompt = blind_pack(a.stills)
        print(f"Neutral stills in {out}. Give this prompt, with no other context, to at least {MIN_BLIND_GUESSES} separate fresh subagents:\n\n{prompt}")
    elif a.cmd == "blind":
        ok = record_blind(a.slug, a.guess, a.confidence)
        print("PASS" if ok else f"FAIL: needs {MIN_BLIND_GUESSES}+ first guesses that each contain an alias of {a.slug}, each with confidence >= {MIN_BLIND_CONFIDENCE}")
        return 0 if ok else 1
    elif a.cmd == "likeness":
        ok = record_likeness(Path(a.production), a.slug, a.guess, a.confidence)
        print("PASS" if ok else "FAIL: the hero does not read as itself in this production's stills; the final render stays blocked")
        return 0 if ok else 1
    elif a.cmd == "use":
        use(a.slug, a.production)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
