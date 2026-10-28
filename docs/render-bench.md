# Render test bench (owner 2026-10-28) — free options only; NO production default was changed
Test scene: engranajes-papel scene 1 (glossy coated gears + cream gradient + contact shadow), the same frames for every variant: frames 100-111 (12 frames) for timing/blind sheets, 100-159 (60 frames) for the clip pair, frame 105 also rendered at 1024 samples (adaptive 0.001, 12 bounces) as the ground-truth reference. Script: `code3d/scenes/bench_gear.py` (`variant=`). Machine: Apple M5 Pro (16-core GPU), Blender 5.2.3, 1080x1920. Baseline = the current Papel profile at 128 samples (your reference).

## Step 0 — the current configuration (printed by the script)
| item | current production value | answer |
|---|---|---|
| sample count | 128 (`--samples 128`) | an adaptive CEILING, not fixed: adaptive sampling is ON (threshold 0.02, min samples 0 = auto), so pixels stop early when converged |
| denoiser | OpenImageDenoise, quality HIGH, prefilter ACCURATE, passes RGB+albedo+normal | **OIDN runs on the CPU** (`denoising_use_gpu = False`) although a GPU OIDN device is available on this machine |
| compute | engine Cycles, device GPU, compute type **Metal**, only the "Apple M5 Pro (GPU - 16 cores)" device enabled (the CPU device is off) | Metal and GPU Compute are both on; MetalRT (hardware ray tracing) is on AUTO |
| bounces | max 6, diffuse 4, glossy 4, transmission 12 (capped by max 6), volume 0, caustics off | |
| persistent data | off | |
| light tree | on | |
| compositor | Glare (Fog Glow, quality Medium) on every frame | not tested here (it is part of the look) |

## Step 1 — Cycles settings stack (12 frames each, steady-state s/frame from Blender's own timestamps)
| key | variant | settings | s/frame | speed-up | RMSE vs 1024-spp reference (0-255 levels; whole / glossy hero / bg+shadow) |
|---|---|---|---|---|---|
| **cyc_A** | current | 128 ceiling, adaptive 0.02, OIDN CPU, bounces 6/4/4/12, persistent off | **8.89** | 1.00x | 0.61 / 0.80 / 0.67 |
| **cyc_B** | tuned | 128 ceiling, adaptive 0.04, min samples 24, OIDN GPU, transmission 0, volume 0, caustics off, diffuse 3 / glossy 4 / total 8, persistent ON | **3.64** | 2.44x | 0.76 / 0.95 / 0.80 |
| **cyc_C** | tuned + Fast GI | B + Fast GI (replace, 2 AO bounces) | **3.50** | 2.54x | 0.77 / 0.95 / 0.85 |
Differences vs the reference are under 1 level in all three (p99.9 error 7-8 levels at edges/highlights): no visible difference is expected, and in the blind sheet I cannot see one either.
**Blind sheet** `docs/render-bench/blind-A-cycles-settings.png`: panels X, Y, Z (full frame, glossy-gear zoom, top-pair zoom). **KEY: X = cyc_C, Y = cyc_A, Z = cyc_B.** Please judge it before reading the key.
**Where the speed comes from (single switch undone on top of B):** OIDN on CPU instead of GPU 6.76 s/frame (+3.1 s: the largest single lever); adaptive threshold 0.02 instead of 0.04: 5.32 (+1.7 s); persistent data off: 3.97 (+0.3 s); production bounce limits instead of 3/4/8 and transmission off: 3.59 (no effect on this scene). So almost all of the gain is "denoise on the GPU + a looser adaptive threshold".
**Clip pair (cream gradient in motion, 60 frames, graded with the production unify pass: saturation/contrast + grain 5, H.264 crf 16):** `docs/render-bench/blind-clip-pair-cream-gradient.mp4`, panels P (left) and Q (right). **KEY: P = cyc_A, Q = cyc_B.** Objective checks on a pure-gradient patch: raw temporal flicker 0.002 levels (A) vs 0.21 (B) and 0.20 (C): sub-level and invisible; after grain + x264 all three have identical behaviour (temporal std 0.94 / 0.82 / 0.83 levels, i.e. the grain; longest flat band in the gradient column 17 / 16 / 14 rows: no banding difference). Without the grain, the 8-bit cream gradient is stepped for all variants (3-5 levels over 400 rows, flat runs 29-152 rows after x264): the production grain pass is what hides it, so it must stay on whichever variant is chosen. Floor: 16-32 samples was honoured (min samples 24; typical frame converged well above it).
Honest limits: ONE scene, simple lighting and mostly flat materials; interior-heavy scenes (the spring housing, the cross-section) were not benchmarked and Fast GI is exactly the kind of switch that can change them; the speed-up ratio will differ there.

