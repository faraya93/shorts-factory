# huincha-de-medir in PAPEL — video 1 (overnight run, 2026-10-27 23:49 -> 2026-10-28 06:12)
Deliverable: `final.mp4` (68.00 s = 64.00 s timeline + 4 s end card, 1080x1920, 30 fps, 22.2 MB; gitignored). Script, narration, choreography, cameras and timings are identical to the previous final
(`productions/pilot/huincha-de-medir/final.mp4`, kept untouched). $0 spend.
Sheets (gitignored, regenerate from final.mp4): `build/frames/before-after-v1.png` (previous dark final above, Papel below, 8 moments), `build/frames/contact-v1.png` (22 frames, overlays visible).

## What changed (look/palette only)
- Stage: Papel (cream gradient #FDF3DC -> #EFE2C4, ink plinths, soft contact shadow, no vignette/halo) via `render_args: ["look=papel"]` -> `code3d/lib/looks.py` (new driver pass-through in `factory/code3d_render.py`; scene scripts untouched except the stage-floor depth argument added earlier). Real hero colours (yellow tape, black rubber, steel blade with bold ticks); the active quantity is vermilion #F0421C (stress glow, spring, tension bar, CTA tap).
- Text: Papel theme (ink words, spoken word in an ink box, white outline). Counter and labels moved into the safe zone (all <= y 0.74; counter 0.72); the CTA phone moved from 0.58 to 0.57 so it stays below the subtitles (its lower edge still reaches ~0.88: not fully inside the platform-UI zone).
- End card: Papel mark (cream object, cut quadrant, vermilion dot) + working name MECANALIA on an ink veil (4 s). The handle is NOT shown (nothing is registered).
- Samples: 256 (kept; see decision).

## Decision log (7 h rule)
Idle rate measured on scene 2: 10.0 s/frame (scene 1 ran at 13.1 s/frame only because I was rendering drafts/stills on the same GPU). Projected finish ~05:50 / ~6.0 h < 7 h, so 256 samples stayed; no tradeoff taken.

## Actuals (Cycles, Metal GPU, 256 spp, OIDN, adaptive 0.02; costs.json)
| scene | frames | render s | s/frame | note |
|---|---|---|---|---|
| 1 | 180 | 2,354.5 | 13.08 | contended by my draft renders |
| 2 | 294 | 3,128.1 | 10.64 | |
| 3 | 299 | 3,285.3 | 10.99 | |
| 4 | 373 | 5,174.0 | 13.87 | **first attempt crashed at Blender start-up** (transient Metal NSException, 02:15:43); rerun automatically at 04:46 and succeeded |
| 5 | 432 | 5,011.0 | 11.60 | |
| 6 | 196 | 2,233.8 | 11.40 | |
| 7 | 146 | 1,748.8 | 11.98 | |
Total render 22,936 s = **6.37 h** (wall 6.4 h). Previous dark production at the same settings: 2.53 h (grey, 256 spp): the Papel stage costs about 2.5x.
Assembly: 68.00 s, all 30 overlays resolved, background QA vs #FDF3DC: all scenes dE 3.9-6.8 (ok).

## Honest read of the Papel design on this video (stills only; I cannot watch motion)
Held: subtitle hierarchy (ink words, spoken word reversed) is legible everywhere; the yellow tape, red X and vermilion glow separate cleanly from the cream; the contrast scenes read faster than on the dark stage; the counter and labels sit in the safe zone.
Did not hold / flagged: (1) tiny 34 px tag labels are hard to read where they sit on the large ink slabs (e.g. SECCIÓN on the cross-section wall, 6-10 s); (2) the vermilion stress glow on the steel blade looks salmon-pink, not glowing (scene 1/3); (3) the ink plinth, wall and block now dominate scenes 2, 4 and 6 as heavy dark masses, which fights the light stage; (4) the white/silver blade edges are soft against the cream (the expected Papel weakness), carried by ticks and shadow; (5) "3.4 m" is still the unverified figure from the brief; (6) music is the placeholder track; its credit (Sneaky Snitch, Kevin MacLeod, CC BY 3.0) must go in the description at publish; (7) the stress/hook colours use the accent, so the red thermos-style conflicts did not arise here.
