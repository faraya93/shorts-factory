# por-que-te-da-la-corriente-al-bajarte-del-auto: production notes (developed script, 2026-11-11)

Status: DEVELOPED SCRIPT ON FILE (developed set of the 2026-11-11 creative session; lens-decisions row "Developed set 019-024"). Nothing modelled, rendered, queued or published. The production proceeds FROM THIS SCRIPT (produce skill step 1), starting at step 3 (render-cost classes) and the beat sheet; the script may change only through the Reshape ladder, logged here and in lens-decisions.

## Publish package draft (Spanish; the owner publishes)
- **Título:** ¿Por qué te da la corriente cuando te bajas del auto? ⚡
- **Descripción:**
  ¿Por qué te da la corriente cuando te bajas del auto? Porque al deslizarte por el asiento te cargas tú, y la carga salta cuando tocas el metal.
  Esa misma chispa, y no el celular, es la que preocupa en una estación de servicio. ⚡
  Envíaselo a ese amigo que cierra la puerta del auto con el codo para que no le dé la corriente.
- **Hashtags (description, not title):** #electricidad #autos #ciencia #shorts

## Script (6 scenes, family objects, variant chain, 156 words, ~53.8 s at 2.9 w/s; band 45-60 s)
Hook: ¿Por qué te da la corriente cuando te bajas del auto? | false belief: El auto acumula electricidad y te la pasa. | turn: Scene 5: that same spark, not the phone, is the real hazard at a filling station (PEI). | reframe: El auto no te da la corriente: se la das tú a él. | share archetype: ese amigo que cierra la puerta del auto con el codo para que no le dé la corriente
Theme / main tension (TOPIC BALANCE): electricity / hidden.

1. **hook** (~9.3 s): ¿Por qué te da la corriente cuando te bajas del auto? Parece que el auto está cargado y te la pasa. Pero la carga la llevas tú.
   - What changes in the world: Contrast, two actors: a person beside a closed car reaches for the door; a spark snaps between hand and door; the tag ¿EL AUTO? hangs over the car, then TÚ lights over the person, whose body glows faintly.
   - Transformation: persona junto al auto → la mano se acerca y salta la chispa; la etiqueta pasa del auto a la persona; camera: órbita baja entre el auto y la persona
   - Overlay: tag ¿EL AUTO? at 'auto'
   - Overlay: tag TÚ at 'tú.'
   - Element: person beside a car: route library human-figure (standing, sealed) + cartoon-car (sealed); risk low; aliases (fixed now, before any reading): person, human figure, figure, mannequin, man, woman, car
2. **asiento** (~9.0 s): Al bajarte, tu ropa se frota contra el asiento y se despegan. Ese roce te roba cargas: el asiento queda con unas y tú con otras.
   - What changes in the world: The person rises from a car seat (seated to standing); where clothes and seat part, the accent glow builds over the body while a faint opposite glow stays on the seat.
   - Transformation: sentado en el asiento → se levanta y el cuerpo se carga de luz al despegarse; camera: travelling lateral bajo, siguiendo al cuerpo al levantarse
   - Element: person getting up from a car seat: route library human-figure, sealed poses seated then standing; car seat from the library (BlenderKit 'Generic Car Seat PL', 823261c4, RF, search result only) or the open job `car-interior`; risk medium: the in-between frames are interpolation; the gate reads the sealed key poses; the seat must read as a CAR seat; aliases (fixed now, before any reading): person, human figure, figure, mannequin, car seat, seat
3. **voltaje** (~5.5 s): Así, tu cuerpo puede llegar a miles de voltios. Ni lo sientes, mientras no toques nada.
   - What changes in the world: The person walks away from the seat toward the car; the glow on the body keeps climbing step by step while nothing happens.
   - Transformation: cuerpo apenas cargado → camina y la carga sube con cada paso; camera: seguimiento de frente que retrocede delante de la persona
   - Overlay: counter 3 000+ V (mono, from 0) at 'miles'
   - Element: person walking, glowing with charge: route library human-figure, sealed pose walking, emissive overlay; risk low (sealed walking 92/90/85); aliases (fixed now, before any reading): person, human figure, figure, mannequin, man, woman
