# Asset job: ear canal cross-section with outer ear (ear-canal)

Started and sealed 2026-11-11, inside production 024 (an open job blocks nothing; asset-system.md "Advance assets" (g)).

## Brief
Must read as a human ear with its canal shown in section. Seen at 40-70% of the frame, three-quarter from -Y. One rigid state: the bare canal. Wax, swab and sound rings are production-level builds (`code3d/lib/oido_rig.py`).

## Sources searched (query, result, why taken or refused)
- Sketchfab "ear anatomy cross section": one hit, "Ear anatomy" by maryswet9 (da5b25e8, CC Attribution, 40k faces). Taken: a clean outer ear. The planned candidate (brianj.seely, a6a44a28) did not come back in this search and was not imported.
- The scan's own canal is a messy bone cut with a gap of a few mm, too narrow to stage a swab and wax: refused as the canal.
- No CC0 ear exists in the registry sources searched; CC-BY is accepted without asking (CLAUDE.md "Licences and sources"). No credit goes in a description.

## Steps and visual checks
1. Imported at 0.12 m, cropped to the pinna (faces with centre x < -4 mm), faces classified by their baked colour and the whole pinna retinted to one flat skin material (no skin texture).
2. Pinna rotated 50 degrees about Z so it faces the camera three-quarter, then shifted so the ragged crop edge sits inside the block.
3. Built a cream block (62 x 34 x 50 mm, bevelled) and cut a half-open canal trough into it with an exact Boolean: radius 9.5 mm (enlarged for legibility), open toward -Y, eardrum wall at x = 50 mm, canal lining pink, drum grey-mauve.
4. Mesh cleaned (weld, degenerate dissolve, unused slots removed). Visual checks by MCP `look` in material shading from four angles.

## Checks (QA, blind naming, fidelity)
- blender-asset-qa, profile render: PASS with `--eps 0.0002 --tol 0.0005`. At the default 1 mm z-fight distance the cartilage folds of the scan flag 1 coplanar pair; the skill documents lowering eps for small objects and the ear is 6 cm. Accepted warnings: 7 inconsistent-winding edges on the scan's cropped border, 9% UV overlap on the block (no bake is made).
- Blind naming, three isolated readers (`tools/blind_read.py`), neutral stills `job/stills/ear-canal_colour_{front,q1,q3}.png`: "human ear (3D render); white rectangular block/socket attached" 90, "3D-rendered human ear; white rectangular block with a slot" 85, "human ear model, white rectangular block attached" 90. PASS (mean 88).
- Fidelity: none (no reference photo run).

## Wall time, spend ($0 expected), anything skipped
About 40 min of session time, $0. One mishap: a first cleanup pass used a 0.8 mm face-pair tolerance and deleted most of the pinna; the file on disk was untouched and the pinna was reloaded from it.
