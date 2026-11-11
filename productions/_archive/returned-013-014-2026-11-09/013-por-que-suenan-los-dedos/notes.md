# por-que-suenan-los-dedos — production notes (script stage, topic slate 2026-11-07)

Status: SCRIPT ONLY. Nothing modelled, rendered, queued or published. Next stage: asset search for every element below, then scene design (design lens), then the beat sheet with word locks.

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Por qué te suenan los dedos al hacerlos crujir? 😮
- **Descripción:** No son tus huesos chocando: al estirar el dedo, la presión cae y el gas del líquido de la articulación forma una burbuja de golpe. Por eso no puedes repetirlo hasta unos veinte minutos después. 😮 Envíaselo a ese amigo que se hace crujir los dedos antes de escribir cada mensaje.
  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)
- **Hashtags (description, not title):** #dedos #articulaciones #cuerpohumano #shorts

## Script (6 scenes, family body, variant chain, 143 words, ~49.3 s at 2.9 w/s; band 40-50 s)
Hook: ¿Por qué te suenan los dedos cuando los haces crujir? | false belief: El ruido es de los huesos chocando entre sí. | turn: Scene 5: the arthritis warning meets a doctor who cracked only one hand for more than fifty years and compared both. | reframe: No son huesos que chocan: es una burbuja que nace en tu dedo. | share archetype: ese amigo que se hace crujir los dedos antes de escribir cada mensaje

1. **hook** (~7.9 s): ¿Por qué te suenan los dedos cuando los haces crujir? Parece que los huesos chocan. Pero ese ruido es una burbuja que nace.
   - What changes in the world: Contrast: two hands on stage; one finger is pulled and cracks; tags ¿HUESOS? then BURBUJA.
   - Transformation: dos manos quietas → un dedo se estira y cruje; camera: órbita baja alrededor de las dos manos
   - Overlay: tag ¿HUESOS? at 'huesos'
   - Overlay: tag BURBUJA at 'burbuja'
   - Element: hand — route: library human-hand — risk: low (85/85)
2. **capsula** (~6.6 s): Entre los huesos del dedo hay una cápsula sellada, llena de líquido con gas disuelto, como una bebida cerrada.
   - What changes in the world: Push-through: the skin goes x-ray, the knuckle opens into a cutaway: two bones, a sealed capsule, fluid with faint dissolved gas.
   - Transformation: dedo entero → corte de la articulación: dos huesos y una cápsula con líquido; camera: empuje a través de la piel hasta el corte del nudillo
   - Element: finger joint cutaway (bones + capsule) — route: hand-skeleton asset + capsule geometry, cream cutaway plate — risk: medium: cutaways of fingers read 55 in 006; the bones are the context cue, measure early
3. **chasquido** (~10.0 s): Al estirar el dedo, los huesos se separan, la presión cae de golpe, y el gas forma una burbuja: ese es el chasquido. En 2015, una resonancia lo filmó.
   - What changes in the world: The bones pull apart, the capsule stretches, and a bubble snaps into existence with the crack; an MRI-style frame flashes the same moment.
   - Transformation: cápsula estirándose → aparece de golpe una burbuja dentro del líquido; camera: primer plano que retrocede de golpe con el chasquido
   - Overlay: chip 2015 at '2015'
   - Element: gas bubble in joint fluid — route: geometry, transparent profile at minimal volume — risk: low with the bones in frame
4. **espera** (~5.5 s): Por eso no puedes repetirlo enseguida: el gas tarda unos veinte minutos en volver a disolverse.
   - What changes in the world: The finger is pulled again: no crack; a clock face runs and the bubble shrinks back into the fluid.
   - Transformation: segundo tirón sin ruido → la burbuja se encoge mientras corre un reloj; camera: travelling lateral desde el dedo hasta el reloj
   - Overlay: counter 20 min (mono, from 0) at 'veinte'
   - Element: clock — route: library search or clock_rig (003) — risk: low
