# puntos-de-sutura-v5-drawn: lace-world build report (2026-10-25/26)

Six scenes animated from the shared `code3d/lib/lace_world.py` into v4's exact slots (242/367/133/164/185/227 frames, 43.93 s),
v4 narration, subtitles and music, toon pass, flat unify (grain 0, vignette 0). fal spend: US$0.00. No existing production modified.

## Final render actuals (driver `render_seconds`, 1080x1920, 96 samples)
| scene | frames | render | s/frame | note |
|---|---|---|---|---|
| 1 hook | 242 | 243.2 s | 1.00 | |
| 2 curved-needle | 367 | 2120.0 s | 5.78 | wall clock includes an apparent machine stall (~20 min); normal rate ~1 s/frame |
| 3 knots | 133 | 1722.9 s | 12.95 | same: apparent stall; normal rate ~1.3 s/frame |
| 4 absorbable | 164 | 259.2 s | 1.58 | |
| 5 risk | 185 | 245.4 s | 1.33 | |
| 6 ant-twist | 227 | 189.9 s | 0.84 | |
Render time at normal rates would be ~20 min; measured wall time is 76 min because of the two stalls (reported, not hidden).

## Session
Batch start 22:59:48, assembled 01:26: ~2 h 27 min (cap 3 h; no scene passed 60 min). Includes one failed final batch:
scenes 3, 4, 5 crashed Blender (depsgraph) on frame 2 because they toggled `hide_render` per frame with Freestyle on; only
single-frame draft stills had been checked. Fixed with `lw.show` (parks hidden objects at z=-500), retested at draft, re-rendered once.

## Checks (mechanical)
final.mp4 1080x1920 @30, H.264, 43.93 s; narration slots match; background QA dE 0.7 in all six scenes; no clip audio (gate n/a).

## Frames (contact sheet build/frames/sheet.png, start/mid/end per scene; observable only)
1 gap opens, red tongue widens, tabs emerge from under the flaps; 2 needle crosses the eyelets, laces fold into its eye, flaps close;
3 X-laced boot, black bow grows at the top; 4 laces shrink top to bottom, outline bubbles rise, end shows empty eyelets with bubbles still over them;
5 cord stub in hole, tweezers grip and pull it out, end shows a bare plate with the tweezers leaving the top of the frame; 6 ant on a plate with lip folds closing beside its jaws.

## Open polish items
- Scene 2 start: the needle begins mostly off-screen left.
- Scene 3 frame 2: a tiny dot is visible below the boot.
- Scene 4 end: bubbles linger over the eyelets.
- Scene 5 end: tweezers exit with a short cord stub; the frame is nearly empty.
Not judged: motion feel and timing (cannot watch video).
