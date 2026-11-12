# por-que-se-hundio-el-titanic-si-decian-que-era-insumergible: production notes (developed script, block B4 creative session 2026-11-11)

Status: DEVELOPED SCRIPT ON FILE (stamped; block B4, re-stamped by the redesign session 2026-11-11). Proofs P1, P4, P5 at design round 2 (pending one braked proof unit; a round-2 failure returns the unit); P2, P3, P6, P7 passed. Not batch-eligible until every proof in `proofs.json` has passed (doctrine-topics-and-scripts.md "Blind proofs before batch eligibility"). The "Blind proofs" and "Per-element fallbacks" sections below describe round 1; `proofs.json` and the ledger govern. Nothing modelled, rendered, queued or published. A production proceeds FROM THIS SCRIPT; it changes it only through the Reshape ladder, logged in the ledger below.
Staging mode: stage. The liner on a sea slab on the Coral stage, the hull turning x-ray for the compartments; cutaway is excluded by rotation (019, 022, 024 are cutaway: a cutaway 026 would make four in 019-026), and world is not needed for a story told inside one hull.

## Publish package draft (Spanish; the owner publishes)
- **Título:** ¿Por qué se hundió el Titanic si decían que era insumergible? 🚢
- **Descripción:**
  ¿Por qué se hundió el Titanic si decían que era insumergible? No fue un agujero gigante: el iceberg dejó unas rendijas finas.
  Las paredes de adentro no llegaban hasta arriba, y el agua se desbordó de un compartimento al siguiente. 🚢
  Envíaselo a ese amigo que lleva la cubeta de hielo llena hasta el borde.
- **Hashtags (description, not title):** #titanic #historia #barcos #shorts

## Script (7 scenes, family objects, variant story, 198 words, ~68.3 s at 2.9 w/s; band 55-75 s)
Hook: ¿Por qué se hundió el Titanic si decían que era insumergible? | false belief: El iceberg le abrió un agujero gigante en el casco. | turn: Scene 5: the walls between the compartments did not reach the top, so as the bow went down the water spilled over each wall into the next compartment. | reframe: Al Titanic no lo hundió un agujero gigante: lo hundieron unas paredes sin techo. | share archetype: ese amigo que lleva la cubeta de hielo llena hasta el borde
Theme / main tension (TOPIC BALANCE): shipwrecks / dangerous.

1. **hook** (~8.6 s): ¿Por qué se hundió el Titanic si decían que era insumergible? Casi todos creen que el iceberg le abrió un agujero gigante en el casco.
   - What changes in the world: Night on the stage: the liner steams across the sea slab, smoke trailing from its funnels; a faceted iceberg slides in ahead of the bow; the tag ¿AGUJERO GIGANTE? hangs over the bow.
   - Transformation: barco navegando tranquilo → aparece el iceberg delante de la proa; camera: travelling lateral junto al barco, de popa a proa
   - Overlay: tag ¿AGUJERO GIGANTE? at 'agujero'
   - Element `liner-at-sea` (object): ocean liner afloat at sea; route library ocean-liner (sealed, titanic_rig.Liner) on a sea slab; risk low: sealed asset, read 88/90/90 alone; the sea slab is new context; aliases (fixed now, before any reading): ship, ocean liner, liner, passenger ship, steamship, cruise ship, titanic, barco, transatlántico
   - Element `iceberg` (object): iceberg ahead of a ship; route build: faceted low-poly ice mass, pale blue-white, most of it below the sea slab (seen through the translucent sea); risk medium: unsealed; proof P1; aliases (fixed now, before any reading): iceberg, ice, glacier, iceberg and ship, ship and iceberg, iceberg ahead of a ship
2. **diseno** (~7.6 s): Sus constructores lo habían pensado: quince paredes de acero partían el casco en dieciséis compartimentos. Con los cuatro primeros inundados, seguía flotando.
   - What changes in the world: The hull turns x-ray: fifteen steel walls rise one by one across it and split it into sixteen boxes; then the first four boxes at the bow fill with water and the ship settles a little, still afloat.
   - Transformation: casco hueco → quince paredes lo dividen; cuatro compartimentos se llenan y el barco sigue a flote; camera: órbita alta sobre el casco mientras suben las paredes, y bajada a la línea de flotación
   - Overlay: counter 16 at 'dieciséis'
   - Overlay: chip 4 at 'cuatro'
   - Element `hull-compartments` (object): ship hull divided into compartments by walls (x-ray); route library ocean-liner in an x-ray state: translucent shell, opaque walls and floor (titanic_rig cutaway state re-staged as x-ray, not a sealed pose); risk medium-high: an x-ray hull may read as a 'rack' or 'tray'; the funnels and bow shape are the cue; proof P2; aliases (fixed now, before any reading): ship, ship hull, hull, ocean liner, liner, ship compartments, watertight compartments, ship cross-section, ship cutaway, x-ray ship, barco, casco
