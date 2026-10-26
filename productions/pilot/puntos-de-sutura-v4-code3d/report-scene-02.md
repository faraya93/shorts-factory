# v4-code3d — scene 2 (curved-needle): Phase 1 actuals (2026-10-25)

Estimate (Part 4) vs actual, machine wall clock. fal spend $0.

| Item | Estimate | Actual |
|---|---|---|
| Effort class | HIGH | HIGH-shaped work, executed as scripts |
| Iteration rounds | 6-8 | 3 (stills x2, then the whole draft animation) |
| Session time | 1.5-2.5 h | ~17.7 min (20:18:30 sourcing research -> ~20:36 assembled) |
| Final render | 2-5 s/frame, 367 frames (≈ 12-31 min) | 497 s = 8 min 17 s (1.35 s/frame, 1080x1920, 96 samples) |
| Draft render | - | 0.11 s/frame (39.5 s for all 367 frames at 540x960, 12 samples) |

Phase split (min): search/download 1.6 | modelling + animation setup 3.0 | iteration rounds 2.0 | draft renders 0.8 |
final render 8.3 | encode + assembly + checks 2.0.

Library assets used: BlenderKit "SSS Skin Shader" (tinted to palette hexes), Poly Haven studio_small_08 HDRI.
Modelled (nothing in the free libraries): curved needle, thread rig, skin halves, wound floor, anchor knot.
Downloaded but unused: ambientCG Metal063 and Fabric079 (no UVs on a 0.1-unit tube; plain materials were faster).

Output: clips/scene-02.mp4 (1080x1920, 30 fps, 367 frames, no audio track) and the assembled scene with narration and
subtitles at build/test-scene-02.mp4. Audio gate: "no audio track" (code3d clips carry no model audio, so v4 has narration
+ music only, no foley).

Observations (frames and measurements, not a quality verdict):
- Backdrop pixels measure #E0D3EF, dE 0.71 from the #E2D5F1 spec. The editor's QA printed "review" (dE 17.4) because its
  border patches land on skin in this tight framing: a sampler limitation, not a backdrop error.
- The unify pass (grade + grain + vignette) darkens the backdrop towards the edges in the assembled clip, as in v3.
- One diagonal thread crossing and an anchor knot stand in for v3's multi-stitch zigzag; no forearm or hand, just skin blocks.

Reusable library created: code3d/lib/common.py, suture.py (see code3d/TOOLING.md). Scene 3 (knots) should reuse the skin
halves, wound floor and Thread; only the knot objects are new.
