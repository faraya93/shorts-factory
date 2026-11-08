"""Composition gate as a HARD render block (CLAUDE.md "Support colours and composition gate").
  .venv/bin/python factory/gate.py run productions/<ch>/<video>     # renders the production's gate stills (mask=1, under caffeinate) and writes the record
  .venv/bin/python factory/gate.py stills productions/<ch>/<video> [scene ...]   # unmasked stills of each scene's key elements for blind naming (build/gate/likeness/sNN)
  .venv/bin/python factory/gate.py freeze|unfreeze <prod> [reason]   # v2 freeze point after the hero passes; a later change is an explicit, logged unfreeze
  .venv/bin/python factory/gate.py carry <prod> [scene ...]   # v2: stale records whose re-rendered stills match what the readers saw keep their reading
  .venv/bin/python factory/gate.py check productions/<ch>/<video> [scene]   # exit 1 unless a fresh PASS record exists (what the render driver calls)
  .venv/bin/python factory/gate.py check-colour productions/<ch>/<video>   # only the colour record (what the chain asks before re-rendering masked stills)
The production's scenes.json declares `gate_stills`: {"<scene id>": [frame, ...]} (representative frames). The record build/gate/gate.json holds the
verdict, the distance table (gate.md), the stills, and a fingerprint of everything that moves the in-frame colours (identity preset + support
colours + render scripts and rigs); changing any of them makes the record stale and the driver refuses a full render until the gate is re-run."""
import hashlib
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(ROOT / "tools"))
import identity  # noqa: E402
import composition_gate  # noqa: E402
import asset_library  # noqa: E402
import blender_run  # noqa: E402
import gate_deps  # noqa: E402

SAMPLES = 48
STILL_POLICY = {"engine": "CYCLES", "res": 50, "samples": SAMPLES}           # v2 tier 2 (readers + colour): half-resolution Cycles with the GPU denoiser, the final engine; part of every v2 fingerprint
CARRY_THRESHOLD = 1e-4                                                       # mean absolute pixel difference (0..1): at or below it a re-rendered still IS the still the readers saw
EXT = re.compile(rb"[ \t]*# SF-EXT-BEGIN.*?# SF-EXT-END[^\n]*\n", re.S)      # additive profile keys in hashed libs (inert for earlier profiles): v1 records stay fresh


def _bytes(f: Path) -> bytes:
    return EXT.sub(b"", f.read_bytes())


def _cfg(prod: Path) -> dict:
    return json.loads((prod / "scenes.json").read_text(encoding="utf-8"))


def v2(prod: Path) -> bool:
    """Productions from 012 on declare gate_version 2: element-scoped fingerprints, isolated readers, hero first. Earlier records keep the rules they were made under."""
    return _cfg(prod).get("gate_version") == 2


def _preset_digest(prod: Path, cfg: dict) -> str:
    name = cfg.get("identity_preset") or identity.active_name()
    return json.dumps(identity.apply_production_support(identity.presets()[name], cfg), sort_keys=True)


def _script(cfg: dict, sid: int) -> Path:
    return ROOT / "code3d" / "scenes" / f"{cfg.get('scene_script_prefix', 'scene')}_{int(sid):02d}.py"


def _scene_dep_digest(prod: Path, cfg: dict, sid: int) -> tuple[str, str]:
    """Normalized script + the library code it reaches (+ the production list when the walk met something dynamic). Returns (digest, text searched for asset slugs)."""
    gate_deps.fresh()
    script = _script(cfg, sid)
    want, dyn = gate_deps.closure(script)
    if dyn:
        want.update({x: None for x in (cfg.get("rig_libs") or [])})
    src = script.read_text(encoding="utf-8")
    text = src + "".join((gate_deps.LIB / f"{m}.py").read_text(encoding="utf-8") for m in want)
    return hashlib.sha256((gate_deps.normalized(script) + gate_deps.lib_digest(want)).encode()).hexdigest(), text


