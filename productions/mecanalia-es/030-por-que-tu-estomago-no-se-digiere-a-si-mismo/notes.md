# por-que-tu-estomago-no-se-digiere-a-si-mismo: production notes (developed script, block B4 creative session 2026-11-11)

Status: DEVELOPED STANDBY (bank status `standby 030 2026-11-11`): stamped script on file, in no batch. Not batch-eligible until every proof in `proofs.json` has passed (doctrine-topics-and-scripts.md "Blind proofs before batch eligibility"). Nothing modelled, rendered, queued or published. A production proceeds FROM THIS SCRIPT; it changes it only through the Reshape ladder, logged in the ledger below.
Staging mode: cutaway. The sealed digestive system in x-ray, then a section through the stomach wall. Rotation: as the standby after 029 (cutaway), 026 and 027 stage, 028 world: two cutaways in any five.

## Publish package draft (Spanish; the owner publishes)
- **Título:** ¿Por qué tu estómago no se digiere a sí mismo? 🫃
- **Descripción:**
  ¿Por qué tu estómago no se digiere a sí mismo? Porque una capa de moco con bicarbonato frena el ácido antes de tocar la pared.
  Y lo que se daña, se renueva cada pocos días. 🫃
  Envíaselo a ese amigo que se come cualquier cosa sin pensarlo dos veces.
- **Hashtags (description, not title):** #cuerpohumano #estomago #ciencia #shorts

## Script (6 scenes, family body, variant chain, 141 words, ~48.6 s at 2.9 w/s; band 40-50 s)
Hook: ¿Por qué tu estómago no se digiere a sí mismo? | false belief: El ácido del estómago es débil, por eso no lo daña. | turn: Scene 5: some acid still gets through, and the surface cells are wrecked anyway: the lining survives by replacing them every few days. | reframe: Tu estómago sí se ataca a sí mismo: solo que se repara más rápido de lo que se daña. | share archetype: ese amigo que se come cualquier cosa sin pensarlo dos veces
Theme / main tension (TOPIC BALANCE): digestion / bodily.

1. **hook** (~9.0 s): ¿Por qué tu estómago no se digiere a sí mismo? Mucha gente cree que el ácido del estómago es débil, y por eso no lo daña.
   - What changes in the world: The digestive system in x-ray on the stage; a bite of food slides down the oesophagus and drops into the stomach, which glows with acid; the tag ¿ÁCIDO DÉBIL? hangs on it.
   - Transformation: estómago vacío → cae un bocado al ácido; camera: bajada siguiendo el bocado por el esófago hasta el estómago
   - Overlay: tag ¿ÁCIDO DÉBIL? at 'débil'
   - Element `stomach-xray` (object): a human stomach in an x-ray digestive system; route library digestive-system (sealed; x-ray material state); risk low: sealed asset; the x-ray state is its brief; aliases (fixed now, before any reading): stomach, digestive system, digestive tract, human stomach, stomach anatomy, estómago
2. **acido** (~5.9 s): Al contrario: fabrica ácido clorhídrico, tan fuerte que, junto con sus enzimas, deshace la carne que comes.
   - What changes in the world: Inside the stomach, a piece of meat sinks into a pool of glowing acid; its surface frays and comes apart into strands and then a cloud.
   - Transformation: trozo de carne entero → se deshace en el ácido; camera: empuje dentro del estómago hasta el trozo de carne
   - Overlay: label HCl tag at 'clorhídrico'
   - Element `meat-dissolving` (event): a piece of meat dissolving in stomach acid; route build: meat chunk (material route, stylised, no real texture) inside the stomach section; acid as an emissive liquid; risk high: event element; proof P1; aliases (fixed now, before any reading): meat dissolving, dissolving, food dissolving, digesting, digestion, food being digested, meat, steak, food in the stomach, stomach acid
3. **moco** (~7.9 s): Y la pared del estómago también es carne. Lo que la salva es una capa de moco espeso que la cubre por dentro.
   - What changes in the world: Push-through into the wall: a section of the stomach wall in layers, and on its inner face a thick translucent gel spreads out and covers it, between the acid and the cells.
   - Transformation: pared desnuda frente al ácido → una capa de moco la cubre; camera: travelling a través de la pared, del ácido a las capas
   - Overlay: label MOCO tag at 'moco'
   - Element `wall-mucus` (object): a cross-section of the stomach wall with a mucus layer; route build: layered wall section (muscle, cell row, gel), stylised, attached to the digestive-system stomach; risk high: a layer stack reads as a 'cake' unless the stomach is in frame; proof P2; aliases (fixed now, before any reading): stomach wall, stomach lining, stomach cross-section, stomach, mucus, mucus layer, gastric mucosa, estómago
