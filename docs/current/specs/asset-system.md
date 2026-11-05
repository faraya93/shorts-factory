# Asset system: how the factory gets hero objects that look like themselves

Binding since 2026-11-04 (owner instruction). CLAUDE.md "Asset library and hero routing" is the summary; this file is the working manual.

## Why this exists

The owner rejected the whole 006-011 batch: the objects were too abstract and did not resemble their subjects. All six were built from code primitives, and all six passed the
composition gate, because that gate measures colour and never asks whether the object looks like the thing. Two changes follow:

1. **Hero routing.** Code primitives cap likeness. Hard geometric objects pass; organic, soft or complex ones fail. Those now go through the asset route.
2. **A likeness check.** A hero has to be named correctly by someone who was not told what it is. It applies to both routes and blocks the final render.

The rule the system implements: whenever an object cannot be built recognisably from code, the factory sources the best available model or builds it with a proper modelling
method, saves it to the library, and never solves the same object twice.

## Hero routing

For each production, decide the hero object's route **before the beat sheet is final**, and declare it in `scenes.json`:

```json
"hero_route": "asset",
"library_assets": ["human-heart"]
```

| Route | Use it for | Examples | How |
|---|---|---|---|
| `code-primitive` | Genuinely geometric objects: rigid, made of straight lines, circles and extrusions, whose identity survives simplification | gears, tape measure, wall clock, magnets | A rig in `code3d/lib/`, as today |
| `asset` | Anything organic, soft or complex: identity lives in an irregular shape or surface | heart, hand, fingers, animals, corn and popcorn, cloud, soap, fabric, liquids | "How to run an asset job" below |

**In doubt, use the asset route.** If a code-primitive hero fails blind naming, it moves to the asset route; do not keep refining primitives.

Whatever the route, the finished object lands in `assets/library/`. A code-primitive entry has route `code-primitive`, licence `own-work` and `files.rig_module` naming its rig, and
it needs no `.blend`.

Productions numbered 012 and up must declare both fields (`tests/test_asset_library.py`). Older productions are frozen records and declare neither.

### The drawability ban is superseded for hero objects

The old "Drawability law" (`docs/current/specs/style-rubric.md` item 10: hard surfaces only, no people, hands, anatomy, cloth, fluids or animals) banned what code primitives could not draw.
It treated a tooling limit as a content rule, and it pushed topics toward abstract stand-ins, which is the failure the owner rejected. **Anatomy, hands, animals, cloth and fluids are now
allowed when the asset route supplies them.** Without a passing asset they stay off the screen: never draw an abstract stand-in instead.

What does not change: stylised, not photorealistic; no real skin texture, no blood, no gore (age-restriction risk, CLAUDE.md "Format doctrine"). A realistic scan must be simplified and retinted
before it is used, and the gross-out stays conceptual.

## Likeness gate

| Check | When | Tool | Blocks |
|---|---|---|---|
| Blind naming of the asset | end of the asset job | `asset_library.py blind-pack`, then `blind` | status `ready` |
| Blind naming in the video | after the production's gate stills | `blind-pack`, then `likeness` | the final render (`gate.py check`, called by `code3d_render.py`) |
| Silhouette against a reference photo | when a reference exists | kiln `fidelity_check.py` | advisory: read the ranked gaps |
| Mesh health | end of the asset job | `blender-asset-qa` `qa_check.py` | status `ready` |

Blind naming means at least two separate fresh subagents, each shown only neutrally named stills and the prompt `blind-pack` prints. The test passes only if every first guess contains one of the
asset's aliases. The second check exists because stage, crop and colours can destroy a likeness the neutral stills had.

Limits, stated plainly: this is a model's reading of stills, not a human viewer's, and it has **not been calibrated against the rejected 006-011 batch**. It can lean generous, so the owner stays the
final judge (`owner_verdict` in `asset.json`). If it passes something the owner rejects, tighten the test; never loosen it to let a hero through.

## Skill role map

Agreed under the multi-lens protocol (docs/architecture.md), design leading, scriptwriter and marketing consulted. The review was done by one session reasoning through each lens, not by separate agents.
Future sessions inherit this map and do not re-decide it.

- **Design (lead):** likeness needs a measured check and a proper modelling toolset. Factory looks and render profiles stay authoritative, so skills that would compete with them stay out.
- **Scriptwriter:** a mesh that cannot act out the beats is useless. The brief must list moving parts and states from the beat sheet before any search. (Precedent: Poly Haven's tape measure
  was one baked mesh, so it could not extend or cut away.)
- **Marketing:** the hero must read at phone size in the first 2 seconds, so blind naming also runs on the production's own stills. CC-BY credits must reach the description.

