# puntos de sutura, v7 "cutaway": beat sheet for approval (NOTHING GENERATED, $0)

Status: DRAFT for owner approval. No scenes.json, no render, no fal call exists for v7. Doctrine: CLAUDE.md "Reference doctrine"; rules R1-R16 are those of docs/reference-format-spec.md; look rules are those of docs/reference-style-spec.md.
Baseline: the v4 narration and its measured word timings (productions/pilot/puntos-de-sutura-v4-code3d/audio/scene-0N.words.json). Word-lock offsets below are SECONDS FROM THE START OF THE SENTENCE, taken from those timings, so they stay valid when the lines shift; the two new lines and the new hook need TTS before their offsets exist.

## 0. Concept in one paragraph
ONE hero rig: a side-on WOUND BLOCK (skin layers in passive greys, a V-shaped cut, a pair of lips) and the CURVED NEEDLE. The whole video lives on this rig; each fact adds exactly one element to it (ledger in section 3) and the camera never rests. Gold = the active quantity (thread tension, healing tissue); everything else is grey; teal = labels and brackets; red = failure. The hook is a CONTRAST on one stage: a straight sewing needle and the curved surgical needle each try to pass through BOTH lips of the same wound; the straight one fails.

## 1. Narration (lines to approve)
Lines L2-L8 are the owner-approved v4 script, unchanged. Three lines are NEW or REPLACED and need your approval:

| # | Line | Status |
|---|---|---|
| H | "¿Por qué la aguja recta no sirve para coser una herida?" | NEW, replaces v4's "¿Cómo funcionan los puntos de sutura?" (a "¿Cómo…?" opener, which flopped in the references and names no needle, so it cannot carry the contrast hook). Approved opening family for body: "¿Por qué…". Everyday object (a sewing needle) + the false belief ("any needle works"). ~11 words, ~3.6 s. |
| L2 | "Cuando el corte es profundo, los bordes de la piel quedan demasiado lejos para cerrar solos." | v4 |
| L3 | "Por eso el médico usa una aguja curva: su forma permite coser sin desgarrar más tejido." | v4 |
| L4 | "El hilo acerca los bordes y los mantiene unidos, porque una herida cerrada sana más rápido y deja menos cicatriz." | v4 |
| L5 | "Cada punto se asegura con nudos diminutos, para que nada se suelte." | v4 |
| L6 | "Algunos hilos son absorbibles y tu cuerpo los disuelve solos: esos nunca hay que sacarlos." | v4 |
| L7 | "Pero si dejas los normales demasiado tiempo, la piel crece sobre el hilo y retirarlos se vuelve un problema." | v4 |
| L8 | "Y el dato más loco: durante siglos se usaron hormigas vivas como puntos, porque al morder cerraban la herida con sus mandíbulas." | v4 |
| C1 | "Un punto de sutura no cierra la herida: la mantiene unida mientras tu cuerpo hace el trabajo." | NEW to the spoken script: it is the production's `closing_reframe` field, which the v4 narration never spoke (a known script gap) |
| C2 | "Sígueme, y envíaselo a ese amigo que se corta cocinando y dice que no necesita puntos." | NEW to the spoken script: built from the production's `share_archetype` field |

Length: v4 was 43.9 s; with H, C1 and C2 the narration is about 55 s (estimate at 2.87 words/s) plus a 4 s end card, about 59 s total. The body band in CLAUDE.md is 40-50 s and the standard band 45-60 s, so this is over the body band by ~5 s and inside the standard band. Decision needed (section 6).

## 2. Beat sheet: every line mapped to visual EVENTS, word-locked

Event types: XRAY, TRANSFORM, MULT, SCALE, CONTRAST, BEFORE/AFTER, METAPHOR, NUMBER, SOURCE, CTA. "t+" = seconds from the sentence start (measured v4 timings; H, C1, C2 TBD at TTS). Labels are tiny ALL-CAPS Spanish Editor overlays with leader lines; subtitles highlight the keyword at the same instant (R12).

