# termo-por-que-mantiene-el-calor (lima) — production notes, written by the 2026-11-03 batch run

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Por qué tu termo mantiene el café caliente? ☕
- **Descripción:** El calor sale de tres formas: tocando, moviendo el aire y como luz infrarroja. Entre las dos paredes del termo casi no hay aire, y las paredes son espejos: el calor se queda sin camino. Lo que más se pierde es por la tapa. ☕ Sígueme, y envíaselo a ese amigo que deja la tapa del termo abierta.
  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)
- **Hashtags (description, not title):** #termo #calor #comofunciona #shorts

## Script (7 scenes, family objects) and visual per line
1 hook: ¿Por qué tu termo mantiene el café caliente durante horas? Dicen que tiene un aislante por dentro, como espuma. Pero lo que tiene es otra cosa.  (un termo cerrado → se levanta la tapa y sale vapor de café; camera: órbita descendente alrededor del termo)
2 paredes: Por dentro tiene dos paredes, una dentro de la otra, y entre ellas casi no hay aire.  (el termo entero → un plano de corte barre la pared y revela dos paredes de acero, el hueco y el café líquido; camera: empuje a través de la pared hacia el hueco)
3 tres: El calor sabe salir de tres formas: tocando, viajando con el aire, y como luz infrarroja.  (el café cede calor de tres formas: la pared brilla (contacto), esferas de aire suben (aire), rayos de luz cruzan el hueco (luz); camera: travelling lateral y subida siguiendo las tres rutas)
4 vacio: Pero sin aire entre las paredes, ni tocar ni mover aire sirve: el calor se queda sin camino.  (el aire del hueco es expulsado: las esferas salen y quedan paredes sin nada en medio; la pared interior se enfría; camera: plano cenital descendiendo al hueco)
5 espejo: Y las paredes son espejos: la luz infrarroja rebota de vuelta, y regresa al café.  (los rayos cruzan el hueco, chocan con la pared espejo y regresan al café; camera: órbita alrededor del hueco siguiendo un rayo)
6 tapa: Por eso el punto débil es la tapa: por ahí se escapa casi todo el calor que se pierde.  (la tapa se abre: una columna de calor sale por arriba mientras las paredes quedan frías; camera: inclinación hacia la tapa y retroceso)
7 cierre: Así que no es un aislante que guarda el calor: es un vacío que le cierra el camino. Sígueme, y envíaselo a ese amigo que deja la tapa del termo abierta.  (el corte se cierra y el termo vuelve a ser una sola pieza, en una sola imagen; camera: retroceso amplio)
Hook formula: ¿Por qué tu termo mantiene el café caliente durante horas? | false belief: Tiene un aislante por dentro, como espuma. | reframe: No es un aislante que guarda el calor: es un vacío que le cierra el camino. | share archetype: ese amigo que deja la tapa del termo abierta

## Identity
- Preset: **lima**. Departure from Coral: LIMA stage (lime green, dark-green plinth, violet accent). Reason: a steel flask and brown coffee need a bright, clean stage; the violet accent for the heat contrasts hard with lime and avoids the usual red/orange 'hot' cliché that would merge with the coffee.
- Support colours: {"board": "#F2EEFF", "plate": "#F2EEFF"}: Lima (as the first version): the cream plate measured dE 19.5 from the lime stage, so supports are near-white lavender; clear materials (glass, coffee) are classed other by the gate.

## Lens decisions
- Design (lead): owner rule 2026-11-05. The first version's coffee block and flat blue heat dots are gone; liquid, glass-like air spheres, glowing metal and light rays share one realistic language; the thermos hero is rebuilt as a hollow double-walled flask.
- Scriptwriter: journey structure kept (hook, walls, three ways, vacuum, mirror, lid, reframe) with the same narration; each beat now has a transformation that travels (a cut plane sweeps, spheres leave, rays bounce, the lid opens).
- Marketing: dynamism rule (hard bar): seven distinct camera moves and framings; the cutaway is revealed by motion, not shown as a static diagram.

## Sources and numbers (no number is invented; none is rendered as a source on screen)
- Vacuum flask principle (Dewar): double wall with a near-vacuum gap stops conduction and convection; reflective inner surfaces cut radiation; heat loss through the stopper/lid is a main remaining path. Standard physics references. No figures used.

## Scientific simplifications and deviations (stated plainly)
- Heat transfer is choreographed, not simulated; air molecules are drawn far larger and fewer than real ones.
- The cut plane is a visual device: a real thermos is sealed.
- Radiation is drawn as a few rays; the vacuum gap is wider than a real one.
- The coffee is a clear amber liquid; real coffee is opaque at this depth.

## Build log
- SKIPPED 2026-11-05 (unattended run): the extended likeness gate blocks scene 2, so no final render was made. Scenes 1, 3, 4, 5, 6, 7 pass blind naming (85/85, 65/60, 70/70, 60/72, 65/65, 85/80); scene 2 passed as a thermos at 80/72 when the cutaway stood alone but its coffee element was never named ('dark amber liquid').
- Scene 2 coffee: readers called the liquid 'amber', 'brown' or 'red-orange liquid', never coffee or a drink. Aliases were not widened (the rule forbids it). A steaming cup of the same coffee beside the flask made both thermos and 'coffee mug' appear in the guesses but the confidences were 55 and 60, five points under the floor on one reader; a version with the cap lifted and steam scored 75/55.
- What passed and is reusable: a hollow double-walled flask from real lathes, a sweeping cut plane that reveals walls, gap and coffee, coffee as a refracting liquid, glowing inner steel, tracer air spheres, light rays, a steam volume; the handle was the key to recognition (without it readers said 'blue cylinder', 55/50).
- Likely fix: pour the coffee into the cap-cup in scene 1 or 2 (a stream and a filling cup are unmistakably coffee) or add crema and a visible steam column over the open neck; then re-run the gate and blind naming for scene 2 only.
- To resume: fix scene 2, `gate.py run`, `gate.py stills`, blind-name scene 2, then tools/chain_render2.sh (SF_SAMPLES=64, caffeinate). Narration audio exists; scenes termo2_01..07, libs thermos_real.py and real_kit.py, scenes.json with scene_elements are committed.
- RESUME ATTEMPT 2026-11-06 (still SKIPPED; the one-off floor 50 applies to secondary elements only, the thermos is the hero and keeps 60). Scene 2 restaged so each element is named on its own frames: the cup slides in only after the cut has shown the flask alone (thermos frames 70/85, coffee frames 135/155). Fresh readers: thermos 62/55 (the hero floor is 60, so it fails by 5 on one reader; the readers called the cap 'flashlight or grenade-like' and the handle 'a loose ring'), coffee with a plain white mug 60/35 ('flat white coffee mug, 2D icon style'). A second change (red glazed mug, stronger steam) was rendered but NOT read: the steam volume draws as a hard-edged rectangle and hides the coffee surface in the mug, so it was judged a visual defect and not sent to readers. Not done and likely needed: (1) a steam column with soft falloff (a tapered, noise-masked volume) or a pour of coffee into the cap-cup; (2) a thermos cap that reads as a cup (steel or coloured, not a ribbed grey disc), which changes every scene of the production and so needs all seven records re-named. scenes termo2_02.py is left in the red-mug state; its gate record is stale.

