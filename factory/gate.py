"""Composition gate as a HARD render block (CLAUDE.md "Support colours and composition gate").
  .venv/bin/python factory/gate.py run productions/<ch>/<video>     # renders the production's gate stills (mask=1, under caffeinate) and writes the record
  .venv/bin/python factory/gate.py stills productions/<ch>/<video> [scene ...]   # unmasked stills of each scene's key elements for blind naming (build/gate/likeness/sNN)
  .venv/bin/python factory/gate.py check productions/<ch>/<video> [scene]   # exit 1 unless a fresh PASS record exists (what the render driver calls)
  .venv/bin/python factory/gate.py check-colour productions/<ch>/<video>   # only the colour record (what the chain asks before re-rendering masked stills)
The production's scenes.json declares `gate_stills`: {"<scene id>": [frame, ...]} (representative frames). The record build/gate/gate.json holds the
verdict, the distance table (gate.md), the stills, and a fingerprint of everything that moves the in-frame colours (identity preset + support
colours + render scripts and rigs); changing any of them makes the record stale and the driver refuses a full render until the gate is re-run."""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(ROOT / "tools"))
import identity  # noqa: E402
import composition_gate  # noqa: E402
import asset_library  # noqa: E402
import blender_run  # noqa: E402

SAMPLES = 48


def fingerprint(prod: Path) -> str:
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    name = cfg.get("identity_preset") or identity.active_name()
    P = {k: identity.apply_production_support(v, cfg) for k, v in identity.presets().items()}
    h = hashlib.sha256()
    h.update(json.dumps(P[name], sort_keys=True).encode())
    h.update(json.dumps(cfg.get("gate_stills"), sort_keys=True).encode())
    prefix = cfg.get("scene_script_prefix", "scene")
    ids = sorted(int(k) for k in (cfg.get("gate_stills") or {}))
    libs = cfg.get("rig_libs") or {"tape": ["tape_rig"], "gear": ["tape_rig", "gear_rig"]}.get(prefix) or sorted(f.stem for f in (ROOT / "code3d" / "lib").glob("*.py"))
    libs = sorted(set(libs) | {"looks", "common", "composition", "pipeline_config"})        # the shared colour/composition core is always part of the fingerprint
    files = [ROOT / "code3d" / "scenes" / f"{prefix}_{n:02d}.py" for n in ids] + [ROOT / "code3d" / "lib" / f"{x}.py" for x in libs]
    for f in files:
        h.update(f.read_bytes())
    for slug in cfg.get("library_assets") or []:                                           # absent on older productions: their fingerprints do not change
        h.update(asset_library.fingerprint(slug).encode())
    return h.hexdigest()[:16]


def scene_fingerprint(prod: Path, sid: int) -> str:
    """What one scene's element records depend on: its scene script, the rig libraries, the scene's declared elements and the library assets."""
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    prefix = cfg.get("scene_script_prefix", "scene")
    h = hashlib.sha256()
    h.update(json.dumps((cfg.get("scene_elements") or {}).get(str(sid)), sort_keys=True).encode())
    libs = sorted(set(cfg.get("rig_libs") or sorted(f.stem for f in (ROOT / "code3d" / "lib").glob("*.py"))) | {"looks", "common", "composition", "pipeline_config"})
    for f in [ROOT / "code3d" / "scenes" / f"{prefix}_{int(sid):02d}.py"] + [ROOT / "code3d" / "lib" / f"{x}.py" for x in libs]:
        h.update(f.read_bytes())
    for slug in cfg.get("library_assets") or []:
        h.update(asset_library.fingerprint(slug).encode())
    h.update(json.dumps(cfg.get("hero_colours"), sort_keys=True).encode())
    return h.hexdigest()[:16]


