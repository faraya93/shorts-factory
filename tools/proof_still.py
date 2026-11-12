"""One blind-proof still (block B5), through tools/blender_run.py (GPU lock + caffeinate). A proof still is a static frame of a `proof_NN.py` scene script (code3d/scenes), rendered in the lab
production productions/_lab/proofs-b5 (it only carries the identity block). Same render path as tools/draft_still.py; the reader then judges the still with tools/blind_read.py --record proof.
usage: .venv/bin/python tools/proof_still.py <script stem, e.g. proof_01> [frame=10] [--cpu]   -> productions/_lab/proofs-b5/build/stills/<stem>/still-<frame>.png  (EEVEE draft: the builder's own checks only)
       .venv/bin/python tools/proof_still.py <stem> [frame] --reader   -> productions/_lab/proofs-b5/build/reader/<stem>/still-<frame>.png + still-<frame>.render.json
--reader renders under the reader-still policy (factory/gate.py STILL_POLICY: half-resolution Cycles at the gate's samples) and writes the sidecar that factory/proofs.py require_conforming checks
before any reader runs (redesign session 2026-11-11: the B5 readings were taken on EEVEE drafts, which the house rules reserve for a session's own checks)."""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(ROOT / "tools"))
import blender_run  # noqa: E402
import identity  # noqa: E402
from gate import STILL_POLICY  # noqa: E402

LAB = ROOT / "productions" / "_lab" / "proofs-b5"


def main() -> int:
    stem = sys.argv[1]
    frame = next((a for a in sys.argv[2:] if a.isdigit()), "10")
    reader = "--reader" in sys.argv
    out = LAB / "build" / ("reader" if reader else "stills") / stem
    cmd = ["-b", "--python", str(ROOT / "code3d" / "scenes" / f"{stem}.py"), "--", f"production={LAB}", "mode=draft", "slot=30", f"stills={frame}", f"out={out}",
           "look=" + identity.preset()["name"], f"identity={identity.export_json(production=LAB)}"]
    if reader:
        cmd = [a.replace("mode=draft", "mode=final") for a in cmd] + [f"samples={STILL_POLICY['samples']}", f"res={STILL_POLICY['res']}"]
    elif "--cpu" in sys.argv:
        cmd.append("cpu=1")
    if "--final" in sys.argv and not reader:
        cmd = [a.replace("mode=draft", "mode=final").replace(f"out={out}", f"out={LAB / 'build' / 'final' / stem}") for a in cmd] + ["res=75"]
    t0 = time.time()
    r = blender_run.blender(cmd, capture_output=True, text=True)
    if "--final" in sys.argv:
        print(f"seconds_per_frame={time.time() - t0:.1f}")
    if r.returncode != 0 or "Traceback" in r.stdout + r.stderr:
        print((r.stdout + r.stderr)[-3500:])
        return 1
    still = out / f"still-{int(frame):04d}.png"
    if reader:
        still.with_suffix(".render.json").write_text(json.dumps({**STILL_POLICY, "frame": int(frame), "script": f"code3d/scenes/{stem}.py",
                                                                 "seconds": round(time.time() - t0, 1)}) + "\n", encoding="utf-8")
    print("ok", still)
    return 0


if __name__ == "__main__":
    sys.exit(main())
