# que-pasaria-si-se-corta-el-cable-del-ascensor: production notes

Status: SCRIPTED, BUILT AND GATED (2026-11-10). DRAWN from the banked tier (rank 1, replacement for returned 013, 2026-11-09). Topic: whatif, fork, theme elevators, main tension dangerous. Hook and hero route: docs/current/idea-bank.md rank 1. Final render to be queued with `tools/queue_final.py`.

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Qué pasaría si se corta el cable de un ascensor? 😱
- **Descripción:** ¿Qué pasa si se corta el cable de un ascensor? Nada: cuelga de varios cables y, si todos fallaran, un freno lo agarra de los rieles.
  Y saltar no te salva: tu salto frena unos 10 km/h y la caída desde diez pisos llega a casi 90. 😱 Envíaselo a ese amigo que sube por las escaleras porque le da miedo el ascensor.
  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)
- **Hashtags (description, not title):** #ascensor #curiosidades #fisica #shorts

## Script (6 scenes, family whatif, variant fork, 160 words, 57.8 s narrated; band 45-60 s)
Hook: ¿Qué pasaría si se cortara el cable de un ascensor? | false belief: caerías al vacío, y solo te salvaría saltar justo antes del golpe | turn: scene 5 (even if everything failed there is a buffer, and a woman survived a 75-storey fall in 1945) | reframe: un ascensor no cuelga de un cable: está agarrado a sus rieles | closing repeats the opening question (fork), then "envíaselo" with the archetype: ese amigo que sube por las escaleras porque le da miedo el ascensor.

What changes in the world, per scene (flatness test: swapping any two breaks the story):
1. **hook:** the car hangs by ONE rope; the rope snaps on "caerías" and the car drops floor by floor, the camera tracking it to the pit.
2. **cables:** the same car; five more ropes grow in beside the first on "varios", then three are cut one after another and the car does not move.
3. **frenos:** every rope is cut, the car accelerates down the shaft, the rails light up in the accent around its base on "agarra" and it stops mid-shaft (rung 2 and 3 of the reshape, below).
4. **salto:** a cut-away car in free fall down a very tall shaft: a phone drifts up off the floor (all a jump gives you) while the landings stream past and two counters set 10 km/h against 87 km/h.
5. **colchon (the turn):** the camera starts on the buffer ("abajo hay un amortiguador"), cranes up the shaft, the ropes go on "chocó", the car falls the whole height and sinks onto the buffer's spring.
6. **cierre:** the reframe image: the car held by its rails (accent) with six severed ropes above; the question is repeated; "Nada."; the pull-back ends on the whole shaft.

## Sources and numbers (no number is invented; none is rendered as a source on screen)
- 10 km/h and 87 km/h: our arithmetic, v = sqrt(2 g h). h = 10 floors x 3 m = 30 m gives 24.3 m/s = 87 km/h; a 0.5 m standing jump gives 3.1 m/s = 11 km/h, said as "unos diez". The floor height and the jump height are assumptions, stated as approximate.
- 1945: B-25 crash into the Empire State Building, Betty Lou Oliver (not named) survived a 75-storey elevator fall; Guinness World Records "longest fall survived in a lift (elevator)" and the Wikipedia article on the crash (which credits the cushion of air in the shaft). Sources differ on the floor she was on and on whether every cable was cut; the narration claims only the 75 storeys and the survival.
- Several steel hoist ropes, a few of which are enough to carry the car: elevator engineering lecture notes (each rope rated to carry the car; general reference, **flagged to confirm** against a standard before relying on the exact wording "con unos pocos basta").
- Overspeed governor and safety gear gripping the guide rails: Lift and Escalator Library (Cooper), The Elevator Museum (Otis 1854 demonstration, not used in the narration). The narration says only "el freno la agarra de los rieles".

## Scientific simplifications (stated plainly)
- The passenger is never drawn; a phone stands in for the jump. In a free-falling car a jump only makes you drift toward the ceiling, which is what the phone does.
- No counterweight is drawn. The brake is shown only as the rails lighting up around the car's base (real safety gear is a pair of wedges or a clamp; it failed blind naming, see the reshape).
- The fall speed on screen is not to scale; the counters carry the arithmetic.

## RESHAPE LADDER LOG 2026-11-10 (logged in lens-decisions.md, same date)
- **Scene 3, trigger: declared element failed the likeness gate.** Seven isolated readings of the safety hardware across the stagings listed in the lens-decisions row (best: caliper clamp 60/62/60, one reader wrote "clamped" instead of "clamp"; none reached three matching guesses) and two of the governor wheel ("wall safe", "wall-mounted control cabinet"). Rung 1 (re-stage): tight on the wedge pair, wider, jaws, with and without the wheel in frame. Rung 2 (rewrite the beat to a modellable equivalent doing the same job): the rails light up in the accent around the base of the car and it stops dead, read as the elevator car in a wide frame (75/75/72). Rung 3: narration adjusted (see the row). The clamp and the wheel stay off screen (drawability rule). Aliases were fixed before every reading and none was added.
- **Scene 4, rung 1:** phone too small beside the car (80/85/65, the third reader named the car); restaged closer with a larger phone: 80/85/70 mixed. Note for the owner's eye: one of the three readers named the car and listed the phone as an alternative; the tool counts the alias as present.
- **Scene 5, rung 1:** the buffer under the landing car read as "elevator car" (55/55/55); restaged on the buffer alone at the start of the scene: "coil spring" 60/60/72.
- **Scene 2, rung 1:** ropes at 4.2 s read as the car (70/70/75, none named a cable); restaged at 3.6 s with all six ropes over the sheave: "elevator car with cables" 60/80/80.

## Gate record
Colour gate PASS (stage plate set to a dark slate #3B4553 after two BLOCKs measured on steel parts, see the support colours reason in script.json), hero `elevator-car` frozen (neutral 85/85/88, production still 90/90/85), every element read and carried, visibility PASS (p90 dE 41-53, area 1.06-13.8 %). The hero was unfrozen and re-read three times (library_assets declared; hero still changed by the scene 3 reshape; Cab class edited for the interior lamp), every reading kept.

## Cost classes
All six scenes `opaque` (no glass, water or volumes): predicted 2-3 s/frame, none above 15, no cost_restage.

## BATCH DIRECTIVE 2026-11-09 (runner)
Write the script at production time under the standing flatness check (CLAUDE.md "Script flatness": event progression, the scene-swap test, the turn before the closing reframe), then produce under standing doctrine, measuring the riskiest element first; a figure with no source comes out of the script. If this topic fails beyond the Reshape ladder, return it only with `.venv/bin/python tools/return_topic.py <prod> --reason "..."`. Under gate_version 2 including the visibility check. No publishing, no spend, no accounts; do not touch the orchestrator, its queue or excluded list.

- UNFREEZE 2026-11-10: library_assets declared after the first hero read, fingerprint moved, same stills, hero re-read before any other scene

- UNFREEZE 2026-11-10: scene 3 reshape rung 2 and 3: the clamp hardware failed blind naming in seven readings and is removed from every scene, so the hero still changed; hero re-read before any other scene

- UNFREEZE 2026-11-10: Cab class edited (an interior lamp for the cut-away car, scene 4); hero still pixels unchanged; hero re-read before any other scene
