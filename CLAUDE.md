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
- Visual style: the REFERENCE LOOK (see "Reference doctrine" below):
  dark low-key stage, stylized 3D, NOT photorealistic, no real skin
  texture, no blood, no gore. Realistic graphic content risks YouTube
  age-restriction (kills reach and monetization) and disgust-skips; in
  this format the gross-out is conceptual, not visual. Our pilot v1
  rendered photorealistic — that is the anti-pattern to avoid. The
  earlier bright "Pixar-style" lavender stage is RETIRED.
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
- Typography (owner 2026-10-27): Montserrat ExtraBold (Google Fonts, SIL
  OFL; factory/assets/fonts/Montserrat-VF.ttf, logged in
  factory/assets/fonts/LICENSES.md) for subtitles, counters, labels and
  chips; non-spoken subtitle words use SemiBold of the same family.
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

## Channel identity (ADOPTED 2026-10-28, owner; provisional): CORAL — parameters, not code
The channel's colour identity is PARAMETERS in ONE place: `channels/umbrella-es.yaml`, blocks `identity` (active preset + named presets) and
`render` (profiles). Everything reads it through `factory/identity.py` (the Editor themes, the end-card mark, the code3d stage via an exported JSON
snapshot, brand tools, new productions). **To switch identity: edit `identity.active` (or one preset's values) and re-render; never edit code.**
Full spec: `docs/design-system.md`. Active values: stage gradient #FEA181 -> #EC9172, ink plinth #1D1B2E, deep-teal accent #0A5C6B, error #7A0019,
ink subtitle theme (ink words, white outline, spoken word in an ink box). Coral's production rules: (1) body-family heroes stand in a cream cutaway
plate (skin/organ colours are close to the stage); (2) the accent is dark, so it reads by hue and shape, never by glow or text colour. Papel and the
other directions are kept as presets. **Where this section and the "Reference doctrine" palette points below (dark stage, gold accent, teal
annotation, near-black void, vignette) disagree, THIS section wins**; the doctrine's storytelling rules are unchanged. No CTA phone and no appended
end card (owner 2026-10-28). Render default: the tuned Cycles profile (`render.profiles.tuned`: GPU denoise, adaptive 0.04, min 24, ceiling 128,
Persistent Data on, Fast GI off; EEVEE for drafts; the grain pass stays mandatory); per-scene-type exceptions live in `render.scene_type_profiles`.

## Closing standard (ratified 2026-10-28, owner; supersedes the CTA-phone / end-card text elsewhere in this file)
The phone graphic (overlay type `cta`) and the appended end card (`end_card`) are REMOVED from every production (marketing verdict, docs/marketing-verdicts.md;
audit in docs/cta-endcard-audit.md). The standard closing for EVERY video: the spoken follow + share ask naming the share_archetype (unchanged), plus ONE
tiny ink "ENVÍASELO" tag (`label`, style `tag`) word-locked (`at_word: "envíaselo"`, ~2.6 s) in the last scene, placed in the cream space beside the hero (C2 in
docs/cta-redesign/). No extra seconds, nothing covers the hero. Where "Reference doctrine" point 8, storytelling rule 8, the Editor v2 `cta` / `end_card`
bullets or the beat-sheet wording ("the CTA/end card") still mention the phone or the end card, read them through this section: the code for them stays
(frozen productions), new productions do not use it.

## Reference doctrine (binding, owner 2026-10-26)
Adopted from the reference study of three example channels
(docs/reference-style-spec.md = the LOOK, docs/reference-format-spec.md =
the STORYTELLING GRAMMAR, with frame evidence for every rule; both specs
are binding, this section is their summary). Where this section and an
older paragraph disagree, this section wins.

Identity change (the lavender stage is RETIRED; channels/umbrella-es.yaml
visual_identity carries the values):
- DARK stage: near-black warm void ~#120F10 (cross-section backdrop
  navy #16202C). Never a light or pastel stage.
- ONE accent: gold/amber (#F5C04A / #ECA432) = the ACTIVE QUANTITY
  (energy, charge, tension, growth, the thing being measured).
  Everything passive is GREY (#2D2A2B / #51555A / #DAD8D7). Teal
  (#67CDBE) = annotation graphics only (labels, chips, frames). Red
  (#BE4A4A) = error, failure, overflow. Yellow-green (#CBD764) =
  bacteria/biology. A part stays grey until the narration activates it.
- Productions v1-v6 (lavender, lace-world, toon, glossy boot) are
  FROZEN RECORDS of the retired identity: never modified, never reused
  as a style reference.

Look rules (style spec; evidence cited there):
1. Low-key frames; one soft key light plus a warm rim halo behind the
   hero; emissive accents are the second light. The stage is dark but the SUBJECT
   is LUMINOUS (owner 2026-10-27: "too dark overall, edges included"):
   lifted shadows, no heavy vignette (unify `lift` curve, vignette_angle 0),
   stage never a pure void.
2. Hero models simplified and chunky; detail only on the feature the
   fact is about; scale exaggerated so the mechanism is legible.
3. Energy and charge are emissive glowing tubes with bloom.
4. Cross-sections are flat clean cuts with a layer stack and tiny parts;
   cutaways get a glass plate and a cyan/teal frame.
5. The camera never rests: push-through (into a surface), pull-back
   (multiplication/context), or orbit/tilt. Scene changes are
   push-throughs or blur wipes, not bare cuts.
6. Caption band: the top ~25% of the frame is reserved; the hero is
   centred in the lower 70% with large dark negative space.
7. Text system: subtitles of 1-4 words with the spoken word bold white,
   the others grey (~55%), key words in a selection box; tiny ALL-CAPS
   labels with hairline leader lines (1-2 words); monospace counters;
   teal chips (figures/units only, never sources). BUILT in factory/editor.py +
   factory/overlays.py (Editor v2, 2026-10-26; see "Data overlays").
8. ONE hero rig per video, revisited and re-lit with new data, +1 new
   element per fact. End with a dimmed end card (~25% brightness,
   animated logo, @handle, ~4 s).

Storytelling rules (format spec; each narration line becomes a visual
EVENT, never a static illustration):
1. Every sentence changes something on screen; no 3 s window without an
   object, number or camera change.
2. The hook stages the false belief as a CONTRAST in the first 2-3 s:
   two actors on one stage, one of them fails.
3. "Inside / under / made of" = push through the surface into a cutaway
   or exploded layers, active part in the accent colour.
4. "Each / all / many" = multiplication with a pull-back.
5. EVERY NUMBER IS A SCREEN OBJECT (counter, chip, bar, year) that
   appears on the spoken word. A number is NEVER invented: an unsourced
   figure is flagged to the owner in the report. SOURCES ARE NOT RENDERED
   ON SCREEN (owner rule 2026-10-27, binding for every future production):
   no citation lines, no "ficha técnica / fuente" chips, no brand-name
   credit cards. Numbers stay as counters/chips/bars and are understood
   as approximate; the source lives in the beat sheet and report, and the
   spoken narration may name it. Counters, labels and dynamic comments
   stay. overlays.validate_scene_overlays rejects type "citation".
6. "But / what if not" = a counter-actor on the same stage with the same
   readout.
7. "Imagine..." = a named-person micro-scene; set it up early, return to
   it as the payoff.
8. The closing reframe is ONE single-image visual; then the CTA is acted
   out in the visual world (follow, share sheet, sent) naming the
   share_archetype, then the end card.
9. Event timing is word-locked (+-0.3 s) to the highlighted subtitle
   word.
10. Transitions carry meaning (blur wipe / push-through).
A production brief is a BEAT SHEET approved by the owner BEFORE any
generation: every narration line mapped to an event type with its word
lock, the hero-rig element ledger, every number with its source (or
flagged), and the CTA/end card.

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
- Phases: A Producer ✓ · B Editor ✓ · C Scriptwriter (an LLM agent that
  writes scenes.json) · D Orchestrator · E Publisher (YouTube API,
  uploads private; the owner always makes the publish call).
- A production lives in productions/<channel>/<video-slug>/; scenes.json
  and costs.json are versioned, generated media is gitignored.

## code3d sourcing and optimization (binding, owner 2026-10-25)
Your job is the FASTEST route to each clip, not the most from-scratch one.
- SOURCE FIRST: search the libraries before modelling anything; model only
  what no library has. For every element choose in this order and log a
  one-line reason: (1) an existing library asset (BlenderKit, Poly Haven,
  ambientCG, Poly Pizza), (2) an AI-generated mesh (Meshy free tier; its
  output is CC-BY and needs an attribution line), (3) modelled primitives,
  only when 1 and 2 have nothing usable.
- Free tiers only. NEVER subscribe or sign up for a paid plan (including
  BlenderKit Full); if something needs payment, skip it and report it.
  Tripo's free tier is non-commercial: never use it. Every downloaded
  asset is logged in code3d/assets/LICENSES.md (committed; the assets
  themselves are gitignored under code3d/assets/).
- Verify the current best option LIVE (web search), never from memory:
  this session alone found a renamed repo (BlenderKit/Blendkit) and a
  renamed package (blender-mcp -> mcp-for-blender).
- While iterating render DRAFT quality only (half resolution, low EEVEE
  samples, short frame ranges); render full quality ONCE, at the end.
- Never remodel or re-download anything that already exists locally:
  check code3d/assets/ and code3d/lib/ first.
- Report per-clip wall time split by phase: search/download, modelling,
  animation setup, iteration rounds, draft renders, final render.
- If a faster method is discovered mid-build, adopt it and write it here.
- Tooling facts and the verified integrations are in code3d/TOOLING.md.

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
  t2v enabled. code3d enabled. Tooling: Blender 5.2.3 LTS (installed
  2026-10-25 with the owner's approval via `brew install --cask blender`;
  headless `blender -b --python <script>`, EEVEE; trivial scene rendered in
  0.58 s warm). The earlier Pillow software rasterizer PoC
  (spikes/code3d_poc.py) was flat and schematic and is only a fallback
  record. Exact colours in Blender need node-based world/material colours,
  the Standard view transform and sRGB->linear conversion (measured: the
  spec backdrop #E2D5F1 renders at dE 0.0; see spikes/blender_smoke.py and
  the spike report). The code3d production pipeline (scene -> Blender
  script -> frames -> clip) is not built yet; its first full test is
  puntos-de-sutura-v4-code3d. keyframes DISABLED: R2 (fal-ai/flux-2) produced
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
- **Render launches ALWAYS run under caffeinate (standing rule, owner 2026-10-28).** EVERY render launch (finals, benches, stills, drafts, any
  Blender or ffmpeg-render invocation, direct or via a script) is prefixed with `caffeinate -dimsu`, held for the render process's whole life, so
  the Mac cannot idle-sleep mid-render. `factory/code3d_render.py` already wraps its Blender calls; scripts that launch Blender must do the same.
  If a render is ever launched without it, say so explicitly in the report.
- Commit and push after each working phase, with a clear message. Never
  commit media files or .env.
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
- The owner approves topics, scripts, spend and publishing. You cannot
  hear audio or watch video: verify mechanically (format, durations,
  extracted frames) and never claim a render looks or sounds right
  beyond that.

## Support colours and composition gate (binding, owner 2026-10-28)
The stage colour is the BACKGROUND ONLY. Every support element (backing boards, cutaway plates, plinths, panels, large housing surfaces) gets a colour chosen per production by the design lens:
1. SEPARATION: CIEDE2000 >= 20 from BOTH ends of the stage gradient (`identity.support_errors`).
2. HARMONY: derived from the hero, ink or accent system; value and reason recorded in the production's notes.md.
Support colours are parameters (`identity.<preset>.support {board, plate, panel}`, overridden per production by `scenes.json` `support_colours`; per-production hero colours in `hero_colours`), never code literals and never the stage value.
THE GATE IS A HARD BLOCK in the render driver: `factory/code3d_render.py --mode final` refuses to launch (exit 2) unless the production has a FRESH PASSING gate record (`build/gate/gate.json` + the distance table `build/gate/gate.md` + the stills). Create it with
`.venv/bin/python factory/gate.py run productions/<ch>/<video>` (renders the stills declared in scenes.json `gate_stills` {scene id: [frames]} with `mask=1` under caffeinate, tabulates the pairs through `tools/composition_gate.py`); `gate.py check` verifies it. The record carries a fingerprint of the identity preset, support/hero colours, the gate scene scripts and the rig libraries (scenes.json `rig_libs`), so any change makes it stale and forces a re-run.
Thresholds: stage-support, stage-hero, support-hero >= 20 (CIEDE2000, in frame); accent-stage >= 20 and 3:1 luminance contrast; the rendered accent/error must match its swatch family (dE <= 15; calibrate the preset's `emission_gain`). Any BLOCK stops the render until fixed.