def _assets_for(cfg: dict, text: str, extra: str) -> list[str]:
    slugs = cfg.get("library_assets") or []
    hay = text + extra
    hit = [s for s in slugs if s in hay or s.replace("-", "_") in hay]
    return hit if hit else slugs                                             # nothing named it: something loads it dynamically, so every asset counts


def hero_fingerprint(prod: Path) -> str:
    """v2: the hero's asset(s) + the hero rig functions + hero colours + identity + still policy. A camera file of some other scene is not part of what the hero looks like."""
    cfg = _cfg(prod)
    h = hashlib.sha256(json.dumps([cfg.get("hero_colours"), STILL_POLICY, _preset_digest(prod, cfg)], sort_keys=True).encode())
    gate_deps.fresh()
    want: dict = {}
    for ref in cfg.get("hero_rig") or []:                                    # "module" or "module.name"
        mod, _, name = ref.partition(".")
        if not name or want.get(mod, set()) is None:
            want[mod] = None
        else:
            want.setdefault(mod, set()).add(name)
    if want:
        h.update(gate_deps.lib_digest(want).encode())
    for slug in cfg.get("library_assets") or []:
        h.update(asset_library.fingerprint(slug).encode())
    return h.hexdigest()[:16]


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def same_pixels(a: Path, b: Path, threshold: float = CARRY_THRESHOLD) -> bool:
    from PIL import Image, ImageChops, ImageStat
    x, y = Image.open(a).convert("RGB"), Image.open(b).convert("RGB")
    if x.size != y.size:
        return False
    return sum(ImageStat.Stat(ImageChops.difference(x, y)).mean) / 3 / 255 <= threshold


def _read_ok(prod: Path, rec: dict) -> tuple[bool, str]:
    """The stills the readers judged must still be what the current stills show."""
    for src, saved in (rec.get("read_stills") or {}).items():
        cur, kept = prod / src, prod / saved
        if not cur.exists() or not kept.exists():
            return False, f"the still the readers saw is gone ({src})"
        if _sha(cur) != _sha(kept) and not same_pixels(cur, kept):
            return False, f"{src} no longer matches what the readers saw"
    return True, ""


def fingerprint(prod: Path) -> str:
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    if cfg.get("gate_version") == 2:
        h = hashlib.sha256(json.dumps([_preset_digest(prod, cfg), cfg.get("gate_stills"), STILL_POLICY], sort_keys=True).encode())
        for sid in sorted(int(k) for k in (cfg.get("gate_stills") or {})):
            d, text = _scene_dep_digest(prod, cfg, sid)
            h.update(d.encode())
            for slug in _assets_for(cfg, text, ""):
                h.update(asset_library.fingerprint(slug).encode())
        return h.hexdigest()[:16]
    name = cfg.get("identity_preset") or identity.active_name()
    P = {k: identity.apply_production_support(v, cfg) for k, v in identity.presets().items()}
    h = hashlib.sha256()
    h.update(json.dumps(P[name], sort_keys=True).encode())
    h.update(json.dumps(cfg.get("gate_stills"), sort_keys=True).encode())
    prefix = cfg.get("scene_script_prefix", "scene")
    ids = sorted(int(k) for k in (cfg.get("gate_stills") or {}))
    libs = cfg.get("rig_libs") or {"tape": ["tape_rig"], "gear": ["tape_rig", "gear_rig"]}.get(prefix) or sorted(f.stem for f in (ROOT / "code3d" / "lib").glob("*.py") if f.stem != "cheap_kit")
    libs = sorted(set(libs) | {"looks", "common", "composition", "pipeline_config"})        # the shared colour/composition core is always part of the fingerprint
    files = [ROOT / "code3d" / "scenes" / f"{prefix}_{n:02d}.py" for n in ids] + [ROOT / "code3d" / "lib" / f"{x}.py" for x in libs]
    for f in files:
        h.update(_bytes(f))
    for slug in cfg.get("library_assets") or []:                                           # absent on older productions: their fingerprints do not change
        h.update(asset_library.fingerprint(slug).encode())
    return h.hexdigest()[:16]