4. **bicarbonato** (~5.2 s): Ese moco atrapa bicarbonato, que neutraliza el ácido justo antes de que toque las células.
   - What changes in the world: Acid droplets fall into the gel; as they sink they meet bicarbonate beads, fizz and change from the acid colour to neutral before reaching the cell row.
   - Transformation: gotas de ácido → se apagan dentro del moco antes de la pared; camera: seguimiento de una gota de ácido hundiéndose en el moco
   - Overlay: label BICARBONATO tag at 'bicarbonato'
   - Element `acid-neutralised` (event): acid drops neutralised inside a mucus layer; route same section as P2; drops as emissive spheres with a colour change and fizz; risk high: event element, read with the P2 section; aliases (fixed now, before any reading): stomach lining, stomach wall, mucus, mucus layer, acid, stomach acid, neutralizing, neutralising, fizzing, bubbling
5. **renueva** (~9.0 s): Aun así, algo de ácido pasa y daña las células de la superficie. Por eso se renuevan cada pocos días, antes de que el daño avance.
   - What changes in the world: The turn: a few drops get through; cells on the surface darken, crack and peel away; new cells push up from below and take their place, row after row, and the gel closes over them again.
   - Transformation: células dañadas → se desprenden y otras nuevas ocupan su lugar; camera: empuje a la fila de células y retroceso cuando suben las nuevas
   - Overlay: mark red on the damaged cells at 'daña'
   - Element `cells-renewing` (event): damaged cells peeling off a stomach lining as new ones grow; route same section as P2; cells as rounded blocks, peel and rise animation; risk high: event element; proof P3; aliases (fixed now, before any reading): stomach lining, stomach wall, cells, cell renewal, cells regenerating, regenerating, peeling, shedding, healing
6. **cierre** (~11.7 s): Así que tu estómago sí se ataca a sí mismo: solo que se repara más rápido de lo que se daña. Envíaselo a ese amigo que se come cualquier cosa sin pensarlo dos veces.
   - What changes in the world: Single reframe image: back out to the whole stomach in x-ray, its inner lining lit in the accent and renewing in waves while the acid churns inside.
   - Transformation: corte de la pared → el estómago entero renovando su revestimiento; camera: retroceso desde la pared hasta el sistema digestivo completo
   - Overlay: ENVÍASELO tag at_word 'envíaselo'

## Staging notes: wardrobe
- No figure on screen.

## Sources and numbers (no number is invented; none is rendered as a source on screen; FLAGGED items are confirmed or removed at the beat sheet)
- Stomach acid is hydrochloric acid secreted by parietal cells; with pepsin it digests protein (meat): standard physiology; TeachMePhysiology 'Mucus production' and 'Gastric acid' (live search 2026-11-11). FLAGGED: add a textbook or Britannica reference at the beat sheet. No pH value is spoken.
- Protection: surface (foveolar) cells secrete a thick mucus gel; bicarbonate trapped in it keeps the cell surface near neutral while the lumen is strongly acidic; tight junctions between cells: TeachMePhysiology 'Mucus production'; IFLScience 'Your stomach juices are so acidic they can digest zinc and meat, so why don't they digest you?' (live search 2026-11-11).
- Renewal: the surface lining is replaced every few days (commonly given as 3-5 days). FLAGGED: only secondary sources were found on 2026-11-11; read a physiology source at the beat sheet. Spoken as 'cada pocos días', no number.
- When the barrier fails the acid damages the wall (peptic ulcer): TeachMePhysiology. Not spoken as a medical claim; the script makes no health advice.
- No number is spoken or rendered in this script.

## Scientific simplifications (stated plainly)
- The wall section is enlarged and reduced to a few layers; the mucus is drawn as a uniform gel and bicarbonate as beads.
- Cell renewal is shown as a row replaced in seconds; it takes days.

## Reuse plan (P12; from code3d/lib/INDEX.md and assets/patterns.md, generated by tools/lib_index.py)
- asset_rig.load (sealed digestive-system) and asset_rig.retint for the x-ray state; voz_rig.skull_material pattern (a Value node blends the base toward the accent) for the lining glow.
- oido_rig.half_pipe and oido_rig.Conveyor (bands riding along a wall, cloned): the model for the cell rows that peel and rise in scene 5.
- manz_rig.cloud / manz_rig.drops (accent beads released from a point): the acid drops and bicarbonate beads; real_kit.wet_tissue for the wall layers; real_kit.water (tinted) for the acid.
- New: the layered wall block, the gel layer, the meat chunk (a stylised material route, no real texture).

