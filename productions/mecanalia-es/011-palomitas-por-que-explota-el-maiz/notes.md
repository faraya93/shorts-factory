# palomitas-por-que-explota-el-maiz (mandarina) — production notes, written by the 2026-11-03 batch run

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Por qué explota un grano de maíz? 🍿
- **Descripción:** Un grano de maíz guarda una gotita de agua: al calentarse se vuelve vapor, la presión sube hasta unas nueve atmósferas y la cáscara cede de golpe. 🍿 Sígueme y envíaselo a ese amigo que cree que el aceite hace explotar el maíz.
  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)
- **Hashtags (description, not title):** #palomitas #maiz #comofunciona #shorts

## Script (7 scenes, family objects) and visual per line
1 olla: ¿Por qué un grano de maíz explota y se vuelve palomita? Muchos creen que lo revienta el aceite caliente, pero el secreto está adentro.  (granos y aceite en una olla sobre el fuego → la cámara se mete dentro de un grano; camera: órbita a la olla y empuje hacia un grano)
2 grano: Dentro de cada grano hay una gotita de agua, rodeada de almidón y de una cáscara dura que no deja escapar nada.  (un grano opaco → se vuelve transparente y muestra su gotita, el almidón y la cáscara; camera: empuje y órbita alrededor del grano)
3 presion: Al calentarse, el agua hierve, pero la cáscara la deja atrapada, y la presión sube y sube.  (una gotita → vapor que se agita y hace subir un manómetro, el grano se hincha; camera: empuje al grano con vibración lenta)
4 cede: Cuando llega a unas nueve atmósferas y unos ciento ochenta grados, la cáscara cede de golpe.  (termómetro y manómetro llegan al límite → la cáscara estalla en fragmentos; camera: plano fijo-vivo con empuje corto y sacudida)
5 espuma: El almidón, ya blando como gel, se expande con el vapor, y se enfría y se endurece al instante, hecho espuma.  (el almidón blando → se infla y se endurece en una espuma blanca irregular; camera: órbita rápida con retroceso)
6 olla-llena: En segundos, el grano duro y pequeño se vuelve una nube blanca, decenas de veces más grande.  (granos pequeños en la olla → palomitas que llenan la olla y la desbordan; camera: retroceso con elevación mientras desborda)
7 cierre: Así que una palomita no es un grano quemado: es un pequeño explosivo de vapor. Sígueme, y envíaselo a ese amigo que cree que el aceite hace explotar el maíz.  (un grano con mecha encendida → estalla en palomita y llena un tazón; camera: órbita amplia con retroceso)
Hook formula: ¿Por qué un grano de maíz explota y se vuelve palomita? | false belief: El aceite caliente es lo que revienta el grano. | reframe: Una palomita no es un grano quemado: es un pequeño explosivo de vapor. | share archetype: el amigo que cree que el aceite hace explotar el maíz

## Identity
- Preset: **mandarina**. Departure from Coral: the MANDARINA orange stage (#FF9A4A -> #F26A1D), a hot-kitchen mood, with the dark ink plinth #1B1410; supports are a dark roasted brown #4A2F26 (cream merged with the cream popcorn); accent blue #1B3BD6 (flames, dial) with emission_gain tuned to 0.1.
- Support colours: {"board": "#4A2F26", "plate": "#4A2F26"}: Mandarina's cream supports merged with the cream popcorn foam, so the supports are a dark roasted brown derived from the preset's ink plinth #1B1410; the popcorn stays cream, the kernel a deep gold.

## Lens decisions
- Marketing: objects family, "¿Por qué…?" on a snack everybody has made, the false belief ("the hot oil bursts it") in the hook; two numbers carried by overlays (9 atm, 180 °C); the reframe renames the popcorn (a small steam explosive).
- Design: seven set pieces with a transformation arc of the same kernel (opaque kernel, x-ray layers, pressure, shatter, foam, a pot that overflows, a lit fuse that pops into a bucket); heavy motion in every scene (jitter, shards, steam, camera dive into the kernel).

## Sources and numbers (no number is invented; none is rendered as a source on screen)
- Popping at ~180 °C and ~9 atm: Virot & Ponomarenko 2015 (J. R. Soc. Interface); kernel moisture ~14 %; the hull is nearly moisture-tight; the starch gelatinises and then sets as foam; volume expands tens of times (spoken "decenas de veces").

## Scientific simplifications and deviations (stated plainly)
- The hull shatters into shards in the drawing; in reality it ruptures at a weak point and the kernel flips. Gel to foam is shown as a quick colour-and-size swap.
- The pot is a solid cylinder with a flat oil disc (no liquid simulation); steam is a cloud of balls; 44 kernels pop one after another with randomised timing.

## Build log
