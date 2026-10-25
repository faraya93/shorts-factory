# Engine spike — stitches scene 2 (2026-10-25)

Same ~7-12 s scene (curved needle passes through skin, thread pulls the edges together) produced three ways.
Media is gitignored; this report and costs.json are versioned.

## Results against the rubric

| Route | Clip | Duration | Result | Evidence from extracted frames |
|---|---|---|---|---|
| R1 baseline | r1-baseline.mp4 (v2 scene 2 reused) | 10.14 s | not graded (baseline) | strip-r1-baseline.png |
| R2 keyframes | r2-keyframes.mp4 | 12.23 s (scene-2 narration slot) | **FAIL** | strip-r2-keyframes.png, r2-keys-sheet.png |
| R3 code3d PoC | r3-code3d.mp4 | 5.00 s | **PASS** (with a stated ceiling) | strip-r3-code3d.png |

R2 — needle and thread are recognisable and no model text appears, but "no warped geometry" fails: stills 2-4 show
fused/twisted hands and an arm split by a vertical band; the needle changes shape between stills (straight sewing
needle, thick bent hook, fish-hook rod) instead of a curved surgical needle; the arm orientation changes between
stills, so the crossfades show double exposures of two different arm poses. fal also rejected one prompt with
`content_policy_violation` (a false positive; reworded neutrally and retried, safety checker left ON).
Model used: fal-ai/flux-2 (dev) — chosen over flux-2-pro because only flux-2 exposes `enable_prompt_expansion`
(kept false); flux-2-pro was not tested, so the failure is for this model/prompting, not for every image model.

R3 — rendered with the only tooling installed (Pillow; no node, Blender or 3D library): the curved needle reads as an
arc, enters the skin left of the cut, is hidden while under the cut, reappears on the right; the cut closes and the
thread runs taut across it. No warping, no text. Ceiling: flat colours, no lighting or shading, schematic look — a
polished render needs tooling that is not installed (the owner decides about installs).

## Estimate vs actuals

| Route | fal estimate | fal actual | Claude effort (est.) | Rounds est. / actual | Session time est. / actual | Local render |
|---|---|---|---|---|---|---|
| R1 | $0 | $0 | LOW | 0 / 0 | ~2 min / ~1 min | none |
| R2 | ≈ $0.048 | ≈ $0.048 (4 x $0.012; the API does not report cost) | MEDIUM | 2-3 / 2 (one rejected prompt, one retry) | ~35 min / ~3 min | ~2.8 s (ffmpeg) |
| R3 | $0 | $0 | HIGH (no 3D library) | <= 4 / 3 builds (2 probe renders, 1 full) | <= 60 min / ~1 min | 6.7 s for 150 frames |

Session times are machine wall-clock between the first and last command of each route.

## Calibration data point (first code3d actuals)
One data point only, for the SIMPLEST geometry (primitives, flat shading, ~120 lines): ~1 min wall-clock, 3 renders,
6.7 s local render. It says nothing yet about HIGH objects with lighting or complex motion; the timeboxes in
CLAUDE.md stay as initial values until a real code3d production adds more points.

## code3d tooling notes (added 2026-10-25, after the owner approved installing real 3D tooling)
- Installed: Blender 5.2.3 LTS via `brew install --cask blender` (build 2026-10-22), app at /Applications/Blender.app,
  command wrapper /opt/homebrew/bin/blender. Install took ~30 s, no errors.
- Headless check: `blender -b --python spikes/blender_smoke.py -- <out.png> BLENDER_EEVEE` renders cube + sun light +
  camera to a 540x960 PNG. First run 3.5 s render (includes shader compilation, 3.75 s process); second run 0.58 s.
- Exact colours (needed because code3d scenes must use the visual_identity hex values literally):
  (1) `world.color` and `material.diffuse_color` are viewport-only; the final render reads node-based world/material
  (`use_nodes = True`, Background colour, Principled BSDF Base Color). (2) Set `view_transform = "Standard"` (the
  default tone-mapper shifts colours). (3) Blender works in linear space: convert sRGB hex to linear first.
  With all three the rendered background measured #E2D5F1 against the #E2D5F1 spec, dE 0.0.
- This supersedes the Pillow rasterizer as the code3d ceiling; the Pillow PoC (spikes/code3d_poc.py) is kept as a
  fallback record. Blender's quality on the real stitches scenes is not demonstrated yet (that is v4's job).
