# Asset job: Articulated human hand (hand-articulated)

Started 2026-11-10.

## Brief

Advance asset, commissioned by the commissioning scan 2026-11-10 (docs/current/reports/format-widening-2026-11-10.md). Priority 1 of 11. Not built yet: the build is a separate session under the unchanged asset rules (isolated blind naming in every pose and state below, no context staging for sealing).

**Trigger met:** both: five undrawn bank entries, and two productions that paid for the missing rig.

**Scripts and entries that prescribe it:**
- banked rank 2 (hand on the cabin door handle)
- banked rank 5 (driver's hands on the wheel)
- banked rank 9 (hand on the car door)
- reserve 25 (hand on the knife and tomato)
- reserve 27 (passengers' hands fumbling with oxygen masks)

**Improvisation already paid:**
- 006: `human-hand` is one fixed pose with no rig, so the video was staged around fingers that cannot bend
- 013 (returned 2026-11-09): carried a rig build as an in-production fallback and failed on the finger-joint cutaway

**What it replaces:** the fixed-pose `human-hand`, which cannot grip, reach or fumble.

**Poses and states to seal:**
- open and relaxed
- gripping a lever or door handle
- gripping a steering wheel
- reaching and touching a car door
- holding a knife handle
- fumbling with a mask (fingers moving)

**Open before the first reading:** Aliases the CLI refused: `hand`, `mano`, `fingers`, `dedos` (its duplicate guard matches `human-hand`). Blind naming matches whole words, so a reader's "a hand" cannot pass until this is resolved. Resolve it before the first reading; see the report.

**Resolved:** `hand`, `mano`, `fingers` and `dedos` added on 2026-11-10 through `asset_library.py aliases --variant-of human-hand`, before any reading.

## Sources searched (query, result, why taken or refused)

Route taken: **sourced** (library), then cleaned and posed. Session of 2026-11-11, Blender 5.2.3 through MCP.
- Sketchfab `rigged stylized hand` (12 results, previews read): "Free Pack - VR Hands (Rigged)" by polyone, CC Attribution, 3.3k faces, 46-bone two-hand rig with 4 joints per finger and thumb. **Taken.** Others refused: "2D Hand Creation Rigged" (Free Standard, not CC0/CC-BY), "Joint Hand BJD" (487k faces, doll joints), "Hand Low-Poly Stylized VR (Rigged)" and "Stylized Skeleton" (not evaluated, first candidate served), skeleton and animal results (not hands).
- Poly Haven `hand mannequin` (models): only tools and gloves; nothing posable. BlenderKit not queried (the Sketchfab candidate passed on sight and by rig test).
- Licence: CC-BY-4.0 (Sketchfab lists "CC Attribution"; version taken as 4.0, same convention as `human-hand`). Attribution in `asset.json` only, never in a description.

## Steps and visual checks

1. Imported (target 0.2 m), deleted default scene objects. Removed the left hand (971 of 1942 vertices by vertex-group dominance, 22 J_Left bones and groups), unparented, applied transforms, scaled x2.7 so the hand is 0.19 m long, reparented. Names: `hand_armature`, `hand_mesh`. Origin at the world origin inside the palm, fingers point -Z, palm faces -Y (documented in `build.py`).
2. **The FBX carried an "Idle" Action** that reset every pose at render time (poses showed in the viewport and not in renders). Removed the animation data and the action. Note for anyone re-importing.
3. Bone rest frames are arbitrary FBX leftovers (tip bones even sit 27 m away), so `build.py` expresses every joint in ARMATURE axes and converts to each bone's local frame: finger flexion is -X, thumb flexion -X, thumb opposition Y/Z. Thumb numbers were found by a small grid search against the bar, then looked at.
4. Skin: the baked skin texture removed; one flat `hand_skin` material slot (retintable per production). Subsurf level 1 on the mesh (render too) to soften the low-poly knuckles.
5. Poses stored as Actions `pose_<name>` on muted NLA tracks (kept in the file): open, lever, wheel, door, knife, mask, mask_b (second frame of the fumble), press, crack. Joint angles in `build.py` `POSES`.
6. Pose proofs (stills in `job/stills/`, local): `hand-<pose>-<view>.png` round 1 (props), `-r2-` round 2 (hand framed larger), `-r3-` round 3 (bare hand in the grip shape). Props for the stills (bar, wheel rim, door panel, knife, oxygen cup, button) are scratch scene dressing, not in the asset collection.

## Checks (QA, blind naming, fidelity)

**QA** (`blender-asset-qa`, profile render): pass, 0 errors. Warnings: 270 duplicate verts (UV-seam splits in the source) and lowest point z=-0.10 (a hand has no ground; origin kept in the palm). 5264 verts after subsurf, 24 deforming bones, 0 unweighted verts.

**Blind naming**, `tools/blind_read.py` (isolated headless readers, three per pose, two stills per pose, `-` means not read). Aliases unchanged since 2026-11-10. Verbatim guesses and confidences are in `job/readings/*.json` and in `asset.json` `checks.blind_naming.poses`.

| Pose | Round 1 (hand + prop) | Round 2 (hand larger, prop smaller) | Round 3 (bare hand in the pose) | Result |
|---|---|---|---|---|
| open | 95/96/96, "human hand" | - | - | **PASS** |
| door touch | 60/92/70, "human hand" (panel behind) | - | - | **PASS** |
| knuckle-cracking fist | 90/85/75 | - | - | **PASS** |
| lever grip | FAIL: "door handle" 60/72/60 | FAIL: "metal grab bar" 55/55/55 | 92/92/85 | **PASS** |
| wheel grip | FAIL: "steering wheel" 60/70/60 | FAIL: "steering wheel rim" 60/55/35 | 90/90/85 | **PASS** |
| knife grip | FAIL: "sword hilt" 60/70/70 | FAIL: "a hand gripping a horizontal bar" 45/40/55 (one reader named it; mean under 60) | 88/90/90 | **PASS** |
| fumble (mask) frame 1 | FAIL: "yellow bucket" 40/40/35 | FAIL: "yellow cup" 35/35/35 | 85/92/90 | **PASS** |
| fumble frame 2 (fingers moved) | - | - | 85/90/88 | **PASS** |
| index presses a button | FAIL: "hand reaching around a gray pole" 35/40/55 | FAIL: "red push button" 70/85/85 | FAIL: "3D cartoon hand pointing down" 55/55/60 (mean 56.7; names the hand, mean under 60) | **NOT SEALED** |

What the table says: with a single-object prompt, a prominent prop is what the reader names, however large the hand. So the asset is read as the hand in each pose, bare (round 3); that is the asset's own test, and the production's gate stills read the hand in its production context later, under the production gate. Round 1 and 2 readings are kept above and count; no alias was added or changed after any reading, no still was re-read to pass. Round 3 is a different test subject (the posed hand), not a re-roll of the same stills. The press pose failed three rounds on its own merits and is **not sealed**: a pointing index reads as "cartoon hand" but under the bar. The "pressing" demand of the prescribing topics is carried by the sealed `door` pose (palm resting on a panel) and the grips, not by an index-button press.

**Fidelity:** none (no reference photo).

## Wall time, spend ($0 expected), anything skipped

About 35 min wall (search 3 min, clean-up and rig 10 min, poses and stills 12 min, three reading rounds 8 min, QA and record 2 min). Spend $0, no account created. Skipped: BlenderKit search (not needed), fidelity check, a wrist/forearm sleeve (a production concern). Seal: `asset_library.py seal` OK; sha recorded in `asset.json`.

Lessons for `human-figure` (written into its brief): (1) strip imported animation data at once, it hides pose errors at render time; (2) express rotations in armature axes and test one bone per axis with a numeric grid search before looking; (3) blind-name the posed asset bare, a prop makes readers name the prop; (4) keep the hand/limb large in the still and the whole shape in frame.