def check_elements(prod: Path, scene: int | None = None) -> tuple[bool, str]:
    """EXTENDED LIKENESS GATE (owner rule 2026-11-05, docs/current/specs/asset-system.md "Every element"): the key represented element of EVERY scene must have been
    named correctly, blind, at the confidence floor, in that scene's own stills. Same teeth as the hero gate, but it blocks only the scene concerned.
    Active when scenes.json declares `scene_elements`: {"<scene id>": [{"id", "name", "aliases", "route", "source"}, ...]}. Earlier productions declare none."""
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    decl = cfg.get("scene_elements")
    if not decl:
        return True, "no scene_elements declared (production predates the every-element rule)"
    ids = [str(scene)] if scene is not None else [str(s["id"]) for s in cfg["scenes"]]
    missing_decl = [i for i in ids if not decl.get(i)]
    if missing_decl:
        return False, f"scene(s) {', '.join(missing_decl)} declare no key element in scene_elements; every scene needs at least one"
    rec_path = prod / "build" / "gate" / "elements.json"
    recs = json.loads(rec_path.read_text(encoding="utf-8")) if rec_path.exists() else {}
    for i in ids:
        fp = scene_fingerprint(prod, int(i))
        for el in decl[i]:
            r = recs.get(f"{i}:{el['id']}")
            if not r:
                return False, f"scene {i}: no blind-naming record for element '{el['id']}'; run: .venv/bin/python factory/asset_library.py element {prod} {i} {el['id']} --guess ... --confidence ..."
            if r.get("fingerprint") != fp:
                return False, f"scene {i}: element '{el['id']}' record is STALE (scene script, rig, colours or asset changed); repeat the blind naming"
            if not r.get("pass"):
                return False, f"scene {i}: element '{el['id']}' FAILED blind naming (guesses: {r.get('guesses')}, confidences: {r.get('confidences')}); fix the element, not the threshold"
    return True, "every declared scene element passed blind naming"


def check_colour(prod: Path) -> tuple[bool, str]:
    """Only the colour record: what decides whether the masked stills must be re-rendered."""
    rec = prod / "build" / "gate" / "gate.json"
    if not rec.exists():
        return False, f"no gate record ({rec.relative_to(prod)}); run: .venv/bin/python factory/gate.py run {prod}"
    r = json.loads(rec.read_text())
    if r.get("fingerprint") != fingerprint(prod):
        return False, "gate record is STALE (identity, support colours, scripts or rigs changed since it passed); re-run the gate"
    if not r.get("pass"):
        return False, "gate record says BLOCKED; fix the colours and re-run the gate (see build/gate/gate.md)"
    return True, "colour gate PASS on file"


def check(prod: Path, scene: int | None = None) -> tuple[bool, str]:
    ok, msg = check_colour(prod)
    if not ok:
        return ok, msg
    ok, msg = check_hero(prod)
    if not ok:
        return ok, msg
    return check_elements(prod, scene)


def check_hero(prod: Path) -> tuple[bool, str]:
    """Colour passing never meant the object looks like itself (the 006-011 batch passed this gate and was rejected for likeness). Productions that declare
    hero_route must also have a ready library asset and a fresh passing likeness record (docs/current/specs/asset-system.md). Older productions declare none."""
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    if not cfg.get("hero_route"):
        return True, "gate PASS on file"
    for slug in cfg.get("library_assets") or []:
        status = asset_library.read_meta(slug)["status"] if (asset_library.asset_dir(slug) / "asset.json").exists() else "missing"
        if status != "ready":
            return False, f"library asset {slug} is {status}, not ready; finish its asset job first"
    rec = prod / "build" / "gate" / "likeness.json"
    if not rec.exists():
        return False, f"no likeness record; blind-name the hero in the gate stills: .venv/bin/python factory/asset_library.py blind-pack, then likeness {prod} <slug>"
    r = json.loads(rec.read_text(encoding="utf-8"))
    if r.get("fingerprint") != fingerprint(prod):
        return False, "likeness record is STALE (the stills, rig or asset changed since it passed); repeat the blind naming"
    if not r.get("pass"):
        return False, f"likeness FAILED, the hero does not read as itself (guesses: {r.get('guesses')}); fix the hero, not the threshold"
    return True, "gate PASS and likeness PASS on file"


