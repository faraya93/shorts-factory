# cepillo-de-dientes-junto-al-inodoro — production notes (script stage, topic slate 2026-11-07)

Status: SCRIPT ONLY. Nothing modelled, rendered, queued or published. Next stage: asset search for every element below, then scene design (design lens), then the beat sheet with word locks.

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Por qué tu cepillo de dientes no debe estar junto al inodoro? 🤢
- **Descripción:** Cada vez que tiras la cadena, el agua lanza al aire una nube de gotitas que no ves: en un experimento con láseres subió metro y medio en ocho segundos. Y bajar la tapa ayuda menos de lo que crees. 🤢 Envíaselo a esa persona que guarda su cepillo de dientes al lado del inodoro.
  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)
- **Hashtags (description, not title):** #inodoro #cepillodedientes #comofunciona #shorts

## Script (7 scenes, family objects, variant chain, 165 words, ~56.9 s at 2.9 w/s; band 45-60 s)
Hook: ¿Por qué no deberías tener tu cepillo de dientes cerca del inodoro? | false belief: Al tirar la cadena, todo se va por el desagüe. | turn: Scene 6: bajar la tapa, the obvious fix, barely changed surface contamination in a 2024 study; cleaning the bowl did. | reframe: Tu inodoro no solo se traga las cosas: también las estornuda. | share archetype: esa persona que guarda su cepillo de dientes al lado del inodoro

1. **hook** (~9.0 s): ¿Por qué no deberías tener tu cepillo de dientes cerca del inodoro? Crees que, al tirar la cadena, todo se va por el desagüe. No todo.
   - What changes in the world: A clean bathroom; the flush starts and a faint haze rises toward the toothbrush on the sink.
   - Transformation: baño quieto, cepillo en su vaso junto al inodoro → se tira la cadena y una neblina tenue sube hacia el cepillo; camera: travelling lateral desde el cepillo hasta el inodoro, a la altura del lavamanos
   - Element: toothbrush in a cup — route: library search (BlenderKit/Poly Haven), geometric — risk: low
   - Element: toilet — route: 005 toilet_rig (accepted control) or CC0 asset — risk: low
2. **descarga** (~7.2 s): Al tirar la cadena, el agua entra con fuerza por el borde y choca contra lo que hay en la taza.
   - What changes in the world: Water bursts in from the rim and crashes into the bowl water: a calm pool becomes a turbulent swirl.
   - Transformation: agua quieta en la taza → chorros desde el borde que chocan y la revuelven; camera: picado cenital que baja hacia el interior de la taza
   - Element: bowl water (turbulent) — route: physically based water; draft profile for gate rounds, minimal transmission volume (render-time rule c) — risk: medium: render cost
3. **nube** (~9.0 s): Ese choque lanza al aire miles de gotitas invisibles. Con láseres, en un inodoro público sin tapa, la nube subió metro y medio en ocho segundos.
   - What changes in the world: The x-ray moment: a green laser sheet switches on and reveals the invisible plume erupting and climbing past the seat.
   - Transformation: aire vacío sobre la taza → una lámina de láser verde revela una columna de gotitas que sube como un cohete; camera: grúa ascendente que sigue la columna desde la taza hasta la altura de la cara
   - Overlay: counter 1,5 m at 'metro' (bracket alongside the plume)
   - Overlay: counter 8 s at 'ocho'
   - Element: droplet plume in a laser sheet — route: particles (instanced spheres) + emissive sheet; geometric — risk: medium: must read as spray, not smoke; aliases decided before reading
4. **carga** (~6.6 s): Las más finas siguen flotando en el aire. Y si en la taza había caca, viajan con sus bacterias.
   - What changes in the world: The plume stops rising and hangs; a fraction of the droplets turn yellow-green (biology colour), carrying what was in the bowl.
   - Transformation: gotitas que suben → quedan suspendidas y una parte se tiñe de verde amarillento; camera: órbita lenta alrededor de la nube suspendida
   - Element: tinted droplets — route: same particles, palette colour; microbes are NOT drawn — risk: low
