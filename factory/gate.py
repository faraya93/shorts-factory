"""Composition gate as a HARD render block (CLAUDE.md "Support colours and composition gate").
  .venv/bin/python factory/gate.py run productions/<ch>/<video>     # renders the production's gate stills (mask=1, under caffeinate) and writes the record
  .venv/bin/python factory/gate.py check productions/<ch>/<video>   # exit 1 unless a fresh PASS record exists (what the render driver calls)
The production's scenes.json declares `gate_stills`: {"<scene id>": [frame, ...]} (representative frames). The record build/gate/gate.json holds the
verdict, the distance table (gate.md), the stills, and a fingerprint of everything that moves the in-frame colours (identity preset + support
colours + render scripts and rigs); changing any of them makes the record stale and the driver refuses a full render until the gate is re-run."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(ROOT / "tools"))
import identity  # noqa: E402
import composition_gate  # noqa: E402

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
    return h.hexdigest()[:16]


def check(prod: Path) -> tuple[bool, str]:
    rec = prod / "build" / "gate" / "gate.json"
    if not rec.exists():
        return False, f"no gate record ({rec.relative_to(prod)}); run: .venv/bin/python factory/gate.py run {prod}"
    r = json.loads(rec.read_text())
    if r.get("fingerprint") != fingerprint(prod):
        return False, "gate record is STALE (identity, support colours, scripts or rigs changed since it passed); re-run the gate"
    if not r.get("pass"):
        return False, "gate record says BLOCKED; fix the colours and re-run the gate (see build/gate/gate.md)"
    return True, "gate PASS on file"


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
        subprocess.run(["caffeinate", "-dimsu", "blender", "-b", "--python", str(ROOT / "code3d" / "scenes" / f"{prefix}_{int(sid):02d}.py"), "--",
                        f"production={prod}", "mode=final", f"samples={SAMPLES}", f"stills={','.join(str(f) for f in frames)}", "mask=1", f"out={out}", *extra],
                       capture_output=True, text=True)
        lines, b = composition_gate.gate(out, preset)
        md += [f"\n## scene {sid}"] + lines
        blocked |= b or not lines
    verdict = "BLOCKED" if blocked else "PASS"
    (gdir / "gate.md").write_text(f"# Composition gate: {prod.name}, preset {name}, board {preset['support_board']} plate {preset['support_plate']} panel {preset['support_panel']}\n"
                                  + "\n".join(md) + f"\n\nGATE: {verdict}\n", encoding="utf-8")
    (gdir / "gate.json").write_text(json.dumps({"pass": not blocked, "preset": name, "fingerprint": fingerprint(prod), "stills": {k: v for k, v in stills.items()},
                                                "table": "build/gate/gate.md"}, indent=1))
    print(f"GATE {verdict}  (table: {gdir / 'gate.md'})")
    return 1 if blocked else 0


if __name__ == "__main__":
    cmd, p = sys.argv[1], Path(sys.argv[2]).resolve()
    if cmd == "run":
        sys.exit(run(p))
    ok, msg = check(p)
    print(msg)
    sys.exit(0 if ok else 1)
