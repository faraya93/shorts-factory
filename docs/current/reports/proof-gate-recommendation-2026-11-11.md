# Proof gate after B5: recommendation to the owner (2026-11-11)

This is analysis only. One Opus session ran it. Before starting, no `tools/run_productions.py` process was alive. No code, doctrine, build, reading, production or publish was touched. The owner decides; this report recommends.

**Sources read:** `b5-2026-11-11.md`, `architecture-second-opinion-2026-11-11.md` (P7, P8), `b4-2026-11-11.md`, and every recorded reading in `proofs.json` for 022, 026, 027, 028 and 030. Also: the asset blind-naming records for bird, electric-arc and earth-globe, `tools/blind_read.py`, `factory/asset_library.py` (`judge_guesses`, `blind_pack`), `factory/proofs.py`, the `returned.json` files and notes for 021, 022, 023 and 025, the doctrine sections "Extended likeness gate", "Event elements", "Context staging" and "Likeness gate", `cadence-decision.md`, and `format-policy.md` (read-out).

**Two measurements taken here, both read-only:**
1. A scan of all 118 element records in `build/gate/elements.json`.
2. A visual check of 022's N1 still against the clean rung-4 still of the same staging.

## 0. The short answer

1. **Reader prompt:** keep its text unchanged. Add one narrow supplement that already exists in code and doctrine. An element staged inside a dominant context (an event on a carrier, an element next to a sealed hero) is declared as a two-element scene and read with the existing `--multi` reading. This is chosen in `proofs.json` before any reading, and every reading records which prompt produced it. First run a calibration replay on stills the owner has already judged; it costs under US$0.15 in Haiku readers.
2. **Failed proofs:** the B5 report blames the dominant-object pull for most failures. It explains 4 of the 15. The other 11 come from alias specification errors (4), low confidence on collective subjects (2) and builds that read as something else (5). Section 2 sorts all 15. Accept three capability boundaries:
   - magnified tissue (all of 030)
   - a free-standing electric arc
   - electric current as a visible thing on its own
3. **Canary:** one Opus redesign session, then one braked Sonnet proof unit, then **027, 026 and 022** if the supplement is adopted. If it is not, the third unit is 028. 030 goes back to the bank and 029 is parked. 022 is the cheapest unit in the system to finish, and its spark is the purest proven-risky element.
4. **What the repair got wrong:** a proof that failed on an off-spec still returned a topic for good. Proof readings were taken on EEVEE drafts, which the house rules reserve for the session's own checks. Alias sets are inconsistent within a unit. No reading records which prompt produced it. The standby buffer is effectively empty.

## 1. The reader prompt: keep, change, or supplement

### What the gate measures today, from the records

The single-object prompt asks readers to "name the single object they show ... your first guess in one short noun phrase, then two alternatives". The matcher (`judge_guesses`) searches each reader's whole reply for a declared alias, so the alternatives count too.

A scan of the 118 current element records shows that **20 of the 109 passes (18%) already rest on an alias found outside the reader's first guess.** Some of those readings used the existing `--multi` prompt ("up to three short noun phrases, most prominent first": 008, 009, 010, 015). Others matched on a single-prompt "alternative":
- 017 scene 4, "elevator car (alternatives: smartphone, vending machine)"
- 020 scene 2, "a car ..., alternatives: a lightning bolt"
- 024 scene 4

So in practice the gate already measures "is the element among the first three things a scroller names" for about a fifth of its passes, 020's lightning bolt among them. The single-object wording is not a fixed property of the gate.

### What the prompt does and does not explain in B5

Each failed proof, with its cause read from the recorded guesses:

