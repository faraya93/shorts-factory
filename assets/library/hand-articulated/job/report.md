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

## Steps and visual checks

## Checks (QA, blind naming, fidelity)

## Wall time, spend ($0 expected), anything skipped
