# Standing doctrine: building a production

Moved verbatim out of CLAUDE.md on 2026-11-11 (block B2, P14 "CLAUDE.md diet", `docs/current/reports/doctrine-b2-2026-11-11.md`); later amendments are recorded in `docs/current/reports/lens-decisions.md`. Each section below is the CANONICAL HOME of its rules; CLAUDE.md keeps a summary under the same section name and points here. Where a summary and this text differ, this text governs.

**Precedence.** These files (`doctrine-topics-and-scripts.md`, `doctrine-format-and-look.md`, `doctrine-production.md`, `doctrine-pipeline.md`) and CLAUDE.md are ONE body of doctrine: a precedence statement written in CLAUDE.md before the move ("this section wins", "supersedes ...", "where older text in this file ...") keeps the meaning it had there, wherever the sections it names now live. "This file" in moved text means that body of doctrine.

**Reading.** Read one section at a time: `.venv/bin/python tools/doc_section.py docs/current/specs/doctrine-production.md "<section>"` (`--list` shows the sections and their sizes). Never read the whole file to follow one pointer.


## Asset library and hero routing (binding, owner 2026-11-04; manual: docs/current/specs/asset-system.md)
Why: the owner rejected batch 006-011 (too abstract, objects do not resemble their subjects; do not publish). All six were code-primitive builds and all passed the composition gate, which only measures colour.
- **Routing, per production, before the beat sheet is final:** genuinely geometric hero objects keep the code-primitive route. Anything organic, soft or complex takes the asset route: search `assets/registry.yaml` in priority order (best licence wins);
  if nothing fits, build it with the modelling skills or a generator, with visual checks through MCP screenshots. In doubt, asset route. Declare `hero_route` and `library_assets` in scenes.json (required from production 012).
- **Whatever the route, the finished object lands in `assets/library/<slug>/`,** and the same object is never solved twice. Check first: `.venv/bin/python factory/asset_library.py find <words>`. To run a job, follow "How to run an asset job" in the manual.
- **Drawability exceptions (supersedes the old ban for hero objects):** anatomy, hands, animals, cloth and fluids are allowed when the asset route supplies them; without a passing asset they stay off screen, and no abstract stand-in replaces them. Reason: the ban
  treated a tooling limit as a content rule and produced the abstract objects the owner rejected. Still binding: stylised, no real skin texture, no blood, no gore.
- **Likeness gate (hard block):** a hero must be named correctly by THREE fresh subagents (owner 2026-11-07; replaces pair readings: pass = every reader names it, mean confidence >= 60, no reader under 45) who see only neutrally named stills, once for the asset and once in the production's gate stills. `gate.py check` refuses the final render otherwise. Never add an alias to make a guess pass. Calibrated 2026-11-04 on 006-011 plus two accepted controls (docs/current/reports/likeness-calibration.md). The owner's eye remains the last gate on output.
- **Licences and sources:** **CC0 FIRST:** when a CC0 asset serves the production, use it. Royalty-Free acceptable. If no CC0 asset serves and a CC-BY asset is needed, use it: do NOT ask the owner and do NOT credit it in the description (owner 2026-11-07, decided with the licence terms in view; see "No credits in descriptions"). The licence, source and attribution text are still logged in the asset README and `licence.attribution`. Anything unclear (NC, ND, SA, unknown) is not used. BlenderKit anonymous search and download is a connected route (owner 2026-11-04). Sketchfab is connected with the owner's free account (token only in `.env`; read each result's licence, because NonCommercial models appear in results). Sessions create no accounts. Poly Pizza stays an owner-step source. `generate_3d` is not used: its providers need accounts or credits.
- **Skill roles:** `docs/current/specs/asset-system.md`, "Skill role map" (which of the listed skills serves which asset job; the list itself is "Project skills").
- **Operating model:** asset-building is interactive, with Blender open through MCP for Blender; production rendering stays headless.
- **Advance assets have an owner (owner 2026-11-10; rule and scan: asset-system.md "Advance assets"):** the owner does not commission individual assets. Every idea-bank fill or other creative session ends with the commissioning scan and opens the qualifying jobs, ordered by evidence. A production session that improvises around a missing element class leaves an `Asset need:` line in its notes.md. Builds are separate later sessions, one per asset.

