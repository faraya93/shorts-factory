# que-pasaria-si-te-cae-un-rayo-dentro-de-un-auto: production notes (developed script, 2026-11-11)

Status: DEVELOPED SCRIPT ON FILE (developed set of the 2026-11-11 creative session; lens-decisions row "Developed set 019-024"). Nothing modelled, rendered, queued or published. The production proceeds FROM THIS SCRIPT (produce skill step 1), starting at step 3 (render-cost classes) and the beat sheet; the script may change only through the Reshape ladder, logged here and in lens-decisions.

## Publish package draft (Spanish; the owner publishes)
- **Título:** ¿Qué pasaría si te cae un rayo dentro de un auto? ⚡
- **Descripción:**
  ¿Qué pasaría si te cae un rayo dentro de un auto? Te salva la carrocería de metal, que lleva la corriente por fuera, no los neumáticos.
  En un descapotable, en cambio, esa caja ya no existe. ⚡
  Envíaselo a ese amigo que en plena tormenta se baja del auto para correr a su casa.
- **Hashtags (description, not title):** #rayos #tormenta #ciencia #shorts

## Script (7 scenes, family whatif, variant fork, 156 words, ~53.8 s at 2.9 w/s; band 45-60 s)
Hook: ¿Qué pasaría si te cae un rayo mientras vas dentro de un auto? | false belief: Te salvan los neumáticos de goma, porque aíslan el auto del suelo. | turn: Scene 5: the premise changes on the same stage: the roof is gone (a convertible), so the shell can no longer carry the current around the driver. | reframe: Con techo de metal, estás a salvo: te salva la caja, no la goma. | share archetype: ese amigo que en plena tormenta se baja del auto para correr a su casa
Theme / main tension (TOPIC BALANCE): electricity / dangerous.

1. **hook** (~7.2 s): ¿Qué pasaría si te cae un rayo mientras vas dentro de un auto? Dicen que te salvan los neumáticos de goma.
   - What changes in the world: A car drives along a wet road at night under a storm sky; through the windows a driver sits at the wheel; the sky above flickers as charge gathers; tag ¿GOMA? pops beside a tyre.
   - Transformation: auto en marcha bajo la tormenta → el cielo se carga y parpadea sobre él; camera: travelling lateral junto al auto que avanza
   - Overlay: tag ¿GOMA? at 'goma.'
   - Element: car on a wet road at night: route library cartoon-car (sealed, static); road and wet asphalt as a material (no water simulation); driver = human-figure seated (sealed); risk low-medium: the car is sealed; night lighting must keep it readable; aliases (fixed now, before any reading): car, sedan, automobile, auto
2. **golpe** (~6.9 s): El rayo cae sobre el techo, con unos treinta mil amperes. Pero no entra: corre por fuera, por el metal.
   - What changes in the world: The bolt strikes the roof; the car's metal shell lights in the accent and the current sweeps over roof, pillars and doors, while the driver inside stays dark and untouched.
   - Transformation: techo oscuro → el rayo pega y la carrocería entera se enciende por fuera; camera: caída en picado siguiendo el rayo hasta el techo
   - Overlay: counter 30 000 A (mono, from 0) at 'treinta'
   - Element: lightning bolt striking a car: route build: branching emissive bolt in the doctrine's energy language, under the open job `electric-arc` brief (state 'full branching bolt'); library alternatives seen in search only: BlenderKit 'Lightning' (a9fab929, RF); risk medium: an unsealed class; a branching bolt above a car at night is an iconic read; aliases (fixed now, before any reading): lightning, lightning bolt, lightning strike, rayo, thunderbolt
