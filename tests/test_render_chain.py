"""A failed render sub-step must not pass silently. Run: python tests/test_render_chain.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_chain_scripts_report_failed_scenes_as_incomplete():
    for name in ("chain_render.sh", "chain_render2.sh"):
        s = (ROOT / "tools" / name).read_text()
        assert "INCOMPLETE" in s and "render-failures.txt" in s, name
        assert s.index("INCOMPLETE") < s.index("factory/editor.py"), f"{name}: failures must be checked before the editor runs"
        assert "recovered on retry" in s, name


def test_code3d_render_tolerates_missing_costs_json():
    s = (ROOT / "factory" / "code3d_render.py").read_text()
    assert "costs_path.exists()" in s


def test_every_code3d_production_has_costs_json_with_all_clips():
    import json
    for d in (ROOT / "productions").glob("mecanalia-*/[0-9][0-9][0-9]-*"):
        if (d / "clips").is_dir() and any((d / "clips").glob("scene-*.mp4")) and (d / "scenes.json").exists():
            sc = json.loads((d / "scenes.json").read_text())
            if sc.get("primary_engine") == "code3d":
                assert (d / "costs.json").exists(), f"{d.name}: costs.json missing"


if __name__ == "__main__":
    n = 0
    for k, v in sorted(globals().items()):
        if k.startswith("test_") and callable(v):
            v(); n += 1; print("ok ", k)
    print(n, "tests passed")
