# Asset system proof, run cold (2026-11-04)

Stills only. No video, no publish package, no production touched. Spend $0, no account created (Sketchfab through the owner's existing token). Render launches all under `caffeinate -dimsu`.
Operator: one fresh session with only the repo docs. Wall time by the machine clock: started 21:50, stills and gate done 22:08, records finished about 22:20 (about 30 min in total, no job passed the 60-minute stop rule). Rough split, not separately timed: sources and download about 4 min, asset building and QA about 8 min (most of it the popcorn z-fighting fix and import bookkeeping), scene and stills about 8 min (stills themselves 38 s hand, 16 s popcorn), blind naming and records the rest.

## Job 1: 006 key scene, fingers in water (`006-hand-water/`)
- **Route:** asset (library). Hero `human-hand` from Sketchfab, "hand" by kevinruiz, CC Attribution (record says 4.0, to be confirmed on the model page). Not modelled, not generated.
- **Water: physically based water material, NOT Mantaflow.** Principled BSDF, full transmission, IOR 1.333, in a glass tray (IOR 1.45), a displaced top surface for the ripples (wood-rings texture round the finger). Mantaflow was not attempted: a stills proof does not need a simulation, and contact ripples from a displacement texture are enough for a key frame. For moving water (finger entering) a bake would be needed; untested.
- **Wrinkle state:** material parameter `wrinkle_amount` on the asset (0 smooth, 1 pruney), masked to the distal 3 cm of the fingers. Still 3 shows it.
- **Stage:** Coral gradient (#FEA181 to #EC9172) and ink plinth from the exported identity. The cream cutaway plate rule for body heroes was not applied (no cutaway in this key scene).
- **Render:** tuned Cycles profile (GPU denoise, adaptive 0.04, min 24, ceiling 128, Persistent Data on, Fast GI off, Metal) at 1080x1920, **one recorded deviation: transmission_bounces 0 to 8**. Measured: with the tuned 0 the tray and water render black (test frame kept in the session only). About 9 s per still.
- **Stills:** `006-hand-water/stills/` (1 dip smooth, 2 glass side, 3 wrinkled close-up, 4 overview). Scene script `proof_scene.py`, shared with job 2.
- **Likeness gate (production stills):** PASS. Reader 1: "a human hand (stylised 3D, chunky, reaching into a glass box)", confidence 65. Reader 2: "a stylized 3D hand reaching into a glass display case (vitrine)", confidence 85. Margin is thin: 65 against the floor of 60, and both readers named the glass box as the main alternative (the tray competes with the hero). Asset-level blind naming also PASS (85, 85). Records: `006-hand-water/build/gate/likeness.json`, `assets/library/human-hand/asset.json`.
- **Not run:** the composition (colour) gate, because it needs code3d scene scripts (`gate.py run`). Colour separation of hand, tray and stage was not measured. The hand's final tone (#B5754F base) sits close to coral in the render; unmeasured.
- **Honest quality notes:** large specular patches on the water in stills 1 and 2, a purple cast on the plinth from the HDRI, still 2 is a weak composition. The hand is a single mesh in one fixed pose, so the existing 006 pinch/marble beat is not possible with this asset.

## Job 2: popcorn (011), hero `popcorn` (`011-popcorn/`)
- **Route:** asset (library). Sketchfab "Popcorn" by varun_malhotra1, CC Attribution. Rejected candidates recorded in `asset.json` (scan shell with holes; lettered bucket).
- **Library record:** `assets/library/popcorn/` (README with source, licence, date; job report; QA pass; blind naming PASS 90 and 95). `check` prints OK.
- **Render:** same tuned profile with its own transmission setting (no refraction here). Three stills: `011-popcorn/stills/` (box, eruption using the 86 separate pieces, close-up).
- **Likeness gate (production stills):** PASS, 90 and 92. First guesses "a striped popcorn bucket (paper popcorn box) full of popcorn, with popped kernels bursting out of it" and "a striped popcorn bucket (a paper popcorn box filled with popcorn)". Both name marshmallows as the alternative when the pieces are seen alone.
- **Retint:** pieces cream #F7E7C2, stripes ink #1D1B2E / #FFF3E0 so the stage coral does not swallow the red source stripes. Composition gate not run (see above).
- **Caveat that matters for 011:** the asset is the popped end state. The video's mechanism (kernel, steam, hull rupture) needs a kernel and a cutaway asset that do not exist yet.

## Likeness gate caveats common to both
Readers are haiku subagents run inside this repo (isolation unverified, same limit as the calibration report). Neither the hand nor the popcorn has been judged by the owner; the owner's eye remains the last gate.

## Verdict: could a cold session operate this system from the documentation alone?
**Yes, with work-arounds: the documentation carried it to two passing heroes and 7 stills, but 10 gaps cost time or forced a judgement call.** Nothing needed an account, money or a repo edit. Gaps:
1. **`likeness` needs a real production.** `asset_library.py likeness <production>` fails on a lab folder (it reads `scenes.json` and fingerprints code3d scene scripts). The manual does not say how to gate a lab or asset-only job. Work-around: a stub `scenes.json` (marked as a stub) in each lab folder. Suggest the manual say so, or the command accept a lab path.
2. **`gate.py run` (composition gate) cannot run on a non-code3d scene,** so a proof job that renders its own scene has no colour gate. The manual does not say whether lab stills need it.
3. **Tuned profile vs refraction.** `render.profiles.tuned` sets transmission_bounces 0 and volume_bounces 0; glass and water then render black (measured). No documented profile for transparent heroes (water, ice, glass). The 008 ice and 010 fluid remakes will hit this. Needs a lens decision for a `transparent` scene-type profile.
4. **`build/identity-export.json` is stale and shared:** its `coral` preset carried `support_board/plate #1B4F5A`, the 011 override, not Coral's documented `#D2EAE6/#FFF3E0`. The doc says presets come from brand.yaml; the export is rewritten per production. A cold reader copying values from it gets wrong supports. (`identity.py export` was not run, to leave the build untouched.)
5. **Export is flat, brand.yaml is nested** (`stage.top` vs `top`); the docs describe `identity.<preset>.stage` only for the YAML. My script had to discover the JSON shape.
6. **`import_asset` needs `id` and `target_size`** for Sketchfab, and the manual's examples do not show the arguments. `look` ignores its `objects` argument for framing in this build (it framed the whole scene). Hidden objects (`hide_viewport`) return a fake 2 m bounding box, which cost several minutes on the popcorn import. The manual's step 6 mentions none of this.
7. **Sketchfab results show "CC Attribution" without a version;** the validator wants CC-BY-4.0 or CC-BY-3.0. I recorded 4.0 and noted it. The manual does not say how to resolve the version.
8. **QA z-fighting on multi-piece assets** (copies of a few meshes nested in the same orientation). The manual says "fix errors" with no recipe; scaling did not work, random rotation did. Worth a line in the manual.
9. **Vertex-group masks do not survive into Cycles after `load_hero`** (an Attribute node read zero). I used an object-space height ramp instead. Worth documenting for any state-by-region material. Also: the manual says nothing about hands with separate fingers or rigging, so the "moving parts" rule cannot be met for a hand with this source.
10. **No stated test command.** CLAUDE.md says "run the full test suite"; pytest is not installed in `.venv`, and the commands are only in each test file's header (`.venv/bin/python tests/<name>.py`). Run: layout 6/6, asset_library 25/25, channel 13/13, gate 4/4 pass.
Smaller: `blind-pack` copies stills but the test fingerprints include every code3d lib when `rig_libs` is absent, so any lib edit stales a lab record; the 60-minute stop rule has no stated clock start for a two-job session.

## What this does not prove
Mantaflow or any moving water; a rigged or posable hand; internal anatomy (vessels, nerve) for the 006 cutaway beat; an unpopped kernel; clouds, ice, soap or a heart (not searched). The gate passed both heroes, but on stills made by the operator, with the same family of readers that calibrated it.