## Every element at hero standard (binding, owner 2026-11-05; supersedes the hero-only scope of "Asset library and hero routing" and of the likeness gate)
Why: the owner watched the remade 006-011 batch: heroes reached the new standard while secondary elements (blood vessels as glossy red cylinders, a capsule and a ball as a grip comparison, ice as a translucent blue box, coffee as a brown block, heat as flat blue dots) were still flat-colour primitives. The standard is the best possible modelling in EVERY scene.
- **Routing applies to every element that represents a real object or substance, in every scene** (vessels, liquids, ice, glass, food, props, cutaway contents): library asset > proper material or build > code primitive. A code primitive is allowed only when the real thing is genuinely geometric AND reads instantly (a cube of metal, a plate, a pin). Flat-colour stand-ins for organic, liquid or real-world elements are banned in all scenes. **Materials count as modelling:** a represented substance takes its best material route (physically based water, the `transparent` render profile for ice and glass; building and measuring that profile is part of the remake that first needs it). Abstract energy graphics (heat, signals) must be in a visual language consistent with the scene's realism, not flat dots.
- **Extended likeness gate:** blind naming (three fresh subagents; pass = mean confidence >= 60, no reader under 45; owner 2026-11-07) runs on the key represented element of EVERY scene, in that scene's own stills, not only on the hero. scenes.json declares `scene_elements` {scene id: [{id, name, aliases, route, source}]}; `gate.py stills` renders the stills, `asset_library.py element` records the naming, and `gate.check(prod, scene)` (called per scene by `code3d_render.py --mode final`) refuses that scene's final render while a declared element has no fresh passing record. Same teeth as the hero gate; never add an alias to make a guess pass.
- **Event elements (lens decision 2026-11-11, block B2, forward-only):** an element that is a happening rather than a thing (sparks, an electric arc, a splash, a flash, a flow) is declared with `"kind": "event"` in `scene_elements`, and its aliases include, at script stage and before any reading, the verb forms readers write for it ("sparking", "arcing") next to the nouns. `scenes_schema.py` rejects an event element with no verb-form alias. The matcher is unchanged (whole words, plurals): a verb form counts only when it was declared, never by stemming, never added after a guess, and recorded readings are never re-judged under this rule. Why: the matcher is literal, so readers who described the event ("fork sparking in a microwave") failed against noun-only aliases. Since 2026-11-11 (redesign session), an event that is a small accent on a dominant object is a capability boundary and is staged as an ungated cue: `doctrine-topics-and-scripts.md` "Capability boundaries".
- Productions made before this rule declare no `scene_elements` and are audited, not reworked, unless the owner asks. Reasoned and logged in `docs/current/reports/lens-decisions.md` (2026-11-05); manual: `docs/current/specs/asset-system.md` "Every element".

## Gate v2 (binding from production 012, 2026-11-08; manual: docs/current/specs/asset-system.md "Gate v2")
scenes.json `gate_version: 2`. **Hero first:** `hero_rig`, `hero_still` {scene, frames}; the hero passes and `gate.py freeze` runs before any other scene's stills are read; a later change is `gate.py unfreeze <prod> <reason>`, logged in notes.md. **Element-scoped invalidation:** each scene's record depends only on the library functions its script reaches (comments and docstrings do not count); the hero's record depends on the hero asset, rig, colours and identity, not on other scenes' camera files. **Isolated readers:** three headless sessions through `tools/blind_read.py --record ...`; the check refuses a record made any other way (audit: docs/current/reports/reader-isolation/). Every reading counts: never re-roll. **Carry-over:** `gate.py carry` keeps a reading only when the re-rendered stills match what the readers saw. Productions 001-011 keep the v1 rules their records were made under.

## Reshape ladder (binding, owner 2026-11-07; integration recorded in docs/current/reports/lens-decisions.md)
Why: scenes that were hard to model or failed the likeness gate have stalled whole productions (009 stays skipped on one scene), and topics have been dropped for capability limits. A capability limit is a problem for the staging or the beat, not a reason to stall or abandon the topic.
- **Trigger:** a scene proves hard to model (the house-rule timebox: past 60 min or 2x its estimate) or a declared element fails the likeness gate. The production does not stall: the other scenes continue, and the failing scene works the ladder IN ORDER, trying first, at each rung, the fallback the creative session wrote for that element (doctrine-topics-and-scripts.md "Per-element fallbacks", 2026-11-11):
  1. **RE-STAGE the beat:** same script and narration, different staging (another framing, another context cue, another view or cutaway of the same element, another library asset or route).
  2. **REWRITE THE BEAT** in the script to a modellable equivalent that does the SAME narrative job (same fact or step of the mechanism, same position in the event progression, same turn if it is the turn).
  3. **ADJUST THE NARRATION** line to match the new beat.
  4. **CONTEXT STAGING (owner 2026-11-10; final rung, element-level):** re-stage the failing ELEMENT embedded in its narrative setting, so the setting visible in the frame identifies the element's situation (for example a swallowed object already inside a modelled digestive tract instead of the object alone). The gate reads the element from that staging under the unchanged rules. Owner rules: (1) the context must be visible inside the rendered frame; the blind readers' isolation does not change (they see only neutrally named stills, no narration, title or topic information); (2) the pass bar does not move: every reader names the element by one of its declared aliases, mean confidence >= 60, no reader under 45; (3) it applies ONLY to scene elements inside a production: library asset blind naming (`asset_library.py blind` / `record_blind`) stays isolated forever, with no context staging for sealing an asset; (4) ONE attempt per element, attempted after the re-staging rungs and before the topic is returned; if it also fails, the ladder is exhausted and the topic is returned as today; (5) a pass through this rung is flagged in the production's notes.md (which element, which scene, that it passed via context staging) so the owner's verdicts on such videos can be reviewed against it later. Doctrine only: no gate, runner or verifier code changed.
  Each rung gets a real attempt before the next; a further failed gate round on the same rung is the signal to step down, not to iterate the same staging indefinitely. The timebox is still reported.
