# Modellability audit of productions 012-016 (2026-11-07)

Owner check, run under CLAUDE.md "Reshape ladder", "Every element at hero standard" and "Asset library and hero routing". Scope: modellability only, read from each committed `script.json`. Nothing was modelled, downloaded, rendered or changed in a script. Pre-written fallbacks live in each production's `notes.md`, section "Modellability audit and pre-written fallbacks".

## Verdicts

| Production | Verdict | Riskiest element |
|---|---|---|
| 012 toothbrush and toilet plume | MODELABLE WITH THE WRITTEN FALLBACKS | the droplet plume in the laser sheet (scene 3): risks reading as steam or smoke |
| 013 knuckle cracking | MODELABLE WITH THE WRITTEN FALLBACKS | the knuckle joint and bubble (scenes 2-3); the library hand is not rigged, so it needs a rig build or the no-bend restaging |
| 014 swallowed gum | MODELABLE WITH THE WRITTEN FALLBACKS | the gum ball blocking the bowel (scene 6): risks reading as a tumour or a lump |
| 015 flies rubbing their legs | MODELABLE WITH THE WRITTEN FALLBACKS | the mouthparts and leg macro (scenes 2, 3, 5); the CC0 scan is unlikely to carry hairs, pads or a readable sponge mouth |
| 016 lifetime poop | MODELABLE WITH THE WRITTEN FALLBACKS | the pile at scale (scenes 2-4): risks reading as dirt, chocolate or firewood |

None is NOT MODELABLE, so no replacement is proposed. Had one been, the replacement could not have come from the toilet theme: 012 and 016 already fill it (CLAUDE.md "Topic selection", TOPIC BALANCE), which rules out the wet-wipes and brown-poop candidates.

## Method

- **Local first.** `asset_library.py find` for every element. Only `human-hand` and `popcorn` exist in `assets/library/`. Local rigs checked: `toilet_rig` (005) is a flat side-profile cutaway with no lid, so it does not serve a 3D bathroom; `corn_rig` (011) supplies the corn kernel; `clock_rig` (003) is a gear train with a dial.
- **Live searches on 2026-11-07:** BlenderKit through `tools/asset_blender.py blenderkit-search`, which accepts only CC0 and Royalty-Free (27 queries). Sketchfab through the public v3 search with `license=cc0` and `license=by` only (15 queries x 2). Candidate model details came from the Sketchfab API (licence, downloadable, animation count, description).
- **Judged by eye.** Thumbnails of the 19 deciding candidates were reviewed as a contact sheet. A hit was not taken as a match until seen.
- **Licence order:** CC0 first, Royalty-Free acceptable, CC-BY where no CC0 serves, with no description credit (owner 2026-11-07). Every ID below is a search result, not a downloaded asset. Licences are re-read at the asset job.
- **Risk levels are predictions, not readings.** No blind-naming gate was run. Aliases for every flagged element are fixed in the notes now, before any reading.

## Shared asset jobs

- **Toilet:** one job serves 012 and 016. BlenderKit "Toilet ceramic white" (6a342733, RF, lid). Fallback: Sketchfab "Toilet" by hippostance (132a8ee2, CC-BY; lid and seat are separate objects per its description).
- **Rigs (builds, effort unmeasured):** the 013 hand and the 015 fly's front legs. Each has a no-rig fallback in the notes.

## Per production: hero and every scene's key element

### 012 cepillo-de-dientes-junto-al-inodoro (objects, chain, 7 scenes)
Hero: the toilet (library, see above). The context cue for every element is the bathroom: toilet, sink, toothbrush cup.

