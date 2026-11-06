# dedos-arrugados-agua (esmeralda) — production notes, written by the 2026-11-03 batch run

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Por qué se arrugan tus dedos en el agua? 💧
- **Descripción:** Si fuera agua absorbida, tu brazo también se arrugaría. No: tu sistema nervioso aprieta los vasos de la yema y la piel se pliega en surcos, en canales de drenaje, para que agarres mejor lo mojado. 💧 Sígueme, y envíaselo a ese amigo que se queda mirando sus dedos de pasa en la bañera.

Modelo 3D de la mano: "hand" de kevinruiz (Sketchfab), licencia CC Attribution.
  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)
- **Hashtags (description, not title):** #dedosarrugados #piel #cuerpohumano #shorts

## Script (6 scenes, family body) and visual per line
1 contraste: ¿Por qué se te arrugan los dedos en el agua? Dicen que la piel se empapa y se hincha. Pero entonces, ¿por qué tu brazo no se arruga?  (mano y antebrazo sumergidos en agua real, lisos → solo las yemas se arrugan, el antebrazo sigue liso; camera: órbita baja alrededor de la mano en el agua)
2 orden: Lo decide tu sistema nervioso. Tras unos minutos mojados, manda una orden, y los vasos sanguíneos de la yema se aprietan.  (corte de la yema con piel, pulpa y hueso: una señal baja por el nervio → los vasos se estrechan; camera: empuje hacia dentro del corte)
3 surcos: Con menos volumen por dentro, la piel se jala hacia adentro y se pliega en surcos.  (yema lisa → la pulpa pierde volumen y la piel se pliega en surcos; camera: macro: acercamiento y giro sobre la yema)
4 canales: Y esos surcos son canales de drenaje: sacan el agua de en medio, y por eso no resbalas.  (una yema lisa flota sobre una película de agua → una yema con surcos expulsa el agua por los canales y toca el vidrio; camera: travelling lateral a ras del vidrio mojado)
5 agarre: En un estudio, la gente con dedos arrugados movió objetos mojados más rápido. Con objetos secos, no hubo diferencia.  (dos yemas lisas dejan escapar una piedra mojada → dos yemas arrugadas la levantan; camera: dolly lateral siguiendo la piedra)
6 cierre: Así que no es piel empapada: son canales de agarre que tu cuerpo enciende. Sígueme, y envíaselo a ese amigo que se queda mirando sus dedos de pasa en la bañera.  (yema arrugada con agua corriendo por sus canales, en una sola imagen; camera: retroceso amplio)
Hook formula: ¿Por qué se te arrugan los dedos en el agua? | false belief: La piel se empapa y se hincha de agua. | reframe: No es piel empapada: son canales de agarre que tu cuerpo enciende. | share archetype: ese amigo que se queda mirando sus dedos de pasa en la bañera

## Identity
- Preset: **esmeralda**. Departure from Coral: ESMERALDA stage (deep green). Reason: the owner's standing reservation about a skin-toned hand on the Coral stage; a warm hand on a cool green stage separates by hue, not only by value.
- Support colours: {"board": "#FFF3E0", "plate": "#26323A"}: Esmeralda board stays cream; the cutaway plate is a deep slate so pale tissue layers (skin, pulp, ivory bone) read against it and the gate separation holds (plate vs hero >= 20).

## Lens decisions
- Design (lead): owner rule 2026-11-05, every element at hero standard. Vessels, fingertip, water, glass and stone are built or material-routed, each blind-named in its scene; the hero hand stays (approved asset).
- Scriptwriter: the tyre analogy is dropped (a tyre would be a new unmeasured asset and the analogy is carried by the real drainage beat); the reframe becomes 'canales de agarre'. The grip comparison is the same fact (Kareklas 2013) acted by real fingertips and a wet stone.
- Marketing: same hook and archetype as the first version (verifiable in the bath); structure `chain`, 6 scenes; the before/after pair is archived.

## Sources and numbers (no number is invented; none is rendered as a source on screen)
- Mechanism: sympathetic nervous system causes vasoconstriction in the digits after prolonged wet exposure; the pulp loses volume and the skin folds. Only glabrous skin (fingers, palms, toes, soles) wrinkles. Denervated fingers do not wrinkle (clinical nerve test).
- Function: Changizi et al. 2011 (drainage-channel pattern); Kareklas, Nettle, Smulders 2013 (wrinkled fingers handled wet objects faster, dry objects no difference). Stated as 'en un estudio'; no figure rendered.
- Hero: Sketchfab 'hand' by kevinruiz, CC Attribution (assets/library/human-hand).

## Scientific simplifications and deviations (stated plainly)
- The wrinkle pattern is procedural transverse folds on a real mesh, not the branching pattern of real skin.
- The cutaway is a stylised layer stack (skin, pulp, bone), not anatomy to scale; vessels and nerve are schematic tubes, with no blood cells drawn.
- The wet-grip beat and the drainage beat are choreographed, not simulated.
- Water is physically based (IOR 1.333) but its motion is keyframed.

## Build log
- SKIPPED 2026-11-05 (unattended run): the extended likeness gate blocks scenes 2 and 5, so no final render was made. Scenes 1, 3, 4, 6 pass (blind confidence 60-85) and their draft stills are good.
- Scene 2 (fingertip with vessels and nerve inside): four rounds, blind confidences 35/40, 35/35, 30/35, 60/25 (a half-cut section, then an x-ray tube, then an x-ray window on an opaque finger). Readers keep naming a glass tube or a generic cross-section; only the last pass-of-two-readers variant reached 60 on one reader.
- Scene 5 (wet grip): a stone (40/65, 75/40, 40/35) then a bar of soap with suds (65, 55/60). Readers name fingers and soap/pebble but with confidence 55-65 because the fingers are long generic tubes.
- Likely fix, not tried for lack of budget: give the cutaway a hand context (translucent skin on the hand asset itself, with vessels placed along its real finger centrelines) and give the grip beat shorter fingers with knuckles, i.e. an articulated finger model through the asset route; both need modelling the unattended run did not have time for.
- Everything needed to resume exists: scene scripts dedos2_01..06, rigs finger_rig.py and real_kit.py, scenes.json with scene_elements, narration audio. To resume: fix scenes 2 and 5, run `gate.py run`, `gate.py stills`, blind-name, then tools/chain_render2.sh.
- Records for scenes 1, 3 and 6 were carried over after a library edit (stills re-rendered and compared: mean pixel difference < 0.07 of 255; the readers' verbatim guesses are in build/gate/elements.json).
