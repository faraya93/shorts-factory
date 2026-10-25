# shorts-factory — project brief

## What this is
A factory that produces faceless YouTube Shorts in Spanish, engineered to
maximize views and retention. Every technical choice serves that goal. The
reference format is Zack D Films' stylized 3D "how it works" explainers —
we copy the mechanics, never scripts or footage: all scripts are original.

## Format doctrine (channel research, Oct 2026; evidence in docs/reference-channels.md)
- Vertical 9:16. Duration, by topic family (measured pace of the channel
  voice: ~2.9 words/s on the pilot): standard target 45–60 s of narration
  (~130–170 words); body/medical may run 40–50 s (~115–145 words);
  impossible numbers/scale 50–60 s (~145–170 words). This supersedes the
  earlier 30–35 s target: the reference accounts run 36–95 s.
- Title: short question or "How X works", second person when natural,
  exactly ONE trailing emoji as an emotion label. No hashtags.
- Hook formula: the first sentence is a question (¿…?) about a TANGIBLE
  EVERYDAY OBJECT the viewer has already seen, plus an explicit FALSE
  BELIEF to bust. Approved openings by topic family: objects and body
  "¿Por qué…"; numbers "¿Por qué…", "¿Cuántos…", "¿Cuántas…", "¿Sabías
  que…"; whatif "¿Qué pasaría si…", "¿Por qué…". "¿Cómo…?" openers
  flopped in the references. Hook in the first 2 seconds. Reveal order: build
  the object up step by step — never show the finished phenomenon first.
- Structure: one hero object or one mechanism chain; each scene
  visualises ONE step of the mechanism (a new fact AND a new visual per
  step, roughly every 5–9 s). Numbers are carried by animated Editor
  overlays, not only spoken.
- Dynamics live INSIDE the shot, not in fast cutting: transformation arcs
  (start state → end state), camera movement (travels, orbits, tracks),
  multiplying/exploding objects, and one x-ray/cross-section reveal per
  "how it works" video. A slow push-in on an otherwise static action is a
  defect. Flat 2D is an anti-pattern (the reference flops were flat 2D).