| Scene | Key element | Route | Context cue | Risk |
|---|---|---|---|---|
| 1 hook | toothbrush in a cup; toilet | BlenderKit "Toothbrushes" Cenek Studio (f70efd3c, RF); toilet asset; sink f12eb8ca (RF) | sink and toilet together | low |
| 2 descarga | bowl water, turbulent | physically based water, draft profile in gate rounds, shallow transmission | the bowl around it | medium (render cost) |
| 3 nube | droplet plume in a laser sheet | instanced droplets + emissive sheet (build) | the open bowl and seat below, tiles as a ruler | **high**: invisible subject, may read as steam |
| 4 carga | tinted droplets hanging | same particles, palette tint | toilet rim and toothbrush cup in the orbit | medium |
| 5 aterrizaje | toothbrush bristles | same toothbrush asset | head, handle neck, cup rim | medium |
| 6 giro | lid closing; toilet brush scrubbing | toilet lid (separate object); BlenderKit "Plastic Toilet Brush" (283b619f, RF) | the toilet | low |
| 7 cierre | reframe tableau | assets above | whole bathroom | low |

### 013 por-que-suenan-los-dedos (body, chain, 6 scenes)
Hero: the hand. The library `human-hand` (blind 85/85) is not rigged. Sketchfab "Hand Skeleton&Skin" by Novaky (e24e96b6, CC-BY) has skin and a matching skeleton in one file, which suits the x-ray. Precedent: the 006 scene 2 x-ray finger read 85/75.

| Scene | Key element | Route | Context cue | Risk |
|---|---|---|---|---|
| 1 hook | two hands, one finger pulled | hand asset + rig (build) or the axial-pull restaging | two hands | medium (rig) |
| 2 capsula | finger joint: bones and capsule | skeleton asset, translucent skin, capsule geometry | the whole x-ray hand | **medium-high** |
| 3 chasquido | gas bubble in joint fluid | geometry, transparent profile at minimal volume | the bones on either side | **medium-high** |
| 4 espera | wall clock | BlenderKit "Wall Clock" abd3d (a8c30fba, CC0) or Poly Haven (e6b0a61b, CC0) | beside the hand | low |
| 5 giro | two hands; two radiographs | mirrored hand; skeleton rendered flat on a lightbox (build) | the lightbox | low-medium |
| 6 cierre | five knuckles cracking | rig, or open-hand sequence (fallback) | the hand | medium (rig) |

### 014 que-pasa-si-tragas-un-chicle (whatif, journey, 7 scenes)
Hero: the gum, a build (no stick or wrapper asset exists: BlenderKit returned 0 results and the Sketchfab hits are branded packaging, refused). Stage: BlenderKit "Stylized Digestive System" by danes_dysfunction (313d76be, RF). Alternatives: Sketchfab f78ce703 (CC-BY) and BlenderKit stomach 1855ece9 (RF).

| Scene | Key element | Route | Context cue | Risk |
|---|---|---|---|---|
| 1 hook | gum stick + wrapper; digestive system | build; digestive asset (no torso) | the wrapper; the organ set on the cream plate | medium |
| 2 esofago | oesophagus with a squeeze ring | asset tube + lattice/hook, or a built tube | stomach below | medium |
| 3 estomago | stomach, acid, food pieces | stomach asset with a boolean cut; liquid material; BlenderKit bread (d9812418, RF) | oesophagus attached | medium |
| 4 intestino | gum and corn leaving the stomach | `corn_rig` kernel (011) | stomach exit | **high as scripted** (hulls are flakes, not an object); low with the kernel fallback |
| 5 salida | whole coiled intestine | digestive asset, or Sketchfab "Small and large intestine" (8a1ca8e3, CC-BY) | iconic coils | low-medium |
| 6 giro | gum ball (bezoar) | instanced chewed pieces (Sketchfab 486222e1 CC-BY or a build) | the intestine; the pieces' identity | **high** |
| 7 cierre | the traced route | assets above | whole tract | low |

### 015 por-que-las-moscas-se-frotan-las-patas (objects, journey, 6 scenes)
Hero: the housefly. Sketchfab "Musca domestica" by disc3d (15790094, **CC0**) is a scan of a real 5 mm housefly. It needs a stylised material and a two-chain front-leg rig. Alternatives: Sketchfab 5fe7cbd2 (CC-BY), or BlenderKit 1fd6b0b2 (RF, rigged, blowfly colours, needs retinting).