| Role | Skill | Use |
|---|---|---|
| Entry point, Blender API rules | `blender-core` | First, on every job |
| Sourcing and likeness measurement | `blender-kiln` | `references/sourcing-strategy.md`, `references/reference-fidelity.md`, `tools/review_renders.py`, `tools/fidelity_check.py`, `tools/cutout.swift` |
| File organisation, scale, naming | `blender-scene-setup` | Every job |
| Cleaning downloaded meshes | `blender-workflow-recipes` recipe 5, `blender-retopology-uv` | Library route |
| Hard-surface modelling | `blender-hardsurface-modeling` | Complex rigid objects primitives cannot carry |
| Organic modelling | `blender-sculpting` | Library has nothing usable |
| Procedural forms and multiples | `blender-geometry-nodes` | Scatter, repeats, parametric shapes |
| Materials | `blender-pbr-materials` | Every job; ambientCG textures |
| Baking high to low detail | `blender-texture-baking` | After sculpting or retopology |
| Neutral presentation light | `blender-lighting-lookdev` | Judging the asset only; production light stays in `code3d/lib/looks.py` |
| Deforming and articulated heroes | `blender-character-rigging`, `blender-animation` | Hands, animals, soft organs |
| Fluids, cloth, soft motion | `blender-simulation` | Bake it, then render headless |
| Mesh QA (mandatory) | `blender-asset-qa` | Every job, before `ready` |

**Who wins on overlap:** this document sets the job's steps. Kiln supplies sourcing and likeness tools, the `blender-*` skills supply craft, and `blender-asset-qa` is the QA of record.

**Do not use from kiln:** the full `/kiln` CONFIG-to-EXPORT pipeline (it targets GLB export for games, web and AR; the factory stores `.blend`), Kiln Studio (its worker can bill an API key, and its AR link opens to
the local network; removed from the installed copy, see below), AI backends (`assets/registry.yaml` `excluded`), `/kiln setup` (not run; `gltf-transform` needs Node, which this Mac lacks, and the factory does not need it).

**Installed** in `~/.claude/skills/` by folder copy, no installer: 14 skills from `EL4CTEO/blender-skills` (MIT, commit `fb92cfb`, v1.2.0) and kiln from `elithril/blender-kiln` `plugin/` (MIT, commit `e9a4214`, v3.0.0). The kiln copy deliberately omits `.mcp.json`, `.claude-plugin/` and `studio/`: left in place, Claude Code auto-registers them as a `kiln-studio` MCP server. Repeat that removal on any kiln update.
**Not installed**, because they serve games or conflict with factory rules: `blender-rendering` (factory render profiles), `blender-stylized-npr` (toon look retired), `blender-game-optimization`, `blender-export-pipelines`,
`blender-environment-kits`, `blender-video-editing`, `blender-time-of-day`, `blender-addon-development`, `blender-pipeline-automation`, `blender-texturing`, `blender-facial-shapekeys`, `blender-clothing`, `blender-hair-grooming`,
`blender-weather-fx`. `blender-core` and `blender-workflow-recipes` still mention some of these; ignore those routes. If a hero truly needs one (fur: `blender-hair-grooming`), clone the repo to a scratch folder, read the skill, copy the folder over, and add it to this list.

## Operating model

- **Asset-building is interactive:** Blender open, driven through MCP for Blender. **Production rendering stays headless,** exactly as today (`factory/code3d_render.py`, `blender -b`).
- Any render launched in a job (stills, fidelity, review) runs under `caffeinate -dimsu`. This includes a render started inside the open Blender: hold it with `caffeinate -dimsu -w $(pgrep -x Blender) &`.
- Assets reach a video only through `load_hero`, in a code3d production. This is not a new engine, and code3d still never mixes with diffusion footage.
- MCP for Blender: server `blender` (`uvx mcp-for-blender`), project-scoped in Claude Code; add-on `blender_mcp` 1.8 on port 9876. Verified end to end on 2026-11-04.
- `generate_3d` is **not used**: every provider is off and would need an account or credits.

## Sources

The registry is `assets/registry.yaml`: how each source is reached, its licence and its status. Search in this order; the best licence that fits wins.

| Priority | Source | Provides | Licence | Status |
|---|---|---|---|---|
| 1 | Poly Haven | HDRIs, textures, models | CC0 | connected through MCP |
| 2 | ambientCG | PBR textures | CC0 | connected through API |
| 3 | BlenderKit free plan | models, materials | per asset | **owner step** (account) |
| 3 | Sketchfab free downloads | models | per model | **owner step** (account, API token) |
| 3 | Poly Pizza | low-poly models | CC0 or CC-BY | **owner step** (API key) |
| 4 | MB-Lab | human bodies | **AGPL, see the flag** | candidate, not installed, archived project |
| 4 | CharMorph | human bodies | per base model | candidate, not installed |
| 5 | Smithsonian 3D Open Access | scanned objects, animals | CC0 where marked | candidate, not wired |

