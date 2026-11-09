"""VISIBILITY CHECK (owner finding 2026-11-08, 009 steam; design and thresholds: docs/current/specs/asset-system.md "Visibility check"). Measures how far each declared element actually moves the
rendered pixels against what sits behind it: the frame WITH the element against the SAME frame rendered WITHOUT it (the plate), at the final profile, in CIEDE2000. Never palette distance.
  .venv/bin/python tools/visibility_check.py --record <prod> [scene ...]          # renders frame + plate, measures in the isolated route, writes build/gate/visibility.json (the only way to make a record)
  .venv/bin/python tools/visibility_check.py --audit-final <prod> <scene> <objects> <frame> [...]   # the frames of final.mp4 itself against the plate (graded the same way, subtitles and overlays excluded)
  .venv/bin/python tools/visibility_check.py --calibrate <map.json> <out.json>    # a named set of scenes, no production record touched
scenes.json `visibility`: {"<scene id>": {"<element id>": {"objects": ["glob", ...], "frames": [n, ...]}}}. The measurement runs as a separate process in an empty folder on neutrally named copies (a.png, b.png),
the same isolation as tools/blind_read.py; gate.check refuses a record that did not come from here."""
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
GRID = (270, 480)                  # box-averaged: 4x4 at 1080p, which removes grain and render noise and is about what a phone resolves
FOOTPRINT_DE = 3.0                 # below this a pixel counts as unchanged (noise control: docs/current/reports/visibility-calibration/)
VISIBLE_DE = 10.0                  # CIEDE2000 of a difference a viewer sees at a glance, not one found by comparing
MIN_VISIBLE_AREA_PCT = 0.8         # frame area where the element reaches VISIBLE_DE (weakest strong element measured 1.06)
MIN_P90_DE = 17.0                  # 90th percentile of the difference inside the element's own footprint: midpoint of the measured gap (009 steam/plume at most 11.4, strong elements at least 23.2)
VERSION = 1
HOOK = f"exec(open({str(ROOT / 'tools' / 'visibility_hide_hook.py')!r}).read())"


def _lab(rgb, cache={}):
    v = cache.get(rgb)
    if v is None:
        lin = [(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4) for c in (x / 255 for x in rgb)]
        xyz = (0.4124564 * lin[0] + 0.3575761 * lin[1] + 0.1804375 * lin[2], 0.2126729 * lin[0] + 0.7151522 * lin[1] + 0.072175 * lin[2], 0.0193339 * lin[0] + 0.119192 * lin[1] + 0.9503041 * lin[2])
        f = [(t ** (1 / 3) if t > 216 / 24389 else (24389 / 27 * t + 16) / 116) for t in (xyz[0] / 0.95047, xyz[1], xyz[2] / 1.08883)]
        v = cache[rgb] = (116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2]))
    return v


