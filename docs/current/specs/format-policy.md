# Channel format policy: one signature, five structures, three staging modes

Decided 2026-11-04 by the lenses under the owner's directive that video structure is a lens decision (CLAUDE.md "Governance"). Channel-level, not per video. Applies from production 012; published videos are untouched. Values live in `channels/mecanalia/brand.yaml` `formats.explainer-short`. Lens record: `docs/current/reports/lens-decisions.md`.

Widened 2026-11-10 by owner decision, from production 019: a staging-mode axis and a fifth structure, Historia. Precedence and what did not change are in "Amendment record" below.

**The policy:** recognition comes from a fixed signature; the structure of each video comes from its mechanism, chosen from five named variants, and each production is staged in one of three modes. The fixed 7-scene template is retired. The closing keeps one fixed slot, and its wording varies.

Confidence: low to medium. No retention data exists yet, so this rests on reference-channel evidence and our own catalogue, and it states below what would overturn it.

## What stays fixed (the signature)

Voice, identity system, typography and top-band subtitles. The hook formula (a question about a tangible object, with a false belief where the family requires one). One hero or one mechanism chain. Dynamics inside the shot. One spoken reframe. The closing slot below. No music, no end card, no phone graphic.

## What varies (the structure)

Every production declares `structure_variant`.

| Variant | Use it when | Shape | Default family |
|---|---|---|---|
| `chain` (Cadena) | A hidden mechanism unfolds in steps | Contrast hook, one step per scene, x-ray reveal, reframe | objects, body |
| `journey` (Viaje) | The story is where something goes | Follow one thing along its route, then pull back to reveal the whole path, reframe | objects, body |
| `scale` (Escalada) | A number is the spectacle | One unit, multiply with a pull-back at each step, everyday comparison as payoff, reframe | numbers |
| `fork` (Bifurcación) | The premise changes the world | Normal world, change the premise on the same stage, escalating consequences, repeat the opening question | whatif |
| `story` (Historia; from production 019) | One complete real story whose engine is what the people did and how it worked | The predicament, what they did step by step and how each step worked, the turn, the full outcome, reframe | whichever fits the hook |

The family column is a default, not a rule: pick the variant the mechanism demands.

**Scene count follows the mechanism.** There is no target number. Never pad or merge scenes to reach one. A scene exists when there is a new fact and a new visual. The sanity range is 4 to 10 scenes, within the duration bands.

**Deliberate variation, in production order:** never three videos in a row with the same variant (all five variants), and never three in a row with the same scene count. If a batch would break this, the scriptwriter lens changes the topic order rather than forcing a mechanism into the wrong shape.

## Staging mode (from production 019)

The structure says what happens. The staging mode says where the viewer watches it from. The design lens chooses one mode per production, consulting the scriptwriter and marketing lenses, and records it in the production's notes.md as a line `Staging mode: <mode>. <reason>`.

| Mode | What the viewer sees | Examples |
|---|---|---|
| `stage` | Hero elements on the channel stage, with the camera travelling around them. The default through production 018 | An object on the Coral stage |
| `world` | The full environment is modelled and the camera is inside the event | Sky, aircraft and approaching ground; a car interior in a storm; a room, not a backdrop |
| `cutaway` | An interior or cross-section view of a mechanism or body | The current cutaway productions |

**Rotation:** in any five consecutive productions from 019 onward, no single mode appears more than three times. Check it at each production against the four before it. Productions before 019 do not count.

**The mode is a staging choice only.** The likeness gate, the visibility check and the dynamism rule apply exactly as before in every mode.

**Priority from 019 (owner):** the channel's videos win on content, not polish, so staging variety and event-first scenes outrank object perfection. The gates remain the bar. Once an element clears them, remaining effort goes to what happens in the scene, not to polishing the object.

In `world`:
- The modelled environment replaces the Coral stage. Typography, subtitles, the meaning of the accent and error colours and the editor's unify pass stay, and the look stays stylised, never photorealistic.
- Everything modelled that represents a real object or substance is held to "Every element at hero standard", and the key element of each scene is read by the gate as usual.
- The composition gate runs unchanged. A sky made with the world shader counts as its `stage` class, so hero separation is measured against the real sky. If meshes fill the whole frame, the stage rows do not apply, and the visibility check carries separation from the background. Backdrop QA REVIEW marks are expected on these scenes; explain them with `qa_note`.
- The top caption band stays reserved, and the environment behind it must not hurt subtitle legibility.
- Environment render cost is unmeasured. The first `world` production measures its riskiest environment first and classes each scene under the render-cost playbook.
- Cadence wins. If a `world` build cannot hold the daily slot, the design lens picks another mode for that production.

