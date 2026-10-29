"""Identity is parameters: one source (channels/umbrella-es.yaml), read through factory/identity.py. Run: python tests/test_identity.py"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import identity  # noqa: E402
import overlays  # noqa: E402

HEX = re.compile(r"#[0-9A-Fa-f]{6}")


def test_every_preset_becomes_a_text_theme_and_legacy_aliases_hold():
    for name in identity.presets():
        assert name in overlays.THEMES
    assert overlays.THEMES["dark"] is overlays.THEMES["reference-dark"] and overlays.THEMES["light"] is overlays.THEMES["celeste"]
    d = overlays.THEMES["dark"]          # frozen productions render with exactly the pre-config reference theme
    assert d["INK"] == (255, 255, 255) and d["INK_STROKE"] == (0, 0, 0) and d["TEAL"] == (103, 205, 190) and d["RED"] == (190, 74, 74)
    assert d["GOLD"] == (245, 192, 74) and d["GREY"] == (150, 150, 155) and d["PASSIVE"] == (81, 85, 90) and d["VOID"] == (18, 15, 16)


def test_active_preset_drives_the_generated_visual_identity_and_the_scenes_embed():
    import json
    import tempfile
    p = identity.preset()
    b = identity.visual_identity_block()
    assert b["background"]["hex"] == p["top"] and b["text_theme"] == p["name"]
    names = {c["name"]: c["hex"] for c in b["palette"]}
    assert names["accent gold"] == p["accent"] and names["error red"] == p["error"]       # the names the rigs look up hold the ACCENT
    with tempfile.TemporaryDirectory() as t:
        f = Path(t) / "scenes.json"
        f.write_text(json.dumps({"scenes": []}))
        identity.apply_to_scenes(f)
        d = json.loads(f.read_text())
        assert d["identity_preset"] == p["name"] and d["visual_identity"]["text_theme"] == p["name"] and f"look={p['name']}" in d["render_args"]


def test_the_export_for_blender_carries_presets_and_render_profiles():
    import json
    import tempfile
    with tempfile.TemporaryDirectory() as t:
        out = identity.export_json(Path(t) / "x.json")
        d = json.loads(out.read_text())
    assert d["active"] == identity.active_name() and d["presets"][d["active"]]["plinth"] == identity.preset()["plinth"]
    assert d["render"]["profiles"]["tuned"]["denoise_gpu"] is True and d["render"]["profiles"]["tuned"]["fast_gi"] is False


def test_no_active_identity_colour_is_hard_coded_in_the_code():
    """If the active identity's own colours reappear as literals in the factory or the 3D libs, a future preset switch would silently miss them."""
    p = identity.preset()
    mine = {p[k].upper() for k in ("top", "bottom", "plinth", "board", "accent", "error", "mark_body", "mark_inner", "mark_accent")}
    mine -= {"#FFFFFF", "#000000"}
    offenders = []
    for folder in ("factory", "code3d/lib", "tools"):
        for f in (ROOT / folder).glob("*.py"):
            if f.name in ("palette_metrics.py",):
                continue
            for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                if line.lstrip().startswith("#") or "TEST FIXTURE" in line:
                    continue
                hits = {h.upper() for h in HEX.findall(line)} & mine
                if hits:
                    offenders.append(f"{f.relative_to(ROOT)}:{n} {sorted(hits)}")
    assert not offenders, offenders


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