3. **choque** (~12.4 s): La noche del catorce de abril de mil novecientos doce, el iceberg solo rozó el costado de la proa. No abrió un agujero: dejó una hilera de rendijas finas que, sumadas, medían como un metro cuadrado.
   - What changes in the world: The iceberg scrapes along the starboard bow; plates buckle and a row of thin bright slits opens one after another along the waterline; a small square (one square metre, to scale) assembles beside the hull from the slits' total area.
   - Transformation: casco intacto → una hilera de rendijas finas a lo largo de la proa; camera: seguimiento rasante del roce, de proa hacia atrás, con un retroceso al final
   - Overlay: chip 1912 at 'doce'
   - Overlay: chip 1 m² at 'cuadrado'
   - Element `iceberg-graze` (event): iceberg scraping the side of a ship; route ocean-liner + iceberg build; slits as emissive accent cuts on the bow plates; risk medium: proof P1 covers the iceberg beside the bow; the scrape is the event; aliases (fixed now, before any reading): iceberg, ship hitting an iceberg, ship and iceberg, iceberg collision, collision, ship scraping an iceberg, scraping, colliding, crashing
4. **cinco** (~9.0 s): Pero las rendijas recorrían la proa, y el agua entró en al menos cinco compartimentos a la vez. Uno más de los que el barco aguantaba.
   - What changes in the world: Inside the x-ray hull, water jets in through the slits and five bow boxes fill together; the fifth box lights in the error colour; the bow starts to dip.
   - Transformation: cuatro compartimentos que aguantaba → cinco llenos, la proa empieza a bajar; camera: empuje dentro del casco a lo largo de los compartimentos de proa
   - Overlay: counter 5 at 'cinco'
   - Overlay: mark red on the fifth compartment at 'uno'
   - Element `bow-flooding` (event): water flooding the front compartments of a ship; route ocean-liner x-ray state; water as a physically based blue material rising in the boxes; risk medium-high: proof P3; aliases (fixed now, before any reading): flooding ship, ship flooding, flooding, sinking ship, sinking, flooded compartments, water flooding a ship, ship filling with water, filling with water, titanic
5. **desborde** (~11.4 s): Y aquí estaba el problema: las paredes no llegaban hasta arriba. Con la proa hundiéndose, el agua pasó por encima de cada una al compartimento siguiente, como en una cubeta de hielo inclinada.
   - What changes in the world: The turn: the bow tilts down; the water in the full bow boxes climbs to the open wall tops and pours over each one into the next box, then the next; beside the ship, an ice-cube tray tilts the same way and spills cube to cube.
   - Transformation: agua contenida en la proa → se desborda por encima de cada pared hacia atrás; camera: travelling a lo largo de los bordes de las paredes, siguiendo el agua de un compartimento al siguiente
   - Overlay: label SIN TECHO tag with leader to a wall top at 'arriba'
   - Element `bulkhead-spill` (event): water spilling over the walls inside a tilted ship; route ocean-liner x-ray state tilted bow-down; water sheets pouring over the wall tops; risk high: the turn of the story and an event element; proof P3; aliases (fixed now, before any reading): water spilling, spilling, overflowing, water overflowing, flooding, flooding ship, sinking ship, sinking, flooded compartments, ship filling with water
   - Element `ice-tray` (object): tilted ice-cube tray spilling water; route build: geometric plastic tray, water material in the cells; risk low-medium: a tray with water reads; secondary element, read with the scene; aliases (fixed now, before any reading): ice cube tray, ice tray, tray, cubeta de hielo
