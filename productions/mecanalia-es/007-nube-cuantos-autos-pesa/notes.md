# nube-cuantos-autos-pesa (celeste) — production notes, written by the 2026-11-03 batch run

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Cuántos autos pesa una nube? ☁️
- **Descripción:** Parece que no pesa nada, porque flota, pero una nube común pesa como unos trescientos autos: guarda unos quinientos mil kilos de agua en gotitas tan pequeñas que el aire que sube las sostiene. ☁️ Sígueme y envíaselo a ese amigo que cree que las nubes son humo.
  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)
- **Hashtags (description, not title):** #nubes #clima #curiosidades #shorts

## Script (7 scenes, family numbers) and visual per line
1 balanza: ¿Cuántos autos pesa una nube? Parece que no pesa nada, porque flota, pero una nube común pesa como trescientos autos.  (una nube inclina la balanza → los autos se apilan en el otro plato hasta equilibrarla; camera: retroceso mientras los autos se multiplican)
2 cubo: Una nube está hecha de millones de gotitas de agua. Una nube de buen tamaño, de un kilómetro por lado, guarda unos quinientos mil kilos de agua.  (la nube se vuelve transparente y se ven las gotitas → el agua se junta en un bloque; camera: empuje hacia dentro de la nube y órbita)
3 corriente: Cada gotita es tan pequeña y liviana que el aire que sube la sostiene, como una pelusa en el viento.  (las gotas caen → la corriente de aire las empuja de vuelta hacia arriba; camera: elevación lenta siguiendo la corriente)
4 reparto: Y ese peso se reparte en un espacio enorme: un metro cúbico de nube apenas tiene medio gramo de agua.  (un metro cúbico con tres gotas → una cuadrícula de miles de cubos; camera: retroceso amplio sobre la cuadrícula)
5 lluvia: Cuando las gotitas chocan y se juntan, crecen. Y cuando una pesa demasiado para el aire, cae: eso es la lluvia.  (gotitas pequeñas → se funden en una gota grande que cae y salpica; camera: inclinación hacia abajo siguiendo la gota)
6 millon: Una sola gota de lluvia reúne alrededor de un millón de gotitas de nube.  (una gota de lluvia → estalla en una nube de miles de gotitas; camera: retroceso al estallar)
7 cierre: Así que una nube no es humo ni vapor ligero: es un lago de gotas flotando sobre ti. Sígueme, y envíaselo a ese amigo que cree que las nubes son humo.  (humo de chimenea tachado → la nube se aplana y se vuelve un lago en el cielo; camera: órbita amplia)
Hook formula: ¿Cuántos autos pesa una nube? | false belief: (none: numbers/what-if) | reframe: Una nube no es humo ni vapor ligero: es un lago de gotas flotando sobre ti. | share archetype: el amigo que cree que las nubes son humo

## Identity
- Preset: **celeste**. Departure from Coral: the CELESTE sky stage (#8FD6F2 -> #62B4DC), because the subject is a cloud and the sky is its natural world. The preset's accent was changed from orange #E8590C to deep violet #5A1AA0 (orange reached only 1.76:1 luminance contrast against a light stage, the gate needs 3:1; emission_gain 0.1) and the supports are peach #E8956A (cream merged with the white cloud, dE 0.5-3). Lake blue #5468E0.
- Support colours: {"board": "#E8956A", "plate": "#E8956A"}: Celeste's cream support merged with the white cloud (dE 0.5-3), so the support is a peach derived from the original orange accent system (#E8956A, dE >= 20 from both ends of the sky gradient and from the white cloud); plinth stays the deep blue #2B4C70.

## Lens decisions
- Marketing: numbers family, hook "¿Cuántos…?" on a tangible object (a cloud everyone has seen) with the false belief stated inside the hook (it floats, so it weighs nothing); the number is carried by a balance scale and a car pile; closing reframe renames the cloud (a lake of drops).
- Design: seven different set pieces (balance + 66-car pile with pull-back; cloud dissolving into droplets with a km cube; updraft with a falling droplet pushed back; 1 m³ cube multiplying into a grid; droplets merging into rain; a raindrop bursting; smoke crossed out and a floating lake). Every scene has a camera path and an in-shot transformation.

## Sources and numbers (no number is invented; none is rendered as a source on screen)
- ~500,000 kg of water in a 1 km³ fair-weather cumulus (about 0.5 g/m³): NCAR / USGS explanation (M. LeMone). Flagged: an order-of-magnitude figure, spoken as "unos".
- "Trescientos autos": 500 t / ~1.5 t per car = ~330. Approximate, spoken as "como trescientos".
- A raindrop (~2 mm) holds about a million cloud droplets (~20 µm): volume ratio (2000/20)^3 = 10^6, spoken as "alrededor de un millón".

## Scientific simplifications and deviations (stated plainly)
- The pile shows 66 cars for 300 (counter carries the number); the droplet swarms are a few hundred spheres for millions; the "km cube" and the water block are schematic, not to scale.
- Droplets are held up by updrafts (and tiny terminal speed); the scene shows it as arrows, no airflow simulation.
- The lake-in-the-sky is a metaphor for the closing reframe.

## Build log
