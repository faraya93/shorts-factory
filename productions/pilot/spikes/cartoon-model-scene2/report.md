# Spike — cartoon RE-MODEL of scene 2 (design proof, not a production), 2026-10-25

Question: does modelling in a cartoon design language FROM THE SHAPE UP fix what the style passes could not? Same beats and
timing as v4's scene 2 (367-frame slot), rendered with the existing toon pass at 1080x1920 (draft samples). $0 spend.
Script: code3d/scenes/spike_cartoon_02.py. Frames: `frames/1-start.png`, `2-needle-mid-pass.png` (frame 118), `3-end.png`
(frame 367), `sheet.png`. No existing production was touched.

## Design
- Limb: ONE fat egg-shaped capsule (a plain smooth ellipsoid, radius 2.0 x half-length 4.4), no shell, no boolean, no anatomy.
- Wound: DRAWN, not cut — a flat red lens between two chubby stadium-shaped lips (a box with a near-full bevel). It closes by
  sliding the lips together and narrowing the lens.
- Needle: arc radius 1.8 (a limb radius is 2.0), tube 0.24 -> 0.04 thick (v4: 0.085), dark steel = the palette's steel grey with
  HSV value x0.5 (#C6CFCE -> #636867). Turns about its circle centre exactly as in v4, so it passes through real geometry.
- Cord: 0.13 thick black (v4 scene 2: 0.028; scene 3 knots: 0.036 in a 3x closer shot).
- Composition: one object, centred, 3/4 view (az 30->36 deg, elevation 36), sun at (-2,-6,6) for a readable terminator.

## What the iteration taught (the doctrine evidence)
1. A boolean cut with a bevel put the dashed outline on the slit: cel lines need simple convex shapes. A wound modelled as a hole
   (realistic construction) fights the toon outline; a wound modelled as lens + lips inks cleanly. The fix was in the MODEL.
2. Pointed ellipsoid lips read as leaves/fins; stadium bars read as lips. Shape language, not shading, decided it.
3. A near-top-down camera made the limb read as a coin; a 3/4 view with the terminator crossing the form made it a volume.
4. The cord's free end drawn as a chord is hidden inside any convex limb; it has to follow the surface.
Bugs of mine found on the way: lens scale applied twice (mesh radii baked in), and zsh not word-splitting an unquoted
argument string (one camera comparison sheet was invalid and was redone).

## Honest observations (frames, not a verdict)
- Needle legibility: bold and dark at the start; in the mid-pass frame only the tail stub (left) and the tapered tip (right)
  show, since the body is inside the limb by design. The needle's flat tail end renders as a dark opening.
- The finished stitch is one thick cord crossing the closed lips plus a left stub; v3 shows a multi-stitch zigzag.
- Time: ~8 min wall clock (22:22:00 -> ~22:30), 7 render rounds plus 2 diagnostic runs.
