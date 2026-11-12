"""One call per staging iteration (block B3, P5 and P4 of docs/current/reports/architecture-second-opinion-2026-11-11.md): draft stills of one scene, ONE contact sheet of them,
and a compact summary. It replaces the sequence draft_still -> ls -> contact_sheet -> Read-each-PNG, and it remembers what the session has already looked at.
usage: .venv/bin/python tools/iterate.py productions/<ch>/<video> <scene id> <frame>[,<frame>...] [--cpu] [--mask]
Runs tools/draft_still.py (EEVEE half-resolution, through tools/blender_run.py: GPU lock + caffeinate), builds build/stills/sheet-s<id>.png with tools/contact_sheet.py, appends
build/iterate-ledger.jsonl, and prints per still: path, size, and whether its pixels are IDENTICAL to the last iteration (then re-reading it tells you nothing).
Read the sheet, one image, not each still. Nothing here is a gate reading: readers stay behind tools/blind_read.py."""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = "iterate-ledger.jsonl"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def last_hashes(prod: Path, scene: int) -> dict[str, str]:
    """Hash of every still at the end of the previous iteration of this scene."""
    seen: dict[str, str] = {}
    try:
        for line in (prod / "build" / LEDGER).read_text().splitlines():
            e = json.loads(line)
            if e.get("scene") == scene:
                seen = e.get("hashes") or seen
    except (OSError, ValueError):
        pass
    return seen


def wanted_stills(out: Path, frames: str) -> list[Path]:
    names = [out / f"still-{int(f):04d}.png" for f in frames.split(",") if f.strip().isdigit()]
    return [p for p in names if p.exists()] or sorted(out.glob("still-*.png"))


def summarize(prod: Path, scene: int, stills: list[Path], sheet: Path | None, seconds: float, before: dict[str, str]) -> tuple[str, dict[str, str]]:
    hashes = {p.name: sha(p) for p in stills}
    lines = [f"iterate {prod.name} scene {scene:02d}: {len(stills)} still(s) in {seconds:.0f}s"]
    for p in stills:
        same = before.get(p.name) == hashes[p.name]
        lines.append(f"  {p.relative_to(ROOT)}  {p.stat().st_size // 1024} KB  {'IDENTICAL to the last iteration: do not re-read' if same else 'changed' if p.name in before else 'new'}")
    if sheet:
        lines.append(f"  contact sheet: {sheet.relative_to(ROOT)}  <- read this one image")
    if stills and all(before.get(p.name) == hashes[p.name] for p in stills):
        lines.append("  NOTHING CHANGED: every still is pixel-identical to the last iteration; change the scene before iterating again")
    return "\n".join(lines), hashes


def main(argv: list[str]) -> int:
    pos = [a for a in argv if not a.startswith("--")]
    if len(pos) != 3 or not pos[1].isdigit():
        print(__doc__)
        return 2
    prod, scene, frames = Path(pos[0]).resolve(), int(pos[1]), pos[2]
    flags = [a for a in argv if a.startswith("--")]
    before = last_hashes(prod, scene)
    t0 = time.time()
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "draft_still.py"), str(prod), str(scene), frames, *flags], capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        print(f"iterate FAILED (draft_still exit {r.returncode}):\n{(r.stdout + r.stderr)[-2500:]}")
        return 1
    out = prod / "build" / "stills" / f"s{scene:02d}"
    stills = wanted_stills(out, frames)
    if not stills:
        print(f"iterate FAILED: draft_still reported ok but no stills are in {out}")
        return 1
    sheet = prod / "build" / "stills" / f"sheet-s{scene:02d}.png"
    cs = subprocess.run([sys.executable, str(ROOT / "tools" / "contact_sheet.py"), str(sheet), *map(str, stills)], capture_output=True, text=True, cwd=ROOT)
    if cs.returncode != 0:
        print(f"contact sheet failed: {cs.stderr[-400:]}")
        sheet = None
    text, hashes = summarize(prod, scene, stills, sheet, time.time() - t0, before)
    with (prod / "build" / LEDGER).open("a") as f:
        f.write(json.dumps({"at": time.strftime("%Y-%m-%dT%H:%M:%S"), "scene": scene, "frames": frames, "hashes": hashes}) + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
