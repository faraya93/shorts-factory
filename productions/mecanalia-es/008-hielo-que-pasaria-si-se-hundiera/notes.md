# hielo-que-pasaria-si-se-hundiera (fucsia) — production notes, written by the 2026-11-03 batch run

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Qué pasaría si el hielo se hundiera? 🧊
- **Descripción:** El agua es rara: al congelarse ocupa cerca de un 9 % más de espacio, por eso el hielo flota y forma una tapa sobre los lagos. Si se hundiera, se congelarían de abajo hacia arriba. 🧊 Sígueme, y envíaselo a ese amigo que siempre saca el hielo del vaso con la mano.
  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)
- **Hashtags (description, not title):** #hielo #agua #quepasaria #shorts

## Script (6 scenes, family whatif) and visual per line
1 flota: ¿Qué pasaría si el hielo se hundiera en lugar de flotar? Hoy flota, y esa pequeña rareza sostiene la vida en los lagos.  (un vaso de agua con tres cubos de hielo reales que flotan, asomando por encima del agua; camera: órbita lenta alrededor del vaso)
2 nueve: El agua es rara: al congelarse ocupa cerca de un nueve por ciento más de espacio, y por eso el hielo pesa menos y sube.  (un vaso de agua se congela de abajo hacia arriba y crece por encima de la marca → en otro vaso, cubos de hielo suben y flotan; camera: empuje al vaso que se congela, luego paneo hacia el segundo vaso y retroceso)
3 hunde: Imagina que no: cada cubo cae al fondo y se apila, uno encima de otro, hasta llenar el vaso de abajo hacia arriba.  (un vaso de agua → seis cubos caen al fondo y se apilan hasta llenarlo; camera: órbita descendente siguiendo la caída)
4 lago: En un lago pasaría igual: el invierno lo congelaría desde el fondo, y el sol de verano solo derretiría la capa de arriba.  (un lago en corte, agua líquida → el hielo crece desde el fondo; el sol solo derrite la capa de arriba; camera: travelling lateral y cenital)
5 tapa: Así que, ¿qué pasaría si el hielo se hundiera? Los lagos serían bloques de hielo, sin vida debajo.  (dos lagos en corte lado a lado: con tapa de hielo flotante → bloque de hielo hasta el fondo; camera: retroceso que revela los dos lagos)
6 cierre: No es solo hielo que flota: es una tapa que protege el agua de abajo. Sígueme, y envíaselo a ese amigo que siempre saca el hielo del vaso con la mano.  (el vaso con una tapa de hielo flotando sobre el agua, en una sola imagen; camera: retroceso amplio)
Hook formula: ¿Qué pasaría si el hielo se hundiera en lugar de flotar? | false belief: (none: numbers/what-if) | reframe: No es solo hielo que flota: es una tapa que protege el agua de abajo. | share archetype: ese amigo que siempre saca el hielo del vaso con la mano

## Identity
- Preset: **fucsia**. Departure from Coral: FUCSIA stage (deep magenta, cream plinth, mint accent). Reason: pale-cyan translucent ice needs a deep, saturated stage for value separation; the mint accent keeps the 'cold' reading. The rejected 008 used cobalt, where ice and water disappeared.
- Support colours: {"board": "#FFF3E0", "plate": "#FFF3E0"}: Fucsia defaults. Clear materials (glass, water, ice) are classed `other` by the gate (they inherit the stage by refraction); their legibility is carried by the extended likeness gate.

## Lens decisions
- Design (lead): every element is a refracting material; the blue box of the first version is gone. New: a `transparent` render profile, measured at roughly 7-25 s per 1080x1920 still at 24-48 samples; clear materials sit in the gate's unmeasured class and are judged by blind naming.
- Scriptwriter: the fork structure is kept (normal world, why, changed premise, escalation, opening question, reframe); freezing is now acted by a front inside one volume, and the lake has a sun that only melts the top.
- Marketing: same hook and archetype; the real-ice close-ups are the first-second hook.

## Sources and numbers (no number is invented; none is rendered as a source on screen)
- Water expands about 9 % in volume on freezing (ice density about 917 kg/m3 vs 1000 kg/m3 for water at 0 C), so ice floats. Standard physical reference values. Rounded.
- Consequence claim: lakes freezing from the bottom up if ice sank is the standard textbook thought experiment (insulating ice lid on real lakes); it is a hypothetical, stated as such ('pasaría').

## Scientific simplifications and deviations (stated plainly)
- Real refraction, but the motion (freezing front, sinking, stacking) is keyframed, not simulated.
- The water level does not rise as cubes are added in the sinking beat (displacement ignored).
- The lake is a glass box of water: no ecology is drawn.
- Freezing is a front that swaps the water material for the ice material along the height of one volume.

## Build log
- SKIPPED 2026-11-05 (unattended run): the extended likeness gate blocks scene 2, so no final render was made. Scenes 1, 3, 4, 5, 6 passed blind naming (scene 1: 92/80, 3: 85/85, 4: 85/70 on the cube-pile version, 5: 90/85, 6: 85/85); their stills show real refracting glass, water and ice cubes.
- Scene 2 (water freezes and expands 9 %): five reader rounds across four stagings (a measuring glass with a freezing front; a tumbler with the front; the tumbler plus a second glass of rising cubes, twice). Readers name the glass and pink liquid (70-88) but call the frozen mass 'frosted glass' or 'ice-like texture' at 25-55, below the floor of 60. The frozen glass of water reads as frosted glass, not ice.
- Earlier rounds on scenes 4 and 5 failed (15/25 and 35/50) while the ice was a smooth slab or a cloudy block (read as mist); replacing it by piles of real cubes took both to 70-90. That is the likely fix for scene 2 too: show the 9 % growth with cubes (a tray of cubes standing above the mark) instead of a freezing front.
- Everything needed to resume exists: scene scripts hielo2_01..06, real_kit.py (freezing front, ice cube, tumbler), scenes.json with scene_elements, narration audio. To resume: restage scene 2 with cubes, `gate.py run`, `gate.py stills`, blind-name, then tools/chain_render2.sh. Note the gate records of the other scenes go stale whenever real_kit.py changes; re-name them.
