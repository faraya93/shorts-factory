# Standing doctrine: pipeline, house rules and repository

Moved verbatim out of CLAUDE.md on 2026-11-11 (block B2, P14 "CLAUDE.md diet", `docs/current/reports/doctrine-b2-2026-11-11.md`); later amendments are recorded in `docs/current/reports/lens-decisions.md`. Each section below is the CANONICAL HOME of its rules; CLAUDE.md keeps a summary under the same section name and points here. Where a summary and this text differ, this text governs.

**Precedence.** These files (`doctrine-topics-and-scripts.md`, `doctrine-format-and-look.md`, `doctrine-production.md`, `doctrine-pipeline.md`) and CLAUDE.md are ONE body of doctrine: a precedence statement written in CLAUDE.md before the move ("this section wins", "supersedes ...", "where older text in this file ...") keeps the meaning it had there, wherever the sections it names now live. "This file" in moved text means that body of doctrine.

**Reading.** Read one section at a time: `.venv/bin/python tools/doc_section.py docs/current/specs/doctrine-pipeline.md "<section>"` (`--list` shows the sections and their sizes). Never read the whole file to follow one pointer.


## Pipeline
Deterministic code wherever money or precision is involved; LLMs only
where judgment is involved.
- factory/producer.py — scenes.json → fal.ai clips. Estimate before
  spending; >US$1 requires the owner's explicit OK; US$3 hard cap per
  run; max 2 attempts per scene; scenes with a valid clip are skipped
  (runs are resumable, never pay twice); every generation is logged to
  the production's costs.json at the normal (non-promo) rate; one fixed
  seed per production; prompt_expansion always "disabled". scenes.json
  is validated by factory/scenes_schema.py BEFORE any estimate or network
  call: an incomplete or contradictory file aborts with zero spend. The
  final prompt is: style string + scene prompt + transformation + camera
  + audio_style (t2v/keyframes routes). The producer implements t2v only
  so far; other routes abort before spend until they are built.
