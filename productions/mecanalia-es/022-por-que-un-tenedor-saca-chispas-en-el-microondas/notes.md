# por-que-un-tenedor-saca-chispas-en-el-microondas: production notes (developed script, 2026-11-11)

Status: DEVELOPED SCRIPT ON FILE (developed set of the 2026-11-11 creative session; lens-decisions row "Developed set 019-024"). Nothing modelled, rendered, queued or published. The production proceeds FROM THIS SCRIPT (produce skill step 1), starting at step 3 (render-cost classes) and the beat sheet; the script may change only through the Reshape ladder, logged here and in lens-decisions.

## Publish package draft (Spanish; the owner publishes)
- **Título:** ¿Por qué un tenedor saca chispas en el microondas y una cuchara no? ⚡
- **Descripción:**
  ¿Por qué un tenedor saca chispas en el microondas y una cuchara no? Porque la carga se amontona en las puntas de sus dientes y rompe el aire.
  Y el propio microondas está hecho de metal, solo que liso. ⚡
  Envíaselo a ese amigo que mete al microondas el plato con el tenedor encima.
- **Hashtags (description, not title):** #microondas #cocina #ciencia #shorts

## Script (6 scenes, family objects, variant chain, 139 words, ~47.9 s at 2.9 w/s; band 45-60 s)
Hook: ¿Por qué un tenedor saca chispas en el microondas y una cuchara no? | false belief: Cualquier metal hace chispas dentro del microondas. | turn: Scene 5: the oven's own walls, and even the door's screen, are metal, and they never spark: they are smooth. | reframe: No chispea el metal: chispean las puntas. | share archetype: ese amigo que mete al microondas el plato con el tenedor encima
Theme / main tension (TOPIC BALANCE): microwave / dangerous.

1. **hook** (~6.2 s): ¿Por qué un tenedor saca chispas en el microondas y una cuchara no? Dicen que cualquier metal chispea.
   - What changes in the world: Contrast, two actors: a cut-away microwave with a fork and a spoon on the turning plate; the fork crackles with sparks at its tines while the spoon stays dark; tag ¿CUALQUIER METAL? appears.
   - Transformation: tenedor y cuchara quietos → el tenedor chispea y la cuchara no; camera: órbita lenta alrededor del plato giratorio
   - Overlay: tag ¿CUALQUIER METAL? at 'cualquier'
   - Element: microwave oven (cutaway): route library: Poly Haven 'Vintage Microwave' (BlenderKit cab01678, CC0, 138 MB) or BlenderKit 'Low Poly Microwave Oven' (c629cd93, RF); the open job `microwave-oven` brief (states door closed, open, cutaway showing metal walls) is the spec, built by the production under asset-system (g); risk medium: an unsealed class; a box with a window door, keypad and glass plate is a strong read; aliases (fixed now, before any reading): microwave, microwave oven, oven, microondas
   - Element: fork and spoon on a plate: route build, geometric (fork, spoon, glass plate); library alternative BlenderKit 'fork' (1142edef, RF); risk low; aliases (fixed now, before any reading): fork, spoon, cutlery, tenedor, cuchara
2. **ondas** (~10.7 s): Adentro, las microondas rebotan de pared en pared, y su campo cambia de sentido miles de millones de veces por segundo: empuja las cargas del metal de un lado a otro.
   - What changes in the world: The cavity fills with accent wave fronts bouncing between the walls; inside the fork and the spoon a glow sloshes from one end to the other in time with them.
   - Transformation: horno vacío de ondas → las ondas rebotan y la carga va y viene dentro del metal; camera: travelling lateral a través de la cavidad, de pared a pared
   - Overlay: chip 2,45 GHz at 'miles'
   - Element: glowing waves bouncing inside a microwave cavity: route energy graphics (emissive rings, doctrine language) inside the oven build; risk medium: energy graphics need the oven walls in frame; aliases (fixed now, before any reading): microwave, microwave oven, microwaves, oven
3. **puntas** (~7.9 s): En la cuchara, la carga se reparte por toda la curva. En el tenedor, se amontona en las cuatro puntas de los dientes.
   - What changes in the world: Close-up side by side: the glow spreads evenly over the spoon's bowl, while on the fork it drains into the four tine tips, which brighten one by one.
   - Transformation: carga repartida en ambos → la cuchara queda pareja y las puntas del tenedor se encienden; camera: empuje desde la cuchara hacia las puntas del tenedor
   - Overlay: ring dotted around the tines at 'puntas'
   - Element: fork tines glowing: route fork build with an emissive tip mask; risk low; aliases (fixed now, before any reading): fork, tenedor, fork tines
4. **chispa** (~6.9 s): Ahí el empuje es tan fuerte que rompe el aire: el aire se vuelve chispa, como un rayo en miniatura.
   - What changes in the world: The air at the tines breaks down: arcs leap between the tips with a flash, branch and snap off.
   - Transformation: puntas brillantes → saltan chispas entre los dientes; camera: primer plano que retrocede de golpe con cada chispa
   - Element: sparks between fork tines: route build: small branching emissive arcs under the open job `electric-arc` brief (state 'small arc between two points'); risk medium: an unsealed class; the fork is the context cue; aliases (fixed now, before any reading): spark, sparks, electric arc, arc, chispa, lightning
