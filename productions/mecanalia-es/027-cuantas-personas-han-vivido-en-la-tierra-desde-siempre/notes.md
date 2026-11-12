# cuantas-personas-han-vivido-en-la-tierra-desde-siempre: production notes (developed script, block B4 creative session 2026-11-11)

Status: DEVELOPED SCRIPT ON FILE (stamped; block B4). Not batch-eligible until every proof in `proofs.json` has passed (doctrine-topics-and-scripts.md "Blind proofs before batch eligibility"). Nothing modelled, rendered, queued or published. A production proceeds FROM THIS SCRIPT; it changes it only through the Reshape ladder, logged in the ledger below.
Staging mode: stage. One figure on the Coral stage, multiplied with a pull-back each step; at globe scale the earth-globe asset sits on the stage. Rotation: 022 and 024 cutaway, 026 stage; a second stage keeps every five-window at three or fewer of one mode.

## Publish package draft (Spanish; the owner publishes)
- **Título:** ¿Cuántas personas han vivido en la Tierra desde siempre? 🌍
- **Descripción:**
  ¿Cuántas personas han vivido en la Tierra desde siempre? Más de cien mil millones, contando desde hace unos doscientos mil años.
  Por cada persona viva hoy, más de doce ya vivieron y murieron. 🌍
  Envíaselo a ese amigo que reenvía datos curiosos sin revisarlos.
- **Hashtags (description, not title):** #poblacion #numeros #historia #shorts

## Script (6 scenes, family numbers, variant scale, 147 words, ~50.7 s at 2.9 w/s; band 50-60 s)
Hook: ¿Cuántas personas han vivido en la Tierra desde siempre? | false belief: Hoy hay más gente viva que todos los muertos de la historia juntos. | turn: Scene 5: the living ring is one of more than thirteen; for every person alive, more than twelve have already lived and died. | reframe: Los vivos no somos la mayoría: somos menos de uno de cada trece. | share archetype: ese amigo que reenvía datos curiosos sin revisarlos
Theme / main tension (TOPIC BALANCE): human population / enormous.

1. **hook** (~8.6 s): ¿Cuántas personas han vivido en la Tierra desde siempre? Se dice que hoy hay más gente viva que todos los muertos de la historia juntos.
   - What changes in the world: One standing figure on the stage, lit in the accent; around it a crowd pops up row by row; the tag ¿MÁS VIVOS QUE MUERTOS? hangs above the crowd.
   - Transformation: una persona sola → una multitud que aparece alrededor; camera: retroceso desde la figura hasta la multitud
   - Overlay: tag ¿MÁS VIVOS QUE MUERTOS? at 'vivos'
   - Element `person` (object): a person standing; route library human-figure, standing pose (sealed asset, sealed pose); risk low; aliases (fixed now, before any reading): person, human, man, woman, figure, human figure, people, crowd, persona
2. **vivos** (~7.2 s): Empecemos por los vivos: somos unos ocho mil millones. En fila, hombro con hombro, daríamos unas cien vueltas a la Tierra.
   - What changes in the world: The crowd forms a single file that runs off the stage; the camera pulls back until the globe sits on the stage and the file wraps it as a glowing accent ring, then a second, third... until a thick band of rings circles it.
   - Transformation: multitud en el escenario → una fila que envuelve la Tierra muchas veces; camera: gran retroceso desde la fila hasta el planeta entero
   - Overlay: counter 8.000.000.000 at 'millones'
   - Overlay: chip ×100 at 'vueltas'
   - Element `ring-of-people` (object): a line of people circling the Earth; route library earth-globe (open job) + human-figure instances along a ring, accent band at globe scale; risk medium-high: at globe scale the figures become a band; the near figures in the first frames are the cue; proof P1; aliases (fixed now, before any reading): earth, planet earth, globe, the earth, world, people around the earth, line of people around the earth, ring of people, planeta, tierra
3. **antes** (~8.3 s): Pero la gente lleva unos doscientos mil años naciendo y muriendo. Los demógrafos sumaron a todos los que nacieron alguna vez, generación tras generación.
   - What changes in the world: Behind the living ring, grey figures appear in waves, generation after generation, each wave standing behind the last, filling the stage outward like rings of a tree; a year counter runs backwards.
   - Transformation: solo los vivos → oleadas grises de todos los que vivieron antes; camera: travelling hacia atrás a través de las oleadas, de los vivos a las más antiguas
   - Overlay: chip 200.000 años at 'doscientos'
   - Element `grey-crowd` (object): waves of grey people behind a coloured crowd; route human-figure instances, grey recolour, rows by instancing (pattern: 016 instanced heaps passed with a reference object in frame); risk medium: a grey crowd may read as statues; proof P2; aliases (fixed now, before any reading): crowd, people, crowd of people, group of people, many people, army, multitud, personas, gente
