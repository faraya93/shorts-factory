# 018-por-que-tu-voz-suena-tan-rara-cuando-la-escuchas-grabada: production notes

Status: RENDERED, VERIFIED (PASS), PACKAGE BUILT AND CHECKED (2026-11-10); the owner's publish/reject verdict is pending. DRAWN from the banked tier (rank 3, replacement for returned 014, 2026-11-09). Topic: body, chain, theme voice, main tension hidden. Hook and hero route: docs/current/idea-bank.md rank 3.

## Script (5 scenes, family body, variant chain, 131 words, 43.3 s narrated; band 40-50 s)
Hook: ¿Por qué tu voz suena tan rara cuando la escuchas grabada? | false belief: el celular o el micrófono la deforman | turn: scene 4 (the bone path exists only inside your own head; a listener and the phone receive only the air) | reframe: tu voz grabada no es la rara: es la única que conocen los demás | closing: "envíaselo" with the archetype ese amigo que nunca manda audios porque no soporta escucharse. Structure rotation: 015 journey, 016 scale, 017 fork (6 scenes), 018 chain (5 scenes).

What changes in the world, per scene (flatness test: swapping any two breaks the story):
1. **hook:** the skull speaks, clean rings cross to the phone; the phone hands back a jagged red zigzag at the skull (the belief).
2. **aire:** the zigzag unspools; the same clean rings leave the mouth, cross the air and reach the phone, which wakes (record dot, level bars).
3. **hueso:** the camera goes into the skull: the bone turns to the accent from the jaw up, rings climb it, a pulse reaches the ear canal with no air gap.
4. **giro (the turn):** a second skull (the listener) enters facing the first, the phone between them; the glow stays in the speaker, only air rings reach the listener and the phone.
5. **cierre:** one wave of air crosses the row; every receiver lights at once; the camera pulls back and up.

## Beat sheet (event, word lock, overlay)
| Scene | Event on screen | Word locks | Overlay |
|---|---|---|---|
| 1 | rings emitted from the mouth every 0.7 s; zigzag grows phone to skull | "celular" (zigzag), emissions from 0.4 s | none |
| 2 | zigzag unspools 0.4-1.4 s; rings from "sonido"; record dot on first arrival | "sonido", "aire" | AIRE tag at "aire" |
| 3 | bone tint ramps at "vibrar"; bone rings climb; ear pulses from "oído" | "vibrar", "hueso", "oído" | HUESO tag at "hueso" |
| 4 | glow held, ear pulses on "grave/llena"; listener pops on "demás"; glow fades at "solo"; air rings from "aire" | "demás", "aire" | none |
| 5 | wave from "única", receivers light on arrival; pull-back | "única" | ENVÍASELO tag at "Envíaselo" |

## Sources and numbers (no number is stated or rendered; none invented)
- Bone conduction adds to the air-borne sound when you hear your own voice, and emphasises low frequencies (Wikipedia "Bone conduction"; Maurer and Landis 1990, Folia Phoniatrica, "Role of bone conduction in the self-perception of speech": cited from memory, **flagged to confirm**). The narration says only "más grave y más llena".
- A microphone records the air-borne sound only.

## Scientific simplifications (stated plainly)
- The vocal cords sit in the throat; the rings start at the mouth and the bone glow rises from the jaw. Bone conduction really runs through the whole head; the ear pulse stands for it. The skull stands for the head.

## Routing and elements
- Hero: `human-skull` (library asset, BlenderKit Royalty-Free; sealed 2026-11-10, QA pass, isolated blind reading 96/96/97). Phone: code primitive (genuinely geometric). Sound rings, bone tint, ear pulses and the zigzag are energy graphics in the doctrine's emissive language.
- Declared `scene_elements` in script.json; visibility entries for each.

## Cost classes
All five scenes `opaque` (no glass, water or volumes): predicted 2-3 s/frame (54k-poly skull, a handful of tori), none above 15, no cost_restage.

## Publish package (Spanish; the owner publishes)
- **Título:** ¿Por qué tu voz suena tan rara cuando la escuchas grabada? 🎙️
- **Descripción:** ¿Por qué tu voz suena tan rara en una grabación? Porque el celular no la deforma: tú te oyes por el aire y también por el hueso del cráneo.
  Y ese hueso añade graves que los demás nunca oyen, ni la grabación tampoco. 🎙️ Envíaselo a ese amigo que nunca manda audios porque no soporta escucharse.
  Música: ninguna (sin pista y sin crédito; decisión del dueño 2026-11-01)
- **Hashtags (description, not title):** #voz #cuerpohumano #shorts