def scene_fingerprint(prod: Path, sid: int) -> str:
    """What one scene's element records depend on: its scene script, the rig libraries, the scene's declared elements and the library assets."""
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    if cfg.get("gate_version") == 2:
        decl = (cfg.get("scene_elements") or {}).get(str(sid))
        d, text = _scene_dep_digest(prod, cfg, sid)
        h = hashlib.sha256(json.dumps([decl, cfg.get("hero_colours"), STILL_POLICY, _preset_digest(prod, cfg)], sort_keys=True).encode())
        h.update(d.encode())
        for slug in _assets_for(cfg, text, json.dumps(decl)):
            h.update(asset_library.fingerprint(slug).encode())
        return h.hexdigest()[:16]
    prefix = cfg.get("scene_script_prefix", "scene")
    h = hashlib.sha256()
    h.update(json.dumps((cfg.get("scene_elements") or {}).get(str(sid)), sort_keys=True).encode())
    libs = sorted(set(cfg.get("rig_libs") or sorted(f.stem for f in (ROOT / "code3d" / "lib").glob("*.py") if f.stem != "cheap_kit")) | {"looks", "common", "composition", "pipeline_config"})
    for f in [ROOT / "code3d" / "scenes" / f"{prefix}_{int(sid):02d}.py"] + [ROOT / "code3d" / "lib" / f"{x}.py" for x in libs]:
        h.update(_bytes(f))
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
            if cfg.get("gate_version") == 2:
                if r.get("reader_isolation") != "headless":
                    return False, f"scene {i}: element '{el['id']}' was not read by isolated readers; use tools/blind_read.py"
                ok, why = _read_ok(prod, r)
                if not ok:
                    return False, f"scene {i}: element '{el['id']}' record is STALE: {why}"
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
    if cfg.get("gate_version") == 2:
        if r.get("fingerprint") != hero_fingerprint(prod):
            return False, "likeness record is STALE (the hero asset, hero rig, hero colours or identity changed since it passed); repeat the blind naming"
        if r.get("reader_isolation") != "headless":
            return False, "the hero was not read by isolated readers; use tools/blind_read.py"
        ok, why = _read_ok(prod, r)
        if not ok:
            return False, f"likeness record is STALE: {why}"
    elif r.get("fingerprint") != fingerprint(prod):
        return False, "likeness record is STALE (the stills, rig or asset changed since it passed); repeat the blind naming"
    if not r.get("pass"):
        return False, f"likeness FAILED, the hero does not read as itself (guesses: {r.get('guesses')}); fix the hero, not the threshold"
    return True, "gate PASS and likeness PASS on file"


def _res_arg(cfg: dict) -> list[str]:
    return [f"res={STILL_POLICY['res']}"] if cfg.get("gate_version") == 2 else []


def frozen(prod: Path) -> bool:
    return (prod / "build" / "gate" / "freeze.json").exists() and json.loads((prod / "build" / "gate" / "freeze.json").read_text()).get("hero_fp") == hero_fingerprint(prod)


def freeze(prod: Path) -> int:
    """Freeze point: the hero (and the elements shared by two or more scenes) passed before any other scene's stills are read."""
    ok, msg = check_hero(prod)
    if not ok:
        print(f"NOT FROZEN: {msg}")
        return 1
    decl, seen = _cfg(prod).get("scene_elements") or {}, {}
    for sid, els in decl.items():
        for e in els:
            seen.setdefault(e["id"], []).append(sid)
    shared = sorted(k for k, v in seen.items() if len(v) > 1)
    (prod / "build" / "gate" / "freeze.json").write_text(json.dumps({"date": date.today().isoformat(), "hero_fp": hero_fingerprint(prod), "shared_elements": shared}, indent=1))
    print(f"FROZEN: hero and shared elements {shared}")
    return 0