4. **total** (~10.0 s): La cuenta pasa de cien mil millones de personas. Si cada fila de vivos es una de estas vueltas, los que ya murieron envuelven la Tierra doce veces más.
   - What changes in the world: Back at globe scale: the accent band of the living stays; around it grey bands stack outward, one per eight billion, until more than twelve grey bands surround the single accent one.
   - Transformation: una banda de vivos → más de doce bandas grises alrededor; camera: órbita amplia alrededor del planeta mientras se apilan las bandas
   - Overlay: counter +100.000.000.000 at 'millones'
   - Overlay: counter ×12 at 'doce'
   - Element `rings-stack` (object): the Earth wrapped in many bands; route earth-globe + stacked band instances (accent and grey); risk medium: proof P1 (same staging, more bands); aliases (fixed now, before any reading): earth, planet earth, globe, the earth, world, planet with rings, planeta, tierra
5. **giro** (~7.9 s): O sea, por cada persona viva hoy, hay más de doce que ya vivieron y murieron. Más que un equipo de fútbol completo.
   - What changes in the world: The turn: back down to people scale: one accent figure stands on the stage; twelve grey figures step in around it one by one, lining up like a football team behind its captain.
   - Transformation: una persona viva sola → rodeada por doce que vivieron antes; camera: bajada desde el planeta hasta una sola figura y órbita cerrada
   - Overlay: counter 1 at 'viva'
   - Overlay: counter 12 at 'doce'
   - Element `one-and-twelve` (object): one coloured person surrounded by twelve grey people; route human-figure standing, 13 instances, recolour; risk low-medium: sealed asset and pose; a small group reads as people; proof P2 covers the grey recolour; aliases (fixed now, before any reading): people, group of people, crowd, team, person, figures, personas, gente
6. **cierre** (~8.6 s): Así que los vivos no somos la mayoría: somos menos de uno de cada trece. Envíaselo a ese amigo que reenvía datos curiosos sin revisarlos.
   - What changes in the world: Single reframe image: the camera rises from the thirteen figures back out to the globe, where the one accent band is the thinnest layer of a thick grey shell.
   - Transformation: trece personas → el planeta con una sola banda de color entre todas las grises; camera: retroceso vertical desde las figuras hasta el planeta
   - Overlay: counter 1/13 at 'trece'
   - Overlay: ENVÍASELO tag at_word 'envíaselo'

## Staging notes: wardrobe
- human-figure standing pose only (sealed). The living: fig_shirt in the accent colour. The dead: one neutral grey for fig_skin, fig_shirt, fig_pants and fig_boots (a desaturated figure, no ghost or skeleton imagery).

## Sources and numbers (no number is invented; none is rendered as a source on screen; FLAGGED items are confirmed or removed at the beat sheet)
- People ever born: Population Reference Bureau, 'How Many People Have Ever Lived on Earth?' (Kaneda and Haub): more than 108 billion in the 2019/2020 update (table total 108,760,543,790); about 117 billion in the update dated to the November 2022 data (cited by secondary sources; FLAGGED: read the figure on the PRB page at the beat sheet). The narration says 'pasa de cien mil millones', true under both updates.
- Start of the count: PRB begins its estimate about 190,000 BCE (FLAGGED: confirm the start date in the same PRB article); spoken as 'unos doscientos mil años'.
- Living population about 8 billion: UN World Population Prospects (the 8-billion mark, November 2022).
- Derived, not a source figure: dead per living person = (ever born - living) / living = (108 - 8) / 8 = 12.5 or (117 - 8) / 8 = 13.6, so 'más de doce' holds under both PRB updates; living share = 8/108 = 1/13.5 or 8/117 = 1/14.6, so 'menos de uno de cada trece' holds under both. The 'twelve more times around' line in scene 4 is the same ratio expressed as bands.
- Derived: a file shoulder to shoulder at about 0.5 m per person: 8e9 x 0.5 m = 4 million km; Earth's equatorial circumference 40,075 km; 4,000,000 / 40,075 = about 100 turns. The 0.5 m shoulder width is an assumption, stated here; spoken as 'unas cien vueltas'.

## Scientific simplifications (stated plainly)
- The rings of people are drawn as bands at globe scale; at that scale the figures are not individually visible.
- The dead are shown as grey figures for the count only; every person who ever lived is drawn with the same figure.

## Reuse plan (P12; from code3d/lib/INDEX.md and assets/patterns.md, generated by tools/lib_index.py)
- paper_rig.figure (the sealed human-figure, standing, feet on z, recolour by cols): the unit in every scene; 13 instances in scene 5.
- corr_rig.Person only if a pose blend is wanted (not needed: standing only).
- caca_rig.Pile / mound pattern (one mesh, many units rewritten per frame) as the model for instancing thousands of figures cheaply in scene 3; 016's instanced-heap pattern (patterns.md: a reference object in frame keeps the heap readable).
- paper_rig.Sky (stage to dark blend) for the globe-scale pull-back; paper_rig.stars if the globe needs a space backdrop.
- New: rings of people as bands (a torus band with a figure texture at globe scale), the year counter. The globe is the library asset earth-globe (open job, A1).

