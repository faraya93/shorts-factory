"""scenes.json schema: validation and final prompt assembly. Pure functions: no network, no spend.

Used by the Producer before any estimate or API call, so an incomplete or contradictory
production aborts with zero spend. Run `python factory/scenes_schema.py <production>` to check one.
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

import visual_identity
from overlays import validate_scene_overlays

ENGINES = ("t2v", "keyframes", "code3d")
# A route that failed the engine spike is DISABLED until it is re-tested; this maps route -> why.
DISABLED_ROUTES = {
    "keyframes": "failed the engine spike on stitches scene 2 (2026-10-25): warped hands/arms and no continuity "
                 "between stills; re-test before re-enabling",
}
FAMILIES = ("objects", "body", "numbers", "whatif")
FALSE_BELIEF_OPTIONAL = ("numbers", "whatif")  # the only families that may leave false_belief empty
NO_TEXT_CLAUSE = "no text on screen"
# approved hook openings per topic family; a hook is a question: starts with ¿ and ends with ?
HOOK_OPENINGS = {
    "objects": ("¿Por qué",),
    "body": ("¿Por qué",),
    "numbers": ("¿Por qué", "¿Cuántos", "¿Cuántas", "¿Sabías que"),
    "whatif": ("¿Qué pasaría si", "¿Por qué"),
}
ARROW_RE = re.compile(r"\s*(?:→|->)\s*")
STATIC_CAMERAS = {"static", "fixed", "still", "none", "locked"}

PRODUCTION_TEXT_FIELDS = ("hook_question", "closing_reframe", "share_archetype")
SCENE_FIELDS = ("id", "name", "prompt", "narration", "target_duration_s", "transformation", "camera")


def _fold(text: str) -> str:
    """Lower-case and strip accents, so '¿Por que' and '¿Sabias que' still match their approved opening."""
    decomposed = unicodedata.normalize("NFD", text.strip().lower())
    return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")


def hook_errors(hook: str, family: str | None) -> list[str]:
    hook = hook.strip()
    if not (hook.startswith("¿") and hook.endswith("?")):
        return [f"hook_question must be a question (start with ¿, end with ?), got {hook!r}"]
    openings = HOOK_OPENINGS.get(family)
    if openings is None:  # invalid family is reported on its own
        return []
    folded = _fold(hook)
    for opening in openings:
        o = _fold(opening)
        if folded.startswith(o) and (len(folded) == len(o) or not folded[len(o)].isalnum()):
            return []
    return [f"hook_question for a {family!r} topic must open with one of {openings}, got {hook!r}"]


def effective_engine(cfg: dict, scene: dict) -> str:
    """The engine a scene is produced with: its override, else the production's primary engine."""
    return scene.get("engine_override") or cfg.get("primary_engine", "")


