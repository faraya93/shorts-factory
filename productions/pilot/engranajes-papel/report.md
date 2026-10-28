# engranajes-papel — video 2 (new topic in the PAPEL identity), built and rendered overnight 2026-10-28
Deliverable: `final.mp4` (60.73 s = 56.73 s narration timeline + 4 s end card, 1080x1920, 30 fps, 28.5 MB; gitignored). Title: "¿Por qué el último engranaje casi no se mueve? ⚙️". $0 spend.
Contact sheet (22 frames, gitignored): `build/frames/contact-v2.png`.

## Topic choice (logged)
- **Chosen:** gear ratios / a compound gear train (family: impossible numbers/scale). **Why:** the references list "gears / gear ratios" as the single biggest hit of the numbers family (143K, docs/reference-channels.md), the family is the one the notes call most code-3D-friendly, and a gear train is a pure hard-surface rig: spur gears, shafts, a board, a block; no organics, people, cloth or fluids. One hero rig revisited in every scene.
- **Hero colours on Papel:** cobalt/deep-blue gears, vermilion input gear and crank, ink block/plinth: nothing white or silver. Hero separation from the cream stage is large (cobalt vs cream dE >> 25).
- No stall at the draft gates, so no topic switch was needed. Gate fixes (logged): scene 1 re-framed and its 1:1 pair enlarged (the pinion pair was too small to read); compound chain re-ordered in depth so every pinion sits in front of its big gear (the mechanism was hidden behind the big gears); axles now appear with their gears. 3 draft rounds of EEVEE (0.31-0.35 s/frame) + 5 low-sample Cycles stills; overlays tuned on the assembled draft once (5 positions moved).

## Script (Spanish, default voice es-CL-LorenzoNeural, 152 words, 56.6 s narration)
Hook question (the false belief: connected gears turn alike) -> one stage (10-tooth pinion into a 40-tooth gear: 4 turns for 1) -> chain of 5 stages (x4 each = 1024) -> time (1 turn/s at the input = 17 minutes for one turn of the last) -> force (what is lost in speed is gained in force) -> reframe (one image: a chain of gears does not transmit speed, it trades it for force) -> acted-out CTA (Editor phone) to "ese amigo que cree que todos los engranajes giran igual" -> end card (Papel mark, MECANALIA).
## Numbers and sources (no on-screen citations)
Every figure is arithmetic on a premise the video states: ratio 4:1 per stage (our rig's design value, 10 vs 40 teeth); 4^5 = 1,024; 1,024 s = 17.07 min ("diecisiete minutos"); "más de mil veces más fuerza, sin contar la fricción" is the ideal torque ratio 1,024 (the narration says "fuerza": the force at the block also depends on the arm length: flag for your review). No external statistic is used.

## Papel design on a different subject: how it held (stills only)
Held well: blue gears on cream are the strongest hero/stage separation of the Papel work so far (much better than the yellow tape); the vermilion input gear, crank, tension bar and counter stand out; the spoken-word ink box and white-outlined words are legible on both cream and the blue gears; the counters (ETAPA 5, 947, 17 min) sit in the safe zone; the end card with the mark reads clearly.
Weaker: the cream stage with one blue hero is calm, not loud (a stopping-power judgement I cannot measure); 34 px tag labels are small and lose contrast over the big blue gears; the pale taupe backing board looks like a ghost slab; the full-chain framing puts the top gear under the caption band (subtitles stay legible thanks to the outline); the vermilion emissive reads orange. The glow around the input gear is the accent's weakest moment, as predicted in the round-2 analysis.

## Things to know / flags
- Scene 4 is a time-lapse device: the last gear makes ONE turn while the Editor timer climbs to 17 min; only the last stages are in frame then (the input would alias at that speed). The first 2.4 s show the input at the real 1 turn/s.
- Scene 5's output arm lifts the block: kinematically consistent with the chain (output angle drives the inverse chain). 
- Samples: 128 for video 2 (video 1: 256), as instructed; denoised frames look clean on stills, flicker untested.
- Music: placeholder (Sneaky Snitch, Kevin MacLeod, CC BY 3.0): credit must be added to the description at publish. MECANALIA is the working name only; the handle is not registered.
- Mark/end card use `tools/brand_mark.py`; names list in `docs/names-general.md`.

## Actuals (Cycles Metal, 128 spp; costs.json)
| scene | frames | render s | s/frame |
|---|---|---|---|
| 1 | 250 | 2,218.3 | 8.87 |
| 2 | 366 | 3,163.8 | 8.64 |
| 3 | 323 | 3,348.6 | 10.37 |
| 4 | 172 | 1,707.9 | 9.93 |
| 5 | 285 | 2,515.6 | 8.83 |
| 6 | 151 | 1,459.2 | 9.66 |
| 7 | 155 | 1,469.4 | 9.48 |
Total 15,883 s = **4.41 h** for 1,702 frames (9.33 s/frame mean). Drafts: EEVEE ~0.31-0.35 s/frame (about 13 min for a full pass). Assembly: 60.73 s, all 24 overlays resolved, background QA dE 3.6-10.5 (ok).
