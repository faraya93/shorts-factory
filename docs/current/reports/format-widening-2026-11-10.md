# Format widening from production 019: amendment report

Date: 2026-11-10. Owner decision, applied under CLAUDE.md "Amending doctrine". One session reasoned through the design, scriptwriter and marketing lenses; they were not separate agents.

**Outcome:** the format policy now has a staging-mode axis and a fifth structure, Historia. The advance-asset rule has an owner, and the first commissioning scan opened 11 asset jobs. Nothing was rendered, built, spent or published, and no file under `factory/` or `tools/` changed.

## What changed, and where

| Rule | Canonical home | Live restatements aligned |
|---|---|---|
| Staging modes (`stage`, `world`, `cutaway`) | `docs/current/specs/format-policy.md` "Staging mode" | CLAUDE.md "Format policy" and "Channel identity"; `channels/mecanalia/brand.yaml`; produce skill step 5 |
| Historia (`story`) | `docs/current/specs/format-policy.md` "Historia" | CLAUDE.md "Format policy", "Format doctrine" (length) and "Reference doctrine" rule 5; `brand.yaml`; `docs/README.md`; idea-bank structure values; produce skill step 2 |
| Commissioning scan and asset-need note | `docs/current/specs/asset-system.md` "Advance assets" (e) to (g) | CLAUDE.md "Asset library" and "Idea bank" step 9; `assets/registry.yaml`; produce skill step 12 |
| Amending doctrine | CLAUDE.md "Amending doctrine" | none |

The advance-asset rule's canonical home is the asset manual, where it already lived, rather than CLAUDE.md, so the rule keeps one home. CLAUDE.md carries the pointer.

**Lens-set values:**
- The Historia variant key is `story`, matching the English keys of the other four.
- The Historia band is 55 to 75 s. The top is the verifier's current ceiling, so it needs no code change.
- The staging mode is recorded in notes.md, because `tools/scenes_from_script.py` copies only a fixed list of keys into scenes.json.
- Real people are shown stylised, never as a likeness.

## What did not change

- The 1-per-day cadence and the test window.
- The fixed signature, including the voice, the subtitles and the closing word ENVÍASELO.
- The likeness gate, its thresholds and its reader isolation.
- Topic balance and the topic-selection tests.
- Productions 015 to 018 exactly as armed. Their `publish.json`, `scenes.json` and `final.mp4` are unchanged, and each still verifies PASS after this amendment.

**Precedence:** from production 019, where older live text and the widened format policy disagree, the widened policy governs.

## Doctrine checks

| Standing rule | Risk found | Result |
|---|---|---|
| Topic balance | A broad "survival" tag would hide repeats; a mode or structure could be mistaken for a theme | Compatible. Theme tags name the specific subject; modes and structures are never tags |
| Dynamism | A scrolling sky around an unchanged subject gives three identical contact-sheet frames | Compatible. `world` scenes need reference objects; the bar is unchanged |
| Script flatness | Chronology can pass as progression ("days later") | Compatible. Time passing is not an event; the swap test applies to what happens on screen |
| Modellability | A `world` staging adds many elements; a Historia adds period objects and people | Compatible. Environments are judged with the context-cue check; people stay off screen without a sealed figure |
| Reshape ladder | Rung 2 could invent events in a true story; a rung could quietly change the mode | Compatible. A rung restages a fact and never changes it; a whole-production mode change is a design-lens decision |
| Likeness gate, visibility check | A mode could be read as an exception | No exception in any mode |
| Composition gate | Written around the stage | Runs unchanged. The world shader counts as `stage`; a frame filled by meshes skips the stage rows, and the visibility check carries separation |
| Every element at hero standard | The priority on event over polish could be read as a lower bar | The gates stay the bar. The priority applies only to effort above it |
| Render cost | Environment cost is unmeasured | The first `world` production measures its riskiest environment first |
| Cadence and test window | The test is recorded as "kept pure" (`cadence-decision.md`); `world` builds cost more | Purity there concerns the cadence, which is unchanged. The owner approved this test inside the window. If a `world` build cannot hold the slot, the mode changes, not the cadence |
| Hook formula, closing, sourcing, no gore | Stories drift from the object-and-false-belief hook | Unchanged and applied to Historia |
| Owner-only boundaries | None | No publishing, spend or account creation |

## Commissioning scan, first run

Read: the idea bank (both tiers), the 2026-11-07 slate, the library, `code3d/lib/`, and the scene elements and notes of productions 006 to 018. An entry counts only if it puts the element on screen and one asset could serve every counted entry. Full evidence is in each `assets/library/<slug>/job/report.md`.

| Priority | Job | Evidence |
|---|---|---|
| 1 | `hand-articulated` | 5 undrawn entries (banked 2, 5, 9; reserve 25, 27); cost paid in 006 and 013 |
| 2 | `human-figure` | Cost paid in 017 (a phone stood in for the passenger); entries 1 (drawn), reserve 16 and 21; banked 9 and reserve 17 reshaped around its absence |
| 3 | `water-droplets` | Scripts 006 and 012, reserve 28; 012 is still blocked on droplets that read as foam |
| 4 | `electric-arc` | Banked 4, 5, 9 |
| 5 | `airliner` | Banked 2, 7; reserve 12, 27 |
| 6 | `car-interior` | Banked 5, 9; `cartoon-car` has no interior |
| 7 | `microwave-oven` | Banked 4; reserve 24 |
| 8 | `tall-building` | Banked 7; reserve 15, 23 |
| 9 | `smartphone` | Scripts 017 and 018, each with its own build; no entry waiting |
| 10 | `human-kidney` | Reserve 18, 19 |
| 11 | `earth-globe` | Reserve 16, 23 |

The figure was the owner's expected first case. On the rule's evidence the hand ranks first, because three of its entries are in the drawable tier.

**Looked at, not commissioned:**
- **Glass and water, bottle, steam:** already consolidated as reusable builds that passed the gate (`real_kit.tumbler` and `real_kit.water`, `bottle_rig.bottle`, `thermos_real.steam_column`). The job manual says to check `code3d/lib/` first.
- **Cloth:** rank 9, reserve 11 and reserve 28 name a sleeve, a wipe and a curtain. They share a route, not an element.
- **Glass tank:** in 006, 008 and 016, but genuinely geometric, with no recorded improvisation.
- **Single-entry classes:** bird, dog, apple, ant, eye, ear and others fail the recurrence test.

## Code changes needed (reported, not made)

1. **`factory/scenes_schema.py` line 95 must accept `story`.** Until it does, no Historia production can validate. This does not block today's work, because no story topic exists yet; it is needed before the first one is drawn.
2. **`factory/asset_library.py` `new` refuses aliases that blind naming needs.** Its duplicate guard rejected `hand`, `mano`, `fingers` and `dedos` for `hand-articulated`, and `man` for `human-figure` (a substring hit on "human"). Blind naming matches whole words, so a reader's "a hand" cannot pass as those jobs stand. Either the guard changes or the lenses approve adding those aliases to `asset.json` before the first reading. The jobs were opened with what the CLI accepts, and nothing was edited around the guard.
3. **Optional:** `tools/verify_production.py` caps finals at 75 s. A Historia longer than that needs it raised. `tools/scenes_from_script.py` would need `staging_mode` added if the mode should live in scenes.json.

## How to revert

Revert the amendment commit. That removes the doctrine edits and the 11 `in_progress` job records together. The produce skill lives outside the repository, so remove its three added sentences by hand.
