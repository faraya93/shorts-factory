# Asset job: cotton swab (cotton-swab)

Started and sealed 2026-11-11, inside production 024.

## Brief
Must read as a double-ended cotton swab, close, one rigid state, lying along x, centred on x = 0, base at z = 0, 75 mm long.

## Sources searched (query, result, why taken or refused)
- Sketchfab "cotton swab": "Cotton Swab" by amhyde (55e6fe76, CC Attribution, 1.5k faces) taken. Refused: "Cotton Swabs" by lsmined (CC Attribution-ShareAlike), "Box" (NonCommercial-ShareAlike); the Poly by Google swab (128 faces, CC-BY) is too coarse.

## Steps and visual checks
Imported at 0.075 m, world transforms baked, rotated to lie along x and centred, materials replaced by flat cotton (#F6F3EE) and pale blue stick (#D5E2E8). Checked with MCP `look` and neutral stills.

## Checks (QA, blind naming, fidelity)
- blender-asset-qa, profile render: PASS; accepted warnings: duplicate vertices at UV seams.
- Blind naming: FIRST ATTEMPT INVALID. The first save wrote a .blend with no objects, so the three stills were empty grey and the readers (correctly) named nothing; that FAIL was recorded and then overwritten after the file was fixed. It said nothing about likeness. Second attempt, three isolated readers: "Cotton swab (double-ended, white tips, light blue plastic stick)" 92, same 92, "double-ended cotton swab" 90. PASS (mean 91).

## Wall time, spend ($0 expected), anything skipped
About 15 min, $0.