| Scene | Key element | Route | Context cue | Risk |
|---|---|---|---|---|
| 1 hook | fly on a plate | fly asset; BlenderKit plate (b9315514, RF) | food | low |
| 2 basura | leg hairs and pads on a peel | built hairs and pads on the scan's leg; Poly Haven "Trashbag" (CC0); Banana (CC0) aged | body in frame, trash | **medium-high** |
| 3 sensores | taste sensors on the leg | emissive points | leg attached to the fly | medium |
| 4 escupe | saliva drop on bread | small liquid volume; BlenderKit bread (d9812418, RF) | the mouth on the bread | medium |
| 5 giro | sponging mouthparts | built labellum on the scan | the fly's head | **medium-high** |
| 6 cierre | the route traced to the trash | BlenderKit "Kitchen set" (8a3fb1a2, RF) | the kitchen | low |

### 016 cuantos-kilos-de-caca-en-tu-vida (numbers, scale, 6 scenes)
Hero: the stool unit, a matte stylised build (alternative: Sketchfab 5b80e6a0, CC-BY). The emoji swirl is refused. The toilet is the shared asset and the context cue in every frame.

| Scene | Key element | Route | Context cue | Risk |
|---|---|---|---|---|
| 1 hook | one unit on a kitchen scale | build; BlenderKit kitchen scale (1cb533b1, RF) | the toilet beside it | medium |
| 2 anio | pile burying the scale; suitcases | instanced units; BlenderKit "Black suitcase" (ebbe0d72, RF) | units falling from the toilet | **medium-high** |
| 3 decada | mound beside a horse | instanced units; BlenderKit "Draft horse" (f844b8ab, RF) or Sketchfab 791844e9 (CC-BY) | toilet at the foot | **medium-high** (plus no walk rig) |
| 4 vida | hill vs two cars on a balance | units; BlenderKit "80's Cartoon Car" (d93bc35f, RF); built balance | toilet dwarfed | **high** |
| 5 giro | water tank + solids | built tank, minimal transmission; units tinted | the tank | medium as scripted ("solid block" = a banned flat stand-in); low with the default fallback |
| 6 cierre | tableau | assets above | toilet in the foreground | low |

## Fallbacks written (each in its production's notes.md)

| Production | Scene | Rungs written | Narration change (rung 3) | Duration after |
|---|---|---|---|---|
| 012 | 3 nube | 1, 2, 3 | +2 words | ~57.6 s (band 45-60) |
| 012 | 2, 4, 5 | 1 (scene 4: 1, 2) | none | — |
| 013 | rig (1, 6) | 1 | none | — |
| 013 | 2 capsula | 1, 2 | none | — |
| 013 | 3 chasquido | 1, 2, 3 | +1 word | ~49.6 s (band 40-50, tight) |
| 014 | 1, 2 | 1 | none | — |
| 014 | 4 intestino | 1 + 3 | 0 words ("cáscaras" -> "granos") | ~56.6 s |
| 014 | 6 giro | 1, 2, 3 | +2 words | ~57.3 s |
| 015 | 2, 3, 4 | 1 (scene 3: 1, 2) | none | — |
| 015 | 5 giro | 1, 2, 3 | -4 words | ~56.9 s |
| 016 | 2-4 pile | 1, 2 | none (the narration never names a hill) | — |
| 016 | 3 horse, 5 giro | 1 (scene 5 applied by default) | none | — |

The lenses (one session) pre-approved every fallback, so a production run applies them without stopping. No fallback touches a hero mechanism, a hook, a false belief, a structure variant or a closing slot, and none merges or pads a scene. Each keeps its scene's event, so the flatness swap test still holds. Hard rules are respected: no blood, the stool is matte and stylised, the fly scan gets a stylised material, and anatomy stays stylised on the cream plate.

## Open points (not blockers)

- **Rigs:** the 013 hand and the 015 fly legs are builds with no measured effort; the no-rig fallbacks cover both.
- **Unverified asset details:** whether the toilet's lid separates (BlenderKit 6a342733), and how much leg and mouth detail the CC0 fly scan carries. Both are checked at the asset job, and both have fallbacks.
- **Sources:** the flagged figures in each notes.md (012 Gerba, 013 Unsworth, 015 fly physiology, 016 comparison weights) are outside this audit's scope and still need confirming before each beat sheet is final.
