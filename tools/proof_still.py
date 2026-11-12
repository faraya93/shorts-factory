"""One blind-proof still (block B5), through tools/blender_run.py (GPU lock + caffeinate). A proof still is a static frame of a `proof_NN.py` scene script (code3d/scenes), rendered in the lab
production productions/_lab/proofs-b5 (it only carries the identity block). Same render path as tools/draft_still.py; the reader then judges the still with tools/blind_read.py --record proof.
usage: .venv/bin/python tools/proof_still.py <script stem, e.g. proof_01> [frame=10] [--cpu]   -> productions/_lab/proofs-b5/build/stills/<stem>/still-<frame>.png"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(ROOT / "tools"))
import blender_run  # noqa: E402
import identity  # noqa: E402

LAB = ROOT / "productions" / "_lab" / "proofs-b5"


def main() -> int:
    stem = sys.argv[1]
    frame = next((a for a in sys.argv[2:] if a.isdigit()), "10")
    out = LAB / "build" / "stills" / stem
    cmd = ["-b", "--python", str(ROOT / "code3d" / "scenes" / f"{stem}.py"), "--", f"production={LAB}", "mode=draft", "slot=30", f"stills={frame}", f"out={out}",
           "look=" + identity.preset()["name"], f"identity={identity.export_json(production=LAB)}"]
    if "--cpu" in sys.argv:
        cmd.append("cpu=1")
    if "--final" in sys.argv:
        cmd = [a.replace("mode=draft", "mode=final").replace(f"out={out}", f"out={LAB / 'build' / 'final' / stem}") for a in cmd] + ["res=75"]
    t0 = time.time()
    r = blender_run.blender(cmd, capture_output=True, text=True)
    if "--final" in sys.argv:
        print(f"seconds_per_frame={time.time() - t0:.1f}")
    if r.returncode != 0 or "Traceback" in r.stdout + r.stderr:
        print((r.stdout + r.stderr)[-3500:])
        return 1
    print("ok", out / f"still-{int(frame):04d}.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