6. **final** (~9.0 s): Uno a uno, los compartimentos se fueron llenando. Dos horas y cuarenta minutos después del choque, el Titanic se hundió, y murieron unas mil quinientas personas.
   - What changes in the world: The boxes fill in order from bow to stern; the stern rises out of the sea slab, the lights on the decks go out, and the whole liner slides under the sea line, leaving the slab's surface empty.
   - Transformation: barco medio inundado → se llena entero y desaparece bajo el mar; camera: retroceso amplio y lento mientras el barco se inclina y se hunde
   - Overlay: chip 2 h 40 min at 'cuarenta'
   - Overlay: counter 1.500 at 'quinientas'
   - Element `liner-sinking` (event): ocean liner sinking stern up; route ocean-liner (sealed) animated down through the sea slab; risk medium: proof P4; aliases (fixed now, before any reading): sinking ship, ship sinking, sinking, titanic sinking, shipwreck, titanic, ship, ocean liner, barco hundiéndose
7. **cierre** (~10.3 s): Así que al Titanic no lo hundió un agujero gigante: lo hundieron unas paredes sin techo. Envíaselo a ese amigo que lleva la cubeta de hielo llena hasta el borde.
   - What changes in the world: Single reframe image: the hull rises back into view as an x-ray, every open wall top lighting in the accent one after another, the row of open tops that did it; the camera pulls back.
   - Transformation: barco hundido → el casco vuelve a aparecer con los bordes abiertos de sus paredes encendidos; camera: retroceso desde los bordes de las paredes hasta el barco entero
   - Overlay: ENVÍASELO tag at_word 'envíaselo'

## Staging notes: wardrobe
- No figure on screen (Historia: people stay off screen; no human-figure staging is needed for this story).