5. **aterrizaje** (~6.2 s): Después bajan y se posan: en el asiento, en el suelo y, si está cerca, en tu cepillo.
   - What changes in the world: The cloud drifts and settles: droplets land on the seat, the floor and finally the bristles of the toothbrush.
   - Transformation: nube suspendida → gotitas que se posan una a una sobre el asiento, el suelo y las cerdas del cepillo; camera: seguimiento de una gotita desde la nube hasta un primer plano de las cerdas
   - Element: toothbrush bristles close-up — route: same toothbrush asset, macro framing — risk: low
6. **giro** (~9.7 s): ¿Y si bajas la tapa? En otro estudio, casi no cambió lo que quedaba en las superficies. Lo que funcionó fue desinfectar la taza. Y aleja el cepillo.
   - What changes in the world: The turn: the lid drops and the plume is squashed, but the seat and floor marks stay; then a brush scrubs the bowl clean and the toothbrush cup slides away.
   - Transformation: tapa abierta → la tapa baja, las marcas siguen ahí → la taza se limpia y el vaso del cepillo se aleja; camera: plano medio frontal que se abre a plano general del baño
   - Overlay: mark (red X) on 'casi no cambió' near the closed lid
   - Element: toilet brush — route: library search, geometric — risk: low
7. **cierre** (~9.3 s): Así que tu inodoro no solo se traga las cosas: también las estornuda. Envíaselo a esa persona que guarda su cepillo de dientes al lado del inodoro.
   - What changes in the world: Single reframe image: one last flush, the plume blooms like a sneeze from the open bowl; the camera pulls back to the whole bathroom.
   - Transformation: inodoro quieto → una última descarga, la nube se abre como un estornudo; camera: retroceso amplio desde la taza hasta el baño completo
   - Overlay: ENVÍASELO tag (label, style tag) at_word 'envíaselo', ~2.6 s, in the free space beside the toilet

## Lens record
- Marketing (lead on topic): curiosity 10/10: Everyone has a toothbrush a metre from a toilet; the invisible spray is gross, hidden and testable tonight (look where your brush is).
- Scriptwriter: flatness test passed (each scene's 'what changes' is a different event; swapping any two breaks the story); the turn comes before the closing reframe; the archetype names a behaviour.
- Design: code3d: rigid bathroom objects (toilet, toothbrush, cup) on the asset route; the plume is thousands of tiny droplets, genuinely geometric, lit by a laser sheet as in the study. Preset chosen at scene design.

## Sources and numbers (no number is invented; none is rendered as a source on screen)
- Plume: Crimaldi et al. 2022, Scientific Reports, 'Commercial toilets emit energetic and rapidly spreading aerosol plumes' (University of Colorado Boulder): lidless commercial flushometer toilet, clean tap water, laser visualisation; particles reached about 1.5 m above the bowl within 8 s. Verified through secondary coverage (The Conversation / TechXplore 2022-12), original paper not opened. Narration states 'inodoro público sin tapa' because home tank toilets were NOT tested.
- Lid: Goforth et al. 2024, American Journal of Infection Control, 'Impacts of lid closure during toilet flushing and of toilet bowl cleaning on viral contamination of surfaces in United States restrooms': surface contamination did not depend on lid position; disinfectant plus brush cleaning reduced bowl contamination by more than 99.99 %. Verified through news coverage (EurekAlert, HealthDay, 2024-01).
- Droplets carry faecal bacteria: Gerba et al. 1975 (household toilets) is the classic source; recalled, FLAGGED for verification before the beat sheet is final. The Crimaldi study used clean water.
- Toothbrush landing: an inference from the above (droplets settle on nearby surfaces), worded 'si está cerca'; no toothbrush study is cited on screen or in narration.

## Scientific simplifications (stated plainly)
- The study toilet was a commercial flushometer without lid; the scene shows a home bathroom and the narration names the setting honestly.
- Microbes are not drawn; the tint on droplets stands for what they carry.