- **Reading budget per element (lens decision 2026-11-11, block B2; makes the step-down signal above a count):** at most TWO isolated readings (each one `tools/blind_read.py --record` run of three readers) at each of rungs 1, 2 and 3, and exactly ONE at rung 4. A second failed reading on a rung means step down; a failed rung-4 reading means the ladder is exhausted. Rung 4 is never skipped to save readings, and the budget never changes the bar (same readers, isolation, aliases, mean >= 60, none under 45) or the rule that every reading counts. Productions armed before 2026-11-11 are not re-judged under it.
- **Where the ladder stops:** before replacing the HERO MECHANISM or the topic's PROMISE (the hook question and its false belief, and what the video answers). A fix that needs either is a different video and goes back to the slate.
- **Not capability limits, never laddered around:** the hard production rules (no gore, no blood, no real skin texture, stylised). A beat or topic blocked by one of them is not reshaped to get past it; it is dropped or re-proposed on its own merits.
- **Every rung keeps every standing bar:** the likeness gate at full strength (three readers, mean >= 60, none under 45; never an added alias, never a lowered floor; the one-off `element_floor_exception` of 006/008/009 does not extend); the every-element routing, so no flat or abstract stand-in replaces an element that failed (the drawability rule: without a passing asset it stays off screen); the dynamism bar; script flatness (a rewritten beat still changes the world, the scene-swap test still fails, the turn still comes before the closing reframe, the beat sheet's "what changes in the world" line is updated); the format policy (the production's `structure_variant`, hook formula and closing slot are unchanged; scenes are never merged or padded to absorb a reshape; if the scene count changes, the rotation rule is re-checked); and, after rung 3, the duration band, word locks and sourced numbers. A rung that cannot keep these fails, and the next rung is tried.
- **Approval and record:** rungs 2 and 3 change the approved beat sheet, so the involved lenses re-approve it under "Governance" (scriptwriter lens leads). Every reshape is logged in the production's notes.md ledger ("Production notes ledger") AND as a row in `docs/current/reports/lens-decisions.md`: what changed, which rung, why (the failing measurement or timebox).
- **At slate screening, one attempt deep:** a topic that fails modellability as conceived gets ONE reshape attempt (rung 1 or 2 applied to the failing beat on paper, with the context-cue check, rung 3 as needed; no asset searches) before it may be rejected for modellability. Since the IDEA BANK, this is step 3 of a bank fill; the bank records the attempt and its outcome, and a banked entry carries its concept-level reshape. At production time the ladder starts again from rung 1 on the live scene. Rejections for the hard rules, the curiosity test, the hook test or balance are not modellability rejections and get no ladder attempt.
- **Relation to script flatness:** a flat script is a script defect, not a capability limit; it is reshaped or rejected under "Script flatness". The ladder never makes a passing script flat.