### Line H (0.0-~3.6 s): HOOK = CONTRAST (R2). The contrast must resolve inside 3 s.
| # | Word lock | EVENT | Rig element | Camera | Graphics / colour |
|---|---|---|---|---|---|
| 1 | 0.0 s (before the first word) | Stage: two IDENTICAL wound blocks side by side on the void, each with a V-cut; a straight needle hovers over the left block, the curved needle over the right. Both needles grey. | wound block (x2), straight needle, curved needle | wide, slow push-in | labels RECTA (left) and CURVA (right) appear as the words "aguja recta" are spoken; teal |
| 2 | "aguja" ~0.9 s (TBD) | CONTRAST: both needles drive into the left lip at the same moment. The straight needle can only go straight down: its tip leaves through the base of the tissue, the path traced RED, a red tear running up the block; it never reaches the right lip. The curved needle swings along its arc under the gap and exits the RIGHT lip; its path traced GOLD. | straight/curved needle paths | tracking push toward both | red X over the left block; gold ring at the right exit |
| 3 | "sirve" ~2.5 s (TBD) | Result hold + push-through: the camera pushes into the right block (the rig); the left block drops to a dim ghost and slides out. | the right block becomes THE hero rig | push-through | no label |

### Line L2: "Cuando el corte es profundo, los bordes de la piel quedan demasiado lejos para cerrar solos."
| # | Word lock | EVENT | Rig element (+1) | Camera | Graphics / colour |
|---|---|---|---|---|---|
| 4 | "corte" t+0.36 | TRANSFORM + XRAY: the cut opens; the cutaway shows the layer stack (epidermis, dermis, fat). | layers visible | orbit down to a 3/4 side-on view | labels PIEL, GRASA |
| 5 | "profundo" t+0.78 | The V is outlined in teal and a vertical depth bracket pulses (NO figure, see number audit). | depth bracket | push-in | teal bracket |
| 6 | "bordes" t+1.59, "piel" t+2.15 | The two lips are tagged. | lips | continue | labels BORDE x2 |
| 7 | "demasiado lejos" t+2.65-3.15, "cerrar solos" t+3.72-4.05 | BEFORE/AFTER: a horizontal bracket spans the gap; the lips spring toward each other and fall back (they cannot close alone). | gap bracket | slow orbit | small red X on the failed closing |

### Line L3: "Por eso el médico usa una aguja curva: su forma permite coser sin desgarrar más tejido."
| # | Word lock | EVENT | Rig element (+1) | Camera | Graphics / colour |
|---|---|---|---|---|---|
| 8 | "médico" t+0.46, "aguja curva" t+1.21-1.58 | The curved needle, now held by a steel needle-holder, enters from the right. | needle-holder | push-in | none |
| 9 | "forma" t+2.14 | SCALE + TRANSFORM: a dotted teal ring draws the full CIRCLE the needle belongs to, then the camera pulls back so the arc and the wound sit inside it. | arc guide | pull-back | teal dotted circle |
| 10 | "coser" t+3.05 | The needle follows the arc: in through the left lip, under the gap, out through the right lip, trailing the thread. | THREAD (first appearance) | tracking orbit | thread grey, the needle's path glows gold only while it moves |
| 11 | "sin desgarrar" t+3.59-4.22 | CONTRAST callback: the hook's red tear path of the straight needle flashes beside the clean curved path; the tissue around the curved path stays intact. | ghost path from the hook | hold + slow orbit | red ghost vs gold path |

### Line L4: "El hilo acerca los bordes y los mantiene unidos, porque una herida cerrada sana más rápido y deja menos cicatriz."
| # | Word lock | EVENT | Rig element (+1) | Camera | Graphics / colour |
|---|---|---|---|---|---|
| 12 | "hilo" t+0.18, "acerca" t+0.34 | TRANSFORM: the thread is pulled taut; a gold tension glow runs along it and the lips slide together. | TENSION glow | push-in | gold = tension (the active quantity) |
| 13 | "unidos" t+1.82 | The lips meet at a hairline; the thread stays lit while it holds. | closed state | hold + orbit | none |
| 14 | "herida cerrada" t+2.92-3.19, "sana más rápido" t+3.62-4.07 | MULT + BEFORE/AFTER: the wound is copied; the left copy stays open, the right copy is closed; two healing bars fill, the closed one finishes first. The bars carry NO figures (number audit). | second wound copy, healing bars | pull-back to show both | gold fill on the bars |
| 15 | "menos cicatriz" t+5.06 | SCALE: macro on the two healed skin surfaces: a wide scar line vs a hairline. | macro surface | push-in | none |

### Line L5: "Cada punto se asegura con nudos diminutos, para que nada se suelte."
| # | Word lock | EVENT | Rig element (+1) | Camera | Graphics / colour |
|---|---|---|---|---|---|
| 16 | "punto" t+0.28, "asegura" t+0.63 | SCALE: dive to the thread exit: a knot is tied (loop crosses and tightens). | KNOT | push-through | label NUDO |
| 17 | "nudos diminutos" t+1.24-1.53 | MULT: pull back along the wound; the stitch repeats left to right, each with a knot that pops in. NO counter (no figure). | stitch row | pull-back | none |
| 18 | "nada se suelte" t+3.04 | CONTRAST: an end is tugged. A stitch WITHOUT a knot slides out and the lips reopen (red); the knotted stitch holds (gold tension surge along the row). | unknotted counter-stitch | tracking | red vs gold |

