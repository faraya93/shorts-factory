# Project skills: roles and evidence

Moved out of CLAUDE.md on 2026-11-11 (block B2, P14 "CLAUDE.md diet", `docs/current/reports/doctrine-b2-2026-11-11.md`). The ALLOWLIST itself (the skill names and the rule) stays canonical in CLAUDE.md "Project skills"; this table gives each listed skill's role and the evidence that sanctions it, verbatim from the lens decision of 2026-11-11. The census and the reasons: `docs/current/reports/skills-hardening-2026-11-11.md`. Evidence is one of: *runner/produce* (invoked by `tools/run_productions.py` or the produce skill), *doctrine* (named in this repo's doctrine), *closure* (a hard dependency of a sanctioned skill). A skill added or removed in CLAUDE.md gets its row here in the same commit.

| Skill | Role in this project | Evidence |
|---|---|---|
| `produce` | the order of work for one production (the only skill created for this project) | runner/produce |
| `blender-core` | entry point and API rules for every Blender job; its `run_in_blender.py` runs only through `tools/blender_run.py --skill` | runner/produce, doctrine (asset-system.md "Skill role map") |
| `blender-kiln` | asset sourcing and likeness measurement tools (never its full pipeline, Studio or AI backends) | doctrine |
| `blender-asset-qa` | mesh QA of record before an asset is `ready` (third-party, adopted) | doctrine |
| `blender-scene-setup` | file organisation, scale, naming | doctrine, closure (asset-qa) |
| `blender-retopology-uv` | cleaning downloaded meshes | doctrine, closure (asset-qa) |
| `blender-character-rigging` | rigs for hands, animals, soft organs | doctrine, closure (asset-qa) |
| `blender-workflow-recipes` | mesh-cleaning recipe for the library route | doctrine |
| `blender-hardsurface-modeling` | complex rigid objects | doctrine |
| `blender-sculpting` | organic modelling when the library has nothing | doctrine |
| `blender-geometry-nodes` | scatter, repeats, parametric shapes | doctrine |
| `blender-pbr-materials` | materials on every asset job | doctrine |
| `blender-texture-baking` | baking high to low detail | doctrine |
| `blender-lighting-lookdev` | neutral light for judging an asset only | doctrine |
| `blender-animation` | articulated and deforming heroes | doctrine |
| `blender-simulation` | fluids, cloth, soft motion (baked, then rendered headless) | doctrine |
| `short-form-video-script` | scriptwriter lens craft | doctrine (architecture.md "Multi-lens protocol") |
| `hook-writer` | scriptwriter lens craft, hook stage | doctrine (same) |
| `yt-script` | scriptwriter lens craft, YouTube script and retention beats | doctrine (same, as the "yt-*" kit, resolved to this name) |
| `yt-seo` | marketing lens, title and description | doctrine (architecture.md "Search and packaging policy"), lens-decisions record |
| `youtube-shorts` | marketing lens, Shorts mechanics | same |
| `social-seo` | marketing lens, search wording | same |
| `thumbnail-design` | marketing lens, cover frame | named in the marketing verdicts record |
| `tastemaker` | design lens, with the style lock `.tastemaker/style-lock.md` | doctrine (Repository organization, architecture.md) |
| `design-taste-frontend` | design lens craft | doctrine (architecture.md "Multi-lens protocol") |
