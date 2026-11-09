# Render-cost playbook (in force from production 012)

Written for production sessions, at beat-sheet stage. Evidence: `docs/current/reports/render-cost-bench-2026-11-08.md`. The trade-off is the owner's: optical fidelity may be spent; the likeness bar may not.

## 1. Classify every scene before it is built
Set `render_cost_class` in `script.json`/`scenes.json`. Figures are the expected s/frame under the current profiles (1080x1920 output, 75% render).

| Class | What is in frame | Expected s/frame | Evidence |
|---|---|---|---|
| `opaque` | no glass, water or volumes | 2-3 | 007 scene 2, measured 1.87 |
| `glass_water_sss` | one transparent layer, or skin | 3-6 | 010 and 006 at full size 3-7.6; scaled by the measured 75% factor |
| `volumetric` | smoke, steam, glow, no nested glass | 3-8 | 009 at full size 5-8; scaled |
| `nested_transmission` | transparent inside transparent, no volumes | 5-8 | 010 scene 5 at full size 7.6; scaled |
| `nested_transmission_volumes` | transparent stack holding volumetric objects | 14-25 | 008 scene 4, measured 13.7 |

A class above 15 s/frame needs a `cost_restage` note before modelling (`scenes_schema.py` rejects it otherwise). The restage is ladder rung 1 used for cost: same narration and beat.

## 2. Routes per expensive class

| Class | Route | Measured on | Time | Likeness | Status |
|---|---|---|---|---|---|
| Volumes inside glass | `volume_biased` + step rate 2 (profile `transparent`) | 008 s4 | 72.5 → 24.2 s/frame with adaptive 0.08 | RMSE unchanged (3.5 against 3.2); readers 90/90/88 | **Default** |
| Every final | 75% render, editor Lanczos upscale | 008 s4, 007 s1-s2, 010 s5 | -40 to -45% | readers pass on 008 and 007 | **Default** |
| Layered transmission | adaptive threshold 0.08 | 008 s4, 010 s5 | -16 to -18% | RMSE +0.3 | **Default on `transparent`** |
| Layered transmission | transmission bounces below 8 | 008 s4 | 4: -48%; 6: -19% | RMSE 52 and 20, stacks go black | **Rejected** |
| Thin glass shells | Thin Wall (`cheap_kit.thin_wall`) | 008 s4, 010 s5 | 008 -15%; 010 no gain | RMSE 21-35 | **Rejected as a default**; only for a shell not under test, with a new reading |
| Context glass | indirect fake glass (`cheap_kit.fake_indirect`) | 008 s4 | -3% | RMSE 29 | **Rejected** |
| Cloudy ice core | surface milky ice (`cheap_kit.ice_milky`) | 008 s4 | -80% on top of the rest | ice reads (90/85/90) but the tank no longer read in that frame | **Conditional:** for piles where the container is not a declared element; needs its own reading |
| Cloudy ice core | volumes on the near row only (`ice_front`) | 008 s4 | -41% | ice reads; tank did not | **Conditional**, as above |
| Faint water tint | drop the absorption volume (`cheap_kit.no_volume`) | 008 s4 | -12 to -23% | RMSE +1.4 | **Option** when the water's colour carries nothing |
| Volume bounces | 0 | 008 s4 | -15% | RMSE 25 | **Rejected** |
| Steam, smoke | biased volumes | 009 s3 | none measured | unchanged | Harmless, no gain: steam is cheap |

**On paper first:** fewer volumetric objects in frame, volumes only near the camera, a context cue in place of a transmissive container (`assets/patterns.md`).

**Not measured:** SSS skin alone (006 at 3-6 s/frame was not an outlier). Thin-structure shimmer for classes other than the one tested in section 3 (spokes, bottle necks, fingers, spring towers, and anything on the `transparent` profile).

## 3. The 75% motion test (2026-11-08; lab: `productions/_lab/motion-75/`, numbers in `flicker.json`)

**Scene:** 007 candado, scene 6 (`code3d/scenes/candado_06.py`, 150 frames): the key turns, the shackle, a thin steel arch, pops 2.6 units out of the body, and the camera travels and tilts throughout. It represents the thin-structure class because the shackle is a slim curved bar with long high-contrast edges against the stage, and it MOVES in relation to a travelling camera: the exact case where under-resolved edges crawl or shimmer. Tuned profile (the default). Not covered: spokes and spring coils (denser thin structure), fingers, and anything on the `transparent` profile.

**Method:** the same shot rendered twice through `tools/blender_run.py` (`render_pair.py`): once at the profile's 75% (810x1440) and once with `res=100` (1080x1920), same frames, same samples. Both encoded as the pipeline encodes clips (libx264 crf 16); the 75% clip then scaled with the editor's own filter (`scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop`), both decoded to 8-bit gray (`flicker.py`). Regions: STILL = pixels the 100% render never changes by more than 2 levels (65.9% of the frame); EDGE = Sobel edges of the 100% frames dilated 3 px, minus still (13.8%, the shackle and body outlines). F1 = mean |f[t+1]-f[t]|; F2 = mean |f[t+1]-2f[t]+f[t-1]| (smooth motion cancels, flicker does not). Gray levels, 0-255.

| Measure | 75% upscaled | 100% | Ratio 75/100 |
|---|---|---|---|
| F1 in the still region (literal flicker) | 0.0501 | 0.0387 | 1.30 |
| F2 in the still region | 0.0953 | 0.0749 | 1.27 |
| F2 on thin-structure edges | 2.310 | 2.381 | 0.97 |
| F2 on edges, 99th percentile | 34 | 36 | 0.94 |
| F1 on edges | 2.641 | 2.622 | 1.01 |
| Mean pixel difference 75 vs 100 on edges | 1.17 | | |

Render time: 75% 312 s (2.08 s/frame), 100% 527 s (3.51 s/frame): -41%, as in section 2.

**Verdict: 75% STANDS for the default tuned-profile finals, including the thin-structure class as tested.** On the shackle's edges the shimmer is indistinguishable from the 100% render (0.97, p99 34 against 36). The still region shows the only gap: 75% flickers 1.3x more, but the absolute difference is 0.011 gray levels per frame, two orders of magnitude below one visible level, and the editor's grain pass adds far more than that. No restriction is written.

**Limits, stated plainly:** one scene, one thin object; the edge F2 is dominated by real motion (about 2.3 levels on both), so it can only show that 75% adds NO shimmer on top of it, not detect a small one; the still-region number is the sensitive one. The verdict is for the `tuned` profile. It does not extend to the `transparent` profile (denoised volumes and transmission have their own noise), to spoke or coil densities, or to what the owner's eye sees; a production whose owner review reports crawling edges reopens this with that scene as the next test.
