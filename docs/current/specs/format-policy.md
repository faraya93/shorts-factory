# Channel format policy: one signature, four structures

Decided 2026-11-04 by the lenses under the owner's directive that video structure is a lens decision (CLAUDE.md "Governance"). Channel-level, not per video. Applies from production 012; published videos are untouched. Values live in `channels/mecanalia/brand.yaml` `formats.explainer-short`. Lens record: `docs/current/reports/lens-decisions.md`.

**The policy:** recognition comes from a fixed signature; the structure of each video comes from its mechanism, chosen from four named variants. The fixed 7-scene template is retired. The closing keeps one fixed slot, and its wording varies.

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

The family column is a default, not a rule: pick the variant the mechanism demands.

**Scene count follows the mechanism.** There is no target number. Never pad or merge scenes to reach one. A scene exists when there is a new fact and a new visual. The sanity range is 4 to 10 scenes, within the duration bands.

**Deliberate variation, in production order:** never three videos in a row with the same variant, and never three in a row with the same scene count. If a batch would break this, the scriptwriter lens changes the topic order rather than forcing a mechanism into the wrong shape.

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

Thresholds are judgement, set in advance so the result cannot be argued afterwards. Earliest read-out: 2026-12-01, after the 30-day test. Tag results by `structure_variant` from `scenes.json`. Small differences below these bars are noise, and the policy stands.

| Evidence | Bar | Then |
|---|---|---|
| YouTube average % viewed, by variant | At least 5 videos per variant, at least 1,000 views each; one variant's median is 5 or more points below the others | Drop or rework that variant |
| Same measure, all variants | At least 20 videos and every variant within 3 points | Variation neither helps nor hurts: keep only what is cheapest to make while avoiding monotony |
| Same measure, against the 7-scene catalogue | Variant videos are 5 or more points below comparable 7-scene `chain` videos | Reconsider returning to one structure |
| Retention drop during the closing | On at least 10 videos, the closing loses clearly more than the same length before it | Shorten it, or move the follow out |
| Shares per 1,000 views across platforms that report them | At least 20 videos, still below 1 | Test new closing forms; if behaviour archetypes do no better, reconsider the ask |
| Share rate, behaviour vs belief archetypes | Behaviour archetypes do not beat the earlier belief ones after at least 10 videos | Drop the behaviour rule |
| Comments or owner verdicts | Viewers or the owner call videos repetitive, or say they cannot recognise the channel | Tighten or relax variation accordingly |

**Known gap:** YouTube retention has not been returned yet, so the first two rows cannot be read today. If it is still missing at the read-out, the policy stands and the gap is reported.

The 30-day test measures cadence. Mixing structures within it does not change cadence, but it does add a variable, so the read-out must state which variant each video used.
