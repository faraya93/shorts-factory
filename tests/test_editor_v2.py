"""Editor v2 (reference style): overlay types, word lock, keyframes, subtitles on the dark stage, end card. Run: python tests/test_editor_v2.py"""

import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import editor  # noqa: E402
import overlays as ov  # noqa: E402

FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
WORDS = [{"text": "Cuando", "start": 0.1, "end": 0.4}, {"text": "los", "start": 0.5, "end": 0.6},
         {"text": "bordes,", "start": 0.7, "end": 1.1}, {"text": "bordes", "start": 2.0, "end": 2.4}]


def spec(**kw):
    return {"type": "chip", "text_or_value": "x", "at_offset_seconds": 1.0, **kw}


def render(s, fps=30):
    with tempfile.TemporaryDirectory() as d:
        meta = ov.render_overlay(s, Path(d), "t", FONT, fps)
        frames = [Image.open(Path(d) / f"t-{i:03d}.png").convert("RGBA") for i in range(meta["frames"])]
        return meta, frames


def test_word_lock_resolves_against_spoken_words():
    assert ov.find_word_start(WORDS, "BORDES") == 0.7          # case and punctuation are ignored; first occurrence
    assert ov.find_word_start(WORDS, "bordes", 2) == 2.0
    assert ov.find_word_start(WORDS, "piel") is None
    s = {"type": "chip", "text_or_value": "x", "at_word": "los", "offset_s": 0.25}
    assert abs(ov.start_offset(s, WORDS) - 0.75) < 1e-9
    assert ov.start_offset({"type": "chip", "at_offset_seconds": 3.5}, WORDS) == 3.5
    try:
        ov.start_offset({"type": "chip", "at_word": "piel"}, WORDS)
        raise AssertionError("a missing word must raise")
    except ValueError:
        pass


def test_validation_of_the_new_types_and_fields():
    ok = [spec(x=0.1, y=0.1), spec(type="citation", text_or_value="Vicryl", x=0.2, y=0.2),
          spec(type="counter", text_or_value="DÍA 70", **{"from": 0}, style="mono", x=0.3, y=0.3),
          spec(type="bar", text_or_value="50%", style="slim", show_value=False, marker=0.5, x=0.4, y=0.4),
          spec(type="bracket", **{"from": [0.2, 0.4], "to": [0.6, 0.4]}, text_or_value=None),
          spec(type="ring", radius=0.2, x=0.5, y=0.5), spec(type="mark", kind="x", x=0.3, y=0.3),
          spec(type="label", style="tag", text_or_value="borde", leader_to=[0.6, 0.5], x=0.3, y=0.3),
          spec(type="cta", message="hola", x=0.5, y=0.55), {"type": "chip", "text_or_value": "x", "at_word": "bordes", "x": 0.6, "y": 0.6}]
    assert ov.validate_scene_overlays(1, ok) == [], ov.validate_scene_overlays(1, ok)
    bad = [spec(type="bracket"), spec(type="ring"), spec(type="mark", kind="z"), spec(type="cta"), spec(x=1.5),
           spec(at_word="a", at_offset_seconds=1), {"type": "chip", "text_or_value": "x"},
           spec(keyframes=[{"t": 0, "x": 0.1, "y": 0.1}]), spec(type="label", style="giant"), spec(type="counter", text_or_value="DÍA", **{"from": "a"})]
    for b in bad:
        assert ov.validate_scene_overlays(1, [b]), b


def test_positioned_overlays_may_share_a_time_window_but_centred_ones_may_not():
    assert ov.validate_scene_overlays(1, [spec(x=0.2, y=0.3), spec(x=0.7, y=0.6)]) == []
    assert ov.validate_scene_overlays(1, [spec(), spec(at_offset_seconds=1.5)])


def test_track_expression_is_piecewise_linear():
    expr = ov.track_expr([(0.0, 100.0), (1.0, 200.0), (3.0, 200.0)], start=5.0)
    assert expr.startswith("if(lt(t,5.000),100.00,")

    def ev(t):   # evaluate the ffmpeg expression the way ffmpeg would
        return eval(expr.replace("if(", "_if("), {"_if": lambda c, a, b: a if c else b, "lt": lambda a, b: a < b, "t": t})

    assert abs(ev(4.0) - 100.0) < 1e-6 and abs(ev(5.5) - 150.0) < 1e-6 and abs(ev(6.0) - 200.0) < 1e-6 and abs(ev(9.0) - 200.0) < 1e-6


def test_counter_runs_from_a_start_value_and_ends_on_the_target():
    s = spec(type="counter", text_or_value="DÍA 70", **{"from": 0})
    assert ov.counter_text(s, 1.0) == "DÍA 70"
    v = [int(ov.counter_text(s, (i + 1) / 30).split()[1]) for i in range(30)]
    assert v == sorted(v) and v[-1] == 70 and v[0] < 70
    s2 = spec(type="counter", text_or_value="100", **{"from": 40})
    assert int(ov.counter_text(s2, 0.01)) >= 40 and ov.counter_text(s2, 1.0) == "100"