def unfreeze(prod: Path, reason: str) -> int:
    """A frozen item changes: explicit, logged in notes.md; every dependent scene is re-read because its fingerprint moved."""
    (prod / "build" / "gate" / "freeze.json").unlink(missing_ok=True)
    with (prod / "notes.md").open("a", encoding="utf-8") as f:
        f.write(f"\n- UNFREEZE {date.today().isoformat()}: {reason}\n")
    print("unfrozen, logged in notes.md")
    return 0


def carry(prod: Path, only: list[int]) -> int:
    """Automatic carry-over: a stale element whose freshly re-rendered stills match, within CARRY_THRESHOLD, the stills its readers saw keeps its reading, stamped. Readers are never re-rolled by this."""
    p = prod / "build" / "gate" / "elements.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    n = 0
    for key, r in data.items():
        sid = int(key.split(":")[0])
        if (only and sid not in only) or r.get("fingerprint") == scene_fingerprint(prod, sid) or not r.get("read_stills") or not r.get("pass"):
            continue
        if all((prod / s).exists() and (prod / k).exists() and same_pixels(prod / s, prod / k) for s, k in r["read_stills"].items()):
            r["fingerprint"], r["carried_over"] = scene_fingerprint(prod, sid), date.today().isoformat()
            n += 1
            print(f"carried over {key}")
        else:
            print(f"{key}: stills differ, needs a new reading")
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


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
                            f"production={prod}", "mode=final", f"samples={SAMPLES}", f"stills={','.join(str(f) for f in frames)}", "mask=1", f"out={out}", *extra, *_res_arg(cfg)],
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
    colour_fresh = cfg.get("gate_version") == 2 and check_colour(prod)[0]
    for sid in sorted(int(k) for k in decl):
        if only and sid not in only:
            continue
        if cfg.get("gate_version") == 2 and sid != (cfg.get("hero_still") or {}).get("scene") and not frozen(prod):
            print(f"scene {sid}: REFUSED, the hero is not frozen yet. Pass the hero first (scene {(cfg.get('hero_still') or {}).get('scene')}), then: gate.py freeze")
            rc = 1
            continue
        frames = sorted({f for el in decl[str(sid)] for f in (el.get("frames") or (cfg.get("gate_stills") or {}).get(str(sid)) or [])})
        out = gdir / "likeness" / f"s{sid:02d}"
        if colour_fresh:                                                     # 2.4: one render serves both still sets; the colour run already rendered these beauty frames
            out.mkdir(parents=True, exist_ok=True)
            rest = []
            for f in frames:
                src = gdir / f"s{sid:02d}" / f"still-{f:04d}.png"
                if src.exists():
                    shutil.copyfile(src, out / src.name)
                else:
                    rest.append(f)
            if not rest:
                print(f"scene {sid}: {len(frames)} stills reused from the colour run in {out}")
                continue
            frames = rest
        for _attempt in (1, 2):
            blender_run.blender(["-b", "--python", str(ROOT / "code3d" / "scenes" / f"{prefix}_{sid:02d}.py"), "--", f"production={prod}",
                            "mode=final", f"samples={SAMPLES}", f"stills={','.join(str(f) for f in frames)}", f"out={out}", *extra, *_res_arg(cfg)], capture_output=True, text=True)
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
    if cmd == "freeze":
        sys.exit(freeze(p))
    if cmd == "unfreeze":
        sys.exit(unfreeze(p, " ".join(sys.argv[3:]) or "no reason given"))
    if cmd == "carry":
        sys.exit(carry(p, [int(x) for x in sys.argv[3:]]))
    ok, msg = check_colour(p) if cmd == "check-colour" else check(p, int(sys.argv[3]) if len(sys.argv) > 3 else None)
    print(msg)
    sys.exit(0 if ok else 1)
