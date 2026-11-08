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

**Not measured:** SSS skin alone (006 at 3-6 s/frame was not an outlier). Thin-structure shimmer at 75% over moving frames: the readers judge stills, so a tower or spring is for the contact sheet and the owner's eye.