**Do not create accounts.** An owner-step source is used only after the owner connects it. If a job would have succeeded with one, say so in the report.

**A search hit is not a match.** Poly Haven's search always returns something: "human heart" returned a marble bust and "popcorn" returned a croissant. Look at the asset before taking it.
No-account coverage of organic objects is thin, so expect to fall through to modelling for many of them.

**MB-Lab flag:** generated models are AGPL-3.0, and may only be shared under AGPL. Renders and videos are not considered derived work, per its licence page. The project is archived and untested on Blender 5.2.3. Each use needs the owner's dated OK in `licence.owner_ok`. It makes whole bodies, not organs.

**Licence rule:** CC0 preferred; Royalty-Free acceptable; CC-BY only with the attribution recorded in the asset README; anything unclear is not used. NC, ND and SA are refused. `factory/asset_library.py` enforces this. A CC-BY asset's credit must also appear in the description of every production that uses it: put it in the `notes.md` Publish package text, and `check` fails if a `publish.json` lacks it.

Materials and HDRIs that are not hero objects keep their existing home: `code3d/assets/`, logged in `code3d/assets/LICENSES.md`. Check there first.

## The library

```
assets/
  registry.yaml               the sources
  library/
    README.md
    <object-slug>/
      asset.json              the record (committed)
      README.md               source, licence, date, productions; generated from asset.json (committed)
      build.py                the script that builds it, if any (committed)
      job/report.md           the job report (committed)
      job/stills/             review stills (local, gitignored)
      <slug>.blend            the asset, textures packed (local, gitignored)
```

**Binaries exist only on this Mac,** like all factory media. A library-route asset can be downloaded again from its recorded source, and a scripted one rebuilt from `build.py`. A hand-sculpted asset cannot: **it has no backup until the owner decides on one**, so keep a `build.py` whenever possible.

## How to run an asset job

You need no earlier context. Input: an object and what the video needs it to do. Output: a `ready` library asset. **Spend $0, create no accounts.**

**1. Check it is not already solved.**
```
.venv/bin/python factory/asset_library.py find heart
```
Try the Spanish and English names. If it is `ready`, stop and reuse it. If it is `rejected`, read why first. Also check `code3d/lib/` and `code3d/assets/LICENSES.md`.

**2. Open the record.** Aliases are the names a viewer would use, because blind naming is judged against them.
```
.venv/bin/python factory/asset_library.py new human-heart --name "Human heart" --alias heart --alias corazon --family body
```

**3. Write the brief** in `assets/library/<slug>/asset.json`, `brief`: `must_read_as` (what a viewer must say), `seen_at` (how large in frame), `moving_parts` (from the beat sheet), `states` (for example closed and cut open), `style_notes`. **Moving parts decide whether a mesh is usable.**

**4. Open Blender and connect.**
```
python3 ~/.claude/skills/blender-kiln/tools/open_blender.py
```
Call `get_addon_status`, then enable Poly Haven with `execute_blender_code`: `bpy.context.scene.blendermcp_use_polyhaven = True`. Load `blender-core`. If MCP tools are missing, the server was not loaded in this session: check `claude mcp list`, then restart Claude Code. Opening refuses if a Blender without the add-on server is already running; this happens after a crash, because Blender relaunches itself. Quit that one and open again.

**5. Search the registry in priority order.** Use `search_assets` with `previews` to see thumbnails. Record every query and verdict in `job/report.md`, and add refused candidates to `rejected_candidates` so nobody re-evaluates them. A candidate must pass all of these: it looks like the object, its licence is clear and allowed, and it has the moving parts or can be separated into them.

**6. Get the object.**
- **Library:** `import_asset`, then `blender-workflow-recipes` recipe 5 to clean it.
- **Nothing fits:** build it. Use `blender-sculpting` for organic forms, `blender-hardsurface-modeling` for complex rigid ones, `blender-geometry-nodes` for procedural ones, `blender-simulation` for fluids or cloth. Find a reference photo first. Save the build script as `assets/library/<slug>/build.py` if there is one.
- **Humans:** try CharMorph or MB-Lab only with the owner's OK, per the registry notes.
- If the object is still not recognisable after two correction rounds, stop and report. Do not ship a weak hero, and do not substitute an abstract one.