- Scene schema (scenes.json), all REQUIRED unless noted. Production
  level: primary_engine (t2v | keyframes | code3d), topic_family
  (objects | body | numbers | whatif), hook_question (a question
  with an approved opening for the topic_family), false_belief (the wrong idea the video corrects; may be ""
  ONLY for numbers and whatif topics), closing_reframe (the sentence that
  renames the object/fact), share_archetype (the specific person the
  spoken closing names). Scene level: transformation ("start state → end
  state"), camera (how it moves; static is rejected), plus id, name,
  prompt, narration, target_duration_s, and foley (the diegetic sounds
  wanted; required for t2v/keyframes scenes). Optional: engine_override
  ("keyframes", only inside a t2v production; needs engine_override_reason),
  audio_style (legacy), caption_draft, shot_type, qa_note, data_overlays,
  visual_identity. engine_reason (one line: why this primary engine) is
  REQUIRED at production level. A route listed in
  scenes_schema.DISABLED_ROUTES is rejected as primary engine or override.
  Any other override, or any code3d scene in a non-code3d production,
  aborts before spend. Productions created before this schema (pilot v1,
  puntos-de-sutura-v2) are frozen controls and no longer pass validation.
- factory/editor.py — narration per scene (edge-tts) sets the timeline;
  clips are trimmed, slowed (max 1.25x) or last-frame-frozen to fit;
  subtitles are rendered as PNG overlays (this machine's ffmpeg has no
  libass); outputs final.mp4 (1080x1920, 30 fps, H.264/AAC) + cover.jpg.
- Audio architecture (config-driven, 3 layers): the code provides the
  mixer, the production's scenes.json "audio" block declares the recipe.
  Layers: narration (narration_volume), clip effects (effects_volume,
  used only when clip_audio is "effects"; "off" discards the clips' own
  audio) and music (music_file relative to the production folder, looped
  or trimmed to the video length, at music_volume). Clip audio goes
  through a no-music gate first: the mean volume of each clip's audio
  track is measured (volumedetect) before mixing; above
  audio.clip_gate_db (default -35 dB) it is music-level continuous
  audio and is muted entirely, at or below it is genuine foley and is
  admitted at effects_volume. Every decision (scene, measured dB,
  admitted/muted) is logged in the build summary and build/audio-gate.json.
  `editor.py <production> --gate-report` measures without rendering.
  Never retune the threshold silently: if measured values stop
  separating music from foley, report the values. A missing or null
  music_file skips the layer and says so in the run summary — never a
  failure. Different channels declare different profiles; never
  hard-code a recipe in the editor.
- Clip-audio REQUEST doctrine (standing requirement, owner 2026-10-25):
  every model-generated video request must (a) positively name the exact
  diegetic sounds wanted for that scene and (b) explicitly forbid music:
  "no music, no soundtrack, no background score". This is enforced in
  code: each t2v/keyframes scene REQUIRES a `foley` field (diegetic
  sounds only, never the word music) and the producer builds the audio
  clause from a fixed template — "Audio: the only sounds are <foley>. No
  music, no soundtrack, no background score, no voices, no narration."
  (scenes_schema.audio_clause; the old production-level audio_style is a
  legacy fallback only). The request is BEST-EFFORT, never trusted.
  Measured compliance with the earlier softer clause: v2 3 of 6 clips
  clean, v3 2 of 6. The clip-audio gate remains the enforcement
  mechanism, with a known limit: it measures mean volume of ONE mixed
  stem, so a muted clip loses its real animation foley together with the
  music, and a quiet clip it admits may still carry quiet music (the
  owner heard model music in ALL v3 clips, some also with real foley such
  as the ant biting or the wound opening — v3 ended with no animation
  sound). FUTURE WORK, not built: an Editor SFX-library layer (hand-placed
  sound effects per scene, decoupled from the video model's audio) as the
  durable fix.
- Editor v2 (reference style, built 2026-10-26; tests/test_editor_v2.py):
  * Subtitles: spoken word bold white, others grey (150,150,155), thin
    4 px black outline, no dark box; words listed in the scene field
    `subtitle_emphasis` get a thin teal selection box with corner handles
    while spoken.
  * Overlay types beyond counter/bar/label: chip (teal pill; never a
    source chip), bracket (teal, figure-less measure), ring
    (dotted teal circle), mark (red X / gold ring pop with overshoot),
    cta (acted-out phone: FOLLOW tap, share sheet, chat bubble, sent
    tick; Spanish strings come from the spec). label style "tag" is the
    tiny ALL-CAPS tracked label with an optional leader_to hairline;
    counter style "mono" with `from`; bar style "slim" (gold fill,
    optional marker, show_value false).
  * Placement and timing: x, y = graphic centre as a frame fraction;
    keyframes [{t, x, y}] move it (so a label follows an object); exactly
    one of at_offset_seconds or at_word (WORD LOCK: the overlay starts on
    that spoken word of the scene, optional offset_s, resolved from the
    narration's per-word timings). Positioned overlays may overlap in
    time; legacy centred ones may not.
  * Production field end_card {duration_s, handle, dim}: after the last
    scene the final frame is held and dimmed to `dim` brightness, a
    placeholder logo and the handle (@[CANAL] until the channel exists)
    fade in; narration/effects go silent, the music continues.
  * Not built: inline emoji in subtitles.
- Data overlays (editor): a scene may declare data_overlays, a list of
  {type: counter | bar | label, text_or_value, at_offset_seconds,
  duration_s?, visible_s?}, timed from the scene's narration start and
  placed at the frame CENTRE (the upper band belongs to the subtitles):
  a counter counts up to its number ("170 °C"), a bar fills to a fraction
  or percentage ("75%"), a label fades in. Bold white, thick black
  outline, rendered with Pillow as one PNG sequence per overlay. Overlays
  of one scene may not overlap in time. Numbers in the script should be
  carried by overlays, not only spoken.
- Visual identity (values: the dark stage in the Reference doctrine
  above; the mechanism below is unchanged): ONE `visual_identity` block per channel (background
  hex + description, palette hexes, lighting and material wording, the
  shared `unify` pass parameters, qa_tolerance_de). Each production
  embeds a verbatim copy in scenes.json so it stays reproducible. EVERY
  engine consumes it literally: the producer injects it right after the
  style string in every t2v and image prompt (same style string, same
  seed); code3d scenes use the exact hex values and render on the spec
  background. The editor applies ONE unifying pass to every scene before
  assembly, whatever its engine: shared colour grade (eq/colorbalance) +
  film grain + vignette. Engines change only at scene boundaries, never
  mid-action. QA: the backdrop and its QA apply ONLY to establishing
  (wide) shots and to code3d productions; close-ups are exempt because
  their "background" is the subject — there, consistency is carried by
  the palette, the lighting wording and the editor's unify pass. A scene
  declares shot_type "establishing" (default) or "closeup". For checked
  scenes the background colour of the raw clip is sampled from 3 frames
  (median of 8 border patches) and compared with the spec hex by CIE76
  delta-E; scenes above qa_tolerance_de (default 15) get a REVIEW mark
  in the build report and build/visual-qa.json. A mark is a signal for
  human review, never an automatic defect (an intentional background
  is recorded with the scene's qa_note, e.g. the jungle in stitches
  scene 6). Sampling is done BEFORE the vignette, which darkens the
  corners.
- Phases: A Producer · B Editor · C Scriptwriter (the Opus creative
  session that writes and stamps every script; doctrine-topics-and-scripts.md
  "Who writes the script") · D Orchestrator (`tools/run_productions.py`) ·
  E Publisher (YouTube API, uploads private; the owner always makes the
  publish call; not built).
- A production lives in productions/<channel-id>/<NNN>-<slug>/ (see "Repository
  organization"); scenes.json, costs.json, notes.md and publish.json are
  versioned, generated media is gitignored.

## Runner session mechanics (lens decision 2026-11-11, block B3; forward-only; record: docs/current/reports/b3-2026-11-11.md)
How the runner's headless sessions are bounded. These are mechanics, not production rules: no gate, bar or threshold is touched.
- **Context cap and handoff.** The runner publishes each session's live context to a file (`SF_CTX_FILE`); at `SF_CTX_CAP` (default 200,000 tokens) the PreToolUse hook (`tools/hook_blender_guard.py`) denies every tool except writing the production's `build/checkpoint.md`. A session that reached the cap is continued by a FRESH session briefed from that checkpoint, never `--resume`. Sessions keep the checkpoint current at every stage boundary; it is excluded from the progress fingerprint like notes.md. A usage-limit resume is fresh too when the last context was over `SF_RESUME_MAX_CTX` (150,000) and a checkpoint exists. Without a checkpoint nothing can be handed over and the old resume applies.
- **Callback as code.** After a queued final's render the runner builds and checks the publish package (`tools/publish_package.py`) and runs the verifier itself; the callback is a FRESH session. When all of that passes, the session only writes the report (produce step 12); when it fails, the session gets the failure text and the full callback job.
- **Startup isolation.** Runner sessions load no skills, no claude.ai connectors and no unused tools: `--disable-slash-commands`, `--strict-mcp-config` with `tools/runner-mcp.json` (Blender only), `--disallowed-tools`, and the produce skill's text appended to the system prompt. `SF_ISOLATE=0` restores the old startup.
- **Inline Python and scripts.** The hook denies inline Python (heredoc, `python -`, `python -c`) that spawns a process, reaches the network, reflects, or names provenance, producer, `.env` or Blender; and a runner session runs only the `tools/`, `factory/` and `tests/` scripts as they stand in the commit the batch started from (`SF_TOOLS_REV`). The provenance stamp does not rest on these alone: the runner hashes `provenance.json` around every session and halts the batch if it changed.
- **Sanctioned tools.** `tools/status.py <prod>` orients in one call; `tools/iterate.py <prod> <scene> <frames>` drafts, builds one contact sheet and reports which stills are pixel-identical to the last iteration.
- **What did not change.** The gate (thresholds, readers, isolation, matcher), the ladder, the owner-only list, the budgets' meaning (sessions, hours, brake), the runner's model, and every standing production bar. **Precedence:** this section governs the runner's session mechanics; where it and the produce skill differ, this section governs.

## House rules
- Never spend without showing the estimate first. The gates are rules,
  not suggestions.
- Cost transparency: BEFORE any engine spike or production, present an
  ESTIMATE TABLE per route used — fal spend in dollars (from live fal
  prices), Claude effort (class LOW = library reuse, MEDIUM = new simple
  object, HIGH = new complex object; expected iteration rounds; expected
  session time) and local render time. AFTER each build, report the
  ACTUALS next to the estimate, in the production report and costs.json.
  Effort and time are the honest units: never present token counts as
  precise. code3d actuals, calibrated on the full v4-code3d build
  (2026-10-25, six scenes, Blender 5.2.3 EEVEE, scripted, library first):
  the scene that builds the library took ~18 min / 3 rounds; the five
  reuse scenes took 4-8 min (avg 5.7) / 2-3 rounds; the whole video ~46
  min of session time against the 5.3-9.4 h estimate. Final render is
  ~1.0-1.7 s/frame at 1080x1920 (about 62% of the total time); draft
  ~0.1 s/frame. These replace the earlier guessed timeboxes (LOW ~15 min
  / MEDIUM ~45 min / HIGH ~2 h), which were 5-10x too pessimistic for
  scripted primitive-and-library work. Bespoke organic modelling is still
  unmeasured. Stop and report if a scene passes 60 min or 2x its estimate.
- Verify fal.ai model IDs and prices against the current docs/schema
  before using them — never from memory.
- The fal key lives only in .env (gitignored). Never print, commit or
  echo it.
- Code, comments, filenames and JSON keys in English. Narration and
  titles in Spanish.
- Language: ALWAYS respond to the owner in English in this project
  (standing rule, owner decision 2026-10-25) — chat replies, reports and
  docs. Only the narration, titles and on-screen text of the videos are
  Spanish.
- **One launcher for Blender (2026-11-08).** Every headless Blender starts through `tools/blender_run.py`, which owns the GPU lock (one job at a time; a second one waits; released by the kernel on a crash) and `caffeinate -dimsu`. A live GUI Blender makes a headless job REFUSE (exit 3) unless `SF_ALLOW_GUI=1` is set for a small asset-job still, never a final; the GUI launcher refuses while a render runs. The one chain is `tools/chain_render.sh`, the one queue `tools/queue_chain.sh` (`--watch` reads `output/queue.txt`); a chain lock keeps queues from interleaving; a PreToolUse hook denies direct `blender -b` commands. A skill helper that starts Blender by itself (blender-core's `run_in_blender.py`, used for asset QA) runs only as `.venv/bin/python tools/blender_run.py --skill -- <helper.py> <args>` (same lock, GUI rule and caffeinate; the hook denies the bare form; 2026-11-09).
- **Render launches ALWAYS run under caffeinate (standing rule, owner 2026-10-28).** EVERY render launch (finals, benches, stills, drafts, any
  Blender or ffmpeg-render invocation, direct or via a script) is prefixed with `caffeinate -dimsu`, held for the render process's whole life, so
  the Mac cannot idle-sleep mid-render. `factory/code3d_render.py` already wraps its Blender calls; scripts that launch Blender must do the same.
  If a render is ever launched without it, say so explicitly in the report.
- Commit and push after each working phase, with a clear message. Never
  commit media files or .env.
- **A failed sub-step never passes silently (2026-11-04).** The render chains (`tools/chain_render.sh`, `chain_render2.sh`) log `DONE` only when every scene rendered and the editor ran; a scene that fails both attempts writes `build/render-failures.txt`, skips the editor and logs `INCOMPLETE`; a scene that needed its retry makes the DONE line carry a WARNING. Before reporting a production complete, grep its `output/chain-<name>.log` for FAILED/INCOMPLETE/Traceback, not just for DONE (incident: 006-011 logged FAILED on every scene because `code3d_render.py` could not append to a missing `costs.json`; the clips were intact, verified frame-for-frame, and the cause is fixed). `tests/test_render_chain.py` guards this.
- **No credits in descriptions (owner 2026-11-07).** Attribution credits never go in video descriptions: they dirty the description and read as AI-generated, the same reason the channel uses no music. The publish-package composition has no credit slot for assets (`publish_package.py check` rejects an asset credit in a description); internal asset records keep licence and source. Sourcing is CC0 first, then CC-BY without asking and without a credit line. Not queued, not published: owner-only publishing is unchanged.
- **Render-time operations (owner 2026-11-07; from the 2026-11-06 resume of 006/008/009, ~11.5 h for two finished productions: Cycles transmission at 8.4 / 19.2 / 58.4 s per frame in 008, multiplied by full finals re-rendered every failed gate round, plus renders lost to GPU out-of-memory when Blender jobs ran in parallel).** (a) Two tiers (2026-11-08): the session's own staging and dynamism checks use EEVEE drafts (`tools/draft_still.py`), advisory only and never shown to readers; the check readers and the colour gate judge half-resolution Cycles stills (`gate.py stills`/`run`, the final engine). A scene's full-quality final renders ONCE, after the scene passes. (b) Blender jobs run strictly one at a time, never in parallel (enforced by `tools/blender_run.py`; queue finals with `tools/queue_chain.sh`). (c) When staging transparent elements, prefer compositions that minimise transmission volume where the lenses judge likeness is not hurt.
- NO MUSIC (owner decision 2026-11-01; marketing/design/scriptwriter lenses): productions 001-007 ship narration only, `music_file`/`music_credit` null, and no
  publication carries a music credit line; the description template has no credit slot. A future track needs the owner's explicit OK and, if it carries a credit
  condition, the rule below applies again.
- Music credit: whatever a production stores in audio.music_credit MUST
  be copied into the YouTube description at publish time (Publisher
  phase). Never publish a video that uses a credited track without it.
- Definitive music tracks are downloaded from the official source
  (incompetech.com), not from mirrors. Mirrors are acceptable only for
  throwaway calibration placeholders. Music files are media: gitignored.
- code3d productions are modelled in the reference look (Reference
  doctrine: dark stage, one accent) from the first object; never model
  realistic and restyle afterwards. The lavender lace-world / toon /
  glossy-boot looks of v4-v6 are retired.
- Report failures and semantically wrong renders plainly; never work
  around them silently.
- Spending, publishing, creating accounts and the final publish/reject verdict are the owner's;
  topics, scripts and other creative or technical matters are the lenses' ("Governance"). You cannot
  hear audio or watch video: verify mechanically (format, durations,
  extracted frames) and never claim a render looks or sounds right
  beyond that.

## Repository organization (binding, owner 2026-10-31; spec and map of moves in docs/architecture.md)
Every new file is created in its correct place; orderly file creation is a standing rule, the owner does not have to ask again.
- **productions/** holds only channel trees, `_lab` and `_archive`. Current videos: `productions/<channel-id>/<NNN>-<slug>/` (`mecanalia-es`, `mecanalia-en`);
  three-digit number per channel in order of creation, never reused, highest = newest. CREATE A NEW VIDEO ONLY with
  `.venv/bin/python tools/new_production.py <channel-id> <slug>` (assigns the number, adds a row to the channel's `INDEX.md`). Slugs: lowercase ascii, hyphens.
  Experiments and tests (look tests, benches, validations, spikes, closing tests) go in `productions/_lab/<kind>/<name>`. Superseded or frozen productions
  are moved with `git mv` to `productions/_archive/<series>/`. There is no `pilot` folder any more.
- **Publish package** (factory -> orchestrator contract): in the production folder, `final.mp4` + `cover.jpg` + `publish.json`
  (`tools/publish_package.py build|check`; texts come from the production's notes.md "Publish package" section and the channel package's `publish` block).
- **docs/** holds `README.md`, `architecture.md` and three classes: `docs/current/{specs,reports,research}/` (in force; plus one standing file at `docs/current/idea-bank.md`, the topic pool, see "Idea bank"), `docs/experiments/` (rounds, proposals,
  tests, dated run logs in `runs/`), `docs/archive/` (superseded, kept verbatim, with a first line saying what replaced them). Evidence folders sit next to the
  document that cites them. File names: lowercase with hyphens.
- **channels/** holds brand packages and their channel variants only (`channels/<brand>/brand.yaml`, `<lang>.yaml`, `assets/`); **craft skills never live in
  this repo** (they are at user level, `~/.claude/skills/`); this repo holds channel packages, doctrines and style-locks (`.tastemaker/`).
- Never delete material: move it to the right class. When moving a path, update every reference (code, docs, notes) and run the full test suite
  (`tests/test_layout.py` guards this layout; `tests/test_channel.py` the packages). Editing `code3d/lib/{looks,common,composition,pipeline_config,tape_rig}.py`
  or any rig library, even a comment, invalidates composition-gate records.