## Historia (`story`, from production 019)

A Historia production tells ONE complete real story, beginning to end. It is never serialized, never a cliffhanger and never a "part 2". The outcome is told before the reframe.

- **Mechanism heart.** What the people did and how it worked is the engine of the narration. Survival stories qualify by this, not by drama alone. Test: remove the mechanism sentences; if the story still stands, it fails.
- **Topics.** Story topics pass the curiosity test and the one-line hook test like every topic, and enter only through a normal idea-bank fill. The hook keeps the formula: an approved opening for its family, a tangible object and an explicit false belief. There is no story family: `topic_family` is whichever fits. The theme tag names the specific subject, never "survival" or "story".
- **Sourcing.** The figures rule extends to story facts. Every load-bearing fact (who, when, where, how long, what was done, how it ended) is flagged until sourced at the beat-sheet stage. A fact that cannot be sourced comes out of the script, and if the story no longer stands without it, the topic is returned. Sources stay in the beat sheet and report, never on screen.
- **Length (lens value).** 55 to 75 s of narration, about 160 to 215 words at the channel's measured pace. The scene range stays 4 to 10. The 75 s ceiling is the production verifier's current limit, well inside Shorts limits and inside what the reference hits run (36 to 95 s). Going longer needs a verifier change and a new lens decision.
- **People.** Real people are shown stylised, never as a likeness. Without a sealed `human-figure` they stay off screen, as the drawability rule requires. No gore, no blood, no real skin texture: a story that needs injury on screen is staged without it or dropped.
- **Closing.** The standard slot: reframe, then the sentence with "envíaselo".

**Declare it honestly.** `factory/scenes_schema.py` accepts `story`. A Historia is never labelled as another variant.

## How standing doctrine applies to the new options

- **Script flatness.** Chronology does not count as progression: "and then, days later" is not an event. In a Historia each scene still changes something in the world, the scene-swap test is applied to what happens on screen, and the turn comes before the reframe.
- **Dynamism.** A scrolling environment around an unchanged subject is not a visible change. A `world` scene needs reference objects (ground, aircraft, clouds, walls) so its first, middle and last frames are different pictures.
- **Modellability.** Fills and production sessions judge the whole environment of a `world` staging, and every period object of a Historia, with the context-cue check. An environment often supplies context, which can help an element read.
- **Reshape ladder.** Rungs act on scenes and leave the production's declared mode alone. A rung-4 setting inside one scene does not reclassify the production; moving the whole production to another mode is a design-lens decision, re-checked against the rotation. In a Historia, a rewritten beat (rung 2) may change how a fact is staged, never the fact. If a true event cannot be staged, the ladder ends and the topic is returned.
- **Topic balance.** Unchanged. Staging modes and structures are never theme or tension tags, and the rolling window applies to Historia topics as to any other.

## The closing

The slot is fixed: reframe, then the share ask naming a person, with no added seconds.

- **The reframe is mandatory** and renames the object or fact. The `fork` variant repeats the opening question.
- **The word "envíaselo" is the fixed brand word,** spoken in every video, with the tiny word-locked ENVÍASELO tag. It costs no time and covers nothing.
- **The sentence around it varies.** "Sígueme, y envíaselo a ese amigo que…" is one allowed form, not the standard. Keep it to one sentence, and end on the person, because that is the twist.
- **The archetype names a behaviour, not a belief.** "Ese amigo al que nunca le funciona el móvil con las manos mojadas", not "el amigo que cree que…".

## Reasoning

| Evidence | Quality | What it says |
|---|---|---|
| References: "the surface template is the same in both groups [hits and flops], so the template alone is not the differentiator" (`docs/current/research/reference-channels.md`) | Observational, like counts only | A fixed template does not win views. Hook, mechanism chain and reframe separate hits from flops |
| Reference hits run 4-7 setups and 36-95 s, and setup count follows the process | Sampled estimates | Their structure flexes, while voice, subtitles and closing slot stay constant |
| All three reference accounts keep a fixed spoken closing slot, and hits name a person by a concrete behaviour; the flops had vaguer archetypes or none | Observational | Keep the slot; sharpen the archetype |
| Our catalogue: 10 of 11 videos have exactly 7 scenes, whatever the mechanism | Measured | The count came from the template, not from the mechanism. The exception, 005 at 9 scenes, follows a route |
| Our catalogue: 8 of 11 archetypes state a belief ("cree que", "jura que"); 7 of 11 use "cree que" | Measured | Our closing has become rote and drifted from what hits do |
| Owner's verdict on the archived original 006/007: "very monotonous, the same scene throughout" | Owner's eye, one judgement | Monotony is a real risk here, though that verdict was about scenes within a video |
| Our analytics (snapshot 2026-11-03): Instagram shares 0 on 2,434 views across 002-004; YouTube retention not returned yet | Tiny, days old | No conclusion in either direction. It does not support the current closing |

