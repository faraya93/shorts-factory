# Asset job: Stylised human figure (human-figure)

Started 2026-11-10.

## Brief

Advance asset, commissioned by the commissioning scan 2026-11-10 (docs/current/reports/format-widening-2026-11-10.md). Priority 2 of 11. Not built yet: the build is a separate session under the unchanged asset rules (isolated blind naming in every pose and state below, no context staging for sealing).

**Trigger met:** both: a finished production paid for its absence, and bank entries prescribe it.

**Scripts and entries that prescribe it:**
- banked rank 1, drawn as 017 (passenger as a stylised figure)
- reserve 16 (stylised falling figure)
- reserve 21 (one person as the unit of scale)
- banked rank 9 and reserve 17 are reshaped around the missing figure (hand, sleeve and seat; legs and boots)

**Improvisation already paid:**
- 017: "the passenger is never drawn; a phone stands in for the jump"; the phone stand-in needed a re-stage and one of three readers still named the car first

**What it replaces:** phone-for-a-person and body-part framings; without this asset people stay off screen (drawability rule).

**Poses and states to seal:**
- standing
- jumping, mid-air
- falling, limbs spread and tumbling
- seated (passenger or driver)
- sunk to the waist, legs and boots visible through a cutaway

**Open before the first reading:** Alias the CLI refused: `man` (a substring hit on `human`). Readers often say "a man". Resolve it before the first reading; see the report.

**Resolved:** `man` added on 2026-11-10 through `asset_library.py aliases`, before any reading, after the guard moved to whole words.

## Lessons carried in from `hand-articulated` (read before starting)

Imported animation data hides pose errors at render time (strip it); express rotations in ARMATURE axes and convert per bone; with a prop in the still, readers name the prop, so the asset is blind-named as the bare figure (a chair or a block is acceptable only when it cannot take the name); keep the whole figure large in frame; every failed round stays in the record.

## Sources searched (query, result, why taken or refused)

Route taken: **modelled** (own work, code-built), after sourcing found nothing in the channel's look. Session of 2026-11-11, Blender 5.2.3 through MCP.
- Sketchfab `mannequin rigged low poly no face`: 1 hit (a skeleton warrior; refused, not a figure). `stylized humanoid character base rigged capsule`: nothing. `mannequin` (15, previews read): shop-window busts, torsos and dress forms with no limbs; art mannequins are unrigged poses or branded ("Fortnite" mannequin: refused, brand). `rigged base character` (15): realistic anatomical bases (muscle male 26k faces with a CMU skeleton, tried: imported, realistic skin and muscles, refused and deleted; female bodies 100k+ faces), chibi, cyborg: none matches the reference (capsule limbs, no face, colour blocks). All CC-BY at best; none taken.
- Poly Haven: not queried (CC0 models are props, not rigged people). BlenderKit: not queried (no new information expected for a stylised mannequin).
- CharMorph and MB-Lab (manual step 6): not installed, not tested on Blender 5.2.3, and both produce realistic bodies (the reference is a faceless capsule mannequin; MB-Lab also needs an AGPL decision). Not used, so no AGPL lens decision was needed.
- Licence of the result: own-work (code-built, nothing sourced), no attribution.

## Steps and visual checks

1. `build.py` generates everything: 19 closed lofted meshes (capsule limbs, shaped torso and pelvis, egg head with no face, boots with shafts), 17 bones (root, pelvis, spine, chest, neck, head, shoulders, elbows, wrists, hips, knees, ankles), each part rigidly weighted (1.0) to one bone; round end caps overlap at joints so bends read as one body. 1.78 m, faces -Y, standing on z=0, origin at the feet.
2. Colour blocks are separate material slots `fig_skin`, `fig_shirt`, `fig_pants`, `fig_boots`, flat, retintable through `hero_colours`.
3. Poses as Actions on muted NLA tracks (`pose_standing`, `walking`, `jumping`, `falling`, `seated`, `sunk`); angles in `build.py` `POSES` (left side given, right mirrored). Pose bug found while building: a hanging arm and a raised arm abduct in opposite Y directions, so the arms crossed over the head until the sign was flipped for the raised poses.
4. Pose proofs: `job/stills/fig-<pose>-<1|2>.png` (local). `seated` stands on a four-leg chair, `sunk` is waist-deep in a round sand pit with a translucent cutaway wall (legs and boots visible through it); props are scratch scene dressing, not in the asset collection.

## Checks (QA, blind naming, fidelity)

**QA** (`blender-asset-qa`, profile render): pass, 0 errors. First run flagged 40 degenerate faces and 80 zero-length edges per mesh (zero-radius pole rings made 20 coincident vertices); fixed in `loft` (a single pole vertex) and rebuilt, rerun clean. Remaining warning: no UV map (flat colour only, by design). No z-fighting, enclosed or floating objects.

**Blind naming**, three isolated readers per pose, two stills each (`tools/blind_read.py`; verbatim guesses in `job/readings/*.json` and `asset.json`). The geometry fix after the readings changed no visible shape (same profiles, poles only).

| Pose | Round 1 | Round 2 | Result |
|---|---|---|---|
| standing | "artist's mannequin" 85/85/60 | - | **PASS** |
| walking | "walking artist's mannequin figure" 92/90/85 | - | **PASS** |
| jumping, mid-air | "jointed 3D mannequin figure" 80/72/55 | - | **PASS** |
| falling, limbs spread | "3D mannequin figure ... mid-air" 90/85/85 | - | **PASS** |
| seated | FAIL: one reader "toilet" 70/45/40 (block seat and backrest read as a toilet) | "seated wooden mannequin figure on a chair" 85/80/72 | **PASS** (round 2: chair with four legs) |
| sunk to the waist, legs and boots visible | FAIL: 60/72/45 (mean 59, "mannequin rising through a table") | FAIL: 55/40/60 (mean 51.7, one reader under 45; "ragdoll rising out of a barrel") | **NOT SEALED** |

Two correction rounds were spent on the sunk pose, as the manual allows; it is recorded as not sealed, not lowered. The readers do name the figure ("mannequin figure"), so the miss is confidence, not likeness: the sand pit and cutaway dominate the frame. A later session may try a third staging; it needs three fresh readers and counts every reading. Every figure reading names the figure as a "mannequin" (an alias), none as "person" or "man": readers see the capsule look as a mannequin, which is what the reference describes.

**Fidelity:** none (no reference photo).

## Wall time, spend ($0 expected), anything skipped

Measured by the system clock: about 7 min (00:53 to 00:59 on 2026-11-11; my phase estimates were guesses and are dropped). Spend $0, no account created. Skipped: CharMorph/MB-Lab (not installed; realistic bodies), BlenderKit, fidelity. Not built: a face (by design), fingers (the figure's hands are mitten capsules; use `hand-articulated` for close hand work), hair.
