"""Build a code3d production's scenes.json from a compact hand-authored `script.json` in the production folder (2026-11-03 batch).
    .venv/bin/python tools/scenes_from_script.py productions/<channel>/<NNN-slug>
script.json: {video,title,topic_family,preset,prefix,engine_reason,hook_question,false_belief,closing_reframe,share_archetype,caption_draft,support_colours,hero_colours,
rig_libs,gate_stills,scenes:[{name,narration,transformation,camera,emphasis:[..],overlays:[..]}]}. Everything else (audio block, voice, no-music, identity embed) is fixed here."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import identity  # noqa: E402

prod = Path(sys.argv[1])
s = json.loads((prod / "script.json").read_text(encoding="utf-8"))
d = {"channel": "mecanalia-es", "video": s["video"], "title": s["title"], "topic_family": s["topic_family"], "primary_engine": "code3d", "engine_reason": s["engine_reason"],
     "hook_question": s["hook_question"], "false_belief": s["false_belief"], "closing_reframe": s["closing_reframe"], "share_archetype": s["share_archetype"],
     **{k: s[k] for k in ("hero_route", "library_assets") if k in s},
     "model": "blender-5.2.3-cycles", "voice": "es-CL-LorenzoNeural", "resolution": "1080x1920", "aspect_ratio": "9:16",
     "style": "Not used: code3d scenes are rendered in Blender from the visual_identity block (exact hex values).",
     "visual_identity": {}, "render_style": s["prefix"] + "-set", "scene_script_prefix": s["prefix"],
     "audio": {"narration_volume": 1.0, "effects_volume": 0.3, "music_volume": 0.1, "clip_audio": "off", "music_file": None, "music_credit": None, "clip_gate_db": -35},
     "render_args": [], "identity_preset": s["preset"], "caption_draft": s["caption_draft"], "gate_stills": s["gate_stills"], "rig_libs": s["rig_libs"],
     "support_colours": s["support_colours"], "hero_colours": s.get("hero_colours", {}), "scenes": []}
for i, sc in enumerate(s["scenes"], 1):
    d["scenes"].append({"id": i, "name": sc["name"], "prompt": f"Escena dibujada con código ({s['preset']}): {sc['name']}.", "narration": sc["narration"],
                        "target_duration_s": sc.get("target_duration_s", 8), "transformation": sc["transformation"], "camera": sc["camera"], "shot_type": "establishing",
                        "subtitle_emphasis": sc.get("emphasis", []), "data_overlays": sc.get("overlays", [])})
(prod / "scenes.json").write_text(json.dumps(d, indent=2, ensure_ascii=False), encoding="utf-8")
identity.apply_to_scenes(prod / "scenes.json", s["preset"])
print("scenes.json written:", len(d["scenes"]), "scenes,", sum(len(x["narration"].split()) for x in d["scenes"]), "words")
