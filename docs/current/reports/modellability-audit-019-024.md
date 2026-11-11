# Modellability audit of the developed set 019-024 (2026-11-11)

Run under CLAUDE.md "Reshape ladder", "Every element at hero standard" and "Asset library and hero routing", in the same form as `modellability-audit-012-016.md`. Scope: modellability only, read from each developed `script.json`. Nothing was modelled, downloaded, rendered or read by blind readers. Pre-written fallbacks are in each production's `notes.md`, section "Modellability audit and pre-written fallbacks". Aliases are fixed in each `script.json`, before any reading.

## Verdicts

| Production | Verdict | Riskiest element | Unresolved |
|---|---|---|---|
| 019 plane door (objects, chain, 6, cutaway) | MODELABLE WITH THE WRITTEN FALLBACKS | the airliner exterior (scene 5), an unsealed class; rung 1 restages the event from inside the cabin with sealed seated figures | none |
| 020 lightning on a car (whatif, fork, 7, world) | MODELABLE WITH THE WRITTEN FALLBACKS | the bolt (scenes 2, 3, 6), an unsealed class; the night `world` environment's render cost is unmeasured (fallback: `stage`) | none |
| 021 folding paper to the Moon (numbers, scale, 8, world) | MODELABLE WITH THE WRITTEN FALLBACKS | the mountain (scene 4); `world` cost (fallback: `stage`) | none |
| 022 fork vs spoon in the microwave (objects, chain, 6, cutaway) | MODELABLE WITH THE WRITTEN FALLBACKS | the microwave (every scene) and the sparks (scene 4), both unsealed classes with candidates | none |
| 023 car-door static (objects, chain, 6, stage) | MODELABLE WITH THE WRITTEN FALLBACKS | the fuel pump (scene 5), an unsearched build; the spark (unsealed class) | none |
| 024 ear swabs (body, journey, 5, cutaway) | MODELABLE WITH THE WRITTEN FALLBACKS | the wax plug (scene 4) and the ear-section asset (one CC-BY candidate seen) | none |

None is held out of the batch.

## Rule applied for "only sealed assets and sealed poses"

A script names as AVAILABLE only sealed library assets in their sealed poses: `hand-articulated` (open, lever, wheel, door, knife, mask, mask_b, crack; `press` is not sealed and is not used), `human-figure` (standing, walking, jumping, falling, seated; `sunk` is not sealed and is not used), and `cartoon-car`. Every other element is one of these: a geometric build, a material, energy graphics in the doctrine's language, or a class whose job is open (airliner, electric arc, microwave, car interior) or that has a library candidate. Each such element carries a route, its risk and a ladder fallback that does not need the unsealed class. A production may run an open job itself under its brief (asset-system "Advance assets" (g)). The script never assumes the class is already sealed. This is what "an unsealed pose is a missing asset, not a detail" means in practice: no beat depends on `press` or `sunk`.

## Method

- **Local first.** Library statuses read from every `assets/library/*/asset.json`. Ready classes used: `hand-articulated`, `human-figure`, `cartoon-car`. Open jobs met in these scripts: `airliner`, `electric-arc`, `microwave-oven`, `car-interior`.
- **Live searches on 2026-11-11.** BlenderKit through `tools/asset_blender.py blenderkit-search` (CC0 and Royalty-Free only): ear anatomy (0 results), airplane cabin, airplane interior, airplane door, microwave, lightning, moon, mountain, car seat, fork, spoon, cotton swab. Sketchfab through the public v3 search with `license=cc0` and `license=by`: ear anatomy, ear canal, airliner, airplane cabin interior, cotton swab, lightning bolt.
- **Judged by eye.** Eight Sketchfab thumbnails were reviewed as a contact sheet (scratchpad, not committed): ear section "Ear Anatomy" (brianj.seely, a6a44a28, CC-BY; the thumbnail carries a "VisibleBody" mark, so check the mesh for it at the asset step), outer ears (e1f0f4b6, 9dfbb19c), inner-ear-only model (92d3fe7b; not usable for the canal), Boeing 737-200 (mgg8, e3224d0a, CC0, livery to strip), Airbus A320 (Kyaie, 757aa190, CC-BY, plain white), cabin pieces (4293edb2: unusable, a bare arch), cotton swab (amhyde, 55e6fe76, CC-BY). BlenderKit thumbnails returned HTTP 403 to a direct fetch, so the BlenderKit hits (microwaves, Moon, terrains, car seat, fork) are search results only. They are to be judged at the asset step.
- **Licence order:** CC0 first, Royalty-Free acceptable, CC-BY without a description credit (owner 2026-11-07). Every ID is a search result, not a downloaded asset. Licences are re-read at the asset job.
- **Risk levels are predictions, not readings.** No blind-naming gate was run.

## Rotation and balance of the set (production order 019-024)

| # | Theme / tension | Variant | Scenes | Staging (proposal) |
|---|---|---|---|---|
| 019 | cabin pressure / dangerous | chain | 6 | cutaway |
| 020 | electricity / dangerous | fork | 7 | world |
| 021 | paper folding / enormous | scale | 8 | world |
| 022 | microwave / dangerous | chain | 6 | cutaway |
| 023 | electricity / hidden | chain | 6 | stage |
| 024 | earwax / gross | journey | 5 | cutaway |

Window checks, with 015-018 before them (insects/gross, toilet/gross, elevators/dangerous, voice/hidden; journey, scale, fork, chain; 6, 6, 6, 5 scenes):
- Every five consecutive productions hold at most two of one theme (electricity twice, in 020 and 023) and at least three tensions.
- No variant runs three in a row (018 chain, 019 chain, 020 fork; 022 chain, 023 chain, 024 journey).
- No scene count runs three in a row (022 6, 023 6, 024 5).
- No staging mode appears more than three times in 019-023 or 020-024 (each window: cutaway 2, world 2, stage 1).
- No toilet or poop topic (owner instruction for this set).

**Two `world` productions in the set.** The first `world` production, 020, measures its riskiest environment first (format policy). Both `world` scripts carry the written fallback to `stage`, re-checked against the rotation.
