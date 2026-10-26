# Spike — the other scenes in the LACE-UP graphic system (concept first), 2026-10-25

Owner picked LACE-UP. Same backdrop (#E2D5F1 flat), palette hexes, toon pass, flaps, eyelets, thick black lace, dark-steel
needle with an eye. One draft frame per scene at 1080x1920 (`frames/`, overview `frames/sheet.png`). $0 spend.
Code: code3d/lib/lace_world.py (shared parts), code3d/lib/shapes.py (+ bar_between), code3d/scenes/spike_lace_world.py.

## Fix: the floating lace end (scene 2)
The lace is one cord with two ends and the needle can only be on one. Now the lace is folded DOUBLE through the needle's eye: both
strands converge into it (how a needle is actually threaded), so nothing floats. `frames/2-lace-up-fixed.png`.

| Scene | Frame | One line | Why it reads instantly |
|---|---|---|---|
| 1 setup | `1-setup-wide-gap.png` | Bare eyelets and a very wide red gap; two chubby tabs reach toward each other from the flaps and stop short. | Two things reaching and not touching is the universal picture of "too far apart to meet by themselves". |
| 3 tying off | `3-tying-the-bow.png` | The laces crossed all the way up and finished in a bold bow, the boot's red tongue peeking above. | Everyone ties a bow to finish lacing; it is the end of the action. |
| 4 dissolving | `4-dissolving-beads.png` | The lace is a chain of beads: whole at the bottom, shrinking upward, gone at the top, floating away as outline bubbles while the flaps stay shut. | Beads shrinking and popping into bubbles is the cartoon idiom for dissolving; the shut flaps say the closure stays. |
| 5 removal | `5-removal.png` | One smooth whole plate, no seam; a cord is pulled out of a tiny red hole by chunky tweezers. | Tweezers drawing a thread out of a smooth surface, with nothing left behind, is "removed, whole again". |
| 6 ant | `6-ant-clamp.png` | A cartoon ant (red body, three segments, antennae, black pincers) clamps two raised folds of skin together like a staple. | A recognisable ant biting a pinched fold needs no explanation; its jaws are visibly the stitch. |

## Honest observations (frames, not a verdict)
- Scene 4 is the hardest beat and the weakest metaphor: "slowly over days" is only implied (the gradient from whole to gone); no clock
  or day cue is drawn. The bubbles sit over some eyelets.
- Scene 1: the tabs are plain rounded rectangles; they read as "two pieces not meeting" more than as "reaching".
- Scene 5: the tweezers' two arms overlap into almost one bar; the plate has no hint of the earlier eyelets/seam beyond the hole.
- Scene 6: the ant is built of flat primitives and reads clearly as an ant; the pinched folds are two small fins (their height shows
  only from this low 3/4 view, which differs from the other scenes' top-down view).
- Camera: scenes 1-5 share the top-down 3/4 (60-74 deg) boot view; scene 6 uses a lower side view (30 deg, 38 deg azimuth).
- Time: ~5 min wall clock (22:50:06 -> ~22:55), 4 render rounds. No existing production touched.