5. **giro** (~8.3 s): Pero las paredes del microondas también son de metal, y no chispean: son lisas, sin puntas. Hasta la rejilla de la puerta es metal.
   - What changes in the world: The turn: pull-back to the whole cutaway oven; its walls light evenly, without a single spark; the camera pushes to the door, where the metal screen behind the glass lights as a fine grid.
   - Transformation: chispas en el tenedor → todo el horno se ilumina parejo, sin chispas, hasta la rejilla de la puerta; camera: retroceso a todo el horno y empuje hacia la puerta
   - Overlay: label METAL tag at 'metal,'
   - Element: microwave door with its metal screen: route oven build/import; the screen is a geometric perforated plate behind the window; risk medium; aliases (fixed now, before any reading): microwave, microwave oven, microwave door, oven door
6. **cierre** (~7.9 s): Así que no chispea el metal: chispean las puntas. Envíaselo a ese amigo que mete al microondas el plato con el tenedor encima.
   - What changes in the world: Single reframe image: the fork's four tips spark once more beside the dark, smooth spoon, while the whole oven glows calmly around them.
   - Transformation: tenedor y cuchara → las puntas chispean y todo lo liso queda tranquilo; camera: retroceso desde las puntas hasta el horno entero
   - Overlay: ENVÍASELO tag at_word 'envíaselo'

Staging mode: cutaway (proposal for production; the design lens confirms it at the beat sheet). everything happens inside the oven cavity: a cutaway of the microwave keeps the fork, the spoon, the walls and the door mesh in one frame.

## Staging notes: wardrobe (human-figure recolour slots fig_skin, fig_shirt, fig_pants, fig_boots)
- No figure on screen.

## Lens record (one session, 2026-11-11)
- Marketing (lead on topic): curiosity 9/10: Everyone has been warned about metal in the microwave, and many have seen the sparks; dangerous. Title follows the search rules (question as typed, object word early, one trailing emoji, no hashtags); description line 1 answers in one clause, line 2 the twist, then the share line.
- Scriptwriter: flatness test passed: each scene's 'what changes in the world' is a different event, and no adjacent pair can be swapped without breaking the story; the turn comes before the closing reframe; the closing is one reframe and one 'envíaselo' sentence ending on a behaviour archetype.
- Design: code3d on the asset route; only sealed library assets in sealed poses are prescribed as available (hand-articulated: open, lever, wheel, door, knife, mask, mask_b, crack; human-figure: standing, walking, jumping, falling, seated); every other element is a geometric build, a material, energy graphics, or a library candidate recorded in the audit below with its fallback.

## Sources and numbers (no number is invented; none is rendered as a source on screen; FLAGGED items are confirmed or removed at the beat sheet)
- Mechanism: the oven's field drives charge in the metal; charge gathers at sharp points (field enhancement) until the air breaks down into a spark; smooth objects without points usually do not arc, though they can under some conditions: NPR 'Science Out of the Box: Microwave antics, don't stick a fork in it' (3 November 2006) and Physics Forums 'Metal in microwave ovens' (live search 2026-11-11). FLAGGED: add one physics or manufacturer reference at the beat sheet.
- Oven frequency about 2.45 GHz (patent literature and EMF-Portal, live search 2026-11-11); the field reverses direction about 4.9 billion times a second, so 'miles de millones de veces por segundo' holds.
- The oven's metal case and a metal-wire screen in the door keep the microwaves inside: Swiss Federal Office of Public Health fact sheet 'Microwave ovens'; UL 'Radarange to modern-day microwaves' (screen holes about 1 mm) (live search 2026-11-11).

## Scientific simplifications (stated plainly)
- A spoon CAN arc in some conditions (edges, size, field pattern); the hook question states the common case and the narration says the spoon's charge spreads out, not that a spoon never sparks.
- Waves and charge are drawn as glows; both are invisible.

## Modellability audit and pre-written fallbacks (2026-11-11, `docs/current/reports/modellability-audit-019-024.md`)
Ladder fallbacks pre-approved by the scriptwriter, design and marketing lenses in the audit (one session), so a production run applies them WITHOUT stopping when a scene trips its trigger. The script is unchanged until a rung is applied. When one is: update `script.json`, re-run the flatness swap test, log the reshape here and as a row in `lens-decisions.md`. Aliases are fixed in the script above, before any reading; none may be added after a guess.

**Verdict: MODELABLE WITH THE WRITTEN FALLBACKS.** Riskiest element: the microwave oven (every scene), an unsealed class with library candidates, and the arcs (scene 4), an unsealed class.

Routes: Builds: fork, spoon, plate, door screen (geometric); waves (energy graphics); arcs (emissive branching, `electric-arc` brief). Library: CC0 Poly Haven Vintage Microwave (138 MB) or RF low-poly microwave (0.9 MB), both search results only (BlenderKit thumbnails were not retrievable on 2026-11-11: judge at the asset step). No figure, no hand.

- Microwave (trigger: neither candidate nor a build passes the gate as a microwave). Rung 1: show the closed oven with its window, keypad and turning plate first, then cut away the side wall (the closed oven is the context cue). Rung 4: the cutaway read on a kitchen counter with a plate of food inside.
- Scene 4 sparks (trigger: fail). Rung 1: arcs drawn bluish-white and short, the tines in tight close-up. Rung 2: the spark shown as one bright flash between two tines with a scorch mark left on the plate. Narration unchanged.
- Scene 2 waves (trigger: fail). Rung 1: the oven walls stay in frame, the waves as ripples on the plate surface. Rung 2: the beat is carried by the glow sloshing inside the fork and spoon, without free waves. Narration unchanged.

Unresolved fallbacks: none. Batch: cleared for the 2026-11-11 batch.
