"""75% motion test: render candado scene 6 (007) twice through tools/blender_run.py, once at the final profile (75%) and once at res=100.
Frames go to productions/_lab/motion-75/{r75,r100}; the production folder is only read."""
import json, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "factory"))
import blender_run, identity  # noqa: E402
prod = ROOT / "productions/mecanalia-es/007-candado-solo-abre-su-llave"
cfg = json.loads((prod / "scenes.json").read_text())
extra = list(cfg.get("render_args", [])) + [f"identity={identity.export_json(production=prod)}"]
script = ROOT / "code3d/scenes/candado_06.py"
lab = Path(__file__).parent
for tag, res in (("r75", None), ("r100", "100")):
    out = lab / tag
    args = ["-b", "--python", str(script), "--", f"production={prod}", "mode=final", "slot=150", "frames=1-150", f"out={out}", *extra]
    if res:
        args.append(f"res={res}")
    t0 = time.time()
    r = blender_run.blender(args, capture_output=True, text=True)
    (lab / f"{tag}.log").write_text(r.stdout[-4000:] + r.stderr[-2000:])
    print(tag, r.returncode, round(time.time() - t0, 1), "s", len(list(out.glob("f-*.png"))), "frames", flush=True)