**Lens positions:**
- **Marketing:** recognition is worth keeping, but it lives in voice, look and the closing slot. Nothing suggests viewers recognise a scene count. Shorts are tested largely one by one, so a viewer rarely sees the pattern; a follower who watches daily would.
- **Scriptwriter:** a fixed count forces padding or cramming, which breaks "every sentence changes something". The mechanism should set the shape.
- **Design:** the variants reuse the same stage, camera moves and overlays, so they add no new rendering system. A `journey` or `fork` costs more in staging than a `chain`, and that cost is accepted.

All three agreed. There was no disagreement to settle. The review was one session reasoning through each lens, not separate agents.

**Considered and refused:** keeping one structure for brand recognition (no evidence it helps, and hits and flops share it); free structure per video (loses the shared grammar and makes results impossible to compare); and removing the closing (all reference hits have it, and it adds no time).

## What would change this

Thresholds are judgement, set in advance so the result cannot be argued afterwards. Earliest read-out: 2026-12-01, after the 30-day test. Tag results by `structure_variant` from `scenes.json` and, from production 019, by staging mode from notes.md. Small differences below these bars are noise, and the policy stands.

| Evidence | Bar | Then |
|---|---|---|
| YouTube average % viewed, by variant | At least 5 videos per variant, at least 1,000 views each; one variant's median is 5 or more points below the others | Drop or rework that variant |
| Same measure, all variants | At least 20 videos and every variant within 3 points | Variation neither helps nor hurts: keep only what is cheapest to make while avoiding monotony |
| Same measure, against the 7-scene catalogue | Variant videos are 5 or more points below comparable 7-scene `chain` videos | Reconsider returning to one structure |
| Retention drop during the closing | On at least 10 videos, the closing loses clearly more than the same length before it | Shorten it, or move the follow out |
| Shares per 1,000 views across platforms that report them | At least 20 videos, still below 1 | Test new closing forms; if behaviour archetypes do no better, reconsider the ask |
| Share rate, behaviour vs belief archetypes | Behaviour archetypes do not beat the earlier belief ones after at least 10 videos | Drop the behaviour rule |
| Comments or owner verdicts | Viewers or the owner call videos repetitive, or say they cannot recognise the channel | Tighten or relax variation accordingly |
| YouTube average % viewed, by staging mode | At least 5 videos per mode, at least 1,000 views each; one mode's median is 5 or more points below the others | Drop or rework that mode |
| Average % viewed of `story` against the other variants, read at each video's length | At least 5 `story` videos, at least 1,000 views each; the `story` median is 5 or more points below | Shorten the Historia band, or drop the variant |

**Known gap:** YouTube retention has not been returned yet, so the first two rows cannot be read today. If it is still missing at the read-out, the policy stands and the gap is reported.

The 30-day test measures cadence. Mixing structures within it does not change cadence, but it does add a variable, so the read-out must state which variant each video used. From production 019 the owner has approved testing staging modes and Historia inside the same window, so the read-out also states each video's staging mode. Because both axes change at once, a difference inside the window is a signal, not a proof.

## Amendment record: widening of 2026-11-10

Owner decision, applied under CLAUDE.md "Amending doctrine". Checks and evidence: `docs/current/reports/format-widening-2026-11-10.md`. The reference points were a what-if video of a figure falling from an airplane with the whole sky modelled around it, and a complete real survival story told beginning to end.

**Precedence:** from production 019, where older live text and the widened format policy disagree, the widened policy governs.

**What did not change:**
- The 1-per-day cadence and the test window.
- The fixed signature, including the voice, the subtitles and the closing word ENVÍASELO.
- The likeness gate, its thresholds and its reader isolation.
- Topic balance and the topic-selection tests.
- Productions 015 to 018, exactly as armed.
