"""Non-model verifier between production units: code, not opinion. Exit 0 = PASS. usage: .venv/bin/python tools/verify_production.py productions/<ch>/<video> [--stage script|final]"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import gate  # noqa: E402


def probe(p: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", str(p)], capture_output=True, text=True)
    d = json.loads(r.stdout or "{}")
    return {"duration": float(d.get("format", {}).get("duration", 0)), **(d.get("streams") or [{}])[0]}


def verify(prod: Path) -> list[str]:
    fails = []
    cfg = json.loads((prod / "scenes.json").read_text(encoding="utf-8")) if (prod / "scenes.json").exists() else None
    if cfg is None:
        return ["scenes.json missing"]
    log = ROOT / "output" / f"chain-{prod.name}.log"
    if not log.exists():
        fails.append("no chain log")
    else:
        text = log.read_text(errors="replace")
        last = text[text.rfind(" START "):] if " START " in text else text
        if re.search(r"FAILED|INCOMPLETE|Traceback|GATE BLOCKED", last):
            fails.append("chain log (last run) shows FAILED/INCOMPLETE/Traceback/GATE BLOCKED")
        if " DONE " not in last:
            fails.append("chain log has no DONE for the last run")
    for sc in cfg["scenes"]:
        if not (prod / "clips" / f"scene-{int(sc['id']):02d}.mp4").exists():
            fails.append(f"clip of scene {sc['id']} missing")
        ok, msg = gate.check(prod, int(sc["id"]))
        if not ok:
            fails.append(f"gate scene {sc['id']}: {msg}")
    final = prod / "final.mp4"
    if not final.exists():
        fails.append("final.mp4 missing")
    else:
        v = probe(final)
        if (v.get("width"), v.get("height")) != (1080, 1920):
            fails.append(f"final.mp4 is {v.get('width')}x{v.get('height')}")
        if not 30 <= v["duration"] <= 75:
            fails.append(f"final.mp4 duration {v['duration']:.1f} s outside 30-75")
    if not (prod / "cover.jpg").exists():
        fails.append("cover.jpg missing")
    if (prod / "publish.json").exists():
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "publish_package.py"), "check", str(prod)], capture_output=True, text=True)
        if r.returncode:
            fails.append("publish_package check: " + (r.stdout + r.stderr)[-200:])
    else:
        fails.append("publish.json missing")
    return fails


if __name__ == "__main__":
    f = verify(Path(sys.argv[1]).resolve())
    for x in f:
        print("FAIL", x)
    print("PASS" if not f else f"NOT VERIFIED: {len(f)} failures")
    sys.exit(1 if f else 0)