### Line L6: "Algunos hilos son absorbibles y tu cuerpo los disuelve solos: esos nunca hay que sacarlos."
| # | Word lock | EVENT | Rig element (+1) | Camera | Graphics / colour |
|---|---|---|---|---|---|
| 19 | "absorbibles" t+0.78 | Two thread types sit in the tissue; the pale one is tagged. | absorbable thread | cutaway orbit | label ABSORBIBLE |
| 20 | "cuerpo" t+1.61, "disuelve" t+2.04 | XRAY + TRANSFORM: small body cells (yellow-green) gather; the pale thread breaks into particles from the middle. A progress ring fills with NO figure (number audit). | body cells | push-in | yellow-green cells, ring |
| 21 | "nunca" t+3.30, "sacarlos" t+3.88 | CONTRAST: tweezers come toward the empty path, a red X appears, they retreat. | tweezers | hold | red X |

### Line L7: "Pero si dejas los normales demasiado tiempo, la piel crece sobre el hilo y retirarlos se vuelve un problema."
| # | Word lock | EVENT | Rig element (+1) | Camera | Graphics / colour |
|---|---|---|---|---|---|
| 22 | "normales" t+0.80 | The dark non-absorbable thread stays; it is tagged. | normal thread | orbit | label NORMAL |
| 23 | "demasiado tiempo" t+1.21-1.74 | A time-lapse ring sweeps (NO figure); new skin tissue starts to grow from both lips, glowing gold. | growth front | push-in | gold = growth |
| 24 | "piel crece sobre el hilo" t+2.49-3.32 | BEFORE/AFTER + XRAY: the new epidermis overgrows and buries the thread. | buried thread | cutaway, tilt | none |
| 25 | "retirarlos" t+3.62, "problema" t+4.69 | The tweezers pull; the thread will not come: the tissue tents upward, red flash on the tent. | tweezers again | tracking | red |

### Line L8: "Y el dato más loco: durante siglos se usaron hormigas vivas como puntos, porque al morder cerraban la herida con sus mandíbulas."
| # | Word lock | EVENT | Rig element (+1) | Camera | Graphics / colour |
|---|---|---|---|---|---|
| 26 | "dato más loco" t+0.27-0.73 | Transition: the camera pulls out and tilts the rig flat; a chunky ant silhouette crosses the lip. | ant silhouette | pull-out | none |
| 27 | "durante siglos" t+1.32-1.65 | NUMBER (flagged): a timeline bar spans the frame left to right with the single word SIGLOS. NO figure until sourced (number audit). | timeline chip | static graphic over a slow drift | teal chip |
| 28 | "hormigas vivas" t+2.45-2.90 | The ant (chunky, from primitives) walks to the wound. | ANT | push-in | none |
| 29 | "morder" t+4.40, "cerraban" t+4.70 | SCALE + TRANSFORM: zoom on the jaws; they clamp BOTH lips; the lips pull together. No gore: the ant stays whole. | jaws | macro push | gold pinch at the clamp |
| 30 | "mandíbulas" t+5.94 | MULT: two more ants clamp along the wound; it is closed. | ant row | pull-back | none |