4. **chispa** (~7.9 s): Cuando tu mano se acerca a la puerta de metal, toda esa carga salta de golpe por el aire: esa es la chispa.
   - What changes in the world: Close-up: the hand nears the car door; at a finger's width a spark jumps from the fingertip to the door, and the glow drains out of the body at once.
   - Transformation: mano cargada cerca de la puerta → salta la chispa y el cuerpo se apaga; camera: empuje lento hacia la mano que se acerca a la puerta
   - Overlay: ring dotted at the gap at 'chispa.'
   - Element: hand touching a car door with a spark: route library hand-articulated, sealed pose door; door of the sealed cartoon-car; spark under the open job `electric-arc` brief (state 'single spark'); risk medium: the spark is an unsealed class; the hand and the door are the context; aliases (fixed now, before any reading): spark, static spark, electric spark, static electricity, chispa
5. **giro** (~10.0 s): Esa misma chispa es la que de verdad preocupa en una estación de servicio, no el celular. Por eso piden no volver a subirte al auto mientras cargas combustible.
   - What changes in the world: The turn: the person, at a fuel pump with the nozzle in the car, gets back in and out of the car; the glow builds again, and as the hand returns to the nozzle a small spark jumps; the beat stops at the spark (no fire).
   - Transformation: persona en el surtidor → se sube y se baja del auto y la chispa salta en la manguera; camera: travelling desde el surtidor hasta la mano en la pistola
   - Overlay: tag ¡NO EL CELULAR! at 'celular.'
   - Element: fuel pump with the nozzle in a car: route build: fuel dispenser (box, hose, nozzle; geometric) beside the sealed cartoon-car; person human-figure standing; risk medium-high: no library pump searched; a dispenser box must read as a FUEL pump (hose and nozzle are the cue); aliases (fixed now, before any reading): fuel pump, gas pump, petrol pump, gas station, fuel dispenser, gasoline pump
6. **cierre** (~12.1 s): Así que el auto no te da la corriente: se la das tú a él. Envíaselo a ese amigo que cierra la puerta del auto con el codo para que no le dé la corriente.
   - What changes in the world: Single reframe image: the person glows, touches the door, and the charge visibly flows from the person INTO the car, which flickers once and goes dark.
   - Transformation: persona cargada → la carga pasa de la persona al auto; camera: retroceso desde la mano hasta la persona y el auto enteros
   - Overlay: ENVÍASELO tag at_word 'envíaselo'

Staging mode: stage (proposal for production; the design lens confirms it at the beat sheet). a person, a car seat, a car and a fuel pump are each read best on the clean Coral stage; the charge glow on the figure needs a calm background; it also keeps the rotation (019-023 would otherwise hold three cutaways or three worlds).

