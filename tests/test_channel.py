"""Keeps the Mecanalia brand package + channel variants valid, inheriting correctly, credential-free, and in sync with the code they mirror.
Run: .venv/bin/python tests/test_channel.py"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import channel  # noqa: E402
import editor  # noqa: E402
import identity  # noqa: E402
import visual_identity as vid  # noqa: E402
from scenes_schema import FAMILIES  # noqa: E402

CFG = channel.load("mecanalia-es")          # brand + Spanish variant, merged


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


def test_channel_variants_extend_the_brand_and_inherit_it():
    ids = channel.variants()
    assert {"mecanalia-es", "mecanalia-en"} <= set(ids)
    brand = channel.load_brand("mecanalia")
    for cid in ids:
        cfg = channel.load(cid)
        assert cfg["extends"] == brand["brand"] and cfg["channel"] == cid
        for block in ("render", "style", "subtitles", "visual_identity", "audio", "topic_families"):
            assert cfg[block] == brand[block], block
        assert cfg["identity"] == brand["identity"], "a channel variant must not copy or fork the identity"
    es, en = channel.load("mecanalia-es"), channel.load("mecanalia-en")
    assert es["language"] == "es" and en["language"] == "en" and es["handles"]["primary"] == "@mecanalia" and en["handles"]["primary"] == "@mecanaliaen"
    assert en["handles"]["fallbacks"] == ["mecanalia_en", "mecanalia.en"]
    assert es["duration"]["standard_s"] == en["duration"]["standard_s"] == brand["duration"]["standard_s"]


def test_variants_store_only_what_differs():
    allowed = {"channel", "extends", "language", "register", "promise", "handles", "voice", "duration", "publish"}
    for cid, f in channel.variants().items():
        extra = set(yaml.safe_load(f.read_text(encoding="utf-8"))) - allowed
        assert not extra, (cid, extra)


def test_packages_hold_no_credentials():
    banned = ("token", "secret", "password", "api_key", "apikey", "access_key", "client_id", "bearer")
    for f in (ROOT / "channels").glob("*/*.yaml"):
        low = f.read_text(encoding="utf-8").lower().replace("tokens live only", "")      # the comment that states the rule
        for k in banned:
            assert k not in low, (f.name, k)


def test_hashtag_policy_is_valid_and_enforced():
    import importlib.util
    spec = importlib.util.spec_from_file_location("publish_package", ROOT / "tools" / "publish_package.py")
    pp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pp)
    for cid in ("mecanalia-es", "mecanalia-en"):
        cfg = channel.load(cid)
        h = cfg["publish"]["hashtags"]
        assert 3 <= h["min"] <= h["max"] <= 5 and h["base"] and set(h["family"]) == set(cfg["topic_families"]) - {"avoid"}, cid
    assert pp.hashtag_errors(["#imanes", "#magnetismo", "#comofunciona", "#shorts"], "mecanalia-es", "objects") == []
    for bad in (["#shorts", "#imanes", "#comofunciona"], ["#imanes", "#shorts", "#comofunciona"], ["#imanes", "#shorts"],
                ["#a", "#b", "#c", "#d", "#e", "#comofunciona", "#shorts"], ["#imanes", "#imanes", "#comofunciona", "#shorts"]):
        assert pp.hashtag_errors(bad, "mecanalia-es", "objects"), bad


def test_platform_bios_fit_their_limits():
    limits = {"instagram": 150, "tiktok": 80, "facebook": 255, "youtube": 1000}
    pub = channel.load("mecanalia-es")["publish"]
    assert set(pub["bios"]) == set(limits)
    for platform, limit in limits.items():
        assert 0 < len(pub["bios"][platform]) <= limit, platform
        if platform != "tiktok":
            assert pub["bios"][platform] == pub["bio"], platform      # the stored wording stays unchanged wherever it fits


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
