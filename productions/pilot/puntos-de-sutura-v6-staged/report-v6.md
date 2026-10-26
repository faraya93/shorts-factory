# puntos-de-sutura-v6-staged: glossy 3D cartoon build (2026-10-26)

**Phase 1 clip (scene 2, recipe proof, narration + subtitles):** productions/pilot/puntos-de-sutura-v6-staged/build/test-scene-02.mp4 (12.23 s)
**Full video:** productions/pilot/puntos-de-sutura-v6-staged/final.mp4 (43.93 s, 1080x1920, 30 fps). Media is gitignored (local only).

Recipe: chunky modelled volumes, Principled glossy materials, one soft sun + ambient HDRI (soft shadows), subtle depth of field,
no outlines, no cel bands, camera orbiting and pushing in during every scene. Same slots, narration, subtitles and music as v4. fal spend US$0.00.

## Render actuals (driver render_seconds = wall clock; "active" = frame-timestamp pace without gaps > 60 s)
| scene | frames | wall | active | stalls |
|---|---|---|---|---|
| 1 hook | 242 | 1588 s | 383 s (1.60 s/f) | 2, 1204 s |
| 2 curved-needle | 367 | 673 s | ~1.8 s/f | none (rendered unattended-free) |
| 3 knots | 133 | 3862 s | 193 s (1.51 s/f) | 4, 3667 s |
| 4 absorbable | 164 | 2925 s | 313 s (1.97 s/f) | 4, 2610 s |
| 5 risk | 185 | 1652 s | 324 s (1.78 s/f) | 2, 1326 s |
| 6 ant-twist | 227 | 1219 s | 446 s (2.01 s/f) | 4, 771 s |
The machine stalled/slept repeatedly during the unattended batch (single gaps of 650-1000 s between consecutive frames). By wall clock
scene 3 took 64 min (over the 60-min safeguard); ~61 of those minutes are stalls, ~3 min is rendering. The batch ran unattended, so
the safeguard could not interrupt it; no scene failed or was re-rendered. Session: v6 started 09:20, assembled ~12:50 (wall, includes stalls); active rendering ~28 min.

## Build notes
- Library: code3d/lib/boot_world.py (GlossStage, chunky boot, Flaps, adopt, back/overshoot); scenes code3d/scenes/stage_01..06.py (scene_script_prefix "stage").
- Iterations before the final render: boot shape (4 rounds: brick -> tapered boot with toe cap and collar rim), sensor height fix (36 mm), needle/cord chunkier, camera framing, bubble material (coat made them opaque).
- Deviation: the channel's default vignette greyed the lavender stage, so v6 sets unify vignette_angle 0 (grain 5 and the colour grade kept).
- Palette additions in the production's visual_identity: leather brown, flap leather, toe cap brown, sole cream, thread black (the brief asked for leather-brown).
- Floor: a plane that renders as the exact backdrop where lit and darkens in shadows (a shader trick; the backdrop is unchanged: QA dE 0.7 in all scenes).

## Checks (mechanical)
final.mp4 1080x1920 @30 H.264, 43.93 s, slots match; background QA dE 0.7 in all six scenes; no clip audio.

## Frames (build/frames/v6-sheet.png; start/mid/end per scene; observable only)
1 flaps start nearly shut with two cords hanging, spring wide open showing the red tongue, camera pushes in; 2 needle with a thick cord laces diagonals row by row, flaps narrow to a thin seam, cord ends at the top; 3 laced boot, knot then a big black bow; 4 bead lace shrinks from the top, glassy bubbles drift up, empty eyelets at the end; 5 hole with cord, tweezers pinch and lift it, seamless panel at the end with the tweezers leaving the top; 6 glossy red ant on the panel, jaws closing on two pale folds.

## Open items (not judged: motion feel and timing; I cannot watch video)
- Scene 1: the dangling cords are stiff angular hooks rather than soft cords.
- Scene 6: the two folds read weakly (two pale pillars below the jaws).
- The boot is a stylised toy boot (tapered wedge with toe cap, collar rim); the brown body is a large plain area.