def validate_production(cfg: dict) -> list[str]:
    """Return every schema violation (empty list = valid)."""
    errors = []
    primary = cfg.get("primary_engine")
    family = cfg.get("topic_family")

    if primary not in ENGINES:
        errors.append(f"primary_engine must be one of {ENGINES}, got {primary!r}")
    elif primary in DISABLED_ROUTES:
        errors.append(f"primary_engine {primary!r} is disabled: {DISABLED_ROUTES[primary]}")
    if not str(cfg.get("engine_reason", "")).strip():
        errors.append("missing production field: engine_reason (one line: why this primary engine)")
    if family not in FAMILIES:
        errors.append(f"topic_family must be one of {FAMILIES}, got {family!r}")
    for field in PRODUCTION_TEXT_FIELDS:
        if not str(cfg.get(field, "")).strip():
            errors.append(f"missing production field: {field}")
    hook = str(cfg.get("hook_question", "")).strip()
    if hook:
        errors += hook_errors(hook, family)
    if "false_belief" not in cfg:
        errors.append("missing production field: false_belief (use an empty string where it may be empty)")
    elif not str(cfg["false_belief"]).strip() and family not in FALSE_BELIEF_OPTIONAL:
        errors.append(f"false_belief may be empty only for {FALSE_BELIEF_OPTIONAL} topics (family is {family!r})")

    # model-generated footage must forbid on-screen text: labels and numbers are Editor overlays
    if primary != "code3d" and NO_TEXT_CLAUSE not in str(cfg.get("style", "")).lower():
        errors.append(f"style string must contain '{NO_TEXT_CLAUSE}' for model-generated footage")

    if "visual_identity" in cfg:  # optional until the channel config exists; validated whenever present
        errors += visual_identity.validate(cfg["visual_identity"])

    scenes = cfg.get("scenes") or []
    if not scenes:
        errors.append("no scenes")
    for s in scenes:
        sid = s.get("id", "?")
        for field in SCENE_FIELDS:
            if field not in s or not str(s[field]).strip():
                errors.append(f"scene {sid}: missing {field}")
        t = str(s.get("transformation", "")).strip()
        if t and len(ARROW_RE.split(t, maxsplit=1)) != 2:
            errors.append(f"scene {sid}: transformation must read 'start state → end state', got {t!r}")
        elif t and not all(part.strip() for part in ARROW_RE.split(t, maxsplit=1)):
            errors.append(f"scene {sid}: transformation needs both a start and an end state, got {t!r}")
        cam = str(s.get("camera", "")).strip().rstrip(".").lower()
        if cam in STATIC_CAMERAS:
            errors.append(f"scene {sid}: camera must move (travels, orbits, tracks), got {cam!r}")

        if s.get("shot_type", "establishing") not in visual_identity.SHOT_TYPES:
            errors.append(f"scene {sid}: shot_type must be one of {visual_identity.SHOT_TYPES}, got {s['shot_type']!r}")
        if "qa_note" in s and not str(s["qa_note"]).strip():
            errors.append(f"scene {sid}: qa_note must not be empty")

        if "data_overlays" in s:
            errors += validate_scene_overlays(sid, s["data_overlays"])

        override = s.get("engine_override")
        if override is not None:
            if not str(s.get("engine_override_reason", "")).strip():
                errors.append(f"scene {sid}: engine_override needs engine_override_reason (one line)")
            if override in DISABLED_ROUTES:
                errors.append(f"scene {sid}: engine_override {override!r} is disabled: {DISABLED_ROUTES[override]}")
            elif primary == "code3d":
                errors.append(f"scene {sid}: a code3d production is code3d in every scene (no engine_override)")
            elif override == "code3d":
                errors.append(f"scene {sid}: code3d is never mixed into a non-code3d production")
            elif override != "keyframes":
                errors.append(f"scene {sid}: engine_override may only be 'keyframes', got {override!r}")
            elif primary != "t2v":
                errors.append(f"scene {sid}: engine_override keyframes is only allowed inside a t2v production")
    return errors


def build_prompt(cfg: dict, scene: dict) -> str:
    """Final generation prompt: style + visual identity (if any) + scene prompt + transformation + camera
    + audio_style (if any)."""
    start, end = ARROW_RE.split(scene["transformation"].strip(), maxsplit=1)
    parts = [cfg["style"].strip()]
    if cfg.get("visual_identity"):  # every engine consumes the identity literally, right after the style string
        parts.append(visual_identity.identity_clause(cfg["visual_identity"]))
    parts += [scene["prompt"].strip(),
             f"Transformation during the shot: {start.strip().rstrip('.')} becoming {end.strip().rstrip('.')}.",
             f"Camera: {scene['camera'].strip().rstrip('.')}."]
    if cfg.get("audio_style"):
        parts.append(cfg["audio_style"].strip())
    return " ".join(parts)


if __name__ == "__main__":
    config = json.loads((Path(sys.argv[1]) / "scenes.json").read_text(encoding="utf-8"))
    problems = validate_production(config)
    print("\n".join(f"  - {p}" for p in problems) if problems else "scenes.json: OK")
    sys.exit(1 if problems else 0)