def de00(p, q):
    from math import atan2, cos, degrees, exp, radians, sin, sqrt
    L1, a1, b1 = p
    L2, a2, b2 = q
    Cb = (sqrt(a1 * a1 + b1 * b1) + sqrt(a2 * a2 + b2 * b2)) / 2
    G = 0.5 * (1 - sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1, C2 = sqrt(a1p * a1p + b1 * b1), sqrt(a2p * a2p + b2 * b2)
    h1 = degrees(atan2(b1, a1p)) % 360 if C1 else 0.0
    h2 = degrees(atan2(b2, a2p)) % 360 if C2 else 0.0
    dL, dC = L2 - L1, C2 - C1
    dh = 0.0 if C1 * C2 == 0 else (h2 - h1 if abs(h2 - h1) <= 180 else h2 - h1 - 360 if h2 > h1 else h2 - h1 + 360)
    dH = 2 * sqrt(C1 * C2) * sin(radians(dh / 2))
    Lm, Cm = (L1 + L2) / 2, (C1 + C2) / 2
    hm = h1 + h2 if C1 * C2 == 0 else ((h1 + h2) / 2 if abs(h1 - h2) <= 180 else (h1 + h2 + 360) / 2 if h1 + h2 < 360 else (h1 + h2 - 360) / 2)
    T = 1 - 0.17 * cos(radians(hm - 30)) + 0.24 * cos(radians(2 * hm)) + 0.32 * cos(radians(3 * hm + 6)) - 0.20 * cos(radians(4 * hm - 63))
    SL, SC, SH = 1 + 0.015 * (Lm - 50) ** 2 / sqrt(20 + (Lm - 50) ** 2), 1 + 0.045 * Cm, 1 + 0.015 * Cm * T
    RT = -2 * sqrt(Cm ** 7 / (Cm ** 7 + 25 ** 7)) * sin(radians(60 * exp(-(((hm - 275) / 25) ** 2))))
    return sqrt((dL / SL) ** 2 + (dC / SC) ** 2 + (dH / SH) ** 2 + RT * (dC / SC) * (dH / SH))


def _grid(path):
    from PIL import Image
    return Image.open(path).convert("RGB").resize(GRID, Image.BOX).tobytes()


def measure(frame, plate, exclude=None) -> dict:
    """exclude: an image of the same content as `frame` without subtitles/overlays; grid cells that differ from it are left out of the measurement (final.mp4 audits only)."""
    a, b = _grid(frame), _grid(plate)
    c = _grid(exclude) if exclude else None
    ds, skipped, cache = [], 0, {}
    for i in range(0, len(a), 3):
        pa, pb = tuple(a[i:i + 3]), tuple(b[i:i + 3])
        if c is not None and de00(_lab(pa), _lab(tuple(c[i:i + 3]))) >= 12:
            skipped += 1
            continue
        k = pa + pb
        d = cache.get(k)
        if d is None:
            d = cache[k] = de00(_lab(pa), _lab(pb))
        ds.append(d)
    n = len(a) // 3
    foot = sorted(d for d in ds if d >= FOOTPRINT_DE)
    p90 = foot[int(0.9 * (len(foot) - 1))] if foot else 0.0
    area = {f"area_pct_de{t}": round(100 * sum(1 for d in ds if d >= t) / n, 3) for t in (5, 8, 10, 15, 20)}
    return {"footprint_pct": round(100 * len(foot) / n, 3), "p90_de": round(p90, 2), "max_de": round(max(ds), 2) if ds else 0.0, "excluded_pct": round(100 * skipped / n, 2), **area}


def verdict(m: dict) -> bool:
    return m[f"area_pct_de{int(VISIBLE_DE)}"] >= MIN_VISIBLE_AREA_PCT and m["p90_de"] >= MIN_P90_DE


def measure_isolated(frame: Path, plate: Path) -> dict:
    """The same isolation as the blind readers: an empty folder, neutral file names, a fresh process that knows no production, scene or element name."""
    with tempfile.TemporaryDirectory(prefix="vis-") as d:
        shutil.copyfile(frame, Path(d) / "a.png")
        shutil.copyfile(plate, Path(d) / "b.png")
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--measure", "a.png", "b.png"], cwd=d, capture_output=True, text=True, env={k: v for k, v in os.environ.items() if not k.startswith(("CLAUDE", "SF_"))})
        if r.returncode:
            raise SystemExit(r.stderr[-800:])
        return json.loads(r.stdout)


def render(prod: Path, cfg: dict, script: Path, frames: list[int], out: Path, hide: list[str]) -> None:
    """Final profile AND the narration slot: a script's timing and camera keys scale with the slot, so a plate without it is a different shot from the final (found by the first final.mp4 audit)."""
    sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "factory")]
    import blender_run
    import identity
    name = cfg.get("identity_preset") or identity.active_name()
    extra = list(cfg.get("render_args", [])) + [f"identity={identity.export_json(production=prod)}"]
    if not any(a.startswith("look=") for a in extra):
        extra.append(f"look={name}")
    out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, SF_VIS_HIDE=",".join(hide))
    env.pop("SF_VIS_DUMP", None)
    for f in frames:                                                          # a stale still must never pass for a fresh render
        (out / f"still-{f:04d}.png").unlink(missing_ok=True)
    for _attempt in (1, 2):                                                   # one retry: Metal can fail transiently at kernel load (seen 2026-11-08)
        r = blender_run.blender(["-b", "--python-expr", HOOK, "--python", str(script), "--", f"production={prod}", "mode=final", f"slot={_slot_frames(prod, int(script.stem.rsplit('_', 1)[-1]))}", f"stills={','.join(map(str, frames))}", f"out={out}", *extra], capture_output=True, text=True, env=env)
        if all((out / f"still-{f:04d}.png").exists() for f in frames):
            if hide and not re.search(r"VIS_HIDDEN [1-9]", r.stdout):
                raise SystemExit(f"no object matched {hide} in {script.name}")
            return
    raise SystemExit(f"render failed: {script.name} {frames}: {(r.stdout + r.stderr)[-800:]}")


def script_of(cfg: dict, sid: int) -> Path:
    return ROOT / "code3d" / "scenes" / f"{cfg.get('scene_script_prefix', 'scene')}_{sid:02d}.py"


def record(prod: Path, only: list[int]) -> int:
    sys.path[:0] = [str(ROOT / "factory")]
    import gate
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    decl = cfg.get("visibility") or {}
    vdir = prod / "build" / "gate" / "visibility"
    path = prod / "build" / "gate" / "visibility.json"
    data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    rc = 0
    for sid in sorted(int(k) for k in decl):
        if only and sid not in only:
            continue
        frames = sorted({f for e in decl[str(sid)].values() for f in e["frames"]})
        render(prod, cfg, script_of(cfg, sid), frames, vdir / f"s{sid:02d}" / "frame", [])
        for eid, e in decl[str(sid)].items():
            plate = vdir / f"s{sid:02d}" / f"plate-{eid}"
            render(prod, cfg, script_of(cfg, sid), e["frames"], plate, e["objects"])
            rows = {str(f): measure_isolated(vdir / f"s{sid:02d}" / "frame" / f"still-{f:04d}.png", plate / f"still-{f:04d}.png") for f in e["frames"]}
            ok = all(verdict(m) for m in rows.values())
            rc |= not ok
            data[f"{sid}:{eid}"] = {"pass": ok, "frames": rows, "objects": e["objects"], "fingerprint": gate.visibility_fingerprint(prod, sid, eid), "isolation": "headless", "version": VERSION, "date": date.today().isoformat()}
            print(f"scene {sid} {eid}: {'PASS' if ok else 'FAIL'} " + json.dumps({f: (m['p90_de'], m[f'area_pct_de{int(VISIBLE_DE)}']) for f, m in rows.items()}), flush=True)
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 1 if rc else 0


