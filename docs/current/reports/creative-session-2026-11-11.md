# Creative session 2026-11-11: revival review, developed set 019-024, bank fill 2, script-model settlement, commissioning scan, batch

Owner instruction "DEVELOP THE BANKED SLATE + REFILL + BATCH LAUNCH". One Opus session reasoned through the marketing (lead on topics), scriptwriter and design lenses. These were not separate agents, and the lenses had no disagreement that needed settling, except the cut-rule reading in Part 3, which was settled on written doctrine. Every decision has a row in `lens-decisions.md` dated 2026-11-11. Nothing was published, armed, spent or signed up for. No code under `factory/` or `tools/` changed.

## Part 1: revival review of the archived returns

| Production | Recorded failure | Class | Capability since the return | Decision |
|---|---|---|---|---|
| 013 knuckle cracking | scene-2 knuckle capsule: rung 1 bones read 93-96 but the capsule read as a "clip"; rung 2 the bottle won the frame (0 of 3 named the joint) | likeness of one element | rung 4 CONTEXT STAGING (never tried); `hand-articulated` sealed incl. the `crack` pose, so the capsule's narrative setting (a hand cracking its knuckles) is now a sealed asset in a sealed pose; `cutaway` mode | **REVIVED** |
| 014 swallowed gum | the gum protagonist failed six stagings in scenes 1 and 6 (lipstick tube, lollipop, slime jellyfish, brain, pink pills, berries) | likeness of the protagonist | rung 4 CONTEXT STAGING (never tried; its lens row names 014 as the motivating case); `hand-articulated` `open` adds one cue in scene 1; the faceless figure adds nothing (no mouth); `cutaway` is what 014 already used | **REVIVED, LOW confidence** |

Neither failure was the promise. The 014 record's phrase "replacing the gum would replace the promise" rules out swapping the protagonist, not trying to make it read. Both folders were moved back with `git mv`, with numbers and names unchanged. Each notes.md has a REVIVED section with the re-check under the widened policy and the single rung-4 attempt to make. 013's script was re-routed from the fixed-pose `human-hand` to the sealed `open` and `crack` poses, a staging change with no narration change. 014's runner sidecar `returned.json` was renamed `returned-2026-11-09.json`, because under its old name `tools/run_productions.py` would treat the production as returned at once. Bank status: banked ranks 38 and 39, status `revived`. They competed on the same rubric: curiosity 9, last on the tie-break because of their measured likeness failures, so neither made the developed set.

## Part 2: developed set 019-024

Drawn from the banked tier as it stood at the start of the session, in rank order under TOPIC BALANCE. The window was 015-018 (insects/gross, toilet/gross, elevators/dangerous, voice/hidden). Skips:
- **Rank 4:** skipped at 020 (it would make three `chain` in a row) and at 021 (the window would hold only two tensions). It was drawn at 022.
- **Rank 6:** skipped at 021 and 023 (two tensions) and at 024 (a third electricity topic in the window). It is still undrawn.
- **Rank 8:** skipped at 021 and 023 (two tensions) and at 024 (three `chain` in a row). It is still undrawn.

| # | Title | Family | Structure | Scenes | Words / s | Staging (proposal) | Riskiest element and fallback |
|---|---|---|---|---|---|---|---|
| 019 | ¿Por qué nadie puede abrir la puerta de un avión en pleno vuelo? ✈️ | objects | chain | 6 | 146 / 50.3 | cutaway | airliner exterior (open job): rung 1 restages the 2024 panel event inside the cabin with sealed seated figures |
| 020 | ¿Qué pasaría si te cae un rayo dentro de un auto? ⚡ | whatif | fork | 7 | 156 / 53.8 | world | the bolt (open job `electric-arc`); night `world` cost: fallback to `stage` |
| 021 | ¿Cuántas veces tendrías que doblar una hoja para llegar a la Luna? 🌕 | numbers | scale | 8 | 154 / 53.1 | world | the mountain: a stylised build; `world` cost: fallback to `stage` |
| 022 | ¿Por qué un tenedor saca chispas en el microondas y una cuchara no? ⚡ | objects | chain | 6 | 139 / 47.9 | cutaway | the microwave (CC0/RF candidates, open job) and the sparks |
| 023 | ¿Por qué te da la corriente cuando te bajas del auto? ⚡ | objects | chain | 6 | 156 / 53.8 | stage | the fuel pump (a build; rung 2 stages the nozzle in the filler) |
| 024 | ¿Por qué no deberías limpiarte los oídos con un palito de algodón? 👂 | body | journey | 5 | 129 / 44.5 | cutaway | the ear section (CC-BY candidate seen) and the wax plug |

Every script passes the flatness swap test and puts the turn before the reframe. Each closes with one reframe and one "envíaselo" sentence ending on a behaviour archetype; 020 (fork) repeats its opening question. Every hook passes `scenes_schema.hook_errors`, and every duration sits in its family band. Every number is sourced from live searches of 2026-11-11 or is arithmetic; the ones still to confirm are FLAGGED, each with a written rung-3 line that removes the number if it cannot be confirmed. The wardrobe rule is applied: 019's four passengers wear distinct slot combinations, 021's student differs from its generic person, and every lone figure keeps the default outfit. Only sealed poses are prescribed. Audit: `docs/current/reports/modellability-audit-019-024.md`. All six are MODELABLE WITH THE WRITTEN FALLBACKS, with no unresolved fallback, so none is held out.