3. **neumaticos** (~7.2 s): ¿Y la goma? Ese rayo ya cruzó kilómetros de aire. Unos centímetros de neumático no lo frenan: salta al suelo igual.
   - What changes in the world: Pull-back from a tyre to the whole bolt reaching up into the cloud base (the kilometres it crossed), then back down: an arc leaps from the rim past the rubber to the wet road; the ¿GOMA? tag takes a red X.
   - Transformation: neumático en primer plano → el arco salta del aro al suelo pasando por encima de la goma; camera: gran retroceso vertical hasta las nubes y descenso rápido a la rueda
   - Overlay: bracket 'km' along the bolt at 'kilómetros'
   - Overlay: mark red X on ¿GOMA? at 'frenan:'
   - Element: arc jumping from a car wheel to the road: route build: short emissive arc (open job `electric-arc`, state 'small arc between two points'); wheel from the sealed cartoon-car; risk medium: the arc must not read as a laser; the wheel and road are the cue; aliases (fixed now, before any reading): lightning, electric arc, spark, electricity, arc
4. **jaula** (~7.2 s): Lo que te protege es la carrocería: una caja de metal que lleva la corriente a su alrededor, como una jaula.
   - What changes in the world: Reveal: the car body turns into a glowing cage of accent lines around the seated driver; the current flows around the cage and drains into the road; the driver stays dark in the middle.
   - Transformation: carrocería normal → se vuelve una jaula de luz que rodea al conductor; camera: órbita completa alrededor del auto
   - Overlay: label JAULA tag at 'jaula.'
   - Element: car shell as a glowing cage around a seated driver: route cartoon-car with an emissive wire overlay (edges of the sealed mesh); driver human-figure seated; risk low-medium; aliases (fixed now, before any reading): car, sedan, automobile, cage, auto
5. **sin_techo** (~4.1 s): Ahora cambia una sola cosa: un auto descapotable, sin techo de metal.
   - What changes in the world: The premise changes on the same stage: the roof slides away and is gone; rain-darkened air now falls straight onto the driver's seat.
   - Transformation: auto con techo → el techo desaparece y el conductor queda al aire; camera: subida en grúa sobre el auto mientras se va el techo
   - Overlay: tag SIN TECHO at 'descapotable,'
   - Element: convertible car with the driver exposed: route cartoon-car with the roof faces removed (a production edit of the sealed mesh: the gate reads the edited car as usual); risk medium: an edited library mesh; a roofless sedan reads as a convertible; aliases (fixed now, before any reading): car, convertible, sedan, automobile, auto
6. **consecuencia** (~5.9 s): El rayo ya no tiene una caja por donde rodearte. El camino más corto pasa por ti.
   - What changes in the world: A second bolt comes down; with no shell, its path turns error-red and heads through the open cabin toward the seat; the beat ends on the red path reaching the seat, with no harm shown.
   - Transformation: segundo rayo → su camino se vuelve rojo y apunta al asiento del conductor; camera: empuje rápido desde arriba hacia el asiento
   - Element: red lightning path into an open car: route same bolt build in the error colour; risk medium; aliases (fixed now, before any reading): lightning, lightning bolt, rayo, lightning strike
7. **cierre** (~15.2 s): Así que, ¿qué pasaría si te cae un rayo dentro de un auto? Con techo de metal, estás a salvo: te salva la caja, no la goma. Envíaselo a ese amigo que en plena tormenta se baja del auto para correr a su casa.
   - What changes in the world: Single reframe image: the roofed car returns, the cage glows once more around the driver and the bolt's current flows around it into the road; the opening question is repeated over it.
   - Transformation: descapotable → vuelve el auto con techo y su jaula se enciende alrededor del conductor; camera: retroceso amplio hasta el auto bajo la tormenta
   - Overlay: ENVÍASELO tag at_word 'envíaselo'

Staging mode: world (proposal for production; the design lens confirms it at the beat sheet). the premise is a car in a storm: the camera rides a wet road at night under the storm, so the bolt has kilometres of sky to cross on screen (the tyres-vs-kilometres beat needs that height); the first `world` production measures its riskiest environment first (format policy).

