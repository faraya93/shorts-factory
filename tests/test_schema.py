"""Plain-assert tests for factory/scenes_schema.py. Run: python tests/test_schema.py"""

import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "factory"))
import scenes_schema  # noqa: E402
from scenes_schema import build_prompt, effective_engine, validate_production  # noqa: E402

VALID = {
    "primary_engine": "t2v",
    "engine_reason": "Organic transformation and camera travel: t2v.",
    "topic_family": "objects",
    "hook_question": "¿Por qué la punta de una cinta métrica está floja?",
    "false_belief": "It is a manufacturing defect.",
    "closing_reframe": "No está floja: se mueve el grosor de la propia punta.",
    "share_archetype": "ese amigo que siempre mide mal",
    "style": "Bright stylized 3D cartoon animation, no text on screen.",
    "audio_style": "Audio: foley only.",
    "scenes": [
        {"id": 1, "name": "hook", "prompt": "A tape measure on a table.", "narration": "x", "target_duration_s": 5,
         "transformation": "closed tape → fully extended tape", "camera": "slow orbit around the tape"},
        {"id": 2, "name": "tip", "prompt": "The metal tip slides.", "narration": "y", "target_duration_s": 5,
         "transformation": "tip pressed in → tip pulled out", "camera": "tracks along the blade"},
    ],
}


def errors_for(**changes):
    cfg = copy.deepcopy(VALID)
    for key, value in changes.items():
        if value is None:
            cfg.pop(key, None)
        else:
            cfg[key] = value
    return validate_production(cfg)


def scene_errors(index, **changes):
    cfg = copy.deepcopy(VALID)
    for key, value in changes.items():
        if value is None:
            cfg["scenes"][index].pop(key, None)
        else:
            cfg["scenes"][index][key] = value
    return validate_production(cfg)


def expect(errors, fragment):
    assert any(fragment in e for e in errors), f"expected an error containing {fragment!r}, got {errors}"


def test_valid_passes():
    assert validate_production(VALID) == []


def test_missing_production_fields_abort():
    for field in ("primary_engine", "hook_question", "closing_reframe", "share_archetype", "topic_family"):
        assert errors_for(**{field: None}), field


def test_hook_must_be_a_question():
    expect(errors_for(hook_question="Por qué se mueve la punta"), "must be a question")
    expect(errors_for(hook_question="¿Por qué se mueve la punta"), "must be a question")
    expect(errors_for(hook_question="Por qué se mueve la punta?"), "must be a question")


def test_hook_openings_per_family():
    ok = {
        "objects": ["¿Por qué se mueve la punta?", "¿POR QUE se mueve la punta?"],
        "body": ["¿Por qué bostezas cuando otro bosteza?"],
        "numbers": ["¿Por qué nunca se repite un mazo barajado?", "¿Cuántos mazos distintos existen?",
                    "¿Cuántas partidas de ajedrez son posibles?", "¿Sabías que barajas algo irrepetible?",
                    "¿Sabias que barajas algo irrepetible?"],
        "whatif": ["¿Qué pasaría si desaparece la Luna?", "¿Que pasaria si cae internet?", "¿Por qué lo harías?"],
    }
    for family, hooks in ok.items():
        for hook in hooks:
            assert errors_for(topic_family=family, hook_question=hook, false_belief="x") == [], (family, hook)
    bad = {
        "objects": ["¿Cómo funciona una cinta métrica?", "¿Sabías que la punta está floja?", "¿Cuántos dientes tiene?"],
        "body": ["¿Qué pasaría si no bostezas?", "¿Cuántos puntos te ponen?"],
        "numbers": ["¿Cómo se calcula 52!?", "¿Qué pasaría si barajas siempre?"],
        "whatif": ["¿Cuántos días sin internet?", "¿Sabías que internet puede caer?", "¿Cómo sería sin Luna?"],
    }
    for family, hooks in bad.items():
        for hook in hooks:
            expect(errors_for(topic_family=family, hook_question=hook, false_belief="x"), "must open with one of")
    # an opening must be a whole word: '¿Por quésito…' is not '¿Por qué'
    expect(errors_for(hook_question="¿Por quésito se mueve?"), "must open with one of")


def test_false_belief_optional_only_for_numbers_and_whatif():
    expect(errors_for(false_belief=""), "false_belief may be empty only")
    assert errors_for(false_belief="", topic_family="numbers") == []
    assert errors_for(false_belief="", topic_family="whatif") == []
    expect(errors_for(false_belief=None), "missing production field: false_belief")


def test_style_needs_no_text_for_model_footage():
    expect(errors_for(style="Bright stylized 3D cartoon animation."), "no text on screen")
    assert errors_for(style="Flat code render.", primary_engine="code3d") == []


def test_scene_requires_transformation_and_camera():
    expect(scene_errors(0, transformation=None), "scene 1: missing transformation")
    expect(scene_errors(1, camera=None), "scene 2: missing camera")
    expect(scene_errors(0, transformation="a closed tape"), "start state → end state")
    expect(scene_errors(0, transformation="closed tape →"), "start and an end")
    expect(scene_errors(0, camera="static"), "camera must move")


def test_engine_override_rules():
    saved = dict(scenes_schema.DISABLED_ROUTES)
    scenes_schema.DISABLED_ROUTES.clear()  # these rules are about structure; disabling is tested below
    try:
        ok = dict(engine_override="keyframes", engine_override_reason="contact mechanics")
        assert scene_errors(1, **ok) == []
        expect(scene_errors(1, engine_override="keyframes"), "needs engine_override_reason")
        expect(scene_errors(1, engine_override="code3d", engine_override_reason="x"), "never mixed")
        expect(scene_errors(1, engine_override="t2v", engine_override_reason="x"), "may only be 'keyframes'")
        cfg = copy.deepcopy(VALID)
        cfg["primary_engine"] = "keyframes"
        cfg["scenes"][1].update(ok)
        expect(validate_production(cfg), "only allowed inside a t2v production")
        cfg["primary_engine"] = "code3d"
        cfg["style"] = "Flat code render."
        expect(validate_production(cfg), "code3d in every scene")
    finally:
        scenes_schema.DISABLED_ROUTES.update(saved)


def test_routes_that_failed_the_spike_are_disabled():
    assert "keyframes" in scenes_schema.DISABLED_ROUTES
    expect(scene_errors(1, engine_override="keyframes", engine_override_reason="contact mechanics"), "is disabled")
    cfg = copy.deepcopy(VALID)
    cfg["primary_engine"] = "keyframes"
    expect(validate_production(cfg), "primary_engine 'keyframes' is disabled")


def test_every_engine_assignment_is_logged_with_a_reason():
    expect(errors_for(engine_reason=None), "engine_reason")
    expect(errors_for(engine_reason="  "), "engine_reason")


def test_prompt_assembly_order():
    prompt = build_prompt(VALID, VALID["scenes"][0])
    order = [VALID["style"], VALID["scenes"][0]["prompt"], "Transformation during the shot: closed tape becoming "
             "fully extended tape.", "Camera: slow orbit around the tape.", VALID["audio_style"]]
    positions = [prompt.index(part) for part in order]
    assert positions == sorted(positions), prompt
    no_audio = copy.deepcopy(VALID)
    del no_audio["audio_style"]
    assert build_prompt(no_audio, no_audio["scenes"][0]).endswith("Camera: slow orbit around the tape.")


def test_effective_engine():
    assert effective_engine(VALID, VALID["scenes"][0]) == "t2v"
    assert effective_engine(VALID, {"engine_override": "keyframes"}) == "keyframes"


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