- Closing: a spoken REFRAME that renames the object or fact ("they are
  not hairs, they are the print of each air bubble"), then follow, then
  "send this to that specific friend who…" naming a concrete person
  archetype (production field share_archetype). A twist in the last 3 s
  loops back to the hook; dilemma videos repeat the opening question.
- Topic families (the channel's portfolio, rotated under one format,
  voice and brand; every script is tagged with its family): (a) everyday
  objects with a hidden mechanism, (b) body/medical how-it-works,
  (c) impossible numbers/scale, (d) what-if/dilemmas. Avoid generic
  textbook science with no everyday anchor (tornado, GPS flopped) and
  off-promise topics (news, sports, labour law). Prefer topics the
  viewer can verify or try on the spot.
- Audience: pan-Hispanic. Neutral Spanish, universal topics and objects
  that exist identically in every Spanish-speaking country; no
  country-specific systems and no local slang in scripts or titles.
- Visual style: STYLIZED 3D animation, clearly CGI (Pixar-style explainer),
  NOT photorealistic, no real skin texture, no blood, no gore. Realistic
  graphic content risks YouTube age-restriction (kills reach and
  monetization) and disgust-skips; in this format the gross-out is
  conceptual, not visual. Our pilot v1 rendered photorealistic — that is
  the anti-pattern to avoid.
- The style string of every model-generated production MUST contain
  "no text on screen". Labels, counters and numbers are Editor overlays,
  never model-generated text (validated by scenes_schema.py).
- Scene prompts must spell out the ACTION (what moves, enters, exits,
  where): video models render nouns well and actions badly. Add an
  explicit "never ..." clause for the plausible wrong reading. Every
  scene prompt is prefixed by the production's identical style string.
- Narration: Spanish, channel voice es-CL-LorenzoNeural (edge-tts) until
  the owner decides otherwise. Voice-led audio: fast continuous
  narration, no prominent music bed; clip audio only when it is genuine
  mechanism foley (see the audio gate).
- Subtitles: burned in, upper band centred at SUBTITLE_Y_CENTER = 0.24 of
  the frame height (a channel constant that moves to the channel config),
  short phrases (max 4 words) with the WHOLE current phrase visible; the
  currently spoken word sits in a dark rounded box with light text, the
  other words light grey with a thick black outline. Size and position
  are tuned constants in editor.py.
- Captions/descriptions are mini-hooks (hook + twist), not bare text or
  links; every script ships with a caption draft.
- Engine architecture: three visual engines — t2v (fal text-to-video),
  keyframes (fal stills animated by the Editor), code3d (3D drawn with
  code, rendered locally). The factory assigns engines AUTOMATICALLY; the
  owner is never asked to choose one. Selection is at VIDEO level: each
  production declares ONE primary_engine. The only per-scene exception is
  engine_override "keyframes" inside a t2v production (both are
  diffusion-family and share a photographic look). code3d is NEVER mixed
  with diffusion footage: a code3d production is code3d in every scene.
  scenes_schema.py rejects violations before any spend. The binding
  selection rules are in "Engine selection" below.

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
  prompt, narration, target_duration_s. Optional: engine_override
  ("keyframes", only inside a t2v production; needs engine_override_reason),
  audio_style, caption_draft, shot_type, qa_note, data_overlays,
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
  hard-code a recipe in the editor. The optional "audio_style" field in
  scenes.json is appended to every producer prompt.
- Data overlays (editor): a scene may declare data_overlays, a list of
  {type: counter | bar | label, text_or_value, at_offset_seconds,
  duration_s?, visible_s?}, timed from the scene's narration start and
  placed at the frame CENTRE (the upper band belongs to the subtitles):
  a counter counts up to its number ("170 °C"), a bar fills to a fraction
  or percentage ("75%"), a label fades in. Bold white, thick black
  outline, rendered with Pillow as one PNG sequence per overlay. Overlays
  of one scene may not overlap in time. Numbers in the script should be
  carried by overlays, not only spoken.
- Visual identity: ONE `visual_identity` block per channel (background
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
- Phases: A Producer ✓ · B Editor ✓ · C Scriptwriter (an LLM agent that
  writes scenes.json) · D Orchestrator · E Publisher (YouTube API,
  uploads private; the owner always makes the publish call).
- A production lives in productions/<channel>/<video-slug>/; scenes.json
  and costs.json are versioned, generated media is gitignored.

## Channel strategy (owner decisions, 2026-10-25)
- Audience: pan-Hispanic Spanish speakers, NOT one country (a single small
  country was explicitly rejected). Neutral Spanish, universal topics, no
  country-specific systems, no local slang.
- ONE umbrella channel first. Its promise is "why/how the things you see
  and use every day work", rotating the four topic families (everyday
  objects, body/medical, impossible numbers, what-if/dilemmas) under ONE
  format, voice and brand. Body/medical is one family, not the channel.
  Why: the recommendation algorithm clusters by audience-and-promise,
  Shorts test each video largely on its own merits, so rotation inside one
  promise widens the viral surface; off-promise drift (news, sports,
  labour law) is what hurt the reference accounts.
- A channel is CONFIGURATION, never hard-coded: channels/umbrella-es.yaml
  (DRAFT until the owner approves) holds voice, language, style,
  duration bands, topic-family mix (starting mix objects 40 / body 25 /
  numbers 20 / what-if 15), subtitle constants, the visual_identity block
  and the audio profile. tests/test_channel.py keeps it valid and in sync
  with the code constants it mirrors. Productions embed a verbatim copy of
  the blocks they use. This config creates no accounts and uploads nothing.
- Spin-off channels are decided LATER and ONLY by data, never micro-topic
  splits from day one. Criteria: (1) a topic family that consistently wins
  AND can sustain its own publishing cadence, or (2) the English-language
  version of the channel.

## Engine selection (binding; from the 2026-10-25 engine spike)
Evidence: productions/pilot/engine-spike/report.md. The factory assigns
engines automatically from these rules; the owner is never asked.
- (a) Choose ONE primary engine per production from the script's dominant
  mechanism type. Ambient/organic transformation and camera travel
  (bodies, tissues, soft or flowing things) → t2v. Rigid geometric hero
  objects and numbers/scale spectacle → code3d (R3 passed, so the route is
  enabled; its ceiling is stated below). If a route is disabled, fall
  back to t2v.
- (b) The ONLY per-scene override is keyframes inside a t2v production,
  for contact-mechanics scenes. It is currently unavailable (see d): a
  contact-mechanics scene in a t2v production stays t2v with a
  strengthened ACTION prompt (what moves, enters, exits, where, plus a
  "never ..." clause), and the production report says why.
- (c) code3d is never mixed into a non-code3d production, and a code3d
  production is code3d in every scene.
- (d) A route that failed the spike is DISABLED until re-tested
  (scenes_schema.DISABLED_ROUTES, enforced before any spend). Status:
  t2v enabled. code3d enabled, with the ceiling measured in the spike:
  the only installed tooling is a Pillow software rasterizer (flat
  colours, no lighting), so renders are schematic; polished shading would
  need tooling that is not installed (node/three.js, Blender) — installs
  are the owner's decision. The code3d production pipeline (scene →
  code → frames) is not built yet; the proof of concept is
  spikes/code3d_poc.py. keyframes DISABLED: R2 (fal-ai/flux-2) produced
  warped hands/arms, a needle that changes shape between stills, and no
  continuity between stills; flux-2-pro and reference-image conditioning
  (flux-2/edit) were not tested. Re-testing means a new spike, then
  removing the route from DISABLED_ROUTES.
- (e) Every assignment and override is logged with a one-line reason
  (production engine_reason, scene engine_override_reason) and printed
  in the production report.

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
  precise. code3d work is timeboxed per effort class (initial values,
  to be calibrated by the spike actuals: LOW ~15 min / 1–2 rounds,
  MEDIUM ~45 min / 3–4 rounds, HIGH ~2 h / 6+ rounds).
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
- Commit and push after each working phase, with a clear message. Never
  commit media files or .env.
- Music credit: whatever a production stores in audio.music_credit MUST
  be copied into the YouTube description at publish time (Publisher
  phase). Never publish a video that uses a credited track without it.
- Definitive music tracks are downloaded from the official source
  (incompetech.com), not from mirrors. Mirrors are acceptable only for
  throwaway calibration placeholders. Music files are media: gitignored.
- Report failures and semantically wrong renders plainly; never work
  around them silently.
- The owner approves topics, scripts, spend and publishing. You cannot
  hear audio or watch video: verify mechanically (format, durations,
  extracted frames) and never claim a render looks or sounds right
  beyond that.