### Line C1 (reframe, ~5.9 s, TBD): "Un punto de sutura no cierra la herida: la mantiene unida mientras tu cuerpo hace el trabajo."
| # | Word lock | EVENT | Rig element | Camera | Graphics / colour |
|---|---|---|---|---|---|
| 31 | whole line | THE SINGLE IMAGE (R10): the rig in cross-section, the thread as a GREY inert line holding the two edges; beneath it a GOLD fibre bridge grows across the gap (the body's work). Frozen composition, slow orbit only. On "no cierra" the thread dims to grey; on "tu cuerpo" the gold bridge begins; on "hace el trabajo" it completes. | gold bridge | slow orbit | gold = the active quantity |

### Line C2 (CTA, ~5.6 s, TBD): "Sígueme, y envíaselo a ese amigo que se corta cocinando y dice que no necesita puntos."
| # | Word lock | EVENT | Graphics / colour |
|---|---|---|---|
| 32 | "Sígueme" | CTA acted out: the rig shrinks into a generic phone frame (no platform logo); a finger taps a FOLLOW button. | placeholder UI |
| 33 | "envíaselo" | Share sheet with four avatar circles; the finger picks one. | placeholder |
| 34 | "ese amigo... no necesita puntos" | Chat: friend bubble "solo es un corte, no necesito puntos" (Editor overlay text, Spanish, for your approval); a SENT tick. | placeholder text |

### End card (~4 s, PLACEHOLDER)
35. The last frame dims to ~25% brightness; a placeholder logo glyph and "@[CANAL]" fade in (channel name and handle are not decided; nothing invented).

Density check: 35 events across ~55 s of narration = about 1.6 s per event, denser than the references (3.4-5 s). Several events are sub-beats of one idea; grouped by idea the video has about 20 beats, roughly 2.8 s each, still denser than the references. Option: trim the sub-beats if it feels busy.

## 3. Hero-rig ledger (+1 element per fact)
Hook: wound block + straight needle + curved needle -> L2: layer labels, depth bracket, lip tags, gap bracket -> L3: needle-holder, arc guide, THREAD, ghost path -> L4: TENSION glow, second wound, healing bars, macro skin -> L5: KNOT, stitch row, unknotted counter-stitch -> L6: absorbable thread, body cells, tweezers -> L7: normal thread, growth front, buried thread -> L8: ant (and two more) -> C1: gold bridge -> C2: phone frame. The camera orbits, pushes or pulls in every event; no static hold exceeds ~1 s.

## 4. Number audit (R5: every number is a screen object; no source = flag, never invent)
The v4 narration contains ONE explicit quantity word and several implied quantities. No digit appears in the script and the repo holds NO source for any figure. Nothing below is shown as a figure.

| Where | Quantity in the narration | Screen object planned | Status |
|---|---|---|---|
| L8 | "durante siglos" (centuries) | timeline chip with the word SIGLOS only (event 27) | FLAG: no source and no figure. Also the claim itself ("live ants used as stitches, for centuries") has no source in the repo. Needs your source or approval before production. |
| L4 | "más rápido" (heals faster) | two healing bars, no figures (event 14) | FLAG: if you want figures (healing time of closed vs open wounds) they need a source. |
| L7 | "demasiado tiempo" (too long) | time-lapse ring, no figure (event 23) | FLAG: a day counter (when stitches should come out) would be the strongest object here; the figure varies by body site and needs a source. |
| L6 | dissolving time of absorbable thread | progress ring, no figure (event 20) | FLAG: needs a source before any chip. |
| L2 | "demasiado lejos" (gap distance) | bracket, no figure (event 7) | FLAG: no figure. |
| L5 | "cada punto" (how many stitches) | stitch row, no counter (event 17) | no figure used |

Net: the references carry numbers on almost every beat (counters, chips, years). This script has none, so these beats are weaker than the references until sources are supplied; this is the main content gap.

## 5. Doctrine compliance (format spec rules)
R1 every sentence an event: yes (35 events). R2 hook contrast in 3 s: events 1-3. R3 cutaway: events 4, 20, 24. R4 multiplication: events 14, 17, 30. R5 numbers as objects: BLOCKED by sourcing (section 4). R6 counter-actor: events 11, 18, 21. R7 named-person micro-scene: not used (no "imagine" line in the script). R8 cards/citations: none (needs sources). R9 home experiment: not applicable. R10 reframe single image: event 31. R11 acted-out CTA + end card: events 32-35. R12 word-lock: columns above (offsets measured for v4 lines). R13 meaningful transitions: events 3, 16, 26. R14 one rig revisited: yes. R15 labels while named: yes. R16 colour semantics: gold only for tension/growth/measured thing.

## 6. Decisions I need from you
1. Hook: approve the replacement H, or give your own line (it must name the needle so the contrast reads).
2. Approve C1 and C2 as spoken lines, and accept ~55 s of narration (over the 40-50 s body band) or ask me to cut lines.
3. Numbers: supply sources/figures for any of the six slots in section 4, or approve shipping without figures (weaker against the references). The "siglos" ant claim needs a source either way.
4. Editor work: the target subtitle style, leader-line labels, chips and counters at arbitrary positions do not exist in factory/editor.py yet (it still has the old dark-box subtitles and centre-placed counters). Building them is a separate task; I will estimate it only after this beat sheet is approved.
5. Engine: code3d (rigid cutaway rig, emissive accents) per the engine rules; the estimate table follows approval.
6. Channel name, handle and logo for the end card (placeholder until then); and whether the CTA phone mock should avoid any platform branding (it is drawn generic here).
