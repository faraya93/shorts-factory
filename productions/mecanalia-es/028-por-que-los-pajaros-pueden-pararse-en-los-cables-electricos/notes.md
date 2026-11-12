# por-que-los-pajaros-pueden-pararse-en-los-cables-electricos: production notes (developed script, block B4 creative session 2026-11-11)

Status: DEVELOPED SCRIPT ON FILE (stamped; block B4, re-stamped by the redesign session 2026-11-11). A1 (pigeon seal), P2-P5 at design round 2 and A2 (eagle seal, new) pending one braked proof unit (a round-2 failure returns the unit); W1 and P1 passed. Not batch-eligible until every proof in `proofs.json` has passed (doctrine-topics-and-scripts.md "Blind proofs before batch eligibility"). Sections below that describe the bird asset and the proofs describe round 1; `proofs.json` and the ledger govern. Nothing modelled, rendered, queued or published. A production proceeds FROM THIS SCRIPT; it changes it only through the Reshape ladder, logged in the ledger below.
Staging mode: world. A street at dusk modelled as an environment (sky gradient, a row of poles, three wires in catenary curves, a rooftop line); the camera travels along the wire with the current. First `world` production: its riskiest environment frame is timed first (W1). Rotation: 024 cutaway, 026 and 027 stage; world keeps every window at three or fewer of one mode.

## Publish package draft (Spanish; the owner publishes)
- **Título:** ¿Por qué los pájaros pueden pararse en los cables eléctricos? 🐦
- **Descripción:**
  ¿Por qué los pájaros pueden pararse en los cables eléctricos? Porque sus dos patas están en el mismo cable, al mismo voltaje.
  Si tocan el cable y el poste a la vez, la corriente sí los cruza. 🐦
  Envíaselo a ese amigo que cambia un enchufe sin cortar la luz.
- **Hashtags (description, not title):** #electricidad #pajaros #ciencia #shorts

## Script (6 scenes, family objects, variant journey, 167 words, ~57.6 s at 2.9 w/s; band 45-60 s)
Hook: ¿Por qué los pájaros pueden pararse en los cables eléctricos sin electrocutarse? | false belief: Sus patas los aíslan de la electricidad. | turn: Scene 5: a bird that touches two things at once, the wire and the pole, opens a path through its body, which is why big birds are the ones electrocuted. | reframe: Al pájaro no lo salvan sus patas: lo salva tocar un solo cable. | share archetype: ese amigo que cambia un enchufe sin cortar la luz
Theme / main tension (TOPIC BALANCE): electricity / dangerous.

1. **hook** (~7.9 s): ¿Por qué los pájaros pueden pararse en los cables eléctricos sin electrocutarse? Casi todos creen que sus patas los aíslan de la electricidad.
   - What changes in the world: A street at dusk: a small bird glides in and lands on the middle wire between two poles; the wire bounces under it; the tag ¿PATAS AISLANTES? appears by its feet.
   - Transformation: cable vacío → un pájaro aterriza encima; camera: seguimiento del pájaro en vuelo hasta que se posa, y acercamiento a las patas
   - Overlay: tag ¿PATAS AISLANTES? at 'aíslan'
   - Element `bird-on-wire` (object): a small bird perched on a power line; route library bird (open job; perched-on-a-wire state) on a geometric wire between poles; risk medium-high: the hero is an unsealed asset; the wire and poles are the context cue; proof P1; aliases (fixed now, before any reading): bird, bird on a wire, bird on a power line, sparrow, pigeon, swallow, songbird, pájaro, ave
2. **viaje** (~8.6 s): Sigamos a la electricidad. Viaja por el cobre del cable, empujada por la diferencia de voltaje entre un extremo de la línea y el otro.
   - What changes in the world: The camera drops onto the wire far down the line: accent pulses race along the copper toward the bird, passing pole after pole; at the far end of the line a high glow, at the other a low one.
   - Transformation: cable apagado → pulsos de corriente que corren por él hacia el pájaro; camera: travelling rasante a lo largo del cable, acompañando los pulsos
   - Overlay: label VOLTAJE tag at 'voltaje'
   - Element `current-on-wire` (event): electric current flowing along a power line; route emissive accent pulses travelling inside a semi-transparent wire jacket; poles in frame; risk medium-high: readers may name only 'power lines'; the pulses are the event; proof P2; aliases (fixed now, before any reading): electricity, electric current, current, electrical current, electricity flowing, current flowing, flowing electricity, electrified power line, electrified wire, electricidad, corriente