def test_chip_is_a_teal_outlined_pill_that_pops_in_with_overshoot():
    meta, frames = render(spec(text_or_value="~500 a. C.", x=0.5, y=0.5))
    assert meta["frames"] == 9 and "left" in meta
    last = frames[-1]
    px = {p for p in last.getdata() if p[3] > 200}
    assert any(abs(r - 103) < 12 and abs(g - 205) < 12 and abs(b - 190) < 12 for r, g, b, a in px), "teal outline missing"
    areas = [sum(1 for p in f.getdata() if p[3] > 0) for f in frames]
    assert max(areas) > areas[-1] * 0.98, "pop should reach its full size"


def test_tag_label_draws_a_leader_to_the_target():
    meta, frames = render({"type": "label", "style": "tag", "text_or_value": "borde", "at_offset_seconds": 0,
                           "x": 0.3, "y": 0.3, "leader_to": [0.6, 0.5], "duration_s": 0.5})
    assert meta["left"] <= 0.3 * ov.W and meta["left"] + meta["w"] >= 0.6 * ov.W - 10
    assert meta["top"] + meta["h"] >= 0.5 * ov.H - 10
    lit = lambda f: sum(1 for p in f.getdata() if p[3] > 0)
    assert lit(frames[-1]) > lit(frames[2]), "the leader grows over the animation"


def test_bracket_ring_mark_render_in_their_colours():
    for s, colour in ((spec(type="bracket", **{"from": [0.3, 0.4], "to": [0.7, 0.4]}), (103, 205, 190)),
                      (spec(type="ring", radius=0.15, x=0.5, y=0.5), (103, 205, 190)),
                      (spec(type="mark", kind="x", x=0.5, y=0.5), (190, 74, 74)),
                      (spec(type="mark", kind="ok", x=0.5, y=0.5), (245, 192, 74))):
        meta, frames = render(s)
        found = {p[:3] for p in frames[-1].getdata() if p[3] > 200}
        assert colour in found, (s["type"], list(found)[:3])


def test_slim_bar_fills_gold_and_can_hide_its_figure():
    meta, frames = render(spec(type="bar", text_or_value="50%", style="slim", marker=0.5, x=0.3, y=0.7, duration_s=0.5))
    gold = lambda f: sum(1 for p in f.getdata() if p[3] > 200 and abs(p[0] - 245) < 6 and abs(p[2] - 74) < 6)
    assert gold(frames[-1]) > gold(frames[3]) > 0
    legacy, _ = render(spec(type="bar", text_or_value="75%", show_value=False))
    assert legacy["w"] > 700


def test_cta_phone_sequence_runs_for_its_duration():
    meta, frames = render(spec(type="cta", message="solo es un corte, no necesito puntos", duration_s=2.0, x=0.5, y=0.55))
    assert meta["frames"] == 60 and (meta["w"], meta["h"]) == (640, 1180)
    assert frames[0].tobytes() != frames[-1].tobytes() and frames[30].tobytes() != frames[-1].tobytes()


def test_subtitle_state_is_white_current_grey_others_and_a_teal_box_on_emphasis():
    bold = ImageFont.truetype(FONT, editor.SUB_FONT_SIZE)
    reg = ImageFont.truetype(next(f for f in ov.FONTS["regular"] if Path(f).exists()), editor.SUB_FONT_SIZE)
    texts = ["los", "bordes", "de"]
    lay = editor.layout_cue(texts, bold)
    with tempfile.TemporaryDirectory() as d:
        p1, p2 = Path(d) / "a.png", Path(d) / "b.png"
        editor.render_cue_state(texts, 1, lay, p1, bold, reg, [False, False, False])
        editor.render_cue_state(texts, 1, lay, p2, bold, reg, [False, True, False])
        a, b = Image.open(p1).convert("RGBA"), Image.open(p2).convert("RGBA")
    has = lambda img, c, tol=10: any(px[3] > 200 and all(abs(px[i] - c[i]) <= tol for i in range(3)) for px in img.getdata())
    assert has(a, editor.SUB_CURRENT_COLOR, 2) and has(a, editor.SUB_WORD_COLOR, 2)
    assert not has(a, editor.SUB_EMPH_COLOR) and has(b, editor.SUB_EMPH_COLOR)
    assert min(c for c in editor.SUB_WORD_COLOR) >= 140       # readable on #120F10 (grey ~55% white)


def test_end_card_validation_and_dimming():
    assert ov.validate_end_card(None) == []
    assert ov.validate_end_card({"duration_s": 4, "handle": "@[CANAL]", "dim": 0.25}) == []
    assert ov.validate_end_card({"duration_s": 40, "handle": "", "dim": 2})
    with tempfile.TemporaryDirectory() as d:
        meta = ov.render_end_card({"handle": "@[CANAL]", "dim": 0.25}, Path(d), "e", 30)
        last = Image.open(Path(d) / f"e-{meta['frames'] - 1:03d}.png").convert("RGBA")
    assert (meta["w"], meta["h"]) == (1080, 1920)
    assert abs(last.getpixel((5, 5))[3] - round(255 * 0.75)) <= 2          # black at 75% alpha = the scene at 25% brightness
    assert any(px[3] > 200 and px[0] > 200 for px in last.crop((300, 800, 780, 1200)).getdata())   # logo/handle drawn


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