Call `look` after every significant change, from at least two angles. Numbers do not replace looking.

**7. Make it fit the channel.** Real scale in metres, origin at the base, sitting on z=0, transforms applied. Each moving part is its own named object. Simplify so the feature the fact is about dominates. Remove real skin texture, blood and gore. Colours are set per production later (`hero_colours`), so keep parts in separate material slots.

**8. Save it.** Put every object in one collection named `asset`, then in `execute_blender_code`:
```python
import sys; sys.path.insert(0, "/Users/fernandoaraya/projects/shorts-factory/factory")
import asset_library as al
print(al.save_collection("human-heart", "asset"))
```
This packs the textures and writes only that collection, in its own scene, so stray objects do not get in and the check tools can open the file. In a long session, `importlib.reload(al)` after editing the module.

**9. Run mesh QA** on the saved file; after any fix, save again. Fix errors, then set `checks.qa` to `{"pass": true, "date": "YYYY-MM-DD"}`.
```
python3 ~/.claude/skills/blender-core/scripts/run_in_blender.py --blend assets/library/<slug>/<slug>.blend ~/.claude/skills/blender-asset-qa/scripts/qa_check.py -- --objects <names> --profile render
```

**10. Render review stills** to `job/stills/`. Read them yourself.
```
caffeinate -dimsu blender -b --factory-startup --python-exit-code 1 --python ~/.claude/skills/blender-kiln/tools/review_renders.py -- assets/library/<slug>/<slug>.blend --out assets/library/<slug>/job/stills --views q1,q3,front --mode both --res 800
```

**11. If there is a reference photo, measure it.** The reference must have a transparent background (`tools/cutout.swift` cuts one out). The photo is for measuring only and is never stored in the library unless its licence allows it. Differences of a few percent are noise; large ones are the fix list. Record the result in `checks.fidelity`.
```
caffeinate -dimsu blender -b --factory-startup --python-exit-code 1 --python ~/.claude/skills/blender-kiln/tools/fidelity_check.py -- --reference ref.png --model assets/library/<slug>/<slug>.blend --hdri code3d/assets/hdri/studio_small_08_2k.hdr --out assets/library/<slug>/job/fidelity
```

**12. Blind-name it.** Use colour stills. Run this, then give the printed prompt to at least two separate fresh subagents with no other context. Never tell them what the object is.
```
.venv/bin/python factory/asset_library.py blind-pack assets/library/<slug>/job/stills/<still>.png ...
.venv/bin/python factory/asset_library.py blind <slug> --guess "first guess of agent 1" --guess "first guess of agent 2"
```
Record their words verbatim. On FAIL, go back to step 6. Never add an alias to make a guess pass.

**13. Finish the record.** In `asset.json` fill `route`, `source`, `licence`, `real_size_m`, and set `status` to `ready`, or to `rejected` with the reason in the README Notes. Then:
```
.venv/bin/python factory/asset_library.py seal <slug>
```
`seal` hashes the file, rewrites the README and validates. It must print `OK`.

**14. Report and commit.** Complete `job/report.md`: sources searched, the route taken, visual checks, QA, guesses, wall time, spend. Commit the records, and close Blender if you opened it. Binaries stay out of git by `.gitignore`. Stop if the job passes 60 minutes or twice its estimate (CLAUDE.md "House rules").

### Using an asset in a production

1. Declare `hero_route` and `library_assets` in `scenes.json` (or in `script.json`, which `tools/scenes_from_script.py` copies across).
2. In the scene script: `sys.path.insert(0, str(ROOT / "factory")); import asset_library as al; hero = al.load_hero("human-heart")`. Retint the parts with the production's `hero_colours`.
3. Run `gate.py run` as usual. It now hashes the asset into the fingerprint, so changing the asset makes the record stale.
4. Blind-name the hero in the gate stills: `blind-pack build/gate/<stills>`, then `likeness <production> <slug> --guess ... --guess ...`. Do this after the last change to the stills or rig: any change makes the record stale.
5. `.venv/bin/python factory/asset_library.py use <slug> productions/<channel>/<video>`. It prints any attribution the description must carry.

## Where things go

| What | Where |
|---|---|
| Source registry | `assets/registry.yaml` |
| The asset, its record and README | `assets/library/<slug>/` |
| Job report | `assets/library/<slug>/job/report.md` |
| Job stills | `assets/library/<slug>/job/stills/` |
| Likeness record for a video | `productions/<channel>/<video>/build/gate/likeness.json` |
| Non-hero textures and HDRIs | `code3d/assets/`, `code3d/assets/LICENSES.md` |
| Tests | `tests/test_asset_library.py` |