## Asset needs
- Asset need: earth-globe: open job (in_progress), sealed by the B5 proof unit before P1 (A1).
- Asset need: human-figure: sealed (standing pose).

## Blind proofs (P8; `proofs.json` is the spec the B5 proof unit runs)
Every element below that is not a sealed asset in a sealed pose and not a passed pattern in assets/patterns.md has a proof. unchanged gate bar: three isolated readers (tools/blind_read.py), mean confidence >= 60, no reader under 45, aliases exactly as declared here, none added after a guess; every reading counts.
- **A1** scene 2 `earth-globe` (asset seal): ASSET SEAL, not an element reading: finish the open job assets/library/earth-globe (state 'whole globe') under asset-system, isolated blind naming with factory/asset_library.py (no context staging for sealing).
- **P1** scene 2 `ring-of-people` (element reading): The globe on the stage, a single file of figures leaving the stage edge in the foreground and wrapping the globe as an accent band; mid pull-back frame.
- **P2** scene 3 `grey-crowd` (element reading): Rows of grey figures behind a front row of accent-shirted figures, filling the stage, camera at head height.
- **P3** scene 4 `rings-stack` (element reading): The globe with one accent band and twelve grey bands stacked outward, 3/4 view.
- **P4** scene 5 `one-and-twelve` (element reading): One accent figure, twelve grey figures in a loose team formation around it, full bodies in frame.

## Per-element fallbacks (P9; written before any reading; the production tries them first, rung by rung, within the reading budget)
Rung 3 changes narration only where a line is given; otherwise the narration is unchanged.
- **ring-of-people (s2)**: rung 1 re-stage: an earlier pull-back frame with near figures large. Rung 2: beat rewritten: the file of people seen running across a map of the world before it wraps the globe; narration unchanged. Rung 4 context staging: the stage with the crowd in the foreground and the globe behind, the file running from one to the other.
- **grey-crowd (s3)**: rung 1 re-stage: warmer light-taupe grey, accent row in front. Rung 2: beat rewritten: generations appear as rows behind a single accent figure, each row slightly greyer; rung 3 line: 'detrás de cada uno de nosotros hay generaciones y generaciones'. Rung 4 context staging: the crowd seen from behind the living row, the grey rows reaching to the horizon.
- **rings-stack (s4)**: rung 1 re-stage: fewer, thicker bands with silhouettes on the nearest. Rung 2: beat rewritten: a balance scale with one accent figure against a heap of twelve grey figures; narration unchanged. Rung 4 context staging: the globe small at frame top, the stage crowd of grey figures below it.
- **one-and-twelve (s5)**: rung 1 re-stage: tighter frame, six grey behind the accent figure. Rung 2: beat rewritten: the twelve grey figures step out from behind the accent one in a line; narration unchanged. Rung 4 context staging: the thirteen figures lined up on a football pitch line drawn on the stage.

## Lens record (one Opus session, block B4, 2026-11-11)
- Marketing (lead on topic): curiosity 9/10: The 'more alive now than ever died' line circulates as a fact and is false; enormous; puts the viewer inside the count. Title is the query as typed, object word early, one trailing emoji, no hashtags; description line 1 answers in one clause, line 2 the twist, then the share line.
- Scriptwriter: flatness test passed (each scene's event below is a different change in the world; no adjacent pair swaps); the turn comes before the reframe; the closing is one reframe and one 'envíaselo' sentence ending on a behaviour archetype.
  1. hook: one figure, then a crowd appears around it. / 2. vivos: the crowd becomes a single file that wraps the globe in a band of about a hundred turns. / 3. antes: waves of grey figures from earlier generations fill in behind the living. / 4. total: grey bands stack around the globe, more than twelve for the single accent band. / 5. giro: one living figure, twelve grey figures step in around it (turn). / 6. cierre: pull-back to the globe: the accent band is the thinnest layer of a grey shell.
- Design: code3d; sealed assets in sealed poses where named, every other element a build or material with a written proof and fallbacks; staging mode checked against the rotation.

## Ledger (one line per event, appended, never rewritten)
- 2026-11-11: script written and stamped by the block B4 creative session (Opus); proofs.json written; record docs/current/reports/b4-2026-11-11.md.

## Earlier stub (kept verbatim)
# 027-cuantas-personas-han-vivido-en-la-tierra-desde-siempre: production notes

Status: DRAWN from the banked tier (rank 32, replacement for returned 023, 2026-11-11). No script yet: written at production time under the standing flatness check. Topic: numbers, scale, theme human population, main tension enormous. Hook and hero route: docs/current/idea-bank.md rank 32.
