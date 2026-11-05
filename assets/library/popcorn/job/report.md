# Job report: popcorn (2026-11-04, asset-proof session)

Route: **library** (Sketchfab, CC Attribution). Spend $0, no accounts created (Sketchfab used through the owner's connected token).

## Sources searched (registry order) and verdicts
| Source | Query | Result |
|---|---|---|
| Library / code3d | find popcorn, palomitas, corn; `code3d/lib/pop_rig.py` exists (the rejected 011 primitive rig) | nothing `ready`; pop_rig is the failed route, not reused |
| Poly Haven | popcorn (models) | croissant, cakes, rocks: no popcorn (fuzzy hits, as the manual warns) |
| BlenderKit | popcorn, popped popcorn | one hit "Popcorn Buckets" (Royalty-Free); thumbnail fetched, not downloaded (not inspected further) |
| Sketchfab | popcorn | 20 results, all CC Attribution; 4 inspected |

Sketchfab candidates: **Popcorn Flake** (Geksaedr): rejected, open scan shell (about 40% boundary edges). **Popcorn** (pulsion_one, 903c...): reads as popcorn but the bucket carries printed lettering (text on screen risk); rejected. **Popcorn** (varun_malhotra1, 52cede4d...): **taken**: striped box + 86 separate pieces, no text.

## Work
Import (target 0.1 m), flattened the Collada hierarchy, rescaled with numpy on vertex data (the import's transforms and stale bounding boxes cost a few minutes; see doc gaps), box height 0.175 m, base at z=0, 86 pieces renamed `popcorn_01..86` with their own origins, two material slots (`popcorn_piece`, `box_stripes`).
QA (`qa_check.py --profile render`) first FAILED: 20 z-fighting pairs, because the source pieces are copies of a few meshes nested in the same orientation. Fix: random rotation of nested pieces (seeded), looped through qa_check live until 0 errors. Scaling the pieces did not converge. Final QA: pass, 0 errors, 97 warnings (UV overlap between piece copies, duplicate vertices, hidden back-to-back faces; none blocks `render`).
Review stills: `job/stills/` (q1, q3, front; colour and matcap).

## Likeness (blind naming of the asset stills)
Reader 1: "a popcorn bucket (striped red-and-white cardboard tub filled with popcorn)", confidence 90.
Reader 2: "popcorn bucket (a red-and-white striped popcorn box filled with popcorn)", confidence 95. Result PASS.
Readers were haiku subagents run in this repo (isolation not verified; same limit as the calibration report).

## Known limits
No unpopped kernel and no x-ray cut: the 011 remake needs a kernel asset (separate job). Pieces are low-poly (516 triangles each), reading as stylised, not photographic.
Wall time about 12 min by the machine clock, including the z-fighting detour. Attribution for the description: "Popcorn" by varun_malhotra1 (Sketchfab), CC Attribution.