| Cause | Proofs | What the readers wrote |
|---|---|---|
| Dominant-object pull (the element shares the frame with a stronger object) | 022 N1, 026 P1, P4, P5 | "microwave oven with open door"; "ocean liner"; "cutaway ocean liner ... half-submerged"; "ocean liner model in a blue glass block" |
| Alias specification error (right object named, by a word the proof did not declare) | 028 A1, P3, P4, P5 | "pigeon", 85-93, all three readers. P1 of the same unit declared "pigeon" before any reading and passed |
| Collective subject, one reader's confidence low | 027 P2, P4 | All three named a crowd or figures (alias matched); one reader at 40, one at 35. Two wrote "Not a single object" |
| Build reads as something else | 028 P2; 030 P1, P2, P3, P4 | "glass-tube railing" 30/30/30; "flying saucer", "translucent cone", "dessert bar", "candy bar" at 15-45 |

A prompt change can only help the first row, and partly the third. The fourth row is the gate doing its job: water that reads as a glass block, a wire that reads as a glass tube and tissue that reads as candy would fail the owner's eye too.

### The options

| Option | What the gate would then measure | Comparability of past passes | Verdict |
|---|---|---|---|
| **Keep, unchanged** | Single-object likeness. Events pass only when a reader happens to put them in a modifier ("fork *sparking* in a microwave") | Untouched | Right for heroes, asset seals and one-element scenes. Wrong for events in context: the same 022 staging read "sparking" once and missed it once (see section 4) |
| **Change the wording for every reading** | A new instrument everywhere | Breaks all 109 element passes, every asset seal and the 2026-11-04 calibration (`likeness-calibration.md`) | Reject. Large cost for a cause behind 4 of 15 failures |
| **Supplement: use the existing `--multi` reading for elements declared in context** | Single-object likeness for heroes, seals and one-element scenes. "Named among the main things" for an element declared beside a dominant object | Untouched. `--multi` is already in `asset-system.md`, already in `blind_read.py`, and already carries passes on record | **Recommend**, with the calibration replay first and the three conditions below |

### Conditions on the supplement

1. **Declared in advance.** `proofs.json` (or `scene_elements`) states `reading: multi` and declares both elements before any reading. It is never chosen after a failed single reading of the same staging.
2. **The event is named, not just its carrier.** An event element's aliases always contain the event itself (noun or declared verb form), never only the carrier object. Otherwise the gate checks the ship and not the flooding. 026 P6 passes on "sinking" under this rule. P4 and P5 as written would still fail, which is right: their water reads as glass.
3. **Flagged like context staging.** A pass through `multi` is flagged in `notes.md` (owner rule 5 of "Context staging"), so the owner's verdicts on those videos can be checked against it.

**Every reading records its prompt.** Add `prompt: single|multi` and a prompt hash to each reading from now on. Today no record says which prompt produced it, so the 20 non-first-guess passes cannot be fully told apart. This is a small B1-style code change.

### The calibration replay

`multi` has no owner-verdict calibration: 008-010 and 015 still await the owner's verdict. Before adopting it, the lenses read a fixed set of stills the owner has already judged under `multi` (three readers each, about 15 readings, under US$0.15), recorded as calibration, not as gate readings:
- **Negative controls:** stills of the archived, owner-rejected 006-011 originals.
- **Positive controls:** stills of videos the owner approved.

Stills from live or returned candidates (022, 023, 026-028) stay out of the set, so the calibration cannot double as a re-roll. If `multi` passes any owner-rejected still, the supplement is dropped.

### The 30-day test

The test runs from 2026-11-01 to 2026-11-30 and measures **publishing cadence** on published videos (`cadence-decision.md`). Its read-out tags each video's `structure_variant` and staging mode (`format-policy.md`). The gate's reading prompt is upstream of the dataset, so changing it does not mix cadence regimes. The test's real exposure is supply: about 13 verified packages await the owner's verdict (006-011, 015-020, 024) against about 19 remaining publish days. If most are approved, the test needs only a few more videos late in the month (ESTIMATE; the publish queue is not visible from this repo). So the test neither forbids the supplement nor justifies skipping the calibration. One extra tag in the read-out ("element passed under multi") covers it, as with context staging.

## 2. The failed proofs, element by element

### Fixable at staging level: same beat, element the subject of its frame, spec-compliant still