5. **giro** (~9.0 s): ¿Y la artritis? Un médico hizo crujir solo su mano izquierda, a diario, durante más de cincuenta años. Al final, ninguna de sus manos tenía artritis.
   - What changes in the world: The turn, a named-person micro-scene: left hand cracks, right hand never; years tick by; the two x-rays slide side by side, both clean.
   - Transformation: mano izquierda que cruje y mano derecha quieta → pasan los años → las dos radiografías iguales; camera: subida en grúa sobre las dos manos y bajada a las radiografías
   - Overlay: counter 50+ AÑOS at 'cincuenta'
   - Overlay: gold ring mark on each hand at 'ninguna'
   - Element: two hands, mirrored — route: library human-hand mirrored — risk: low
6. **cierre** (~10.3 s): Así que no son huesos que chocan: es una burbuja que nace en tu dedo. Envíaselo a ese amigo que se hace crujir los dedos antes de escribir cada mensaje.
   - What changes in the world: Single reframe image: the hand closes, and one bubble glows inside each knuckle as all five crack in sequence.
   - Transformation: mano abierta → los cinco nudillos crujen en fila y en cada uno se enciende una burbuja; camera: retroceso desde un nudillo hasta la mano entera
   - Overlay: ENVÍASELO tag at_word 'envíaselo'

