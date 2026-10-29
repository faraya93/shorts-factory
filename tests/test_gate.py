"""The composition gate is a HARD render block. Run: python tests/test_gate.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import gate  # noqa: E402


def _prod(tmp: Path, stills=None) -> Path:
    p = tmp / "prod"
    p.mkdir()
    (p / "scenes.json").write_text(json.dumps({"scene_script_prefix": "gear", "identity_preset": "coral", "gate_stills": stills or {"3": [230]},
                                               "scenes": [{"id": 1}]}))
    return p


def test_no_record_blocks():
    with tempfile.TemporaryDirectory() as t:
        ok, msg = gate.check(_prod(Path(t)))
        assert not ok and "no gate record" in msg


def test_fresh_pass_record_allows_and_change_makes_it_stale():
    with tempfile.TemporaryDirectory() as t:
        p = _prod(Path(t))
        (p / "build" / "gate").mkdir(parents=True)
        (p / "build" / "gate" / "gate.json").write_text(json.dumps({"pass": True, "fingerprint": gate.fingerprint(p)}))
        assert gate.check(p)[0]
        cfg = json.loads((p / "scenes.json").read_text())
        cfg["support_colours"] = {"board": "#123456"}                       # a support colour change must invalidate the record
        (p / "scenes.json").write_text(json.dumps(cfg))
        ok, msg = gate.check(p)
        assert not ok and "STALE" in msg


def test_blocked_record_blocks():
    with tempfile.TemporaryDirectory() as t:
        p = _prod(Path(t))
        (p / "build" / "gate").mkdir(parents=True)
        (p / "build" / "gate" / "gate.json").write_text(json.dumps({"pass": False, "fingerprint": gate.fingerprint(p)}))
        assert not gate.check(p)[0]


def test_driver_refuses_a_final_render_without_a_record():
    with tempfile.TemporaryDirectory() as t:
        p = _prod(Path(t))
        r = subprocess.run([sys.executable, str(ROOT / "factory" / "code3d_render.py"), str(p), "1", "--mode", "final"], capture_output=True, text=True)
        assert r.returncode == 2 and "RENDER BLOCKED" in r.stdout, (r.returncode, r.stdout, r.stderr)


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