## Step 2 — EEVEE on the same frames (not Cycles): s/frame + blind sheet
EEVEE (Blender 5.2), 1080x1920: **ee_A** = 64 TAA samples, ray tracing on, world lighting only: **1.55 s/frame**. **ee_B** = 128 samples + Fast GI + stage probes baked ONCE (sphere probe at the hero, volume probe over the stage; bake worked headless, about 12 s once per scene): **3.02 s/frame**. EEVEE has no shadow catcher, so the floor was emulated with a shadow-to-alpha shader (see limits).
Fidelity vs the 1024-spp Cycles reference: ee_A RMSE 12.1 (glossy hero 15.5), ee_B RMSE 14.1 (glossy hero 19.4): about 15-20x the Cycles error (levels, not percent). **Blind sheet** `docs/render-bench/blind-B-eevee-vs-cycles.png`: **KEY: E = ee_A, F = cyc_A (Cycles current), G = ee_B.**
Judgement on the glossy hero's reflections: EEVEE shows the plastic's normal-map streaks as strong, higher-contrast specular sweeps (E, G) where Cycles (F) gives a smoother satin coat; the probes (G) darken the gear body and deepen the contact darkness, moving further from Cycles, not closer. EEVEE also lacks the soft ambient fill under the gears. In my emulation the floor shows a visible beige band with a hard horizon: that artefact is mine (the shadow-to-alpha trick is not an exact shadow catcher) and could be improved, but even excluding the band the gear colour/contrast shift would be noticeable against videos already rendered in Cycles.
Verdict: EEVEE is 2.3-5.7x faster than the tuned Cycles at this size... in raw numbers 1.55 vs 3.64 s/frame is only 2.3x, and it does NOT match the look. Not recommended for finals; fine for drafts (as now).

## Table: variant, s/frame, projected hours per video
Projection = frames x s/frame; the production baselines are measured (gears: 1,702 frames, 4.41 h at 9.33 s/frame mean; tape: 1,920 frames, 6.37 h at 256 spp). For the other cases I scale by this bench's ratio to cyc_A (an ESTIMATE: other scenes will differ), and the tape video at 128 spp is itself an estimate (6.37 h x 0.71, the 256->128 ratio measured earlier for the celeste stage).
| variant | s/frame (bench) | ratio to A | gears video (1,702 f) | tape video (1,920 f, at 128 spp) |
|---|---|---|---|---|
| cyc_A current | 8.89 | 1.00 | 4.4 h (measured) | ~4.5 h (estimate) |
| cyc_B tuned | 3.64 | 0.41 | ~1.8 h | ~1.8 h |
| cyc_C tuned + Fast GI | 3.50 | 0.39 | ~1.7 h | ~1.8 h (check interior scenes first) |
| ee_A EEVEE | 1.55 | 0.17 | ~0.8 h | ~0.8 h (look does not match) |
| ee_B EEVEE + probes | 3.02 | 0.34 | ~1.5 h | ~1.5 h (look does not match) |
(The 256-spp tape profile would also drop with the tuned stack; sample ceiling matters little once adaptive sampling is looser.)

## Recommendation (the owner picks; defaults untouched)
1. **Adopt the cyc_B stack for Papel finals** (OIDN on GPU, adaptive 0.04 with min samples 24 and a 128 ceiling, persistent data on, transmission/volume off): same look to within a level, ~2.4x faster, which would take a gears-sized video from 4.4 h to about 1.8 h. The two switches that matter are the GPU denoiser and the looser adaptive threshold; the rest is bookkeeping.
2. **Do not adopt Fast GI yet**: the extra 4% is not worth the risk on interior scenes; test it on scene 5 (spring housing) first.
3. **Keep EEVEE as the draft path only.**
4. Keep the production grain pass: it is what hides the 8-bit gradient steps.
5. Next, if wanted: benchmark cyc_B on a tape scene with the cross-section (scene 2) and the exploded housing (scene 5) before changing any default.
