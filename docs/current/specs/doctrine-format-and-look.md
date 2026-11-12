# Standing doctrine: format, look and channel

Moved verbatim out of CLAUDE.md on 2026-11-11 (block B2, P14 "CLAUDE.md diet", `docs/current/reports/doctrine-b2-2026-11-11.md`); later amendments are recorded in `docs/current/reports/lens-decisions.md`. Each section below is the CANONICAL HOME of its rules; CLAUDE.md keeps a summary under the same section name and points here. Where a summary and this text differ, this text governs.

**Precedence.** These files (`doctrine-topics-and-scripts.md`, `doctrine-format-and-look.md`, `doctrine-production.md`, `doctrine-pipeline.md`) and CLAUDE.md are ONE body of doctrine: a precedence statement written in CLAUDE.md before the move ("this section wins", "supersedes ...", "where older text in this file ...") keeps the meaning it had there, wherever the sections it names now live. "This file" in moved text means that body of doctrine.

**Reading.** Read one section at a time: `.venv/bin/python tools/doc_section.py docs/current/specs/doctrine-format-and-look.md "<section>"` (`--list` shows the sections and their sizes). Never read the whole file to follow one pointer.


## Format doctrine (channel research, Oct 2026; evidence in docs/current/research/reference-channels.md)
- Vertical 9:16. Duration, by topic family (measured pace of the channel
  voice: ~2.9 words/s on the pilot): standard target 45–60 s of narration
  (~130–170 words); body/medical may run 40–50 s (~115–145 words);
  impossible numbers/scale 50–60 s (~145–170 words). This supersedes the
  earlier 30–35 s target: the reference accounts run 36–95 s. Historia
  (`story`, from production 019) runs 55–75 s (~160–215 words).
- Title: short question or "How X works", second person when natural,
  exactly ONE trailing emoji as an emotion label. No hashtags. Forward SEO
  rules (marketing lens, 2026-11-08; "Search and packaging" below) refine
  the title and description of future productions.
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
  OFL; channels/mecanalia/assets/fonts/Montserrat-VF.ttf, logged in
  channels/mecanalia/assets/fonts/LICENSES.md) for subtitles, counters, labels and
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

## Closing standard (ratified 2026-10-28, owner; supersedes the CTA-phone / end-card text elsewhere in this file)
The phone graphic (overlay type `cta`) and the appended end card (`end_card`) are REMOVED from every production (marketing verdict, docs/current/reports/marketing-verdicts.md;
audit in docs/current/reports/cta-endcard-audit.md). The standard closing for EVERY video (wording per "Format policy"): the spoken follow + share ask naming the share_archetype, plus ONE
tiny ink "ENVÍASELO" tag (`label`, style `tag`) word-locked (`at_word: "envíaselo"`, ~2.6 s) in the last scene, placed in the cream space beside the hero (C2 in
docs/current/reports/cta-redesign/). No extra seconds, nothing covers the hero. Where "Reference doctrine" point 8, storytelling rule 8, the Editor v2 `cta` / `end_card`
bullets or the beat-sheet wording ("the CTA/end card") still mention the phone or the end card, read them through this section: the code for them stays
(frozen productions), new productions do not use it.

## Reference doctrine (binding, owner 2026-10-26)
Adopted from the reference study of three example channels
(docs/current/specs/reference-style-spec.md = the LOOK, docs/current/specs/reference-format-spec.md =
the STORYTELLING GRAMMAR, with frame evidence for every rule; both specs
are binding, this section is their summary). Where this section and an
older paragraph disagree, this section wins.

Identity change (the lavender stage is RETIRED; channels/mecanalia/brand.yaml
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
   figure is flagged to the owner in the report (in a Historia production this covers every load-bearing story fact: format-policy.md). SOURCES ARE NOT RENDERED
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
A production brief is a BEAT SHEET approved by all involved lenses (see "Governance") BEFORE any
generation: every narration line mapped to an event type with its word
lock, the hero-rig element ledger, every number with its source (or
flagged), and the CTA/end card.

## Channel identity (ADOPTED 2026-10-28, owner; provisional): CORAL — parameters, not code
The channel's colour identity is PARAMETERS in ONE place: `channels/mecanalia/brand.yaml`, blocks `identity` (active preset + named presets) and
`render` (profiles). Everything reads it through `factory/identity.py` (the Editor themes, the end-card mark, the code3d stage via an exported JSON
snapshot, brand tools, new productions). **To switch identity: edit `identity.active` (or one preset's values) and re-render; never edit code.**
Full spec: `docs/current/specs/design-system.md`. Active values: stage gradient #FEA181 -> #EC9172, ink plinth #1D1B2E, deep-teal accent #0A5C6B, error #7A0019,
ink subtitle theme (ink words, white outline, spoken word in an ink box). Coral's production rules: (1) body-family heroes stand in a cream cutaway
plate (skin/organ colours are close to the stage); (2) the accent is dark, so it reads by hue and shape, never by glow or text colour. Papel and the
other directions are kept as presets. **Where this section and the "Reference doctrine" palette points below (dark stage, gold accent, teal
annotation, near-black void, vignette) disagree, THIS section wins**; the doctrine's storytelling rules are unchanged. From production 019 a `world`-mode production replaces the stage with its modelled environment (format-policy.md "Staging mode"). No CTA phone and no appended
end card (owner 2026-10-28). Render default: the tuned Cycles profile (`render.profiles.tuned`: GPU denoise, adaptive 0.04, min 24, ceiling 128,
Persistent Data on, Fast GI off; EEVEE for drafts; the grain pass stays mandatory); per-scene-type exceptions live in `render.scene_type_profiles`.

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
- A channel is CONFIGURATION, never hard-coded, as PACKAGES (docs/architecture.md):
  channels/mecanalia/brand.yaml is the BRAND package (language-independent:
  identity, style, duration bands, topic-family proportions (objects 40 /
  body 25 / numbers 20 / what-if 15, descriptive only: an outcome, never a quota, see "Topic selection"), subtitle constants, visual_identity, render
  and audio profiles); each channel is a thin variant that EXTENDS it and stores
  only what differs (channels/mecanalia/es.yaml = mecanalia-es, en.yaml =
  mecanalia-en: language, handles, voice, bio, publish texts, words_per_second).
  A channel value wins, a missing value inherits (factory/channel.py: `load(id)`).
  tests/test_channel.py keeps the packages valid, thin and credential-free.
  Productions embed a verbatim copy of the blocks they use (a record, not a
  second source). Packages are public and versioned: NO platform credentials in
  them, ever (tokens live only in the orchestrator's credential store). The
  factory never publishes; nothing publishes without the owner's per-video OK.
  Default: one channel, one format; an exception needs the owner's explicit
  instruction for that video and never becomes the default.
- Spin-off channels are decided LATER and ONLY by data, never micro-topic
  splits from day one. Criteria: (1) a topic family that consistently wins
  AND can sustain its own publishing cadence, or (2) the English-language
  version of the channel.
