# imanes: how magnets work (Coral) — production notes, 2026-10-29

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Por qué un imán no atrae todos los metales? 🧲
- **Descripción:** Un imán levanta un clip, pero ignora una lata de aluminio… y las dos son de metal. 🧲 El secreto es un campo invisible que solo organiza ciertos materiales: lo ves cuando las limaduras de hierro se ordenan entre los dos polos, y cuando un clip se vuelve imán temporal para sostener a otro. Sígueme y envíaselo a ese amigo que cree que los imanes pegan a todo.
  Música: Sneaky Snitch by Kevin MacLeod (incompetech.com), CC BY 3.0 (placeholder track; the credit MUST be copied into the YouTube description).
- **Hashtags (description, not title):** #imanes #magnetismo #cienciaencasa #sabiasque #shorts

## Script (7 scenes, ~69 s) and visual per line
1 hook: ¿Por qué un imán levanta un clip, pero ignora una lata de aluminio, si las dos son de metal? Mira: el clip salta hacia el imán, y la lata ni se inmuta. (objects pop in on their words; the clip hops to the magnet; the magnet is pushed to the can, which never moves)
2 Los imanes no atraen todos los metales: solo el hierro, el níquel, el cobalto y los aceros que los contienen. El aluminio y el cobre no se mueven, y algunos aceros inoxidables casi tampoco. (a magnet sweeps a row: steel clip jumps, can/coin stay, the stainless bar only leans)
3 Lo que atrae no es el imán, sino un campo invisible a su alrededor. Si esparces limaduras de hierro, se ordenan en líneas que salen de un polo y llegan al otro. (rings, scattered filings, then organised along dipole field lines)
4 En ese campo, cada clip se vuelve un imán temporal: por eso un clip sostiene a otro, y ese a otro más. Si apartas el imán, casi toda la cadena se suelta. (chain of 4 clips with induced N/S caps; magnet slides away, three clips fall, one stays)
5 Los polos también tienen reglas: los opuestos se atraen, y los iguales se empujan. Acerca dos imanes por el mismo polo, y se rechazan solos.
6 Y si cortas un imán por la mitad, no separas sus polos. Obtienes dos imanes completos, cada uno con su propio norte y su propio sur. (blade cuts the bar; the halves part and each shows both poles)
7 Un imán no es un pegamento mágico. Es un campo invisible que atrae, rechaza y ordena ciertos materiales. Sígueme, y envíaselo a ese amigo que cree que los imanes pegan a todo. (glue bottle crossed out, field + filings, clip taken, small magnet rejected, filings re-organise; C2 "ENVÍASELO" tag)
Hook formula: tangible objects + false belief ("si las dos son de metal"). Central reframe: invisible field, not magic glue. Share archetype: el amigo que cree que los imanes pegan a todo.

## Lens decisions
- Marketing (leads): one escalating story from a testable false belief (every viewer can try a magnet on a can); fridge-magnet "one-sided" beat left out (see below).
- Scriptwriter: question hook, 5 escalating demonstrations, closing reframe that renames the object.
- Design: Coral is the background only. Board #D2EAE6 (pale teal, accent-derived, inherited from gears/clock, gate-verified); plinth = Coral ink; N pole cobalt #2F63D6; S pole **butter yellow #F5D26B** (design lens, after the gate blocked cream: cream merged with the board, distance 4.5); steel #8E9DB4 (metallic 0.25, as the tape blade), aluminium #D5DAE2, copper **#8A4421** (darker after the first gate: the first copper was 19.5 from the stage), stainless #4E586A; filings ink. Accent teal only for the field rings.

## Scientific simplifications (stated plainly)
- Filings do not travel like this in reality: they mostly rotate and shift slightly; here each sliver flies from a random place to its field line (stylised). Field lines are a two-pole (dipole) model of a bar magnet.
- The "induced magnet" caps on the clips are a symbol; "almost all of the chain drops" (soft steel keeps a little magnetism; one clip stays on the magnet).
- Aluminium and copper are not attracted in a static field (they are only very weakly para/diamagnetic); inoxidables vary by alloy (austenitic ones are nearly non-magnetic): the script says "algunos ... casi tampoco".
- NOT included: the fridge-magnet one-sided magnetisation (Halbach-like stripes). It could not be modelled accurately in the time/scene budget, so it was left out rather than drawn wrong.

## Gate
build/gate/gate.md: PASS (after changing S pole and copper). Steel clips are too thin to be measured by the gate's pixel threshold; the same steel hex passed in the tape video (23.3 from the stage).

## Defects found in QA
- Scene 2 frames 210-219: the aluminium can rendered BLACK (Cycles/denoise glitch). Re-render of those frames: see report.