| Proof | Evidence | Fix |
|---|---|---|
| 026 P1 iceberg (scene 1) | The liner was named; one reader listed "iceberg" as an alternative. P3 shows the iceberg reads 92/88/92 when it fills the frame | Iceberg in the foreground, large; the liner small behind it. Or the declared two-element `multi` reading |
| 027 P2 grey crowd | All three named a crowd (mean 75); one reader at 40 wrote "Not a single object" | Fewer, larger figures built from the sealed human-figure, camera closer. As a crowd, also a natural `multi` case |
| 027 P4 one and twelve | All three matched "figures"/"crowd" (85/60/35); the figures read as "mannequins, chess pieces" | Same: sealed human-figure at readable scale, the accent figure central and largest |
| 028 P3, P4 | The bird was named "pigeon" at 85-90; the aliases omitted "pigeon" | Declare the unit's own pre-reading alias set (P1 declared "pigeon" before any reading), so this is not an alias added after a guess. The lenses record that reasoning. The current path stays a cue on the bird; the gate reads the bird |
| 028 P2 current on wire | "glass-tube railing" 30/30/30: the translucent jacket made the wire read as glass | An opaque dark cable with insulators and a crossarm (a power line that reads as one), the current as emissive pulses along it, read as a declared power line + current pair under `multi`. **If it fails again, it is the boundary below** |

### Needs the beat re-staged at script level, so the element is the subject

| Proof | Evidence | What the creative session decides |
|---|---|---|
| 026 P4 bow flooding | "cutaway ocean liner ... half-submerged" (72/75/80): the hull dominates and no flooding is named | Rewrite scene 4 so a compartment filling with water is the subject (close, one or two boxes, the bow silhouette as a small cue). The water uses a material that reads as water: P7's tray water passed |
| 026 P5 bulkhead spill | "ocean liner model in a blue glass block" ×3: water read as glass | Scene 5 already holds the passed ice tray (P7, "water spilling from cell to cell"). Make the tray spill the key element and the hull spill its echo, or rebuild the water as for P4. A script and lens choice |
| 028 P5 big bird on pole | "cartoon pigeon with outstretched wings on a power line" (93 ×3): neither size nor species came across | Either rewrite the beat so the sealed bird's spread wings bridge two conductors (only if that is sourced as true; large birds are the documented case), or source a free-licence raptor. Do not scale the pigeon up and call it large |
| 028 A1 bird seal | "pigeon" 88-93 from all three readers; two replies also contained "bird". The asset was declared generically (bird, birds, goose, pájaro, ave) | The no-added-alias rule bars rescuing this asset, and I do not recommend bending it. Instead, open a new asset job declared at species level before any reading, read from a fresh still set (the wings-spread state P5 needs anyway), recorded as a declaration error. Forward rule: an organic asset is declared at the level readers name (species), not the class |

### Capability boundaries: stop paying

| Element class | Evidence | Recommendation |
|---|---|---|
| **Magnified tissue and cellular-scale sections** (030 P2, P3, P4; P1 too as built) | 15-45 confidence: "translucent cone", "dessert bar", "candy bar", "flying saucer". The same family as 012's droplets and 025's seed interior | Return 030 to the bank, marked boundary: its mechanism heart (mucus, bicarbonate, cell renewal) lives at this scale. Add the class to the modellability screen |
| **A free-standing electric arc** | Asset naming 35/60/60; 022 rung-2 bolt alone 55/40/45; 023 five failures; 020's arc only passed beside a car | Close the electric-arc asset job (keep `arc_rig.py`). Arcs appear only as an event on a sealed carrier, read in context |
| **Electric current as a visible thing on its own** | 028 P2 30/30/30 | Only as a cue on a carrier that reads by itself. No proof for "electricity" as the named subject |

**Not a boundary: 022 N1** (see section 4). **Not built:** 029 (seven new builds, a FLAGGED unsourced turn) and 014 (optional). Park both; no proofs are built until a slot needs them and 029's flagged fact is sourced.

## 3. The path to a valid canary with the least waste

**Composition change:** yes. 022's return removed the one unit with a proven-risky element. 030 is a boundary. 029 is the most expensive to prove.

