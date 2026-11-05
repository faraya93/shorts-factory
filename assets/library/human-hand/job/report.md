# Job report: human-hand (2026-11-04, asset-proof session)

Route: **library** (Sketchfab, CC Attribution). Spend $0, no accounts created.

## Sources searched (registry order) and verdicts
| Source | Query | Result |
|---|---|---|
| Library / code3d | find hand, fingers, dedos, mano | nothing; `code3d/lib/wrinkle_rig.py` is the rejected 006 primitive rig |
| Poly Haven | hand (models) | hand tools, gloves: no human hand |
| BlenderKit | hand, human hand | Sticky Hand (CC0), Stylized Hand, Tiny Hands 2 (Royalty-Free), robotic/wooden hands; thumbnails fetched for two, not downloaded because the Sketchfab hand already fit |
| Sketchfab | hand | 20 results; **hand (kevinruiz, a43c9c90...), CC Attribution, 137k faces: taken** after viewing it in Blender. Others skipped: 1-2M faces, monsters, tools, NC/ND licences |

## Work
Imported at 0.19 m, flattened the hierarchy (two meshes: `hand`, and `hand_thumb_tip`), fingertips placed at z=0, fingers point down, forearm cut flat (no wrist cap).
Skin: the source texture set was REMOVED (no real skin texture rule); a stylised `skin` material replaces it, with a state parameter: node `wrinkle_amount` (0 = smooth, 1 = wrinkled), a wave-band bump masked by an object-space height ramp (0.075 to 0.05 m, the distal ~3 cm of the fingers). Vertex group `fingertips` is also kept, but Cycles did not read it as an attribute after append, so the material uses the height ramp instead.
QA: pass, 0 errors, 2 warnings (duplicate vertices). Re-run after each material change.
Review stills `job/stills/` (q1, q3, front).

## Likeness (blind naming of the asset stills)
Reader 1: "a human hand (3D render, reaching forward, fingers loose)", confidence 85.
Reader 2: "a human hand (3D-rendered, bare, with the forearm cut off flat at the top)", confidence 85. Result PASS.

## Known limits (the moving-parts rule)
Fingers are not separate objects and the hand is not rigged: a finger cannot bend alone. The wrinkle state works as a material state, the pose is fixed (relaxed, fingers hanging). A 006 remake that needs a different grip (pinch for the marble scene) needs a rigged hand (`blender-character-rigging`) or a second pose from another asset. Attribution: "hand" by kevinruiz (Sketchfab), CC Attribution.
