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