## Sources and numbers (no number is invented; none is rendered as a source on screen; FLAGGED items are confirmed or removed at the beat sheet)
- Sixteen watertight compartments divided by fifteen transverse bulkheads: Encyclopaedia Britannica 'Titanic'; British Wreck Commissioner's Inquiry, testimony of Edward Wilding (titanicinquiry.org).
- Flooding threshold. FLAGGED (confirm the wording at the beat sheet): 'could stay afloat with the first four compartments flooded' (Wikipedia 'RMS Titanic'; Titanic Wiki 'Watertight Bulkheads': afloat with 3 flooded or the forward 4, sinks with 5 or more); the US Senate report gives 'any two main compartments' as the safe case. The narration says 'con los cuatro primeros inundados, seguía flotando', which matches the forward-four case and does not claim any four.
- The walls did not reach the top: US Senate Inquiry report (titanicinquiry.org AmInqRep05): only the first bulkhead reached C deck, several reached D, bulkheads 3-9 ended at E deck, and the non-watertight E deck is why the compartments failed; water spilled over the tops into the next compartment (same report; Britannica).
- The damage: six thin openings along the starboard hull totalling about 12-13 square feet (Deseret News 1997-04-08 'Did small holes in hull doom Titanic', reporting the 1996 sonar survey) or 'one square meter (12 square feet)' (NIST, 'NIST reveals how tiny rivets doomed Titanic vessel'); Wilding's 1912 equivalent opening of 12 square feet (Encyclopedia Titanica, 'Somewhere about 12 square feet'). Spoken as 'como un metro cuadrado'. The slit count is not spoken or shown as a number.
- Compartments breached: 'at least five' (Britannica); six of sixteen in other accounts. Spoken as 'al menos cinco'; 'uno más de los que el barco aguantaba' follows from the forward-four threshold above (FLAGGED with it).
- Collision about 11:40 p.m. on 14 April 1912; sinking about 2:20 a.m. on 15 April: about two hours and forty minutes (British Wreck Commissioner's Inquiry via Live Science 'The Titanic: the true story behind the unsinkable ship'). Spoken as 'dos horas y cuarenta minutos'.
- About 1,500 people died: Encyclopaedia Britannica 'Titanic'. Spoken as 'unas mil quinientas personas'.
- Not used: the survivor count, the lifeboat shortage, the rivet-metallurgy debate and any quotation of the 'unsinkable' wording (separate stories, not this mechanism).

## Scientific simplifications (stated plainly)
- The liner is the stylised library model with no livery or name; the hull is shown as an x-ray with the walls simplified to equal-height open boxes (in reality the walls stopped at E or D deck, the first at C).
- The water in each box keeps a level surface when the ship pitches; the order of filling is staged, not simulated.
- The ice-cube tray is an analogy object beside the ship, not a scale model.

## Historia checks (format policy)
- one complete story: From the design to the sinking and the death toll; the outcome is told (scene 6) before the reframe (scene 7). Not serialized.
- mechanism heart: Remove the mechanism sentences (the walls and compartments, the four-compartment limit, the thin slits, the spill over the wall tops) and only 'it hit an iceberg and sank' remains: the story does not stand without them. PASS.
- people: No person on screen; the builders and the dead are named in narration only.

## Reuse plan (P12; from code3d/lib/INDEX.md and assets/patterns.md, generated by tools/lib_index.py)
- titanic_rig.Liner (hull, deckhouse, funnels; root carries pitch and sink; near hull and lid lift away): the hero in every scene. Re-stage its cutaway state as an x-ray (translucent shell, opaque walls) for scenes 2, 4, 5 and 7; the fifteen walls already exist in the rig.
- titanic_rig.Sea (translucent slab whose top is the waterline) for scenes 1, 3 and 6; titanic_rig.Panels only if a scene keeps the cutaway rather than the x-ray.
- titanic_rig.Iceberg (faceted, big mass below the waterline) for scenes 1 and 3.
- titanic_rig.Mats with hero_colours; real_kit.water for the water in the compartments; real_kit.emissive for the slits and the wall-top accents.
- New: the ice-cube tray (real_kit.slab cells + real_kit.water), the slit row, the one-square-metre tile. Nothing else is new.

## Asset needs
- Asset need: ocean-liner: sealed (code-primitive, blind 88/90/90); no job needed.

## Blind proofs (P8; `proofs.json` is the spec the B5 proof unit runs)
Every element below that is not a sealed asset in a sealed pose and not a passed pattern in assets/patterns.md has a proof. unchanged gate bar: three isolated readers (tools/blind_read.py), mean confidence >= 60, no reader under 45, aliases exactly as declared here, none added after a guess; every reading counts.
- **P1** scene 1 `iceberg` (element reading): The liner on the sea slab seen 3/4 from the bow, the iceberg ahead of it at the waterline, a third of its mass visible below the translucent slab; night stage.
- **P2** scene 2 `hull-compartments` (element reading): The whole liner side-on and slightly high, shell at about 25% opacity, the fifteen walls opaque, funnels and bow kept opaque as the cue.
- **P3** scene 3 `iceberg-graze` (element reading): Low camera along the starboard bow, the iceberg face pressed to the plates, a row of bright slits behind the contact point.
- **P4** scene 4 `bow-flooding` (element reading): x-ray hull, the first five bow boxes filled with blue water, water jets entering through the slits, bow dipped 3 degrees.
- **P5** scene 5 `bulkhead-spill` (element reading): x-ray hull tilted bow-down 8 degrees, water sheets pouring over the open top of the fifth wall into the sixth box; the tray beside it is NOT in this still.
- **P6** scene 6 `liner-sinking` (element reading): Wide: the liner bow-under at 20 degrees, stern rising, half below the sea slab.
- **P7** scene 5 `ice-tray` (element reading): The tilted ice-cube tray alone, water spilling from cell to cell.

## Per-element fallbacks (P9; written before any reading; the production tries them first, rung by rung, within the reading budget)
Rung 3 changes narration only where a line is given; otherwise the narration is unchanged.
- **iceberg (s1)**: rung 1 re-stage: faceted iceberg larger and brighter, its underwater mass dark below the slab (the classic 'tip of the iceberg' read). Rung 2: beat rewritten: the iceberg is seen first, alone, before the liner enters frame; narration unchanged. Rung 4 context staging: the iceberg on a wider sea with the liner's lit portholes approaching from frame edge.
- **hull-compartments (s2)**: rung 1 re-stage: opaque hull with the deck lid lifted away (the rig's cutaway state) instead of the x-ray. Rung 2: beat rewritten: the walls drop into the open hull from above, one by one; rung 3 line: 'quince paredes de acero lo dividían por dentro en dieciséis compartimentos'. Rung 4 context staging: the hull exterior and its funnels whole on the left half of the frame, the opened section on the right.
- **iceberg-graze (s3)**: rung 1 re-stage: pull back: whole bow and iceberg peak in frame, slits glowing. Rung 2: beat rewritten: first the scrape (ice chips falling on the deck), then the slits; narration unchanged. Rung 4 context staging: night sea, whole liner and iceberg side by side, slits as a bright dashed line.
- **bow-flooding (s4)**: rung 1 re-stage: hull exterior with the bow lower in the sea, water visible through the shell. Rung 2: beat rewritten: water level rising inside each of the five boxes in turn; narration unchanged. Rung 4 context staging: the whole liner afloat, bow low, water filling the bow behind a translucent shell.
- **bulkhead-spill (s5)**: rung 1 re-stage: two boxes fill the frame, the falling sheet bright, funnels in frame. Rung 2: beat rewritten: the spill shown from the exterior: the waterline climbing the hull wall by wall; rung 3 line: 'el agua pasaba por encima de cada pared, como en una cubeta de hielo inclinada'. Rung 4 context staging: the whole tilted liner, every box visible, the spill lit in the accent from wall to wall.
- **liner-sinking (s6)**: rung 1 re-stage: steeper angle, stern and propellers high. Rung 2: beat rewritten: the decks' lights go out first, then the slide under; narration unchanged. Rung 4 context staging: the sea surface with the stern alone above it and the last funnel going under.
- **ice-tray (s5)**: rung 1 re-stage: half-frozen cubes in some cells. Rung 2: beat rewritten: the tray tilted over a sink edge. Rung 4 context staging: the tray in a freezer door opening.

## Lens record (one Opus session, block B4, 2026-11-11)
- Marketing (lead on topic): curiosity 10/10: The most famous shipwreck; the 'unsinkable' question is carried by nearly everyone; dangerous. Fame evidence in the bank entry. Title is the query as typed, object word early, one trailing emoji, no hashtags; description line 1 answers in one clause, line 2 the twist, then the share line.
- Scriptwriter: flatness test passed (each scene's event below is a different change in the world; no adjacent pair swaps); the turn comes before the reframe; the closing is one reframe and one 'envíaselo' sentence ending on a behaviour archetype.
  1. hook: the liner sails on and an iceberg appears ahead of its bow. / 2. diseno: fifteen walls rise and split the hull; four bow boxes flood and the ship still floats. / 3. choque: the iceberg scrapes the bow and a row of thin slits opens; their total area forms a one-square-metre tile. / 4. cinco: water floods five bow boxes at once; the fifth lights red and the bow dips. / 5. desborde: the bow tilts and water pours over each open wall top into the next box (turn). / 6. final: the boxes fill to the stern and the liner slides under the sea. / 7. cierre: the hull returns as an x-ray with every open wall top lit.
- Design: code3d; sealed assets in sealed poses where named, every other element a build or material with a written proof and fallbacks; staging mode checked against the rotation.

## Ledger (one line per event, appended, never rewritten)
- 2026-11-11: script written and stamped by the block B4 creative session (Opus); proofs.json written; record docs/current/reports/b4-2026-11-11.md.
- 2026-11-11: the Sonnet-written script and scenes.json of the paused batch session are kept as script-sonnet-2026-11-11.json and scenes-sonnet-2026-11-11.json (records, not inputs); its narration audio and stills moved to build/superseded-sonnet-2026-11-11/; its runner state was reset (tools/run_productions.py --reset) so no session can resume.
- 2026-11-11 (redesign session, Opus; rung: none, pre-production proof round 2): P1 iceberg restaged as the subject of its frame (foreground, night stage); P4 restaged as the flooding compartments close (carrier word 'titanic' dropped from its aliases); scene 5's key element is now the ice tray (P5 reads it in the scene, the hull spill is its echo, no longer declared). Script what_changes for scenes 1, 4, 5 and the scene-1 camera edited, narration unchanged, re-stamped. Stop-loss: a round-2 failure returns the unit. Why: B5 readings (P1 liner named, P4 hull named, P5 water read as glass).

## Earlier stub (kept verbatim)
# 026-por-que-se-hundio-el-titanic-si-decian-que-era-insumergible: production notes

Status: DRAWN from the banked tier (rank 31, replacement for returned 022, 2026-11-11). No script yet: written at production time under the standing flatness check. Topic: objects, story, theme shipwrecks, main tension dangerous. Hook and hero route: docs/current/idea-bank.md rank 31.
