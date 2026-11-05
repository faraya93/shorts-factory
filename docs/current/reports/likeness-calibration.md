# Likeness gate calibration (2026-11-04)

**Question:** does the blind-naming gate catch what the owner caught in 006-011?

**Answer:** the gate as first written caught 5 of 6 and wrongly passed 008. With a confidence floor added afterwards it catches all 6 and still passes both accepted controls. The floor was fitted on this same data, so that 6 of 6 is not independent evidence.

## Method
For each video, the existing gate stills (5-9 per video, all scenes) went through `asset_library.py blind-pack`, and two fresh subagents received only the printed prompt, 16 readers in total. The accepted names were fixed before any reader ran. 004 and 005 were added as positive controls by lens decision, because a gate that fails everything would also "catch" all six. Raw data: `likeness-calibration.json`, replayed by `tests/test_asset_library.py`.

## Results
| Video | Subject | Owner | Reader 1, first guess (confidence) | Reader 2, first guess (confidence) | Names only | With floor |
|---|---|---|---|---|---|---|
| 006 | wrinkled fingers | rejected | screw or threaded peg in a block (30) | dental implant in a jawbone (25) | caught | caught |
| 007 | cloud | rejected | cluster of blue balls (25) | cloud made of water droplets (35) | caught, 1 of 2 named it | caught |
| 008 | ice | rejected | glass of ice water (45) | glass of water with ice cubes (40) | **missed** | caught |
| 009 | soap | rejected | molecule or virus particles (15) | abstract animation, no single object (25) | caught | caught |
| 010 | heart | rejected | blue glass flask with two necks (30) | abstract scene; if forced, an anatomical heart (35) | caught | caught |
| 011 | corn, popcorn | rejected | chocolate egg candy, bonbon (30) | popcorn in a pot (45) | caught, 1 of 2 named it | caught |
| 004 | magnet | accepted | bar magnet (70) | bar magnet (70) | passed | passed |
| 005 | toilet | accepted | cutaway of a toilet (95) | a toilet (95) | passed | passed |

## What this changed
**Why 008 got through:** both readers named it from its one strong frame, a glass of ice cubes, while saying the other views "do not resemble anything specific". Naming alone rewards one good frame.

**Lens decision:** every reader must now also report confidence of at least 60. Rejected videos scored 15-45 and controls 70-95, so 60 sits in the gap. The manual's rule already said to tighten the test when it passes something the owner rejects.

## Limits
- Eight videos is a small sample. The floor was chosen after seeing these results, and confidence is the reader's own report.
- Readers are models reading stills, not people watching on a phone. The owner's eye remains the last gate on output.
- Readers ran as subagents in this repo, which may expose them to project instructions. The stills and prompt were neutral, but full isolation was not verified.
- 004 passed on context: both readers said the bar alone reads as toy blocks (confidence 15-20 for "magnet") and that the paperclips and field lines carry it. This is recorded as a signal, not a verdict; that video is already published.
- 005's underground views read as abstract tanks until the wide shot connects them.