## Part 3: bank fill 2

N = 8, chosen to restore 10 drawable undrawn entries. The six draws left only ranks 6 and 8.

- **Generated:** 24 fresh candidates, 5 of them Historia stories, every one famous by the owner's bar, with fame evidence in its entry.
- **Screened out:** 1 discarded at the preliminary screen (sleepwalker: invisible protagonist), 1 failed the ladder check (a bottle starting a fire: the fire route is unmeasured), and 4 were not pooled (3 at curiosity 7 or below; 1 duplicates 023's turn).
- **Pool:** 18 fresh survivors plus the 20 re-scored reserve entries.
- **Banked:** 31 Titanic (story, 10), 32 people who have ever lived (scale), 33 the 33 Chilean miners (story), 34 why the stomach does not digest itself, 35 the Andes snow water (story), 36 the hot car, 37 wet wipes (promoted from the reserve; the toilet theme is drawable at its position, and the developed set carries no toilet topic as instructed), 40 the watermelon and rubber bands.
- **Reserve:** 30 entries.
- **Depth:** 10 drawable undrawn entries, plus 2 revived (12).

**Cut-rule reading (lens decision).** A first simulation tested each candidate against the half-built tier. That skipped the Titanic (10) for an 8, because the two revived bodily entries jam the end of the tier, so the order of testing was overriding rank. The rule as applied: a candidate is skipped only if no completion of the tier with it can be drawn out greedily. Eight candidates were skipped as balance at the cut, most of them because they are dangerous.

**Tool limits reported, not changed (scope: no code):**
- `tools/return_topic.py` orders by the rank number, so it would draw 6 and 8 before 31 although 31 scores higher.
- The same tool never draws a `revived` row. This is deliberate: it would create a duplicate folder. Revived rows are drawn by hand.

## Part 4: the parked step-8 question, settled

- **The fact it turned on:** batch topics now arrive with developed scripts on file.
- **Canonical home:** the rule is now a CLAUDE.md "Idea bank" bullet, "Who writes the script". A developed-set topic, or a revived entry, proceeds from its script on file. A raw-bank draw, including a `return_topic.py` replacement, has none, and its own production writes it. A returning session never writes the replacement's script.
- **Live restatements aligned:** produce skill step 8 (outside the repo, `~/.claude/skills/produce/SKILL.md`) now has the two-case form and points to "Drawing". Fill step 5's "when the production session writes the script" now names both writers. Step 1 of the skill already said a topic with a developed script proceeds from it.
- **What did not change:** `return_topic.py` and its stub notes ("No script yet: written at production time"); the runner prompts; the Reshape ladder; who draws (production sessions draw from the banked tier); the owner-only list.
- **Precedence:** where older text implies that production sessions always write scripts, "Who writes the script" governs.
- **Checks against standing doctrine:** Governance (a lens decision recorded with its reason), one canonical home, no dated record rewritten (the hardening report's open question stays as written and is answered here), flatness still checked whenever a script is written, and the idea-bank drawing rules unchanged.
- **Fossil scan:** the touched passages are the produce skill (no date or production number; grepped) and the two CLAUDE.md sentences. The new bullet's "lens decision 2026-11-11" is standing provenance, in the repo's convention.

## Part 5: commissioning scan and batch

**New jobs (`asset_library.py new`, briefs and evidence in each job report):**

| Priority | Job | Evidence |
|---|---|---|
| 12 | `snowy-mountain` | 021 committed, rank 35 |
| 13 | `moon` | 021 committed, reserve 15 |
| 14 | `ocean-liner` | rank 31, reserve 14 |
| 15 | `sea-surface` | rank 31, reserves 8, 11, 14 |
| 16 | `bird` | rank 6, reserve 8 |

**New evidence appended to open jobs:** `airliner` (019, rank 35, reserves 7, 8, 17), `electric-arc` (020, 022, 023), `microwave-oven` (022) and `car-interior` (023, rank 36).

**Not commissioned (one entry each):** fuel pump (023), ear section (024), watermelon, iceberg, rock strata and capsule, clock (013), and a swimming pose (reserve 11 only). The duplicate guard refused "ocean" for `sea-surface` because it sits inside `ocean-liner`. It was dropped, not worked around.

**Batch:** `tools/batches/2026-11-11-batch-019-024.json`, units 019-024 in production order. The launch record is in the lens-decisions row "Batch 2026-11-11 launched".

**Launch (2026-11-11 08:48):** both preflights PASS; runner pid 36781, detached (parent pid 1), log `output/runner/batch-019-024-launch.log`. START 019 logged at 08:48:36; the first session invoked the produce skill and was reading 019's notes.md. Pre-existing test failures, reported and not caused here: three 6-scene productions in a row (015, 016, 017) in `test_asset_library`, and colour literals in rig files in `test_identity`.