3. **patas** (~6.2 s): Al llegar al pájaro, podría desviarse: subir por una pata, cruzar su cuerpo y bajar por la otra.
   - What changes in the world: The pulses reach the bird's feet and slow; a dotted ghost path draws up one leg, through the body and down the other leg, as if offering the current a detour.
   - Transformation: corriente bajo las patas → aparece el posible desvío por el cuerpo del pájaro; camera: empuje a las patas y subida por el cuerpo del pájaro
   - Element `bird-detour` (object): bird on a wire with a dotted path through its legs and body; route bird asset + dotted accent curve; the bird stays in its sealed perched state; risk medium: proof P1 covers the bird on the wire; the dotted path is an annotation; aliases (fixed now, before any reading): bird, bird on a wire, bird on a power line, sparrow, songbird, pájaro
4. **mismo** (~11.4 s): Pero no lo hace: sus dos patas están en el mismo cable, al mismo voltaje. Sin diferencia entre ellas, nada empuja la corriente por el pájaro, y sigue de largo por el cobre.
   - What changes in the world: Both feet light in the same accent shade; the ghost path fades out; the pulses pass under the feet without slowing and race on down the line; the bird preens, unbothered.
   - Transformation: posible desvío → la corriente pasa de largo bajo las patas; camera: travelling lateral que deja al pájaro atrás siguiendo los pulsos
   - Overlay: label = between the two feet at 'mismo'
   - Element `current-past-bird` (event): current passing under a bird on a wire; route same staging as P2 with the bird in frame; risk medium: proof P2; aliases (fixed now, before any reading): bird on a wire, bird on a power line, bird, electricity, electric current, current flowing, electricity flowing, pájaro
5. **poste** (~14.1 s): El peligro es tocar dos cosas a la vez, como el cable y el poste. Ahí sí hay diferencia, y la corriente cruza el cuerpo. Por eso las aves grandes, que alcanzan con las alas, son las que más mueren electrocutadas.
   - What changes in the world: The turn: the camera pulls back along the whole line to a pole top; a large bird lands on the crossarm and spreads its wings, one wingtip touching the wire; a red path lights from the wire through the wing and body down into the pole; an error-red X closes over it before anything else happens.
   - Transformation: pájaro chico a salvo → un ave grande toca cable y poste y la corriente la cruza; camera: retroceso a lo largo de toda la línea hasta lo alto del poste
   - Overlay: mark red X at 'electrocutadas'
   - Element `big-bird-pole` (object): a large bird with spread wings on a power pole; route library bird (flying, wings spread state, scaled up) on a geometric pole crossarm; red emissive path; risk high: a scaled songbird may not read as a large bird; the pole and wire are the cue; proof P4; aliases (fixed now, before any reading): bird, large bird, eagle, hawk, bird of prey, bird on a power pole, bird on a utility pole, bird with spread wings, pájaro, ave, águila
6. **cierre** (~9.3 s): Así que al pájaro no lo salvan sus patas: lo salva tocar un solo cable. Envíaselo a ese amigo que cambia un enchufe sin cortar la luz.
   - What changes in the world: Single reframe image: back on the middle wire, the small bird sits with both feet lit the same shade while the pulses stream under it; the camera rises to show the whole street of poles and wires, every bird on a single wire.
   - Transformation: un pájaro en el cable → la calle entera con pájaros a salvo en sus cables; camera: subida desde el pájaro hasta la calle entera
   - Overlay: ENVÍASELO tag at_word 'envíaselo'

## Staging notes: wardrobe
- No human figure on screen.