## Staging notes: wardrobe (human-figure recolour slots fig_skin, fig_shirt, fig_pants, fig_boots)
- One person throughout (the viewer, the same person in every scene): default outfit (skin #D99E7A, shirt #2973CC blue, pants #2E3347 grey, boots #59331A): a lone figure keeps the recurring character.

## Lens record (one session, 2026-11-11)
- Marketing (lead on topic): curiosity 9/10: A common, startling daily experience; testable today. Title follows the search rules (question as typed, object word early, one trailing emoji, no hashtags); description line 1 answers in one clause, line 2 the twist, then the share line.
- Scriptwriter: flatness test passed: each scene's 'what changes in the world' is a different event, and no adjacent pair can be swapped without breaking the story; the turn comes before the closing reframe; the closing is one reframe and one 'envíaselo' sentence ending on a behaviour archetype.
- Design: code3d on the asset route; only sealed library assets in sealed poses are prescribed as available (hand-articulated: open, lever, wheel, door, knife, mask, mask_b, crack; human-figure: standing, walking, jumping, falling, seated); every other element is a geometric build, a material, energy graphics, or a library candidate recorded in the audit below with its fallback.

## Sources and numbers (no number is invented; none is rendered as a source on screen; FLAGGED items are confirmed or removed at the beat sheet)
- Mechanism: sliding off the seat separates charge between clothing and upholstery; the person carries the charge away; the car is usually not the charged body; touching metal discharges the person: Car Talk community, caraudio.com and electricvehicleforums explainers (informal) and Motor magazine 2000 ESD article (motor.com/magazine/pdfs/072000_07.pdf) (live search 2026-11-11). FLAGGED: add an electrostatics reference at the beat sheet.
- 'Miles de voltios' and the 3,000 V counter: a shock is felt from about 3,000 V (Motor magazine 2000, about 3,000 V; Mike Holt forum 3,000-3,500 V); body voltages after leaving a car of 7,000-21,000 V by fabric were reported in a 1998 UK study cited by a dealership article (FLAGGED: secondary; find the study or keep only '3 000+ V').
- Filling stations: static electricity can ignite fuel vapours at the pump; PEI has documented no incident caused by a mobile phone; documented static fires are mostly linked to re-entering the vehicle during refuelling; PEI advises never re-entering the vehicle while refuelling: Petroleum Equipment Institute 'Stop Static' pages (pei.org) and archived PEI-derived guidance (live search 2026-11-11).

## Scientific simplifications (stated plainly)
- Charge is drawn as a glow on the body; static charge is invisible.
- The filling-station beat stops at the spark: no fire is shown.

## Modellability audit and pre-written fallbacks (2026-11-11, `docs/current/reports/modellability-audit-019-024.md`)
Ladder fallbacks pre-approved by the scriptwriter, design and marketing lenses in the audit (one session), so a production run applies them WITHOUT stopping when a scene trips its trigger. The script is unchanged until a rung is applied. When one is: update `script.json`, re-run the flatness swap test, log the reshape here and as a row in `lens-decisions.md`. Aliases are fixed in the script above, before any reading; none may be added after a guess.

**Verdict: MODELABLE WITH THE WRITTEN FALLBACKS.** Riskiest element: the fuel pump (scene 5): an unsearched build that must read as a fuel pump; also the spark (scenes 4-5), an unsealed class.

Routes: Sealed: human-figure (seated, standing, walking), hand-articulated (door), cartoon-car. Library (search result only): BlenderKit 'Generic Car Seat PL' (823261c4, RF). Builds: fuel dispenser (geometric), spark (emissive, `electric-arc` brief).

- Scene 2 seat (trigger: the seat fails as a car seat). Rung 1: the person rises from the driver's seat seen through the open door frame of the sealed cartoon-car (context). Rung 2: the person slides along the seat in the seated pose and the glow is born on the trousers; narration unchanged.
- Scene 4 spark (trigger: fails). Rung 1: a bright short arc with a flash on the door paint; the hand in its sealed door pose dominates the frame. Rung 4: the spark read with the whole car door and hand in frame.
- Scene 5 pump (trigger: the dispenser fails as a fuel pump). Rung 1: a library pump (search at the asset step, CC0/RF/CC-BY) or a dispenser with a hose, nozzle in the car's filler, and a canopy column (context). Rung 2: the beat is staged at the car's open fuel door with the nozzle in it (the nozzle and filler are the cue), the pump only partly in frame. Rung 3 (if needed): narration 'Esa misma chispa es la que de verdad preocupa mientras cargas combustible, no el celular. Por eso piden no volver a subirte al auto.' (same job, -3 words).

Unresolved fallbacks: none. Batch: cleared for the 2026-11-11 batch.
