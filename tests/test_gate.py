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


def _lib(t):
    import gate_deps as d
    lib = t / "lib"; lib.mkdir()
    for c in d.CORE:
        (lib / f"{c}.py").write_text("X = 1\n")
    (lib / "kit.py").write_text("K = 2\n\ndef helper():\n    return 1\n\ndef ice():\n    return helper()\n\ndef water():\n    return 3\n")
    (t / "s.py").write_text("import kit as k\nk.ice()\n")
    d.LIB = lib
    d.fresh()
    return d, lib, t / "s.py"


def _digest(d, script):
    d.fresh()
    want, dyn = d.closure(script)
    return d.lib_digest(want), want, dyn


def test_element_scope_other_function_does_not_invalidate():
    import gate_deps
    keep = gate_deps.LIB
    try:
        with tempfile.TemporaryDirectory() as t:
            d, lib, s = _lib(Path(t))
            a, want, dyn = _digest(d, s)
            assert not dyn and want["kit"] == {"ice", "helper"}, want
            src = (lib / "kit.py").read_text()
            (lib / "kit.py").write_text(src.replace("return 3", "return 4"))
            assert _digest(d, s)[0] == a, "editing water must not touch an ice-only scene"
            (lib / "kit.py").write_text(src.replace("return 1", "return 9"))
            assert _digest(d, s)[0] != a, "editing a transitive helper must invalidate"
    finally:
        gate_deps.LIB = keep


def test_comments_and_docstrings_do_not_invalidate():
    import gate_deps
    keep = gate_deps.LIB
    try:
        with tempfile.TemporaryDirectory() as t:
            d, lib, s = _lib(Path(t))
            a = _digest(d, s)[0]
            src = (lib / "kit.py").read_text()
            (lib / "kit.py").write_text("# a comment\n" + src.replace("def ice():\n", 'def ice():\n    """doc"""\n'))
            assert _digest(d, s)[0] == a
            assert d.normalized(s) == (s.write_text("# c\nimport kit as k\nk.ice()  # c\n") and d.normalized(s))
    finally:
        gate_deps.LIB = keep


def test_escaping_module_widens_and_dynamic_flags():
    import gate_deps
    keep = gate_deps.LIB
    try:
        with tempfile.TemporaryDirectory() as t:
            d, lib, s = _lib(Path(t))
            s.write_text("import kit as k\nf = k\nf.ice()\n")
            assert _digest(d, s)[1]["kit"] is None
            s.write_text("import importlib\nm = importlib.import_module('kit')\n")
            assert _digest(d, s)[2] is True
    finally:
        gate_deps.LIB = keep


def test_v1_records_ignore_the_additive_block():
    with tempfile.TemporaryDirectory() as t:
        f = Path(t) / "x.py"
        f.write_text("a=1\n# SF-EXT-BEGIN x\nb=2\n# SF-EXT-END\nc=3\n")
        assert gate._bytes(f) == b"a=1\nc=3\n"


def test_carry_compares_pixels():
    from PIL import Image
    with tempfile.TemporaryDirectory() as t:
        a, b = Path(t) / "a.png", Path(t) / "b.png"
        Image.new("RGB", (64, 64), (100, 100, 100)).save(a); Image.new("RGB", (64, 64), (100, 100, 100)).save(b)
        assert gate.same_pixels(a, b)
        Image.new("RGB", (64, 64), (130, 100, 100)).save(b)
        assert not gate.same_pixels(a, b)


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