def _slot_frames(prod: Path, sid: int) -> int:
    import math
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(prod / "audio" / f"scene-{sid:02d}.mp3")], capture_output=True, text=True, check=True).stdout)
    return math.ceil(d * 30 - 1e-6)


def audit_final(prod: Path, sid: int, objects: list[str], frames: list[int], out: Path) -> list[dict]:
    """final.mp4 against the plate. The plate and the clip frame get the editor's own shared grade (grain off); cells where final.mp4 differs from its own clip frame are subtitles or overlays and are left out."""
    sys.path[:0] = [str(ROOT / "factory")]
    import visual_identity as vid
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
    vf = re.sub(r",?noise=[^,]*", "", vid.unify_filter(cfg.get("visual_identity"))).strip(",") or "null"
    start = sum(_slot_frames(prod, s["id"]) for s in cfg["scenes"] if s["id"] < sid)
    render(prod, cfg, script_of(cfg, sid), frames, out / "plate", objects)
    res = []
    for f in frames:
        idx = start + f - 1
        fin, clip, plate = out / f"final-{f:04d}.png", out / f"clip-{f:04d}.png", out / f"plate-graded-{f:04d}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(prod / "final.mp4"), "-vf", f"select=eq(n\\,{idx})", "-frames:v", "1", str(fin)], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(prod / "clips" / f"scene-{sid:02d}.mp4"), "-vf", f"select=eq(n\\,{f - 1}),scale=1080:1920,{vf}", "-frames:v", "1", str(clip)], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out / "plate" / f"still-{f:04d}.png"), "-vf", f"scale=1080:1920:flags=lanczos,{vf}", "-frames:v", "1", str(plate)], check=True)
        m = measure(fin, plate, exclude=clip)
        m["frame"], m["pass"] = f, verdict(m)
        res.append(m)
    return res


def calibrate(mp: Path, out: Path) -> int:
    """{"<prod glob>": {"<scene>": {"<element>": {"objects": [...], "frames": [...]}}}}; "__control__" as an element hides nothing and gives the render-noise floor."""
    res = json.loads(out.read_text()) if out.exists() else {}
    for pg, scenes in json.loads(mp.read_text()).items():
        prod = next((ROOT / "productions" / "mecanalia-es").glob(pg)).resolve()
        cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8"))
        for sid, els in scenes.items():
            sid = int(sid)
            tag = hashlib.sha1(f"{prod.name}{sid}".encode()).hexdigest()[:8]
            base = Path(tempfile.gettempdir()) / "sf-vis" / tag
            frames = sorted({f for e in els.values() for f in e["frames"]})
            todo = [e for e in els if f"{prod.name[:3]}:{sid}:{e}" not in res]
            if not todo:
                continue
            render(prod, cfg, script_of(cfg, sid), frames, base / "frame", [])
            for eid in todo:
                e = els[eid]
                plate = base / f"plate-{eid}"
                if eid == "__control__":
                    shutil.rmtree(plate, ignore_errors=True)
                    render(prod, cfg, script_of(cfg, sid), e["frames"], plate, [])
                else:
                    render(prod, cfg, script_of(cfg, sid), e["frames"], plate, e["objects"])
                rows = {str(f): measure_isolated(base / "frame" / f"still-{f:04d}.png", plate / f"still-{f:04d}.png") for f in e["frames"]}
                res[f"{prod.name[:3]}:{sid}:{eid}"] = rows
                out.write_text(json.dumps(res, indent=1) + "\n")
                print(prod.name[:3], sid, eid, json.dumps(rows), flush=True)
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", nargs=2)
    ap.add_argument("--record", nargs="+")
    ap.add_argument("--audit-final", nargs="+")
    ap.add_argument("--calibrate", nargs=2)
    a = ap.parse_args()
    if a.measure:
        print(json.dumps(measure(*a.measure)))
    elif a.record:
        sys.exit(record(Path(a.record[0]).resolve(), [int(x) for x in a.record[1:]]))
    elif a.audit_final:
        p, s, objs, *fr = a.audit_final
        print(json.dumps(audit_final(Path(p).resolve(), int(s), objs.split(","), [int(x) for x in fr], Path(tempfile.mkdtemp(prefix="vis-final-")))))
    else:
        sys.exit(calibrate(Path(a.calibrate[0]), Path(a.calibrate[1])))
