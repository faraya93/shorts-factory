"""Keeps channels/umbrella-es.yaml valid and in sync with the code it mirrors. Run: python tests/test_channel.py"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import editor  # noqa: E402
import identity  # noqa: E402
import visual_identity as vid  # noqa: E402
from scenes_schema import FAMILIES  # noqa: E402

CFG = yaml.safe_load((ROOT / "channels" / "umbrella-es.yaml").read_text(encoding="utf-8"))


def test_generated_visual_identity_block_is_valid_for_every_preset():
    for name in identity.presets(CFG):
        assert vid.validate(identity.visual_identity_block(name, CFG)) == [], name


def test_active_preset_exists_and_all_hexes_are_well_formed():
    P = identity.presets(CFG)
    assert CFG["identity"]["active"] in P
    for name, p in P.items():
        for key in ("top", "bottom", "plinth", "board", "accent", "error", "annot", "ink", "ink_stroke", "spoken_box", "spoken_text", "emph",
                    "mark_body", "mark_inner", "mark_accent"):
            assert vid.HEX_RE.match(p[key]), (name, key, p[key])
        assert p["mode"] in ("ink", "white", "reference") and p["lighting"] in ("studio", "dark-stage"), name
    b = identity.visual_identity_block(None, CFG)
    assert b["background"]["hex"] == P[CFG["identity"]["active"]]["top"] and b["text_theme"] == CFG["identity"]["active"]


def test_render_profiles_are_defined_and_per_scene_types_resolve():
    R = CFG["render"]
    assert R["default_profile"] in R["profiles"]
    assert all(v in R["profiles"] for v in R["scene_type_profiles"].values())
    assert set(R["scene_types"].values()) <= set(R["scene_type_profiles"])
    assert R["profiles"]["tuned"]["fast_gi"] is False and R["profiles"]["tuned"]["denoise_gpu"] is True


def test_topic_mix_covers_every_family_and_sums_to_100():
    mix = {k: v for k, v in CFG["topic_families"].items() if k in FAMILIES}
    assert set(mix) == set(FAMILIES) and sum(mix.values()) == 100


def test_subtitle_constants_match_the_editor():
    s = CFG["subtitles"]
    assert s["y_center"] == editor.SUBTITLE_Y_CENTER
    assert s["font_size_px"] == editor.SUB_FONT_SIZE and s["stroke_px"] == editor.SUB_STROKE
    assert s["max_words"] == editor.CUE_MAX_WORDS and s["max_chars"] == editor.CUE_MAX_CHARS
    assert s["max_width_px"] == editor.SUB_MAX_WIDTH


def test_unify_defaults_match_the_code_and_grain_is_mandatory():
    assert {**vid.DEFAULT_UNIFY, **CFG["visual_identity"]["unify"]} == vid.DEFAULT_UNIFY
    assert CFG["visual_identity"]["unify"]["grain"] > 0


def test_style_forbids_text_and_voice_matches_the_editor_default():
    assert "no text on screen" in CFG["style"]["base"].lower()
    assert CFG["voice"]["default"] == editor.DEFAULT_VOICE
    assert CFG["status"] == "draft"


def test_duration_bands_are_ordered():
    d = CFG["duration"]
    assert d["standard_s"][0] < d["standard_s"][1]
    assert all(lo < hi for lo, hi in d["by_family"].values())


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