Ranked by expected cost to eligibility:

| Unit | Open proofs | Expected cost |
|---|---|---|
| **027** | P2, P4: two near-miss stagings, sealed globe | Cheapest |
| **022** (only if the supplement is adopted) | Oven seal (the readers already named the oven at 95-97 in every reading) and one N1 reading under `multi`, declared in advance. Hero and scenes 1-3 and 5 already passed | One seal, one reading |
| **026** | P1 staging; P4 and P5 script rewrites; seven-scene Historia | Moderate |
| **028** | New species asset, P2 restage, P5 script rewrite or new raptor asset | Most expensive |

### Steps

1. **Opus creative session, one session, no builds:**
   - Record the lens decisions: the `multi` supplement after the calibration replay; prompt recorded per reading; proof-still conformance (below); one alias set per element per unit; the three boundaries; 030 returned; 029 parked.
   - Redesign 027 P2/P4, 026 P1/P4/P5 and 022 N1 from the readings above.
   - Run the calibration replay before the `multi` decision.
2. **One braked Sonnet proof unit:**
   - Build the stills to spec: half-resolution Cycles for readers, as the house rules require.
   - Check each still against its spec before any reader runs.
   - Read once.
   - About 7 proofs and 1 seal.
3. **Canary:** 027, 026, 022. If the supplement is rejected, 028 replaces 022 and its redesign joins step 1.

**Stop-loss:** a redesigned proof that fails a second time is that element's boundary, and the unit is returned. There is no third design round.

**If only two units are eligible after step 3:** launch those two and let the third join when ready. Waiting costs videos; the return-rate measurement simply needs one more unit.

**Bank:** the refill stays due (about 5 drawable entries). It belongs in its own Opus session, not the redesign session (second opinion, context-growth argument).

## 4. What the repair got wrong, or left open

1. **A reading on an off-spec still settled a topic for good.** N1's spec said "re-render it (half-resolution Cycles)". It was read on the `--cpu` draft path (10 samples, 432×768, no denoise). Comparing the two stills: the clean rung-4 still of the same staging read "microwave oven with a fork and spoon sparking inside" 96/95/96. Under N1's declared aliases ("sparking") that reading would pass. The noisy N1 still blurs the fork and spoon; it read "microwave oven with open door" 96/96/95. The bolt is visible in both.
   - "Every reading counts" was applied as "every reading is valid".
   - **Forward fix:** before any reader runs, the still's resolution and render path are checked against the proof spec. A non-conforming still is not read. N1 stays on record as it is.
   - Whether 022 comes back is a lens decision. On this evidence the return is an artifact of the render path more than of the element. My recommendation (section 3) brings it back only through the advance-declared `multi` reading, which is a new forward instrument, not a re-read of the old one.
2. **Proof readings were taken on EEVEE drafts** (B5 deviation 2). House rules reserve those for the session's own checks; readers get half-resolution Cycles. Two of the "build reads as something else" failures are transmission materials (water as glass, wire as glass tube), where EEVEE and Cycles differ most. B5's EEVEE passes may not transfer to the production gate, and some failures may be the renderer's.
3. **The diagnosis overstated the dominant-object pull** (section 1 table: 4 of 15). Acting on it alone, for example by rewording the prompt, would have broken comparability and still left 11 failures.
4. **Alias sets are inconsistent within a unit.** 028 declares "pigeon" for P1 but not for A1, P3, P4 or P5. 026 includes "ship" for P2 and P6 but not P4 or P5. The asset brief lists "goose" for a pigeon-like bird. Outcomes depend on unreviewed alias design. **Fix:** one alias set per physical element per unit, which proofs reference, plus a lint test that flags a mismatch.
5. **No reading records its prompt.** Comparability is already blurred: 20 of 109 passes rest on non-first-guess naming, some through `multi`, some through the single prompt's alternatives (017 scene 4 passed with "smartphone" as an alternative). Do not tighten the matcher now (comparability), but record the prompt from here on. The owner's verdict on 017 is the real check of that pass.
6. **Builds were simplified and still counted** (B5 deviation 3: no night stage, no water jets, a faint dotted path, the meat outside the cavity). A failed proof cannot then be attributed. **Fix:** the builder writes a conformance note against the staging spec, and a deviation defers the reading rather than spending it.
7. **The standby buffer is effectively empty.** Both standbys hold pending proofs, one is a boundary (030) and one is unbuilt and costly (029). The P6 design assumed drawable standbys. With 14 of 21 element proofs failing (67%), proofs now feed the creative session faster than it refills. Until a unit passes, every return waits for Opus.
8. **Proof-stage cost is unmeasured.** B5 reports reader costs (about US$0.002-0.007 each) but not the Sonnet session's notional. The owner's metric (cost per verified video) now needs cost per eligible unit, including failed proof rounds. Without it the stop-loss in section 3 cannot be tuned.
9. **The B2 event-alias rule was necessary but not sufficient.** Verb forms only help when a reader happens to write the event as a modifier of an object. Every event proof that passed did so through a carrier noun or such a modifier. Supplement condition 2 makes the carrier question explicit, which today's specs answer differently from proof to proof.

