"""Write notes.md of a 2026-11-03-batch production from its script.json (publish package section in the format tools/publish_package.py reads).
    .venv/bin/python tools/notes_from_script.py productions/<channel>/<NNN-slug>
script.json extra fields: description, hashtags (list), departure (identity departure + reason), lens (list), simplifications (list), sources (list), status_notes (list)."""
import json
import sys
from pathlib import Path

prod = Path(sys.argv[1])
s = json.loads((prod / "script.json").read_text(encoding="utf-8"))
L = [f"# {s['video']} ({s['preset']}) — production notes, written by the 2026-11-03 batch run", "",
     "## Publish package (Spanish; the owner publishes)", f"- **Título:** {s['title']}", f"- **Descripción:** {s['description']}",
     "  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)", f"- **Hashtags (description, not title):** {' '.join(s['hashtags'])}", "",
     f"## Script ({len(s['scenes'])} scenes, family {s['topic_family']}) and visual per line"]
for i, sc in enumerate(s["scenes"], 1):
    L.append(f"{i} {sc['name']}: {sc['narration']}  ({sc['transformation']}; camera: {sc['camera']})")
L += [f"Hook formula: {s['hook_question']} | false belief: {s['false_belief'] or '(none: numbers/what-if)'} | reframe: {s['closing_reframe']} | share archetype: {s['share_archetype']}", "",
      "## Identity", f"- Preset: **{s['preset']}**. {s.get('departure', 'Coral default (no departure).')}",
      f"- Support colours: {json.dumps({k: v for k, v in s['support_colours'].items() if k != 'reason'})}: {s['support_colours'].get('reason', '')}", "", "## Lens decisions"]
L += [f"- {x}" for x in s.get("lens", [])]
L += ["", "## Sources and numbers (no number is invented; none is rendered as a source on screen)"] + [f"- {x}" for x in s.get("sources", [])]
L += ["", "## Scientific simplifications and deviations (stated plainly)"] + [f"- {x}" for x in s.get("simplifications", [])]
L += ["", "## Build log"] + [f"- {x}" for x in s.get("status_notes", [])]
(prod / "notes.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("notes.md written")
