# v4-code3d-cartoon — style pass report (2026-10-25)

Same scenes, choreography, timing, narration, voice, seed, subtitles and audio configuration as v4-code3d; only the visual
register changed, through one shared pass (`code3d/lib/cartoon.py`, enabled by `"render_style": "cartoon"` in scenes.json;
productions without it render as before, so v4-code3d and v3 are untouched). fal spend: $0.
`final.mp4`: 1080x1920, 30 fps, 43.93 s (the v4 timeline).

## What the pass does (applied to modelled AND downloaded elements alike)
- Materials: every material rebuilt in place as a glossy Principled shader (roughness 0.2, clear-coat 0.65, no textures, no
  subsurface) in the EXACT palette hexes: skin peach, shaded skin, tissue red, steel grey. Restyled library assets: the
  BlenderKit skin shader (now plain glossy skin peach), the ant (body = tissue red, black glossy eyes), the tweezers (steel
  grey metal), the ferns (flat green silhouettes keeping the library alpha, no photo colours), the jungle backdrop plane.
  Not touched: the world backdrop (#E2D5F1 spec).
- Geometry: smooth shading everywhere, every bevelled edge widened (up to 0.12, 6 segments), subdivision on the organic
  library meshes (ant, tweezers arms), rounder thread.
- Light: area lights twice as large (soft shadows).
- Colours outside the palette, by design: thread black (#17171B, per the scene brief) and the intentional jungle greens.

## Actuals
| Item | Time |
|---|---|
| Styling (cartoon.py, hooks, production setup, 2 draft rounds) | ~1.0 min (21:21:54-21:22:55) |
| Final renders, all six scenes, once | 1,226.9 s = 20.4 min (wall block 20.6 min) |
| Assembly | 14 s |
| **Total** | **~21.9 min** |

Render seconds per scene (frames): 1: 165.9 (242) | 2: 319.6 (367) | 3: 223.2 (133) | 4: 120.0 (164) | 5: 138.4 (185) |
6: 259.8 (227). Average 0.93 s/frame against 1.31 s/frame for v4-code3d (28.8 min): the plain glossy shaders are cheaper
than the SSS skin shader.

## Observations (frames and measurements, not a quality verdict)
- Background QA: scene 1 ok (dE 0.7); scenes 2-5 "review" (dE 23.3, 25.3, 20.5, 24.7; v4 had 17.4, 20.3, 11.5, 19.7) and
  scene 6 "review (intentional jungle)" (30.8). Same sampler limitation as v4 (border patches land on skin in tight framing);
  the slightly higher values reflect the glossier skin colour, not a backdrop change.
- Scene 6: the ant now casts a soft dark silhouette on the green backdrop in the last frames (the larger light makes it
  visible); v4's frames show less of it.
- Audio is unchanged from v4: narration + music, no foley (code3d clips have no audio track).
- The unify pass vignette still darkens the frame edges strongly (untuned default, as in v3 and v4).