def run(prod: Path) -> int:
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    stills = cfg.get("gate_stills")
    if not stills:
        sys.exit("ERROR: scenes.json has no gate_stills ({scene id: [frames]})")
    name = cfg.get("identity_preset") or identity.active_name()
    gdir = prod / "build" / "gate"
    exp = identity.export_json(gdir / "identity-export.json", production=prod)
    prefix = cfg.get("scene_script_prefix", "scene")
    extra = [a for a in cfg.get("render_args", [])] + [f"identity={exp}"]
    if not any(a.startswith("look=") for a in extra):
        extra.append(f"look={name}")
    md, blocked = [], False
    ident = json.loads(Path(exp).read_text())
    preset = ident["presets"][name]
    for sid, frames in sorted(stills.items(), key=lambda kv: int(kv[0])):
        out = gdir / f"s{int(sid):02d}"
        for _attempt in (1, 2):          # one retry: a still can fail transiently while another render holds the GPU (seen twice, 2026-11-04)
            blender_run.blender(["-b", "--python", str(ROOT / "code3d" / "scenes" / f"{prefix}_{int(sid):02d}.py"), "--",
                            f"production={prod}", "mode=final", f"samples={SAMPLES}", f"stills={','.join(str(f) for f in frames)}", "mask=1", f"out={out}", *extra],
                           capture_output=True, text=True)
            lines, b = composition_gate.gate(out, preset)
            if lines:
                break
        md += [f"\n## scene {sid}"] + lines
        blocked |= b or not lines
    verdict = "BLOCKED" if blocked else "PASS"
    (gdir / "gate.md").write_text(f"# Composition gate: {prod.name}, preset {name}, board {preset['support_board']} plate {preset['support_plate']} panel {preset['support_panel']}\n"
                                  + "\n".join(md) + f"\n\nGATE: {verdict}\n", encoding="utf-8")
    (gdir / "gate.json").write_text(json.dumps({"pass": not blocked, "preset": name, "fingerprint": fingerprint(prod), "stills": {k: v for k, v in stills.items()},
                                                "table": "build/gate/gate.md"}, indent=1))
    print(f"GATE {verdict}  (table: {gdir / 'gate.md'})")
    return 1 if blocked else 0


def stills(prod: Path, only: list[int]) -> int:
    """Unmasked renders of the frames that show each scene's key elements, for the blind-naming readers (the masked gate stills are flat colour masks)."""
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    decl = cfg.get("scene_elements") or {}
    name = cfg.get("identity_preset") or identity.active_name()
    gdir = prod / "build" / "gate"
    exp = identity.export_json(gdir / "identity-export.json", production=prod)
    prefix = cfg.get("scene_script_prefix", "scene")
    extra = [a for a in cfg.get("render_args", [])] + [f"identity={exp}"]
    if not any(a.startswith("look=") for a in extra):
        extra.append(f"look={name}")
    rc = 0
    for sid in sorted(int(k) for k in decl):
        if only and sid not in only:
            continue
        frames = sorted({f for el in decl[str(sid)] for f in (el.get("frames") or (cfg.get("gate_stills") or {}).get(str(sid)) or [])})
        out = gdir / "likeness" / f"s{sid:02d}"
        for _attempt in (1, 2):
            blender_run.blender(["-b", "--python", str(ROOT / "code3d" / "scenes" / f"{prefix}_{sid:02d}.py"), "--", f"production={prod}",
                            "mode=final", f"samples={SAMPLES}", f"stills={','.join(str(f) for f in frames)}", f"out={out}", *extra], capture_output=True, text=True)
            if list(out.glob("*.png")):
                break
        else:
            print(f"scene {sid}: NO STILLS rendered")
            rc = 1
        print(f"scene {sid}: {len(list(out.glob('*.png')))} stills in {out}")
    return rc


if __name__ == "__main__":
    cmd, p = sys.argv[1], Path(sys.argv[2]).resolve()
    if cmd == "run":
        sys.exit(run(p))
    if cmd == "stills":
        sys.exit(stills(p, [int(x) for x in sys.argv[3:]]))
    ok, msg = check_colour(p) if cmd == "check-colour" else check(p, int(sys.argv[3]) if len(sys.argv) > 3 else None)
    print(msg)
    sys.exit(0 if ok else 1)