## Staging notes: wardrobe (human-figure recolour slots fig_skin, fig_shirt, fig_pants, fig_boots)
- One driver throughout (the same person): default outfit (skin #D99E7A, shirt #2973CC blue, pants #2E3347 grey, boots #59331A): a lone figure keeps the recurring character.

## Lens record (one session, 2026-11-11)
- Marketing (lead on topic): curiosity 9/10: The rubber-tyre myth is everywhere; dangerous. Title follows the search rules (question as typed, object word early, one trailing emoji, no hashtags); description line 1 answers in one clause, line 2 the twist, then the share line.
- Scriptwriter: flatness test passed: each scene's 'what changes in the world' is a different event, and no adjacent pair can be swapped without breaking the story; the turn comes before the closing reframe; the closing is one reframe and one 'envíaselo' sentence ending on a behaviour archetype.
- Design: code3d on the asset route; only sealed library assets in sealed poses are prescribed as available (hand-articulated: open, lever, wheel, door, knife, mask, mask_b, crack; human-figure: standing, walking, jumping, falling, seated); every other element is a geometric build, a material, energy graphics, or a library candidate recorded in the audit below with its fallback.

## Sources and numbers (no number is invented; none is rendered as a source on screen; FLAGGED items are confirmed or removed at the beat sheet)
- Hard-topped metal vehicles protect occupants because the metal roof and sides carry the current around them to the ground; rubber tyres provide no protection; convertibles and open vehicles are not safe: US National Weather Service, 'Lightning safety: cars' (weather.gov/safety/lightning-cars) and NWS lightning myths page (verified by live search 2026-11-11).
- Typical flash about 30,000 A and about 300 million volts: NWS 'Lightning power' (weather.gov/safety/lightning-power) and NOAA FAQ (live search 2026-11-11). Narration uses only the amperes.
- 'Kilómetros de aire': a cloud-to-ground channel is several kilometres long. FLAGGED: cite NOAA/NSSL lightning basics at the beat sheet; if not sourced, rung 3 says 'todo el cielo' instead of 'kilómetros de aire' (same word count minus one).
- Current can arc from the vehicle frame to the ground and can damage tyres and electronics: NWS 'Lightning safety: cars' (verified).

## Scientific simplifications (stated plainly)
- The current is drawn as glowing accent lines on the outside of the body; the real current is invisible.
- Arcing to the ground happens through and around the tyres; the arc is drawn past the rubber for legibility.
- NWS also advises not touching metal parts inside the car; the closing's 'estás a salvo' refers to a hard-topped car with the windows closed.

## Modellability audit and pre-written fallbacks (2026-11-11, `docs/current/reports/modellability-audit-019-024.md`)
Ladder fallbacks pre-approved by the scriptwriter, design and marketing lenses in the audit (one session), so a production run applies them WITHOUT stopping when a scene trips its trigger. The script is unchanged until a rung is applied. When one is: update `script.json`, re-run the flatness swap test, log the reshape here and as a row in `lens-decisions.md`. Aliases are fixed in the script above, before any reading; none may be added after a guess.

**Verdict: MODELABLE WITH THE WRITTEN FALLBACKS.** Riskiest element: the lightning bolt (scenes 2, 3, 6), an unsealed class (open job `electric-arc`), and the night `world` environment's render cost (unmeasured).

Routes: Sealed: cartoon-car, human-figure (seated). Builds: road (material), bolt and arcs (emissive branching tubes under the `electric-arc` brief), storm sky (world shader gradient; volumetric clouds avoided for cost), roof removal on the sealed car mesh. Library alternative for the bolt seen in search only: BlenderKit 'Lightning' (a9fab929, RF).

- Bolt (trigger: the bolt fails the gate). Rung 1: thicker trunk with fewer branches, a brighter cloud base above it, and the car lit by the flash (context). Rung 4: the bolt read with the car on the road beneath it.
- Scene 3 arc (trigger: reads as a laser or a stick). Rung 1: the arc branches and the road lights around its foot. Rung 2: the tyre is shown scorched with a short arc, no long jump. Narration unchanged.
- Scene 5 convertible (trigger: the edited mesh breaks, or the roofless car fails the gate). Rung 1: the roof turns transparent and then dissolves, keeping the door line. Rung 2: the premise is staged as the same car seen from above with its roof panel lifted away, the driver visible.
- `world` cost (trigger: the night environment class predicts over 15 s/frame). Format policy: the design lens moves the production to `stage` (the car on the Coral stage under a dark cloud slab), re-checked against the rotation (019-023 would then hold one `world`).

Unresolved fallbacks: none. Batch: cleared for the 2026-11-11 batch.
