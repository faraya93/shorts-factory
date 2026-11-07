# Resume of 006, 008, 009 (2026-11-06)

Written for the owner. Nothing was published, $0 spent, no accounts, orchestrator/queue/excluded list untouched. I cannot watch or hear video; everything below is mechanical (stills, blind readers, frame sheets, ffprobe).

## Rules recorded (CLAUDE.md "Script flatness, floor handling and modellability"; lens-decisions rows 2026-11-06)
Script flatness at script stage; standing floor 60 unchanged; ONE-OFF `element_floor_exception` (floor 50, secondary elements only, never `hero_ids`, stamped on each record it touches) for these three; modellability criterion for topic selection. 010's verdict is in its notes.md and INDEX. Test added (28 pass).

## Results
| # | Result | Package |
|---|---|---|
| 006 | DONE. Scene 2 restaged: a hand (four nailed fingers on a palm block) whose middle finger is an x-ray with bone, vessels and nerve; readers 85/75 on finger and vessels. Scene 5 (soap bar, two fingertips) had earlier read 55/65: it passes ONLY under the one-off floor 50. Other scenes carried over (pixel diff < 1e-4). 45.7 s. | `productions/mecanalia-es/006-dedos-arrugados-agua/` (final.mp4, cover.jpg, publish.json; CC-BY credit for the hand by kevinruiz) |
| 008 | DONE. Scene 2 restaged as an ice-cube tray whose cells freeze into cubes above the rim, plus the glass of rising cubes; readers 85/80 on ice and glass. No floor exception was needed. 45.4 s. | `productions/mecanalia-es/008-hielo-que-pasaria-si-se-hundiera/` (own assets, no credit) |
| 009 | STILL SKIPPED. Scene 2: hero thermos 62/55 (floor 60), coffee 60/35. A second change (red mug, steam) produced a hard-edged steam rectangle and was not read. Remaining fix and its cost are in notes.md. | none |

Per-scene dynamism: first/middle/last contact sheets for 006 and 008 show a changing picture in every scene. Script flatness check: all three scripts have progression (a turn each: cutaway/wrinkle/grip; freeze/sink/lake; three heat paths then vacuum).

Process notes: parallel Blender jobs caused GPU out-of-memory failures (my fault; fixed by running one render at a time, the chain's retry then passed); 008 scene 1 aborted in openvdb because volume cubes were scaled from zero (now dropped in from above); water scenes render slowly (15-58 s/frame, scene 4 of 008 took 3.5 h). Records for unchanged scenes were carried over after pixel diffs, as before. INDEX: my first edit put 010's verdict on the 006 row; fixed.

## Counter-recommendations from the lenses (owner decides)
1. **Floor.** The exception changed the outcome of exactly one scene (006 scene 5, 55/65). The bigger problem is reader variance, not the floor: identical stills got 62 vs 55 (009 thermos) and 85 vs 35 (the same mug scene, two readers). A single weak reader fails a scene. Recommend, instead of any lower floor: three fresh readers, pass if the mean is >= 60 and no reader is below 45, and a reader whose answer names the element correctly but whose confidence is about the whole scene is read per element. This keeps the bar and reduces false blocks. Not applied; needs your decision.
2. **Flatness.** Agree with the rule. Two sharpenings: the turn must happen before the final reframe scene (a reframe-only turn is not progression), and the check should be a one-line "what changes in the world" per scene in the beat sheet, signed by the scriptwriter lens. Caveat: by that test 008 is the weakest of the three (ice and glass in five of six scenes); the owner may find it flat even though the script passes.
3. **Modellability.** Agree. Add a second check: recognisability at phone size needs a context cue (the tray made the ice read, the handle made the thermos read, the mug did not make the coffee read). Topics whose key element is a bare liquid or a bare cylinder should be reshaped around an object that cues them.
4. **Operations.** Render one Blender job at a time; stills and gate runs wait for the chain. Water scenes should get a cheaper profile or lower samples for drafts.

## Open owner items
Publish verdicts on 006, 008 (and 010); whether to resume 009 (needs a soft steam column or coffee pour, and a cup-style thermos cap that touches all seven records); whether to adopt counter-recommendation 1.