## Lens record
- Marketing (lead on topic): curiosity 9/10: Almost everyone has done it and has been warned 'te va a dar artritis'; the viewer can test the 20-minute wait on the spot.
- Scriptwriter: flatness test passed (each scene's 'what changes' is a different event; swapping any two breaks the story); the turn comes before the closing reframe; the archetype names a behaviour.
- Design: code3d on the asset route: the hand is library asset 'human-hand' (blind 85/85); the finger bones come from a CC0/CC-BY hand-skeleton asset; the joint capsule, fluid and bubble are simple geometry read through the bones' context. Preset chosen at scene design.

## Sources and numbers (no number is invented; none is rendered as a source on screen)
- Mechanism: Kawchuk et al. 2015, PLOS ONE, 'Real-Time Visualization of Joint Cavitation': MRI shows the crack coincides with a cavity forming in the synovial fluid (tribonucleation), not a bubble collapsing. Verified (Science News 2015).
- Wait before cracking again: about 20 minutes (some sources say up to 30) for the gas to redissolve; classic source Unsworth, Dowson & Wright 1971, Annals of the Rheumatic Diseases. Unsworth recalled, the ~20 min figure verified through secondary sources. Narration says 'unos veinte minutos'.
- Turn: Donald Unger, letter in Arthritis & Rheumatism 1998: cracked the knuckles of his left hand at least twice a day and never the right, for decades; no arthritis in either hand; Ig Nobel Prize in Medicine 2009. Sources differ on 50 vs 60 years, so the narration says 'más de cincuenta años'. One person: not proof; the narration reports what he found, it does not claim cracking is harmless.
- Gas composition (often cited as CO2 or nitrogen) is deliberately NOT stated: sources disagree.

## Scientific simplifications (stated plainly)
- The capsule and fluid are schematic; the bubble is enlarged for legibility.
- The 'MRI' frame is a stylised flash, not the study's footage.

## Modellability audit and pre-written fallbacks (2026-11-07, `docs/current/reports/modellability-audit-012-016.md`)
Ladder fallbacks pre-approved by the scriptwriter, design and marketing lenses in the audit (one session), so a production run applies them WITHOUT stopping when a scene trips its trigger. The script is unchanged until a rung is applied. When one is: update `script.json` (beat, `what_changes`, narration if rung 3), re-run the flatness swap test, log the reshape here and as a row in `lens-decisions.md` (what changed, rung, why). Aliases listed below are decided NOW, before any reading; none may be added after a guess.

**Verdict: MODELABLE WITH THE WRITTEN FALLBACKS.** Riskiest element: the knuckle joint and its bubble (scenes 2-3), which depend on a rigged finger.

Routes (searched live 2026-11-07): hand = library `human-hand` (blind 85/85) BUT it is NOT rigged (its job report: a finger cannot bend alone). Bones = Sketchfab "Hand Skeleton&Skin" by Novaky (e24e96b6, CC-BY, skin and matching skeleton in one file, not rigged); taking it as the hand too keeps skin and bones aligned for the x-ray. Rig = a build (`blender-character-rigging`, one armature, finger chains), MEDIUM. Precedent: the 006 scene 2 x-ray finger (Fresnel translucent skin, ivory bone) read 85/75. Clock = BlenderKit "Wall Clock" by abd3d (a8c30fba, CC0) or Poly Haven "Wall Clock" (e6b0a61b, CC0). Radiographs = the skeleton rendered flat on a lightbox (build). Capsule, fluid, bubble = geometry inside the x-ray finger.

- **Rig (trigger: rigging passes the timebox).** Rung 1: no bending needed. The pull is a straight translation along the finger's axis (the other hand grips and pulls), with the distal part split at the knuckle; scene 6 becomes an open hand whose five knuckles light and pulse in sequence instead of a closing fist (`transformation`: "mano abierta → los cinco nudillos se encienden en fila"). Narration unchanged.
- **Scene 2 capsula (trigger: the joint element fails the gate).** Rung 1: never an isolated section; the x-ray finger stays inside the whole hand, the capsule a translucent sleeve around the knuckle. Aliases: knuckle, finger joint, finger bones, hand bones. Rung 2: a sealed soda bottle appears beside the knuckle as the analogy the narration already names ("como una bebida cerrada"). Narration unchanged.
- **Scene 3 chasquido (trigger: the bubble fails the gate).** Rung 1: the gap between the bones visibly widens and the bubble appears with a pop ring, the x-ray hand in frame. Aliases: bubble, gas bubble, air bubble. Rung 2: twin staging: the bottle cap twists off and its bubbles burst on the same frame as the joint bubble. Rung 3 narration (+1 word, ~49.6 s, band 40-50): "Al estirar el dedo, los huesos se separan, la presión cae como al destapar una bebida, y nace una burbuja: ese es el chasquido. En 2015, una resonancia lo filmó."

## BATCH DIRECTIVE 2026-11-09 (batch 012-016, runner)
RECORDED PRE-CHECK FIRST: before building the rest of the production, measure the finger-joint cutaway likeness (scene 2 element: hand + bones + capsule in the cream plate, aliases above) with three isolated readers. Apply the written rung 1 then rung 2 fallbacks if it fails. If it still cannot pass, SKIP this production under return-and-replace. Return-and-replace: if this topic fails beyond the Reshape ladder (hero mechanism or promise would change, or the ladder is exhausted), mark it RETURNED in notes.md (reason), mark it `returned 2026-11-09: <reason>` in docs/current/idea-bank.md, then draw the next eligible BANKED entry under the bank draw rules (TOPIC BALANCE window incl. productions before it; never the reserve; never an unbanked topic; no toilet/poop theme), mark it drawn, create its folder ONLY with tools/new_production.py, and write one line `REPLACEMENT: productions/mecanalia-es/NNN-slug` at the end of this notes.md. If no eligible entry remains, write `REFILL DUE: no eligible banked entry` instead. Do not write the replacement script in this session. Under gate_version 2 including the visibility check. No publishing, no spend, no accounts; do not touch the orchestrator, its queue or excluded list.

## RUN LOG 2026-11-09 (verifier run: "scenes.json missing"): NOT COMPLETE, stopped at the recorded pre-check
Status: still script stage. No scenes.json, no gate record, no render, nothing queued, nothing published or spent. The ladder is NOT exhausted and the topic is NOT returned: the pre-check has simply not been measured yet.
- Done: Blender opened through `tools/asset_blender.py open`; Sketchfab search "hand skeleton skin" confirmed the audit's route, Novaky "Hand Skeleton&Skin" (UID e24e96b6bc39423b871b10f098876b8f, CC-BY, 30k faces), imported at 0.4 m. Nothing saved to the library. The Blender GUI session was left open and unsaved (Bash was denied before `asset_blender.py close`): close it before any headless job.
- Finding 1: the file is TWO separate hands side by side (skin hand left, skeleton right), not a skeleton inside a skin. Both are split into ~185 loose islands (skin fingers are separate ~500-face segments; skeleton phalanges separate).
- Finding 2: the skeleton is posed with a widely splayed thumb and spread fingers while the skin hand has closed fingers, so a plain overlay does not put the bones inside the fingers. Using it needs the skeleton's phalanges placed finger by finger inside the skin (a posing or rigging job, MEDIUM per the audit) or a different asset.
- RUN 2 (same day, Bash available): the Blender GUI was closed cleanly at the end (`asset_blender.py close`). Correction to the findings above: the two hands DO line up. Shifting the skeleton by (-0.232, 0, -0.025) in the import's units (not a bounding-box centring, which the wrist and carpals threw off) puts all four finger chains and the thumb inside the skin hand. No rig was needed for a still. Scene: skin as an alpha 0.25 sleeve, ivory bones, a translucent teal capsule cylinder at the proximal-middle joint of the longest finger, cream plate, coral stage; Cycles 540x960, 48 samples. Working file (not committed, scratchpad): `/private/tmp/claude-501/-Users-fernandoaraya-projects-shorts-factory/e6157d0a-7b13-4b7d-b4ba-882250e51381/scratchpad/precheck/013-knuckle-precheck.blend`, still `.../precheck/still_a.png`. Asset licence CC-BY (Novaky), not yet in `assets/library` or LICENSES.
- PRE-CHECK READING 1 (rung 1 staging: whole hand in frame, capsule as a translucent sleeve; `tools/blind_read.py`, 3 isolated readers, no `--record` because there is no scenes.json yet; every reading counts): "skeletal hand model (bones of a hand)" 96; "skeleton hand (white bone model, fingers spread, with a small blue-grey clip on the middle finger)" 96; "white skeletal hand model (anatomical hand bones)" 93. Confidence is far above the floor. Against the pre-written aliases (knuckle, finger joint, finger bones, hand bones) only reader 3 ("hand bones") matches as a phrase; no alias is added to make the others pass. Honest reading: the bones read, the capsule does NOT (a "clip"). Strict verdict: NOT PASSED on rung 1. Next is rung 2 (sealed bottle beside the knuckle, so the capsule and the "como una bebida cerrada" analogy are named by a context cue), then a second reading; failing that, RETURNED and replaced.
- Not done this run: rung 2 staging and reading, scenes.json, hero gate, the other five scenes, narration, render, queue. Still script stage; nothing queued, spent or published.
- PRE-CHECK READING 2 (rung 2: sealed soda bottle beside the whole x-ray hand, same stills procedure; bottle = Sketchfab "Soda Bottle Orange Liquid" by smart61, CC-BY, brand label hidden; hand and capsule as in reading 1; three isolated readers, every reading counts): "orange soda bottle; alternatives: skeleton hand, amber medicine vial" 70; "plastic bottle of orange soda" 85; "plastic bottle of orange soda; alternatives: skeleton hand, amber pill bottle" 85. No reader names knuckle, finger joint, finger bones or hand bones as the answer: the bottle dominates and the joint reads as nothing. FAIL.
- RETURNED 2026-11-09: reason. The scene-2 element (finger-joint cutaway with its capsule) failed the recorded pre-check on rung 1 (bones read at 93-96 but the capsule reads as a "clip"; only 1 of 3 guesses matched a pre-written alias) and on rung 2 (the bottle analogy wins the frame, 0 of 3 name the joint). Rung 3 only adjusts the narration to a staging that already failed, and every further route (a different cutaway that makes the capsule itself readable) would change the hero mechanism of the topic's promise (a sealed capsule and a bubble inside the knuckle), which is where the ladder stops. No alias added, no floor lowered. Per the batch directive the topic is returned and replaced from the bank. Nothing was spent, published or queued. Reusable: the bones-inside-skin alignment (offset above) and the finding that a hand x-ray reads at 93-96; only the capsule is unreadable.
- REPLACEMENT: productions/mecanalia-es/017-que-pasaria-si-se-corta-el-cable-del-ascensor
- Next steps (only if the topic is ever revived by a capability change, e.g. a readable capsule or joint asset), in order: (1) place the bones inside ONE skin finger plus the knuckle (rung 1 stays: whole hand in frame, capsule as a translucent sleeve), stills in the cream plate; (2) `tools/blind_read.py` with three readers on scene 2, aliases knuckle / finger joint / finger bones / hand bones; (3) fail -> rung 2 (sealed bottle beside the knuckle) -> still failing -> RETURNED and replaced per the batch directive; (4) pass -> write scenes.json (gate_version 2, hero_rig, hero_still, render_cost_class, scene_elements, visibility), hero gate and freeze, then the scenes, gate, `queue_chain.sh`.
