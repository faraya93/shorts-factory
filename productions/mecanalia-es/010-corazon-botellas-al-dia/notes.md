# corazon-botellas-al-dia (frambuesa) — production notes, written by the 2026-11-03 batch run

**Rejected by owner, 2026-11-04 — likeness failure, do not publish.** The objects are too abstract and do not resemble their subjects. Not available inventory: this folder, including its `final.mp4` and `publish.json`, stays only as a record.

**Likeness gate calibration (2026-11-04):** subject heart, misnamed by the first; the second saw no single object, naming a heart only if forced. First guesses: "a blue glass flask with two necks on a stand (abstract, glossy 3D render)" (30); "abstract 3D medical/science animation scene (no single object). If forced to one object: a blue glossy anatomical heart" (35). Gate verdict: FAIL with the confidence floor. See docs/current/reports/likeness-calibration.md.

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Cuántas botellas bombea tu corazón al día? 🫀
- **Descripción:** Tu corazón late unas cien mil veces al día y bombea unos siete mil litros de sangre: más de tres mil botellas de dos litros, sin pedirte permiso. 🫀 Sígueme y envíaselo a ese amigo que dice que hoy no ha hecho nada.
  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)
- **Hashtags (description, not title):** #corazon #sangre #curiosidades #shorts

## Script (7 scenes, family numbers) and visual per line
1 botellas: ¿Cuántas botellas de refresco llenarías con la sangre que bombea tu corazón en un solo día? Más de tres mil.  (una bomba que late y llena una botella → miles de botellas llenas en filas; camera: retroceso que revela la multitud de botellas)
2 puno: Tu corazón es un músculo del tamaño de tu puño, y late alrededor de cien mil veces al día, sin pedirte permiso.  (un puño cerrado → junto a la bomba del mismo tamaño que late y deja anillos de cada latido; camera: órbita cercana con empuje)
3 latido: Cada latido empuja unos setenta mililitros de sangre: un par de tragos. Parece poco, pero se suma.  (una vasija vacía → cada latido la llena un poco más; camera: travelling lateral con acercamiento)
4 minuto: En un minuto son unos cinco litros, que es casi toda la sangre de tu cuerpo: da una vuelta completa en cerca de un minuto.  (un circuito vacío → las cuentas dan una vuelta completa mientras un bidón se llena; camera: órbita amplia sobre el circuito)
5 dia: En un día, unos siete mil litros: más de tres mil botellas de dos litros.  (una fila de botellas → un bloque enorme de botellas que crece; camera: retroceso y elevación sobre el bloque)
6 vida: Y en ochenta años, unos doscientos millones de litros, como más de ochenta piscinas olímpicas.  (una piscina → más de ochenta piscinas en cuadrícula; camera: elevación hasta vista cenital)
7 cierre: Así que tu corazón no es solo un órgano que late: es la bomba más constante que tendrás. Sígueme, y envíaselo a ese amigo que dice que hoy no ha hecho nada.  (una persona en el sofá sin hacer nada → la bomba sigue latiendo y llenando botellas a su lado; camera: órbita amplia)
Hook formula: ¿Cuántas botellas de refresco llenarías con la sangre que bombea tu corazón en un solo día? | false belief: (none: numbers/what-if) | reframe: Tu corazón no es solo un órgano que late: es la bomba más constante que tendrás. | share archetype: el amigo que dice que hoy no ha hecho nada

## Identity
- Preset: **frambuesa**. Departure from Coral: the FRAMBUESA raspberry stage (#C21B68 -> #A31256), body-theme colour; cream supports; the pump heart is a deep indigo #1F2F7A (wine and plum tones reflected the raspberry stage and measured only dE 9-18 from it in the gate); mint accent #6BFFD8 with emission_gain tuned to 0.12.
- Support colours: {"board": "#FFF3E0", "plate": "#FFF3E0"}: Frambuesa defaults (cream board and plate, plinth cream): cream separates from the raspberry stage; the heart pump is a deep indigo and the bottles carry their own tones.

## Lens decisions
- Marketing: numbers family, "¿Cuántas…?" with a tangible unit (soda bottles); every figure is a counter; it ends with a twist on the share archetype (a heart that does not rest).
- Design: a stylised pump-heart (no anatomy, no gore; the fluid is a stylised warm red in bottles, tubes and beads), multiplication with pull-backs in three scales (bottles, a block of bottles, 84 pools), a loop with a timer, a fist, a sofa scene.

## Sources and numbers (no number is invented; none is rendered as a source on screen)
- Cardiac output at rest ~5 L/min (~7,200 L/day): textbook value, spoken as "unos siete mil litros"; 7,200 / 2 L = 3,600 bottles ("más de tres mil").
- ~100,000 beats a day (about 70 bpm); stroke volume ~70 mL; total blood volume ~5 L; one circuit takes about a minute at rest: standard physiology figures.
- Lifetime: 7,200 L x 365 x 80 years = ~210 million L = ~84 Olympic pools of 2.5 million L ("unos doscientos millones de litros", "más de ochenta piscinas"). Assumes resting output all life (a stated simplification).

## Scientific simplifications and deviations (stated plainly)
- The pump is a toy heart; the loop is one ring, not the real circuit; bottle and pool counts are drawn at a representative scale (about 176 bottles in the pull-back, a 22x8x5 block, 84 pools exactly).
- The sixty-second circuit is compressed in time.

## Build log
