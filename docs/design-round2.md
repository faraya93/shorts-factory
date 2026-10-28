# Design round 2 — five identity directions from zero (owner pick pending)

Nothing is applied: `channels/umbrella-es.yaml` and `CLAUDE.md` are untouched; no full re-render; $0. Round 1's celeste is not a starting point
(it appears nowhere below except as a thing to avoid copying). Reused infrastructure only: palette math (`tools/palette_metrics.py`), s/frame method, Editor
text themes (now generated per direction from `factory/directions.json`), `code3d/lib/looks.py` (`look=<direction>`).

## 0. Process (Tastemaker, in order) and its limits
1. **Reference study first.** The only references we have are the three dark-stage example channels (docs/reference-style-spec.md; Tastemaker's
   `extract_palette.py` on their frames: dominant colours #1E222A, #0D0C0E, #101821 ... = near-black navy/neutral). Everything else is the owner's description of Zack D Films
   (light-blue backdrop, taken as stated: I could not find any source confirming it; the one web search returned only generic "cinematic 3D" listings).
   Evidence on colour and views is thin and conflicting: one vendor-cited study says saturated backgrounds beat muted/dark by 8-14% CTR, another source says dark saturated wins
   for music thumbnails, a third says contrast matters more than palette; none is Shorts-specific. **There is no verified evidence that any hue wins views.** The directions
   are therefore judged on measurable proxies: phone legibility (contrast), hero separation, accent clarity, ownability against the references, cost.
2. **Palette lock with contrast math.** I swept hue (every 15 deg) x lightness x chroma for the stage and scored weighted CIEDE2000 separation of 12 everyday hero colours
   plus text feasibility (some text colour >= 4.5:1). Finding: mid-dark saturated stages (L* ~40) separate heroes best (score 0.97-0.98), light stages worst (0.83 for cream,
   0.91-0.94 for pastels) because white/silver/grey objects merge with light backdrops. I then chose five directions to be different in hue family AND value strategy,
   and tuned each tone from that sweep.
3. **Style lock + decisions log:** `.tastemaker/` updated (pending-review entries).
4. Design-taste principles applied: one dominant colour, one accent, restraint, specificity; the channel's measured system wins where web-UI taste conflicts.
Two things I changed after rendering because the stills exposed them: **accents that share a hue with a common hero fail** (the gold/lime accent on Esmeralda/Violeta
is the same yellow as the tape's housing: spring invisible, dE 2 vs the housing); accents were re-chosen against the hero set, not only the stage.

## 1. The five directions (each a mini-system; hexes in `factory/directions.json`)
| | stage (top -> bottom, screen-space gradient) | value / hue family | hero grounding | accent = the active quantity | subtitle | mark | ownability argument |
|---|---|---|---|---|---|---|---|
| **ESMERALDA** | #1F8570 -> #1A6E5C (L* 50 -> 41) | mid-dark vivid / green | cream plinth #F4EFE0 + soft shadow | white-hot cream #FFF1B8 (spring/glow reads as light) | white words, 4 px deep-green outline; spoken word in a white box with green text | cream rounded square, quadrant cut revealing the stage, accent dot | the dark-green education palette without the dark: borrows from none of the three references (dark navy/black) nor a light-blue stage |
| **VIOLETA** | #7A4DE8 -> #5B30C2 (L* 46 -> 34) | mid-dark vivid / violet | pale-lilac plinth #EDE7FF | mint #3DFFB0 (a cool neon: stands off the yellow/red heroes) | white words, deep-violet outline; spoken word in a white box with violet text | lilac disc with a cut wedge + mint dot | violet + mint neon is the one pairing none of the references or the celeste stage uses; instantly recognisable as a thumbnail-sized colour field |
| **MANDARINA** | #FF9A4A -> #F26A1D (L* 73 -> 61) | high-key vivid / orange | near-black plinth #1B1410 | cobalt #1B3BD6 (complement: strongest hue contrast) | ink words, white outline; spoken word in an ink box with white text | ink square, cut quadrant, cobalt dot | warm saturated field + cobalt energy: the loudest option, opposite pole to every dark reference |
| **ROSA** | #FFB6C0 -> #F48FA0 (L* 81 -> 70) | high-key pastel / pink | plum plinth #4A1A3A | deep emerald #0A5C45 | plum words, white outline; spoken word in a plum box | plum disc + cut wedge + emerald dot | pink stage is almost unclaimed in mechanism/tech content (my judgement; I did not survey the niche) — maximum difference, highest audience-skew risk |
| **PAPEL** | #FDF3DC -> #EFE2C4 (L* 96 -> 90) | high-key neutral / warm cream | ink plinth #1D1B2E | vermilion #F0421C | ink words, white outline; spoken word in an ink box | ink square, cut quadrant, vermilion dot | editorial paper-and-ink: the hero's real colours ARE the colour system; weakest on stopping power by construction |
Shared: real hero colours (yellow tape / black rubber / steel; red-and-white thermos), same cheap studio lighting (tuned) so cost differences are the palette's own,
contact shadow on a Cycles shadow-catcher floor, no vignette/halo, Montserrat ExtraBold, same overlay geometry as docs/design-system.md section 3-4.

## 2. Measured table per direction (tools/palette_metrics.py; WCAG 2.x ratios, CIEDE2000 dE)
| direction | unspoken-word text on stage (top / bottom) | spoken word (box) | accent vs stage (WCAG top/bottom) | accent hue contrast (dE vs stage) | accent vs yellow tape / red hero (dE) | error on stage (top/bottom) | plinth vs stage (dE) |
|---|---|---|---|---|---|---|---|
| ESMERALDA | 4.5 / 6.1 | 12.7 | 4.0 / 5.4 | 42 | 19 / 54 | 2.0 / 2.7 | 40 |
| VIOLETA | 5.2 / 7.9 | 14.7 | 4.0 / 6.1 | 63 | 40 / 83 | 2.7 / 4.1 | 43 |
| MANDARINA | 8.6 / 5.9 | 18.2 | 3.8 / 2.6 | 58 | 80 / 44 | 5.4 / 3.7 | 51 |
| ROSA | 9.9 / 7.2 | 16.4 | 4.8 / 3.5 | 63 | 54 / 58 | 4.3 / 3.2 | 50 |
| PAPEL | 15.2 / 13.1 | 16.8 | 3.5 / 3.0 | 40 | 40 / 13 | 5.9 / 5.1 | 83 |
Targets: unspoken words >= 4.5 (all pass; Esmeralda's top end is borderline at 4.5), spoken word >= 7 (all pass), accent >= 3:1 for graphics (Mandarina and Papel bottoms
fall slightly short; they rely on hue contrast), error marks always carry an outline (error alone is 2.0-5.9). Wrinkle: Esmeralda's accent vs the yellow tape is only dE 19
(readable as a glow in the still, but the weakest accent/hero pair); Papel's vermilion vs a red hero is dE 13.

### Hero separation (min CIEDE2000 over stage top/bottom; <20 merges, 20-25 weak)
| direction | worst heroes | count < 20 | count < 25 |
|---|---|---|---|
| ESMERALDA | green bottle 18, mid-grey tool 25, black 34 | 1 | 2 |
| VIOLETA | purple 6, blue 17, mid-grey 24 | 2 | 3 |
| MANDARINA | orange 5, yellow tape 20, red thermos 22 | 2 | 3 |
| ROSA | pink 8, silver 22, white appliance 24 | 1 | 3 |
| PAPEL | white appliance 8, silver 16, yellow tape 21 | 2 | 3 |
Every direction has a hue-matched hero it cannot separate by colour alone (green on green, purple on violet...). The stills show the plinth + shading carries white/silver
parts in all five; the weak ones are Papel (white cap barely separates) and Mandarina (orange/yellow heroes).

### Render cost (s/frame, real scenes 1, 3, 5; Cycles Metal, 128 spp, adaptive 0.03, 4 bounces; 6-frame benchmark minus ~4 s startup)
| config | scene 1 | scene 3 | scene 5 | mean | vs dark | est. 1,920 frames |
|---|---|---|---|---|---|---|
| dark A (real colours) @128 | 3.83 | 3.50 | 4.50 | 3.94 | 1.00x | ~2.1 h |
| ESMERALDA | 6.83 | 5.83 | 8.16 | **6.94** | 1.76x | ~3.7 h |
| VIOLETA | 7.33 | 6.66 | 8.50 | 7.50 | 1.90x | ~4.0 h |
| MANDARINA | 7.33 | 6.66 | 8.00 | 7.33 | 1.86x | ~3.9 h |
| ROSA | 7.50 | 6.66 | 8.00 | 7.39 | 1.88x | ~3.9 h |
| PAPEL | 7.66 | 6.66 | 8.00 | 7.44 | 1.89x | ~4.0 h |
Palette barely changes cost (6.9-7.5 s/frame); what costs is the bright shadow-catcher studio itself, about 1.8-1.9x the dark stage at equal settings. Quality at 96-256 spp was
indistinguishable on stills in round 1; flicker is untested. A bright direction costs about +1.6-1.9 h per 64 s video; no direction is a cost outlier.

## 3. Validation sheets (same three moments as round 1; columns ESMERALDA | VIOLETA | MANDARINA | ROSA | PAPEL)
- `docs/design-round2/sheet-1_tape_wide_midgrowth.png` — scene 3, counter 3.2 m climbing, subtitle with spoken-word box.
- `docs/design-round2/sheet-2_glowing_quantity_spring.png` — scene 5, glowing spring + TENSIÓN bar + tag label (the active-quantity moment).
- `docs/design-round2/sheet-3_red_white_thermos.png` — versatility; subtitle with key-word box.
- `docs/design-round2/marks.png` — five mark directions on their stages with a placeholder wordmark.
What the stills show (stills only, no motion): all five keep the subtitle hierarchy (spoken word reversed in a box) legibly; the red thermos reads on all five (least on Mandarina and Papel's
warm fields); the glowing spring reads clearly on all after the accent fix; Papel is calm but has the least pop; Rosa and Mandarina are loud; the thermos's white cap is softest on Papel.

## 4. My recommendation: VIOLETA (runner-ups: ESMERALDA, MANDARINA)
Why VIOLETA, in order of weight:
1. **Accent clarity is the best of the five:** mint on violet is 4.0-6.1:1 and dE 63, and mint is far from the yellow and red heroes (dE 40 / 83). The "active quantity" moment is the format's signature; this direction makes it pop most reliably.
2. **Text:** white words and a white spoken-word box with violet text keep the reference's white-bold subtitle grammar (5.2-7.9:1 unspoken, 14.7 spoken), so the Editor grammar the references proved is intact.
3. **Ownability and grid recognition:** violet + mint neon matches none of the three references (dark navy/black) or the celeste you rejected; a violet block is identifiable at thumbnail size. (My claim about the wider niche is a judgement, not a survey.)
4. **Cost** is average for the bright set (1.9x, ~4.0 h per video).
Honest risks: purple and blue heroes fall into the stage (dE 6 and 17: rare objects, but real); the lower end of the gradient (L* 34) is darker than you asked for: if it reads too dark, lighten
the bottom to ~#6A42D6 (no re-render needed for a decision, a re-validation yes); and nothing proves violet wins views.
When I would choose otherwise: ESMERALDA if hero separation and cost matter most (best separation, cheapest at 6.9 s/frame, keeps the gold-like accent idea) at the price of a more conventional
"educational green"; MANDARINA if you want the loudest stopping power and can accept orange/yellow heroes being weak. PAPEL and ROSA I do not recommend as the constant: Papel loses white/silver
heroes and has the weakest pop; Rosa carries the highest audience-skew risk. No dark direction is proposed: the sweep's best separation is mid-dark, which I included (Esmeralda, Violeta) at L* 41-50, not the very dark stages you ruled out.

## 5. Names (Abre las Cosas rejected) — 12 new, grouped by strategy
Handle checks run 2026-10-27 from this machine, public web only. **What I could verify:** YouTube: `youtube.com/@handle` returns 404 when no channel exists (negative control: a nonsense handle 404, known channels 200).
TikTok: a missing account's page carries `statusCode 10221` (negative control and positive controls behaved as expected). Instagram: an existing profile exposes its `og:title`; a missing one returns a generic login page,
indistinguishable from being blocked — so "no public profile page" is **probable but unreliable** availability. **What I could not verify:** that any handle is actually registrable/unreserved/not banned, other platforms, domains,
trademarks (a single web search per name found no business or channel called Mecanalia, Míralo por dentro, Piezalia or Desmontalia; that is weak evidence, not clearance), or how the names sound to native speakers across countries.
Format note: the format's hook is a "¿Por qué…?" question, so the question-style names echo it.
| strategy | name | handle | YouTube | TikTok | Instagram | rationale |
|---|---|---|---|---|---|---|
| imperative | **Míralo por Dentro** | @miralopordentro | free | free | no profile page | an invitation, 3 words, says the format; neutral in every country |
| imperative | **Mira Qué Hay Dentro** | @miraquehaydentro | free | free | no profile page | curiosity gap as an order; longer |
| imperative | **Asómate Adentro** | @asomateadentro | free | free | no profile page | "peek in": playful, light; "adentro" reads Latin-American |
| descriptive | **El Interior de las Cosas** | @elinteriordelascosas | free | free | no profile page | plain and searchable; long handle |
| descriptive | **Radiografía de Objetos** | @radiografiadeobjetos | free | free | no profile page | promises the x-ray reveal; a little clinical |
| descriptive | **La Cosa por Dentro** | @lacosaporadentro | free | free | no profile page | warm, singular ("the thing"), repeatable as a series title |
| invented | **Mecanalia** | @mecanalia | free | free | no profile page | "mecan-" (mechanism) + "-alia": a made-up word with a festival ring; ownable, one word |
| invented | **Piezalia** | @piezalia | free | free | no profile page | "pieza" (part) + "-alia"; same pattern, parts-focused |
| invented | **Desmontalia** | @desmontalia | free | free | no profile page | "desmontar" (take apart); long to say, very on-theme |
| question | **¿Y Por Dentro?** | @ypordentro | free | free | no profile page | the audience's own next thought; very short; mirrors the hook format |
| question | **¿Qué Hay Ahí Dentro?** | @quehayahidentro | free | free | no profile page | pure curiosity gap; long |
| question | **¿Y Dentro de Eso?** | @ydentrodeso | free | free | no profile page | conversational, tag-line-like |
Tried and found taken on at least one platform (discarded): Destápalo, Desármalo, Mecánica Cotidiana, Funcionalia, Objetalia, Artefacta, Dentralia, Por Dentro de Todo, Asómate, Cosalia, Objetología (IG), Internalia (IG).
**Name recommendation: Mecanalia** — invented and therefore ownable across every country, free on YouTube and TikTok, short enough for a handle and an avatar wordmark, and it carries the mechanism positioning;
the cost is that it means nothing yet (you must teach it). Runner-up: **¿Y Por Dentro?** (shortest, echoes the question hook) or **Míralo por Dentro** (clearest promise).

## 6. Files
- `factory/directions.json` (single source), `code3d/lib/looks.py` (`look=esmeralda|violeta|mandarina|rosa|papel`), `factory/overlays.py` + `factory/editor.py` (per-direction text themes), `tools/brand_mark.py` (`direction_sheet`).
- Validation productions (scenes.json only are versioned): `productions/pilot/dr2-validate/`.
- Raw benchmark: s/frame table above (6-frame runs; per-scene logs not committed).

## 7. Decisions needed
Direction (VIOLETA recommended), name (Mecanalia recommended; or a runner-up), and whether to lighten Violeta's lower stage end. After that, round 3 writes the winner into the channel config
and CLAUDE.md as a diff for approval before any application.
