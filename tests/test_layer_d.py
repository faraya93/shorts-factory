"""Plain-assert tests for factory/overlays.py and factory/visual_identity.py. Run: python tests/test_layer_d.py"""

import copy
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "factory"))
import overlays as ov  # noqa: E402
import visual_identity as vid  # noqa: E402
from PIL import Image  # noqa: E402
from scenes_schema import build_prompt, validate_production  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_schema import VALID  # noqa: E402

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
IDENTITY = {
    "background": {"hex": "#E2D5F1", "description": "soft lavender-white studio backdrop"},
    "palette": [{"hex": "#F2C4A8", "name": "skin peach"}, {"hex": "#FFFFFF"}],
    "lighting": "soft studio lighting", "materials": "smooth clean matte materials",
}


def spec(**kw):
    return {"type": "label", "text_or_value": "x", "at_offset_seconds": 1.0, **kw}


# --- overlays ---------------------------------------------------------------------------

def test_overlay_validation():
    assert ov.validate_scene_overlays(1, [spec(type="counter", text_or_value="170 °C"),
                                          spec(type="bar", text_or_value="75%", at_offset_seconds=5)]) == []
    assert ov.validate_scene_overlays(1, [spec(type="video")])
    assert ov.validate_scene_overlays(1, [spec(at_offset_seconds=-1)])
    assert ov.validate_scene_overlays(1, [spec(type="counter", text_or_value="muchos")])
    assert ov.validate_scene_overlays(1, [spec(type="bar", text_or_value="150%")])
    assert ov.validate_scene_overlays(1, [spec(visible_s=0.1, duration_s=1)])
    assert ov.validate_scene_overlays(1, "nope")


def test_overlays_must_not_overlap_in_time():
    errs = ov.validate_scene_overlays(1, [spec(at_offset_seconds=1), spec(at_offset_seconds=2)])
    assert any("overlap" in e for e in errs), errs
    assert ov.validate_scene_overlays(1, [spec(at_offset_seconds=1), spec(at_offset_seconds=4)]) == []


def test_counter_counts_up_and_ends_exactly_on_target():
    s = spec(type="counter", text_or_value="170 °C")
    values = [float(ov.counter_text(s, (i + 1) / 36).split()[0]) for i in range(36)]
    assert values == sorted(values) and values[0] < values[-1] and values[-1] == 170
    assert ov.counter_text(s, 1.0) == "170 °C"
    assert ov.counter_text(spec(type="counter", text_or_value="10×"), 1.0) == "10×"
    assert ov.counter_text(spec(type="counter", text_or_value="2.5 s"), 1.0) == "2.5 s"
    assert ov.counter_text(spec(type="counter", text_or_value="1000000"), 1.0) == "1 000 000"


def test_bar_fraction():
    assert ov.bar_fraction("75%") == 0.75 and ov.bar_fraction("0.5") == 0.5
    assert ov.bar_fraction("1.5") is None and ov.bar_fraction("abc") is None


def test_render_overlay_writes_a_growing_sequence():
    if not Path(FONT).exists():
        return
    with tempfile.TemporaryDirectory() as d:
        meta = ov.render_overlay(spec(type="bar", text_or_value="75%", duration_s=0.5), Path(d), "t", FONT, 30)
        assert meta["frames"] == 15 and len(list(Path(d).glob("t-*.png"))) == 15
        first, last = (Image.open(Path(d) / f"t-{i:03d}.png") for i in (0, 14))
        assert first.size == last.size == (meta["w"], meta["h"])
        assert first.tobytes() != last.tobytes()
        lab = ov.render_overlay(spec(type="label", text_or_value="Hola", duration_s=0.2), Path(d), "l", FONT, 30)
        a0 = Image.open(Path(d) / "l-000.png").getchannel("A").getextrema()[1]
        a1 = Image.open(Path(d) / f"l-{lab['frames'] - 1:03d}.png").getchannel("A").getextrema()[1]
        assert a0 < a1 == 255  # fades in


# --- visual identity ---------------------------------------------------------------------