## Asset needs
- Asset need: digestive-system: sealed (x-ray state is its brief). No other library asset.

## Blind proofs (P8; `proofs.json` is the spec the B5 proof unit runs)
Every element below that is not a sealed asset in a sealed pose and not a passed pattern in assets/patterns.md has a proof. unchanged gate bar: three isolated readers (tools/blind_read.py), mean confidence >= 60, no reader under 45, aliases exactly as declared here, none added after a guess; every reading counts.
- **P1** scene 2 `meat-dissolving` (element reading): Inside the stomach (its curved wall in frame), a pink-brown meat chunk in glowing acid, its surface frayed into strands.
- **P2** scene 3 `wall-mucus` (element reading): The stomach in x-ray at left, a magnified wall section at right joined by a callout cone; the section shows layers and a thick translucent gel on the inner face.
- **P3** scene 4 `acid-neutralised` (element reading): The P2 section, acid drops entering the gel and fizzing, changing colour halfway down.
- **P4** scene 5 `cells-renewing` (element reading): The P2 section, surface cells darkened and peeling off, new rounded cells pushing up.

## Per-element fallbacks (P9; written before any reading; the production tries them first, rung by rung, within the reading budget)
Rung 3 changes narration only where a line is given; otherwise the narration is unchanged.
- **meat-dissolving (s2)**: rung 1 re-stage: steak cue: fat edge and grain lines. Rung 2: beat rewritten: the chunk shrinks in steps, with the stomach churning around it; narration unchanged. Rung 4 context staging: the whole digestive system with the chunk visible inside the glowing stomach.
- **wall-mucus (s3)**: rung 1 re-stage: curved slice with the organ silhouette behind. Rung 2: beat rewritten: the gel shown spreading over the inside of the whole stomach in x-ray; rung 3 line: 'Lo que la salva es una capa de moco espeso que tapiza todo el estómago por dentro.'. Rung 4 context staging: the stomach in x-ray with the camera passing through its wall into the section.
- **acid-neutralised (s4)**: rung 1 re-stage: fewer, larger drops with bubble trails. Rung 2: beat rewritten: one drop followed from the acid pool to the gel, fizzing out; narration unchanged. Rung 4 context staging: the stomach whole with a magnified circle on the wall showing the fizz.
- **cells-renewing (s5)**: rung 1 re-stage: damaged cells red, new ones in the accent. Rung 2: beat rewritten: the lining shown renewing as a wave travelling over the whole stomach in x-ray; rung 3 line: 'Por eso su revestimiento se renueva cada pocos días.'. Rung 4 context staging: the stomach whole in x-ray with the lining glowing in renewing waves and the section inset.

## Lens record (one Opus session, block B4, 2026-11-11)
- Marketing (lead on topic): curiosity 9/10: Everyone knows the stomach is full of acid; hidden. Title is the query as typed, object word early, one trailing emoji, no hashtags; description line 1 answers in one clause, line 2 the twist, then the share line.
- Scriptwriter: flatness test passed (each scene's event below is a different change in the world; no adjacent pair swaps); the turn comes before the reframe; the closing is one reframe and one 'envíaselo' sentence ending on a behaviour archetype.
  1. hook: a bite drops into the stomach's acid. / 2. acido: a piece of meat comes apart in the acid. / 3. moco: the wall in section; a thick gel spreads over its inner face. / 4. bicarbonato: acid drops fizz and turn neutral inside the gel. / 5. renueva: damaged surface cells peel off and new ones push up (turn). / 6. cierre: the whole stomach, its lining renewing in waves.
- Design: code3d; sealed assets in sealed poses where named, every other element a build or material with a written proof and fallbacks; staging mode checked against the rotation.

## Ledger (one line per event, appended, never rewritten)
- 2026-11-11: script written and stamped by the block B4 creative session (Opus); proofs.json written; record docs/current/reports/b4-2026-11-11.md.

## RETURNED 2026-11-11
CAPABILITY BOUNDARY (redesign session 2026-11-11, lens decision on proof-gate-recommendation-2026-11-11.md section 2): magnified tissue and cellular-scale sections do not read. B5 proofs P1-P4 all failed: readers named 'flying saucer', 'translucent cone', 'dessert bar', 'candy bar' at 15-45; the same family as 012's droplets and 025's seed interior. The mechanism heart (mucus, bicarbonate, lining renewal) lives at that scale, so no staging keeps the promise. Not redesigned; the class is added to the modellability screen.
Replacement: pending a creative session (no eligible developed standby).
