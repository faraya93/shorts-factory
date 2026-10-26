# v4-code3d — complete build report (2026-10-25)

Same narration, voice, seed, subtitle settings and audio configuration as v3; only the visual engine changed (Blender,
EEVEE, all six scenes). fal spend: $0. Final video: `final.mp4` (1080x1920, 30 fps, 43.93 s = the v3 timeline; every clip
lands exactly on its narration slot, zero trims or slowdowns).

## Per-scene actuals vs the Part 4 estimates (machine wall clock)

| Scene | Estimate: effort, rounds, session | Actual rounds | Actual session | Final render (frames) |
|---|---|---|---|---|
| 1 hook | MEDIUM, 3-5, 45-90 min | 2 | 5.8 min | 256.4 s (242) |
| 2 curved-needle | HIGH, 6-8, 1.5-2.5 h | 3 | 17.7 min | 497 s (367) |
| 3 knots | LOW-MEDIUM, 2-3, 20-40 min | 3 | 4.8 min | 203.7 s (133) |
| 4 absorbable | MEDIUM, 3-4, 45-75 min | 2 | 3.7 min | 169.8 s (164) |
| 5 risk | MEDIUM, 4-5, 60-90 min | 2 | 5.9 min | 227.9 s (185) |
| 6 ant-twist | MEDIUM-HIGH, 4-6, 1-2 h | 2 | 8.3 min | 373.1 s (227) |
| **Total** | 22-31 rounds, 5.3-9.4 h, render 45-110 min | **14** | **46.2 min** | **1728 s = 28.8 min (1318 fr)** |

Batch window (scenes 3, 1, 4, 5, 6 + the full assembly): 20:41:34 -> 21:11:22 = 29.8 min. No safeguard triggered (no scene
above 60 min or 2x its estimate; the 3 h batch cap was never near). Final rendering is ~62% of all session time.

Amortisation: scene 2 (builds the library) 17.7 min -> the five reuse scenes average 5.7 min (32%); scene 3, the
designated test, cost 27% of scene 2 (prediction was 10-20 min and 2 rounds; actual 4.8 min and 3 rounds).

## Sourcing (library first)
Tier 1 (library): BlenderKit SSS Skin Shader, Poly Haven studio_small_08 HDRI, BlenderKit Tweezers (scene 5), BlenderKit
Ant (Rigged, CC0) and Tall Forest Fern (scene 6). Tier 3 (modelled, nothing in the free libraries): skin halves, wound
floor, curved needle, thread rig, knots, layered cross-section, forearm slit tube, skin lips/mound. Tier 2 (AI mesh) not used.
Licences: code3d/assets/LICENSES.md.

## Observations (frames and measurements, not a quality verdict)
- No model-generated text anywhere; subtitles in the upper band with the boxed current word, as in v3.
- Audio: code3d clips have no audio track, so every gate decision is "no audio track": v4 carries narration + music only,
  no foley (v3 had foley in the clips the gate admitted).
- Background QA (code3d: every scene is checked): scenes 1 and 4 ok (dE 0.7, 11.5); scenes 2, 3, 5 "review" (17.4, 20.3,
  19.7) and scene 6 "review (intentional jungle)" (35.8). The sampler reads border patches, which in tight framing land on
  skin (scene 2's true backdrop pixels measure dE 0.71): marks are review signals, as the doctrine says.
- The unify pass vignette darkens the frame edges strongly, as in v3 (untuned default).
- Scene 6's ant comes from a library asset with realistic materials, so it looks more photographic than the smooth-block
  skin around it; scenes 2 and 3 use one diagonal thread crossing and a trefoil loop where v3 shows a multi-stitch zigzag.
- Scene 3 has a small hook at the strand join in the loose phase of each knot.