def test_identity_validation():
    assert vid.validate(IDENTITY) == []
    bad = copy.deepcopy(IDENTITY)
    bad["background"]["hex"] = "lavender"
    assert vid.validate(bad)
    bad = copy.deepcopy(IDENTITY)
    bad["palette"] = []
    assert vid.validate(bad)
    bad = copy.deepcopy(IDENTITY)
    del bad["lighting"]
    assert vid.validate(bad)
    assert vid.validate({**IDENTITY, "unify": {"saturation": 9}})


def test_identity_clause_is_literal():
    clause = vid.identity_clause(IDENTITY)
    for needle in ("#E2D5F1", "soft lavender-white studio backdrop", "skin peach #F2C4A8", "#FFFFFF",
                   "soft studio lighting", "smooth clean matte materials"):
        assert needle in clause, needle


def test_unify_filter_is_shared_and_complete():
    f = vid.unify_filter(IDENTITY)
    assert f.startswith("eq=") and "noise=" in f and "vignette=" in f
    assert vid.unify_filter(None) == ""
    assert "colorbalance" in vid.unify_filter({**IDENTITY, "unify": {"warmth": 0.1}})


def test_delta_e():
    assert vid.delta_e((226, 213, 241), (226, 213, 241)) == 0
    assert vid.delta_e((226, 213, 241), (226, 213, 235)) < 5
    assert vid.delta_e((226, 213, 241), (20, 20, 20)) > 60
    assert vid.delta_e((255, 255, 255), (0, 0, 0)) > 99


def test_sample_background_ignores_a_foreground_object():
    with tempfile.TemporaryDirectory() as d:
        img = Image.new("RGB", (400, 700), (226, 213, 241))
        img.paste((200, 60, 60), (0, 250, 400, 450))  # a foreground band covering both side-midpoint patches
        img.save(Path(d) / "f.png")
        assert vid.delta_e(vid.sample_background(Path(d) / "f.png"), (226, 213, 241)) < 2


def test_qa_applies_only_to_establishing_shots_and_code3d():
    assert vid.qa_applies("t2v", {}) and vid.qa_applies("t2v", {"shot_type": "establishing"})
    assert not vid.qa_applies("t2v", {"shot_type": "closeup"})
    assert not vid.qa_applies("keyframes", {"shot_type": "closeup"})
    assert vid.qa_applies("code3d", {"shot_type": "closeup"})  # every code3d scene renders on the spec background


def test_qa_marks_are_review_signals():
    bad, good = {"ok": False}, {"ok": True}
    assert vid.qa_status(False, None, None) == "exempt (closeup)"
    assert vid.qa_status(True, good, None) == "ok"
    assert vid.qa_status(True, bad, None) == "review"
    assert vid.qa_status(True, bad, "jungle").startswith("review (intentional: jungle")


# --- schema integration ------------------------------------------------------------------

def test_prompt_injects_identity_right_after_style():
    cfg = {**copy.deepcopy(VALID), "visual_identity": IDENTITY}
    prompt = build_prompt(cfg, cfg["scenes"][0])
    assert prompt.index(cfg["style"]) < prompt.index("#E2D5F1") < prompt.index(cfg["scenes"][0]["prompt"])
    assert "#E2D5F1" not in build_prompt(VALID, VALID["scenes"][0])


def test_schema_validates_shot_type_and_qa_note():
    cfg = copy.deepcopy(VALID)
    cfg["scenes"][0].update(shot_type="closeup", qa_note="intentional jungle")
    assert validate_production(cfg) == []
    cfg["scenes"][0]["shot_type"] = "wide"
    assert any("shot_type" in e for e in validate_production(cfg))
    cfg["scenes"][0].update(shot_type="closeup", qa_note=" ")
    assert any("qa_note" in e for e in validate_production(cfg))


def test_schema_reports_identity_and_overlay_errors():
    cfg = {**copy.deepcopy(VALID), "visual_identity": {**IDENTITY, "lighting": ""}}
    assert any("lighting" in e for e in validate_production(cfg))
    cfg = copy.deepcopy(VALID)
    cfg["scenes"][0]["data_overlays"] = [spec(type="bar", text_or_value="150%")]
    assert any("bar needs" in e for e in validate_production(cfg))


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