## 5. Judged against the owner's objective

The objective is cost per verified video and verified videos per usage window, with Opus writing and Sonnet producing.

- **Proof waste:** the supplement and the boundaries cut repeated proof rounds on classes that cannot pass (030, the arc asset, abstract current).
- **Cheapest videos first:** 027 and 022 are the cheapest units to finish. 022 especially: its hero and four of its scenes have already passed.
- **Bounded Opus spend:** one redesign session, the refill kept separate.
- **Gate stability:** no change to thresholds, readers, isolation or the hero prompt, so stable operation is not traded for speed.
- **Tokens spent on measurement:** the calibration replay and the proof-cost record. Both are small.

## 6. The strongest objection to the main recommendation

It changes the instrument right after the instrument failed the units the factory wants to pass, which is the shape of goal-post moving. `multi` certifies "noticed among the main things", not "recognisable as the subject". The gate's calibration (2026-11-04) covers single-object readings of heroes only, and no `multi` pass has an owner verdict yet. If the owner rejects videos whose key element passed only under `multi`, the factory will have spent full productions on passes that predict nothing. Reviving 022 through it sharpens the objection: it looks like a rescue of the one topic the old reading killed.

**What answers it, and the limits of that answer:**
- The calibration replay uses only stills the owner has already judged.
- The declaration comes before any reading.
- The `multi` flag lets the owner audit every such video.
- `multi` already carries passes on record, so this formalises existing practice rather than adding a new instrument.

None of this proves the passes predict the owner's eye. Only the owner's verdicts can.

## 7. Evidence that would change my mind

- **The calibration replay passes any owner-rejected still under `multi`:** drop the supplement. Events in context become a boundary, and the canary runs 027, 026 and 028.
- **The owner rejects 008, 009, 010 or 015** for the likeness of an element that passed only as a second-named item: same conclusion.
- **Redesigned proofs fail again at 50% or more with the element as the subject and the stills to spec:** the limit is the factory's build capability, not the instrument. The right move is then a stricter modellability screen at topic selection (sealed-asset-heavy topics), not more proof rounds.
- **Measured proof-stage cost per eligible unit exceeds the cost of a returned unit** (about US$5.50 notional on the 2026-11-11 batch): proofs are not paying. Narrow their scope to element classes with a recorded failure.
- **The publish queue shows the test running out before 2026-11-30:** ship the canary with whatever is eligible (027 first) and defer the 022 decision rather than wait for the calibration.

## 8. What did not change

No code, doctrine, threshold, alias, proof status, asset record, batch file or production folder was touched. This report adds no doctrine. Precedence: `doctrine-topics-and-scripts.md` "Blind proofs before batch eligibility" and `doctrine-production.md` "Extended likeness gate", "Event elements" and "Reshape ladder" govern until a recorded lens decision amends them under the standing procedure.