## Sources and numbers (no number is invented; none is rendered as a source on screen; FLAGGED items are confirmed or removed at the beat sheet)
- Mechanism: a bird on one wire has both feet at essentially the same potential, so there is no voltage across its body and no current through it; the current stays in the conductor. Danger comes when the body bridges two points at different potential (two conductors, or a conductor and a grounded pole). Indiana Public Media 'A Moment of Science: Bird on a wire'; MIT Alumni Association explainer (live search 2026-11-11). FLAGGED: add one utility or textbook reference at the beat sheet.
- Large birds (raptors: eagles, hawks, owls) are the ones most often electrocuted, because their wingspan can bridge a conductor and a pole or two conductors; utilities fit raptor-safe poles. SciShow summary (live search 2026-11-11). FLAGGED: cite the Avian Power Line Interaction Committee (APLIC), 'Suggested Practices for Avian Protection on Power Lines' (2006), at the beat sheet; if it cannot be read, scene 5's last sentence becomes 'Por eso las aves grandes corren más peligro', with the same staging.
- No number is spoken or rendered in this script.

## Scientific simplifications (stated plainly)
- Current is drawn as pulses moving along the wire; the electrons drift slowly and the energy travels in the field. The 'detour' path is an annotation, not a physical path that current 'tries'.
- Both feet are shown at exactly the same potential; in reality the short stretch of wire between them has a tiny voltage drop, far too small to matter.
- The pole is shown as grounded wood/metal for clarity; real crossarm hardware varies.

## Reuse plan (P12; from code3d/lib/INDEX.md and assets/patterns.md, generated by tools/lib_index.py)
- corr_rig.aura / micro_rig.beads (accent beads driven by fn(i, t)): the current pulses along the wire; micro_rig.glow_mat for the translucent accent wire jacket.
- real_kit.tube (tube along points, radius per point, grow): the wires as catenaries and the dotted detour path; real_kit.steel for hardware.
- setpiece.Shot primitives (cyl, box) for poles and crossarms; paper_rig.clouds and paper_rig.Sky (stage-to-dusk blend) as the start of the sky.
- voz_rig.zigzag NOT reused: the danger path is a smooth red tube, not an arc (the arc is the measured failure class of 020, 022 and 023).
- New: the street environment (a rooftop line, poles in perspective), the bird placement on the wire. The bird is the library asset bird (open job, A1).

## Asset needs
- Asset need: bird: open job (in_progress), states 'perched on a wire' and 'flying, wings spread'; sealed by the B5 proof unit before P1 (A1).

## Blind proofs (P8; `proofs.json` is the spec the B5 proof unit runs)
Every element below that is not a sealed asset in a sealed pose and not a passed pattern in assets/patterns.md has a proof. unchanged gate bar: three isolated readers (tools/blind_read.py), mean confidence >= 60, no reader under 45, aliases exactly as declared here, none added after a guess; every reading counts.
- **A1** scene 1 `bird` (asset seal): ASSET SEAL: finish assets/library/bird in both brief states (perched; flying, wings spread), isolated blind naming with factory/asset_library.py.
- **W1** scene 2 `world-environment` (render-cost measurement): RENDER-COST MEASUREMENT, not a reading: the scene-2 frame (wire close, poles receding, sky) rendered once at the final profile at 75%; record s/frame and assign render_cost_class under docs/current/specs/render-cost-playbook.md.
- **P1** scene 1 `bird-on-wire` (element reading): The perched bird on the middle wire, two poles in frame, dusk sky, camera slightly below the wire.
- **P2** scene 2 `current-on-wire` (element reading): Low along the wire, three accent pulses inside a translucent jacket racing toward camera, poles receding.
- **P3** scene 3 `bird-detour` (element reading): The bird on the wire, a dotted accent path up one leg, through the body and down the other.
- **P4** scene 4 `current-past-bird` (element reading): The bird on the wire, both feet lit the same shade, pulses passing under the feet.
- **P5** scene 5 `big-bird-pole` (element reading): The bird asset in its wings-spread state, scaled large, on a pole crossarm, one wingtip on the wire, a red path through wing and body into the pole.