## Production notes ledger (lens decision 2026-11-11, block B2, P11; forward-only)
A production's notes.md is a LEDGER, not a narrative, for productions developed from 2026-11-11 on; older notes stay as written.
- **Header, kept current:** one status line; the `Staging mode: <mode>. <reason>` line; the flags doctrine requires (a pass through context staging: element, scene, "passed via context staging"; `Asset need:` lines); the per-element fallbacks written by the creative session; the "Publish package" section (`tools/publish_package.py` reads it).
- **Ledger lines, appended, never rewritten:** one dated line per event: what changed, the rung if any, and why (the measurement, with the readings' means, or the timebox). A later line that supersedes an earlier one says so. Pasted tool output, restated doctrine and narrative paragraphs stay out: the measurements live in `build/` and the gate records.
- **Why:** notes ran to 13-18 KB per production and are re-read in every session; a ledger is short, and its last lines are the checkpoint a fresh session resumes from.

## Dynamism is a hard bar (binding, owner 2026-11-05; supersedes any reading of "transformation" and "camera" as paperwork)
Why: production 010 (heart and bottles) was well modelled but held ONE static framing for the whole video while a counter climbed; monotony has been a rejection cause before (the original 006/007 "the same scene throughout", 010 now).
- The per-scene `transformation` and `camera` fields are a bar the render must meet, not a description. **No video may hold one static tableau while only a counter or overlay changes.** Every scene stages a visible change in the world (an object transforms, grows, multiplies, moves through states) AND a camera that travels (not a hold, and not a push-in on a still action).
- **Escalation is staged as movement the viewer travels through:** a scale, count or growth ("a thousand bottles", "seven thousand litres") is shown as physical growth and camera travel (the pile builds, the camera climbs or pulls back along it, framings change from close to wide), never as a number rising in a fixed frame. Numbers stay overlays, in addition.
- **Across a video, framings vary:** no two consecutive scenes may share the same camera move and distance; at least three distinct framings per video; the mechanism (what the thing does) is shown at work, not only its parts at rest.
- **Image discipline for the session's own checks (lens decision 2026-11-11, block B3, P4; forward-only):** staging checks go through `tools/iterate.py`, which drafts the stills and builds ONE contact sheet; the session reads the sheet as one image, not each still, and does not re-read a still the tool reports as pixel-identical to the last iteration. Drafts are already half-resolution EEVEE. This changes how the session looks, not what is checked: the contact-sheet bar below, the gate's readers (`tools/blind_read.py`, never EEVEE) and every threshold are unchanged.
- Checked by the lenses before a final render (contact sheet of each scene's first, middle and last frame: if the three frames of a scene are the same picture, the scene is rejected) and audited in every production report. Applies to every future production; productions made before this rule are audited, not reworked, unless the owner asks.

## Support colours and composition gate (binding, owner 2026-10-28)
The stage colour is the BACKGROUND ONLY. Every support element (backing boards, cutaway plates, plinths, panels, large housing surfaces) gets a colour chosen per production by the design lens:
1. SEPARATION: CIEDE2000 >= 20 from BOTH ends of the stage gradient (`identity.support_errors`).
2. HARMONY: derived from the hero, ink or accent system; value and reason recorded in the production's notes.md.
Support colours are parameters (`identity.<preset>.support {board, plate, panel}`, overridden per production by `scenes.json` `support_colours`; per-production hero colours in `hero_colours`), never code literals and never the stage value.
THE GATE IS A HARD BLOCK in the render driver: `factory/code3d_render.py --mode final` refuses to launch (exit 2) unless the production has a FRESH PASSING gate record (`build/gate/gate.json` + the distance table `build/gate/gate.md` + the stills). Create it with
`.venv/bin/python factory/gate.py run productions/<ch>/<video>` (renders the stills declared in scenes.json `gate_stills` {scene id: [frames]} with `mask=1` under caffeinate, tabulates the pairs through `tools/composition_gate.py`); `gate.py check` verifies it. The record carries a fingerprint of the identity preset, support/hero colours, the gate scene scripts and the rig libraries (scenes.json `rig_libs`), so any change makes it stale and forces a re-run.
Thresholds: stage-support, stage-hero, support-hero >= 20 (CIEDE2000, in frame); accent-stage >= 20 and 3:1 luminance contrast; the rendered accent/error must match its swatch family (dE <= 15; calibrate the preset's `emission_gain`). Any BLOCK stops the render until fixed.

## Engine selection (binding; from the 2026-10-25 engine spike)
Evidence: productions/_lab/engine-spike/report.md. The factory assigns
engines automatically from these rules; the owner is never asked.
- (a) (Read with "Asset library and hero routing": an organic hero supplied by the asset route may
  stay in code3d; t2v remains available for ambient footage but is not forced.)
  Choose ONE primary engine per production from the script's dominant
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
  script -> frames -> clip) is `factory/code3d_render.py`. keyframes DISABLED: R2 (fal-ai/flux-2) produced
  warped hands/arms, a needle that changes shape between stills, and no
  continuity between stills; flux-2-pro and reference-image conditioning
  (flux-2/edit) were not tested. Re-testing means a new spike, then
  removing the route from DISABLED_ROUTES.
- (e) Every assignment and override is logged with a one-line reason
  (production engine_reason, scene engine_override_reason) and printed
  in the production report.

## code3d sourcing and optimization (binding, owner 2026-10-25)
Your job is the FASTEST route to each clip, not the most from-scratch one.
- (For HERO objects, "Asset library and hero routing" supersedes this list: its source order applies, and
  an AI-generated mesh needs a recorded lens decision, and a provider needing an account or credits stays owner-only. This list still applies to supporting props.)
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