## Reshape ladder log 2026-11-10 (logged in lens-decisions.md, same date)
- **Scene 4 (two skulls and the phone), rung 1:** first staging (phone full size, dead centre between the skulls, camera far) read 90/60/60: "smartphone between two skulls", "smartphone standing on a shelf" (the phone dominated). Re-staged with the phone at 62% scale, the listener moved closer and the camera nearer: 70/70/70, all three first guesses named the skulls.
- **Scene 5 (the row), rung 1, three re-stagings:** (1) phone centred in front, camera far: 55/80/85, two readers named the phone first; (2) phone moved behind the row at 55% scale, ring streams to both receivers, rings thickened for the visibility bar: the overlapping edge-on rings read as "a teal key" 55/45/60; (3) ring stream to the phone removed, one slimmer stream between the skulls: 60/60/75 PASS; (4) wider single wave for the visibility bar (0.34 then 0.63 against 0.8), camera azimuth opened so the rings are arches and not edge-on slabs: 60/45/88 PASS (mean 64.3; lowest reader exactly at the 45 floor). No alias added, no floor lowered.
- **Scene 1 and 2 phone readings:** the phone passes with the skull named first in scene 1 (phone listed as an alternative by all three readers; the tool counts the alias as present); scene 2 restaged on the phone close-up (88/85/88 before the ring change; 90/88/80 after).
- Aliases were fixed before every reading and none was added. The hero was unfrozen once (the Phone scale argument touched the rig module the hero fingerprint reaches), re-read (70/92/85, then 92/95/90 after ring edits that changed the still) and frozen again.

## Gate record
Colour gate PASS after four support-colour tries (cream plate, mint, slate blue BLOCKED against the pale hero colours; final: sky-blue plate #86B7E3, ivory bone #EAE0B8, ivory phone body with a plate-coloured screen; reasons in script.json support_colours). Hero `human-skull` neutral blind reading 96/96/97, hero still 95/92/92 (first), 70/92/85 and 92/95/90 (re-reads). Every element read and carried or re-read; visibility PASS on all eleven entries (rings were first thin: 0.15-0.7 % of the frame against the 0.8 % bar, fixed on the element with thicker, denser rings, never by moving the threshold).

## Draft log (EEVEE, advisory)
- First draft: bone glow as a full emission mix flooded the skull to a flat silhouette; replaced by a colour tint toward the accent plus 30% emission. Cameras were far too tight (the 9:16 frame at radius 100 holds about 55 units across); widened, with a non-zero azimuth so the rings read as ellipses rather than slits. Ring shadows removed (rings no longer cast shadows).

## REPORT 2026-11-10 (finish after the queued final)
- **Render:** chain log `output/chain-018-por-que-tu-voz-suena-tan-rara-cuando-la-escuchas-grabada.log`: START 14:04:03, DONE 14:57:07 (53 min wall, five scenes), no FAILED / INCOMPLETE / Traceback and no retry warning. `final.mp4` 1080x1920 H.264/AAC, 30 fps, 43.33 s, plus `cover.jpg`. $0 fal spend (code3d). Launched through `tools/queue_final.py` (under caffeinate via the chain).
- **Verify:** `tools/verify_production.py` PASS. `publish_package.py build` and `check` OK (hashtags `#voz #cuerpohumano #shorts`). Nothing published.
- **Estimate vs actual:** all five scenes were predicted `opaque` (2-3 s/frame, no cost_restage); the chain took 53 min wall including the encode, for about 1,300 frames. The session itself was long mainly because of the colour gate (four support-colour tries) and the scene 4 and 5 re-stagings, not render cost. Asset job (skull): about 15 min, $0.
- **Dynamism audit (mechanical, from drafts and gate stills; I cannot watch the video):** each scene stages a visible change and a travelling camera: orbit as rings cross and the zigzag grows (1), tracking from the phone to the mouth and back to a phone close-up as it wakes (2), push in to the skull as the bone turns teal and rings climb (3), pull-back as the listener enters and the glow fades (4), a wave crossing the row with a pull-back and rise (5). Scene 5 is the quietest. The lenses' contact-sheet check and the owner's eye remain the last gate.
- **Flags:** the phone passes in scenes 1, 4 and 5 with the readers naming the skull first and the phone as an alternative (the tool counts the alias); scene 5 passed with its lowest reader exactly at the 45 floor (60/45/88); the bone-conduction citation (Maurer and Landis 1990) is from memory and **to confirm**; the skull stands for the whole head and the vocal cords are not drawn (simplifications above); the ring streams are stylised energy graphics, not to scale. Owner-only: the publish/reject verdict.
- **Not done:** no idea-bank change (the draw was marked 2026-11-09); the bank sits below working depth, a refill is due and is not run by a production session. The asset is Royalty-Free (no CC0 stylised skull exists), with no credit in the description.

## BATCH DIRECTIVE 2026-11-09 (runner)
Write the script at production time under the standing flatness check, then produce under standing doctrine, measuring the riskiest element first; a figure with no source comes out of the script. If this topic fails beyond the Reshape ladder, return it only with `.venv/bin/python tools/return_topic.py <prod> --reason "..."`. Under gate_version 2 including the visibility check. No publishing, no spend, no accounts.

- UNFREEZE 2026-11-10: scene 4 and 5 rung 1 restage, voz_rig Phone gained a scale argument and the listener moved, hero still pixels unchanged, hero re-read before any other scene