## Per-element fallbacks (P9; written before any reading; the production tries them first, rung by rung, within the reading budget)
Rung 3 changes narration only where a line is given; otherwise the narration is unchanged.
- **bird-on-wire (s1)**: rung 1 re-stage: closer, one pole and crossarm behind. Rung 2: beat rewritten: a row of birds already on the wire, the new one landing among them; narration unchanged. Rung 4 context staging: the whole street with birds on every wire, camera then pushing to one.
- **current-on-wire (s2)**: rung 1 re-stage: brighter pulses with streaks, opaque jacket with a window. Rung 2: beat rewritten: the current shown as a glow sweeping along the whole line from the far pole; narration unchanged. Rung 4 context staging: the street at night, the wire alone lit, the poles silhouetted.
- **bird-detour (s3)**: rung 1 re-stage: path drawn outside the body as an arching arrow. Rung 2: beat rewritten: the detour shown as a fork in the glow at the feet; rung 3 line: 'podría desviarse por sus patas y cruzarle el cuerpo'. Rung 4 context staging: the bird and the wire seen from below, the path against the sky.
- **current-past-bird (s4)**: rung 1 re-stage: bird in background, pulses large in foreground. Rung 2: beat rewritten: two '=' marks on the feet, then the pulses pass; narration unchanged. Rung 4 context staging: the street wide, the bird small, the pulses running the whole line under it.
- **big-bird-pole (s5)**: rung 1 re-stage: darker raptor recolour, side view. Rung 2: beat rewritten: the SAME small bird stretches toward the next wire and the path lights the moment its wing touches (no large bird); rung 3 line: 'El peligro es tocar dos cosas a la vez, como dos cables o el cable y el poste. Por eso las aves grandes, que alcanzan con las alas, son las que más mueren electrocutadas.'. Rung 4 context staging: the pole top wide with the crossarm hardware and a large bird landing on it.

## Lens record (one Opus session, block B4, 2026-11-11)
- Marketing (lead on topic): curiosity 9/10: Seen daily in every city of every country; the insulating-feet explanation is the one everyone gives. Title is the query as typed, object word early, one trailing emoji, no hashtags; description line 1 answers in one clause, line 2 the twist, then the share line.
- Scriptwriter: flatness test passed (each scene's event below is a different change in the world; no adjacent pair swaps); the turn comes before the reframe; the closing is one reframe and one 'envíaselo' sentence ending on a behaviour archetype.
  1. hook: a bird lands on an empty wire. / 2. viaje: current pulses race along the wire toward the bird. / 3. patas: the pulses reach the feet and a dotted detour through the bird appears. / 4. mismo: both feet light the same shade, the detour fades and the pulses pass under the bird. / 5. poste: a large bird on the pole spreads its wings onto the wire and a red path crosses its body (turn). / 6. cierre: the whole street, every bird safe on a single wire.
- Design: code3d; sealed assets in sealed poses where named, every other element a build or material with a written proof and fallbacks; staging mode checked against the rotation.

## Ledger (one line per event, appended, never rewritten)
- 2026-11-11: script written and stamped by the block B4 creative session (Opus); proofs.json written; record docs/current/reports/b4-2026-11-11.md.
- 2026-11-11 (redesign session, Opus; rung: none, pre-production proof round 2): A1 becomes the species-level job assets/library/pigeon (declaration error recorded, no alias added to the bird job); new asset job eagle and seal proof A2 for scene 5; P2 gates the power line (opaque cables) with current as a cue; P3/P4 read the pigeon under the unit's one alias set 'pigeon' (as P1 declared before any reading); current is not a gated element anywhere (capability boundary). library_assets now pigeon, eagle; script re-stamped, narration unchanged. Stop-loss: a round-2 failure returns the unit.

## Earlier stub (kept verbatim)
# 028-por-que-los-pajaros-pueden-pararse-en-los-cables-electricos: production notes

Status: DRAWN from the banked tier (rank 6, replacement for returned 025, 2026-11-11). No script yet: written at production time under the standing flatness check. Topic: objects, journey, theme electricity, main tension dangerous. Hook and hero route: docs/current/idea-bank.md rank 6.
