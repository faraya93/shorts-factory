# shorts-factory — project brief

## What this is
A factory that produces faceless YouTube Shorts in Spanish, engineered to
maximize views and retention. Every technical choice serves that goal. The
reference format is Zack D Films' stylized 3D "how it works" explainers —
we copy the mechanics, never scripts or footage: all scripts are original.

## How to read doctrine (block B2, 2026-11-11)
This file is the index of the doctrine plus the rules every session needs on every call. Each other rule lives in ONE canonical home, named under its section here; the summary here never adds or removes a condition, and where a summary and its home differ, the home governs. The homes moved out of this file verbatim on 2026-11-11 (`docs/current/reports/doctrine-b2-2026-11-11.md`) and keep the authority and precedence they had here: `docs/current/specs/doctrine-topics-and-scripts.md`, `doctrine-format-and-look.md`, `doctrine-production.md`, `doctrine-pipeline.md` (same folder).
- **Read one section, not a file:** `.venv/bin/python tools/doc_section.py <file> "<section>"` (`--list` shows a file's sections and sizes). A whole-file Read stays in context for every later call; read a whole spec only when the task is that spec.
- **Size budget:** this file stays under 22,000 bytes (`tests/test_layout.py`). New rule text goes to its home; this file gets at most a short summary and the pointer.

## Governance (owner instruction, 2026-11-04; wins over older text in this file)
The owner does not want to ban anything for the system, and does not want creative or technical decisions escalated one by one. Standing authority, effective 2026-11-04: **the lenses may decide and execute creative and technical matters on their own**, including installing additional free tools (a skill only through "Project skills", which owns the list), changing identity elements such as the Coral stage colour, and adjusting doctrine, methods and sources.
- **The one condition:** ALL involved lenses approve under the existing governance (docs/architecture.md "Multi-lens protocol"), disagreements are settled against measured criteria and written doctrine, never by who argues hardest, and the decision is recorded with its reason in `docs/current/reports/lens-decisions.md` so it can be audited and reverted. If the lenses cannot settle it on those terms, it is not approved: get a measurement, and the current doctrine stands until then.
- **Owner-only, NOT delegated:** spending any money, publishing anything, creating accounts, and the final publish/reject verdict on a finished video (the owner's eye stays the last gate on output).
- **Topic-level outcomes are never escalated to the owner (owner statement, 2026-11-08):** the owner is not attached to any topic or idea. Re-staging a topic, returning it and replacing it from the idea bank are lens and system decisions under standing doctrine. The owner's only touchpoint is his verdict on FINISHED videos; publishing still requires his verdict per video.
- **Reports** state what the lenses decided and why. A "decisions for you" section is reserved for the owner-only list.
- **Video structure is a lens decision too (owner directive, 2026-11-04):** the scene template, the beat sequence and the closing with its spoken CTA, decided as a channel-level policy. Current policy: "Format policy" below.
- Older text in this file that reserves a creative or technical choice for the owner (topics, scripts, beat sheets, voice, music, identity, format exceptions) is read through this section. Spend gates, the publish rule and the no-accounts rule keep their full force.

## Amending doctrine (standing procedure, owner 2026-11-10)
Every change to doctrine follows this procedure; later instructions invoke it by name instead of restating it.
1. **One canonical home per rule.** Other places point to it or summarise it.
2. **Align every live restatement:** this file, specs, skills, brand packages, and any other text read as current.
3. **Never rewrite historical or dated records** (decision rows, dated reports, production notes, archives). Add a new dated entry instead.
4. **Every amendment carries a "what did not change" section and a precedence line.**
5. **Check the amendment against standing doctrine** and list the checks in its report.
6. **Fossil scan:** grep the live procedure surfaces the amendment touches (this file, current specs including the doctrine homes, this project's skills) for production numbers and calendar dates. Generalise, or move to records, each one that states a transition fact (something that will later read as false or inert) rather than a standing rule. Dated records and decision rows are history and are never scanned for removal.
7. **Record it** in `docs/current/reports/lens-decisions.md`.
8. **Size budget (2026-11-11):** the rule text goes to its canonical home; this file keeps it under the budget in "How to read doctrine".

## Project skills (lens decision 2026-11-11; allowlist for sessions in this repo)
**This section is the canonical list** of the skills sessions here may use: `produce`, `blender-core`, `blender-kiln`, `blender-asset-qa`, `blender-scene-setup`, `blender-retopology-uv`, `blender-character-rigging`, `blender-workflow-recipes`, `blender-hardsurface-modeling`, `blender-sculpting`, `blender-geometry-nodes`, `blender-pbr-materials`, `blender-texture-baking`, `blender-lighting-lookdev`, `blender-animation`, `blender-simulation`, `short-form-video-script`, `hook-writer`, `yt-script`, `yt-seo`, `youtube-shorts`, `social-seo`, `thumbnail-design`, `tastemaker`, `design-taste-frontend`. Each one's role and evidence: `docs/current/specs/project-skills.md`. About 196 skill folders sit at user level (`~/.claude/skills/`), shared with the owner's other projects; none is moved, renamed or deleted for this repo's sake. `blender-core`'s `run_in_blender.py` runs only through `tools/blender_run.py --skill`; `blender-kiln` serves asset sourcing and likeness measurement only (never its full pipeline, Studio or AI backends).
**Rule:** sessions working in this repo use only the skills on this list. A task matching some other installed skill's description is not an invitation to use it. If a task needs a capability no listed skill covers, report that instead of reaching for an unlisted skill. Cross-references between listed skills and unlisted ones ("see also", "reads brand-profile first", routes to games or social platforms) are not adopted; the repo's own `channels/mecanalia/brand.yaml` is the brand profile. **Adding a skill** (installed or already present) is sanctioned only when the same recorded lens decision adds it to this list and to `project-skills.md` in the same commit; a skill's own text is read in full before it is listed.

## Format policy (lens decision 2026-11-04; home: docs/current/specs/format-policy.md)
One fixed signature (voice, identity, typography, subtitles, hook formula, one hero or mechanism, dynamics inside the shot, one reframe, the closing slot), five structures (`structure_variant`: `chain`, `journey`, `scale`, `fork`, `story` = Historia, one complete real story with a mechanism heart, sourced fact by fact) and three staging modes (`stage`, `world`, `cutaway`; no mode more than three times in five consecutive productions). Scene count follows the mechanism (sanity range 4-10, never padded or merged); never three in a row with the same variant or the same scene count. Closing: reframe, then one sentence with the fixed word "envíaselo" and its word-locked tag, ending on the person; `fork` repeats the opening question. Where older live text describes a fixed structure or closing, the policy governs.

## Format doctrine (home: doctrine-format-and-look.md "Format doctrine")
Vertical 9:16; narration 45-60 s standard (body 40-50, numbers 50-60, Historia 55-75) at the voice's measured pace. Title: short question or "How X works", one trailing emoji, no hashtags. Hook: the first sentence is a question about a tangible everyday object plus an explicit false belief, with the approved openings per family; never "¿Cómo…?". Each scene shows one step (new fact, new visual); numbers are Editor overlays; dynamics inside the shot; closing reframe, follow, share ask naming `share_archetype`. Four topic families, pan-Hispanic neutral Spanish. Stylised 3D, never photorealistic, no real skin texture, no blood, no gore. Model-generated style strings contain "no text on screen". Voice es-CL-LorenzoNeural, voice-led audio. Montserrat typography; burned-in subtitles in the upper band. Three engines, one primary engine per production ("Engine selection").

## Search and packaging (lens decision 2026-11-08, forward-only; home: docs/architecture.md "Search and packaging policy")
Title = the query a viewer types, approved question form, object word first, one trailing emoji, no hashtags. Description: line 1 question + one-clause answer, line 2 the twist, then the share line. The channel has ONE public playlist, "Empieza aquí", created by the owner; the four families are internal taxonomy only. Published packages are never edited.

## Channel identity (ADOPTED 2026-10-28, owner; provisional; home: doctrine-format-and-look.md "Channel identity", spec docs/current/specs/design-system.md)
Identity is PARAMETERS in `channels/mecanalia/brand.yaml` (`identity`, `render`), read through `factory/identity.py`; to switch, edit the parameters and re-render, never code. Active: CORAL. Where this identity and the "Reference doctrine" palette disagree, the identity wins. No CTA phone, no appended end card. Render default: the tuned Cycles profile; the grain pass is mandatory.

## Closing standard (ratified 2026-10-28, owner; home: doctrine-format-and-look.md "Closing standard")
Every video closes with the spoken follow + share ask naming the share_archetype and ONE tiny ink "ENVÍASELO" tag word-locked to "envíaselo" in the last scene; overlay types `cta` and `end_card` are never used by new productions.

## Reference doctrine (binding, owner 2026-10-26; home: doctrine-format-and-look.md "Reference doctrine")
The look (reference-style-spec.md) and the storytelling grammar (reference-format-spec.md) are binding: luminous subject on a stage, chunky simplified heroes, emissive energy, clean cross-sections, a camera that never rests, the caption band kept clear; every sentence changes something on screen, every number is a screen object that appears on its spoken word and is never invented (an unsourced figure is flagged), SOURCES ARE NEVER RENDERED ON SCREEN, events word-locked to ±0.3 s. A production brief is a BEAT SHEET approved by all involved lenses before any generation.

## Pipeline (home: doctrine-pipeline.md "Pipeline")
Runner session mechanics (context cap and checkpoint handoff, fresh callback with the package built by code, startup isolation, inline-Python hook, stamp hash check, `tools/status.py`, `tools/iterate.py`): `doctrine-pipeline.md` "Runner session mechanics". Deterministic code wherever money or precision is involved; LLMs only where judgment is involved. Producer (`factory/producer.py`): schema-validated before any estimate, estimate before spend, >US$1 needs the owner's OK, US$3 hard cap, max 2 attempts per scene, resumable, every generation logged. Scene schema (`factory/scenes_schema.py`) and its required fields; Editor (`factory/editor.py`), audio layers and the clip-audio gate (never retune its threshold silently), Editor v2 overlays and word locks, the shared visual identity and unify pass.

## code3d sourcing and optimization (binding, owner 2026-10-25; home: doctrine-production.md "code3d sourcing and optimization")
The fastest route to each clip: libraries first, free tiers only (never sign up or pay; Tripo's free tier never), every asset logged in LICENSES.md, verify tools live, draft quality while iterating and one final render, never remodel what exists locally. For heroes, "Asset library and hero routing" governs.

## Channel strategy (owner decisions, 2026-10-25; home: doctrine-format-and-look.md "Channel strategy")
Pan-Hispanic, ONE umbrella channel ("why/how the things you see and use every day work") rotating four families under one format, voice and brand. A channel is configuration (brand package + thin language variants, `factory/channel.py`), never hard-coded, with NO credentials in packages. Spin-offs only by data.

## Asset library and hero routing (binding, owner 2026-11-04; home: doctrine-production.md "Asset library and hero routing", manual docs/current/specs/asset-system.md)
Geometric heroes may be code primitives; anything organic, soft or complex takes the asset route (search `assets/registry.yaml`; in doubt, asset route); every finished object lands in `assets/library/<slug>/` and is never solved twice. Likeness gate: three isolated readers, mean >= 60, none under 45, never an added alias. CC0 first, then Royalty-Free, then CC-BY without asking and without a description credit; NC/ND/SA/unknown never. Sessions create no accounts.

## Every element at hero standard (binding, owner 2026-11-05; home: doctrine-production.md "Every element at hero standard")
Routing and the likeness gate apply to the key represented element of EVERY scene (`scene_elements`), materials included; no flat-colour stand-ins for organic, liquid or real-world elements. Event elements (sparks, arcs) declare `kind: "event"` and verb-form aliases before any reading (2026-11-11).

## Render cost (binding from production 012, 2026-11-08; playbook: docs/current/specs/render-cost-playbook.md)
Finals render at 75% and the editor upscales. Each scene declares `render_cost_class` in the beat sheet and scenes.json; a class predicted above 15 s/frame needs `cost_restage` on paper before modelling. Optical fidelity is negotiable; the likeness bar is not, and a route that changes an element's look needs a new reading.

## Gate v2 (binding from production 012, 2026-11-08; home: doctrine-production.md "Gate v2", manual asset-system.md "Gate v2")
`gate_version: 2`; hero first and frozen (`gate.py freeze`/`unfreeze`); element-scoped invalidation; readers only through `tools/blind_read.py --record`; every reading counts, never re-roll; `gate.py carry` only when the stills match.

## Script flatness, floor handling and modellability (binding, owner 2026-11-06; home: doctrine-topics-and-scripts.md "Script flatness, floor handling and modellability")
A script is FLAT if its scenes are variations of one action or state (scene-swap test); every script needs event progression, the turn before the closing reframe, and a "what changes in the world" line per scene. The likeness floor stays 60 for all future productions. Topics are judged for modellability with the context-cue check.

## Topic selection: curiosity test and one-line hook test (binding, owner 2026-11-07; home: doctrine-topics-and-scripts.md "Topic selection")
Topics must pass the CURIOSITY TEST (a question the viewer already carries, ideally with a tense side) and the ONE-LINE HOOK TEST, on top of the standing screens. TOPIC BALANCE: in any five consecutive productions at most two share a theme (theme = the specific subject) and at least three tensions appear. Family mix is an outcome, never a target.

## Idea bank (binding, owner 2026-11-07; home: doctrine-topics-and-scripts.md "Idea bank")
`docs/current/idea-bank.md`: a ranked BANKED tier (drawable) and a RESERVE tier (not drawable, re-scored at every fill), filled by an Opus session through the standard fill cycle (read first, generate wide, preliminary screen, concept-level ladder check, entry fields, pool and rank, balance-aware cut, depth of ten, commissioning scan). **Drawing** and **Who writes the script (amended 2026-11-11):** EVERY script is written by an Opus creative session, which stamps the folder (`factory/provenance.py`); a production session never draws from the raw bank and never writes a script; the runner refuses an unstamped unit. Returns are replaced only from stamped developed standbys, otherwise the replacement waits for a creative session. The creative session also writes each risky element's ladder fallbacks and its blind proofs (`proofs.json`); a unit joins a batch only after every proof passes (2026-11-11).

## Reshape ladder (binding, owner 2026-11-07; home: doctrine-production.md "Reshape ladder")
A scene that is hard to model or fails the likeness gate works the ladder in order without stalling the production: 1 re-stage, 2 rewrite the beat, 3 adjust the narration, 4 context staging (one attempt per element). Written fallbacks first; reading budget (2026-11-11): at most two readings per element at each of rungs 1-3, exactly one at rung 4. **Where the ladder stops:** before replacing the hero mechanism or the promise; then the topic is returned. Every rung keeps every standing bar; never laddered around the hard rules.

## Production notes ledger (2026-11-11; home: doctrine-production.md "Production notes ledger")
A production's notes.md is a ledger: a short current header, then one appended line per event (what changed, rung, why). Forward-only.

## Dynamism is a hard bar (binding, owner 2026-11-05; home: doctrine-production.md "Dynamism is a hard bar")
No video holds one static tableau while only a counter changes: every scene stages a visible change in the world AND a travelling camera; escalation is movement the viewer travels through; no two consecutive scenes share the same camera move and distance; at least three framings per video. Checked on a first/middle/last contact sheet before the final render.

## Engine selection (binding; from the 2026-10-25 engine spike; home: doctrine-production.md "Engine selection")
The factory assigns ONE primary engine per production automatically (never asks the owner): organic/ambient → t2v, rigid geometric and numbers spectacle → code3d; code3d is never mixed with diffusion footage; keyframes is disabled (`scenes_schema.DISABLED_ROUTES`); every assignment logged with a reason.

## Support colours and composition gate (binding, owner 2026-10-28; home: doctrine-production.md "Support colours and composition gate")
The stage colour is background only; support colours are parameters with CIEDE2000 >= 20 separation, chosen per production. The composition gate is a hard block on `code3d_render.py --mode final`.

## Repository organization (binding, owner 2026-10-31; home: doctrine-pipeline.md "Repository organization", spec docs/architecture.md)
Every new file goes in its correct place. New videos only with `.venv/bin/python tools/new_production.py <channel-id> <slug>`; experiments in `productions/_lab/`, superseded work moved with `git mv` to `productions/_archive/`. Docs: `docs/current/{specs,reports,research}/`, `docs/experiments/`, `docs/archive/`. Never delete material; update every reference when moving a path and run the full test suite. Editing a rig library, even a comment, invalidates composition-gate records.

## House rules (home: doctrine-pipeline.md "House rules")
- Never spend without showing the estimate first; the gates are rules, not suggestions. Estimate tables before, actuals after (fal dollars from live prices, effort, render time). Stop and report if a scene passes 60 min or 2x its estimate.
- Verify fal.ai model IDs and prices live, never from memory. The fal key lives only in .env: never print, commit or echo it.
- Code, comments, filenames and JSON keys in English; narration and titles in Spanish. ALWAYS respond to the owner in English.
- **One launcher for Blender:** every headless Blender through `tools/blender_run.py` (GPU lock, one job at a time, caffeinate; a skill helper as `.venv/bin/python tools/blender_run.py --skill -- <helper.py> <args>`); finals queued through `tools/queue_chain.sh`. **Every render launch runs under `caffeinate -dimsu`;** say so if one ever did not.
- Commit and push after each working phase; never commit media files or .env.
- **A failed sub-step never passes silently:** grep a production's chain log for FAILED/INCOMPLETE/Traceback, not just DONE.
- No credits in descriptions; NO MUSIC unless the owner approves a track.
- Render-time operations: EEVEE drafts for the session's own checks, half-resolution Cycles stills for readers and the colour gate, one full final per scene after it passes; Blender jobs strictly one at a time.
- Report failures and semantically wrong renders plainly. You cannot hear audio or watch video: verify mechanically and never claim more.
