# Colour verdict, second look: the joint panel (marketing + design + scriptwriter)
Written 2026-10-28. NOTHING is applied (no CLAUDE.md, no channel config, no re-assembly). $0.

## Part 1 — scriptwriter kit installed globally (done)
`github.com/Jakeschincariol/youtube-agent-skill` cloned; its 11 skill folders (`yt-audit, yt-chapters, yt-comment, yt-edit, yt-package, yt-plan, yt-retention, yt-script, yt-seo, yt-shorts, yt-viral`; MIT) copied into `~/.claude/skills/`, with its `templates/voice.md` kept in `~/.claude/skills/_yt-templates/` and the licence in `_licenses/`. **`/yt-script` loads**: I invoked it as a load check and its instructions came back (hook options scored with `hookscore.py`, beat-by-beat script with `[ON SCREEN: ...]`, "ship it or change it?"); all 11 have valid frontmatter. I ran none of the bundled `.py` scorers. Honest limit: these skills are written for long-form YouTube; for this panel I used their on-screen-first principle together with `short-form-video-script` ("write the silent version first; on-screen text carries the story") and `hook-writer` ("must work muted").

---
## Part 2(a) — Does the Lima recommendation rest on ANY measured relationship between stage colour and views?
**No. It is judgement over proxies.** I have no measurement, from any source, that links a stage (background) colour to views, swipe-away, retention, follows or shares on Shorts, Reels, TikTok or Facebook. The ranking is my weighted 0-5 scoring of proxies:
| proxy | what it actually measures | the claim it can support | what it cannot support | source quality |
|---|---|---|---|---|
| warm/saturated "stopping power" | lab eye-tracking: warm, saturated hues draw gaze in controlled displays (KAIST; Nottingham) | "more likely to be noticed in a static display" | that a noticed frame is watched, or that Shorts viewers swipe less; Lima is yellow-green, not even "warm" in those studies | academic, small, not feeds |
| contrast vs black/white UI (dE) | discriminability of the frame from the app chrome | "visible on dark and light UIs" | any behaviour | physics, solid |
| distance from platform brand colours | whether the frame is confusable with TikTok/Instagram/YouTube/Facebook chrome | "not mistaken for the platform's own UI" | that distinct colours get more views (or that native-looking ones get fewer) | my construction |
| text and accent contrast, hero separation | legibility and comprehension of our own overlays and heroes | "the words and the active quantity can be read; heroes read" | reach; only whether the video is understandable once seen | measured, solid, but only about our rig |
| the 0-5 scores and weights (30/15/15/20/20) | my judgement | a transparent tiebreaker | anything empirical | none |
Lima won because it was strong on the cheap-to-measure legibility/separation proxies and on the attention proxy; two of its worst risks ("reads cheap/hi-vis", eye strain from a large saturated field) are exactly the things no proxy measures. Its 82 vs Esmeralda's 74 was within the noise (each won ~half of random weightings).
**What evidence would change the ranking** (best first): (1) our own split test on the metric that is statistically feasible: viewed-vs-swiped-away rate per impression (YouTube Studio) and shares/follows per view, same topics in two stages. Sizing, with my assumptions: detecting a 3-point swipe-away difference (70% vs 73% viewed) needs about 3,700 impressions per arm; detecting a 20% difference in *views* needs about 700 videos per arm (log-view spread assumed ~1.2), so views are not a testable outcome for us and the swipe rate is; (2) competitor data in the same niche, scoring each channel's videos against ITS OWN median (the `yt-viral` "beat its own channel" method) against stage colour: observational but cheap; (3) platform creative guidance or a first-party study on background colour in the full-screen feed (none found); (4) feed-realistic eye-tracking or preference tests with pan-Hispanic viewers; (5) the owner's reaction is already a data point (below).

## Part 2(b) — the owner's data point and the panel
**Recorded:** the owner has seen the sheets and neither LIMA nor ESMERALDA convinces him. For Lima this is the "reads cheap / hi-vis" risk I flagged as unmeasurable, now observed once (n = 1, but the owner is the first audience and the decision-maker). For Esmeralda no reason was given and I do not assume one. Treatment: both are demoted by 15 points in the joint score, shown with and without the penalty. No other steer was given; the panel decides.

### Lens 1 — MARKETING (discovery and positioning)
Skills used: thumbnail-design (complementary pairs, desaturation test, consistent palette across the grid, avoid platform-brand colours), profile-optimization/brand-profile (grid and avatar), youtube-shorts / tiktok-growth / instagram-growth (the swipe is the only vote; first frame must stop and read muted).
Reasoning: the job of the stage in the first frame is (i) to separate from the dark chrome and from the dark/black competitor look of the references, (ii) to stay distinct from the platforms' own colours, (iii) to survive both UI modes, (iv) to let the accent and the words land. Saturated, warm-leaning fields do best on (i); Papel fails (iii) (dE 11 vs a white UI) and is neutral on (i). With the owner's data point the marketing ranking is: **1 FUCSIA (73), 2 MANDARINA (72), 3= VIOLETA/ROSA (68), 5 LIMA (82 raw, 67 adjusted), 6 ESMERALDA (74 raw, 59 adjusted), 7 COBALTO (59), 8 PAPEL (48).** Marketing asked design for a refinement of Fucsia because its stage hue sits close to TikTok's pink (dE 16) and its lightness invites a "toy" read; that became FRAMBUESA below, scored 74.

### Lens 2 — DESIGN (its own craft ranking, not only measurements)
Skills used: tastemaker anti-slop checklist; design-taste-frontend `references/colour.md`. Craft principles that apply to a flat colour world: one ground, one ink, one accent; saturated fields used "flat and with conviction"; the gallery study's banned families are **violet/indigo** and **yellow-cream with rust/terracotta** ("the house look of AI assistants"); one saturated field is rare (6% of sites), i.e. distinctive; warmth is not beige. (Caveat: that study is of websites; the channel system wins where it conflicts, and our stage has a soft gradient that a web design would avoid.) Craft ranking from the sheets: **1= ESMERALDA and FRAMBUESA (90): coherent, adult, the real-colour heroes sit on it like objects on a table; 3 MANDARINA (80): striking, flat warm field with a cobalt accent, but the ink plinth is heavy; 4= PAPEL and FUCSIA (70): Papel is refined but its cream + vermilion pairing is the flagged assistant look and white objects vanish; Fucsia has conviction but reads closer to toy; 6= ROSA, COBALTO (60); 8= LIMA, VIOLETA (50): lime reads hi-vis and violet reads generated.** Design's honest note: its own ranking agrees with the owner's reaction to Lima and disagrees with the owner on Esmeralda.

### Lens 3 — SCRIPTWRITER (which stage best serves the stories and the on-screen words of the four families)
Skills used: yt-script (every beat carries what is ON SCREEN), short-form-video-script (silent-first: on-screen text carries the story), hook-writer (the first frame and its text must work muted).
Measured input I added: the heroes of all four families, 36 colours (objects, a stylised body set with skin/organ/bone/tooth/bacteria/vein, numbers/scale pieces, what-if props), separated from each stage. Count of heroes with dE < 20 from the stage: **LIMA 2, FUCSIA 2, ROSA 3, ESMERALDA 4, FRAMBUESA 4, VIOLETA 5, COBALTO 5, MANDARINA 6, PAPEL 10.** Important correction to my own earlier assumption: a pale neutral stage does NOT suit "any hero colour": most families contain white things (appliances, chess pieces, bone, teeth, clouds) that vanish on Papel, and a warm saturated stage swallows the warm heroes (orange tools, yellow, skin, sun). Body family: pink/magenta stages swallow organ pink and muscle red-brown; lime swallows the doctrine's yellow-green bacteria; green or berry stages leave skin and bone readable.
Word legibility (ink or white text on the stage, accent and error clarity), then narrative tone fit across objects/body/numbers/what-if (judgement): scores **LIMA 75 (hi-vis tone and the bacteria problem pull it down), FUCSIA 69.5, FRAMBUESA 67, ESMERALDA 67, ROSA 65.5, COBALTO 59, VIOLETA 57.5, MANDARINA 55.5, PAPEL 53.** Scriptwriter note on the contrast beat: the red X (error) in our grammar must read on the stage: it reads on Papel/Mandarina/Rosa/Lima, is weak on Esmeralda/Violeta/Cobalto and cannot be red on a magenta/berry stage (see mitigations).

### Cross-examination
- Marketing vs design on Lima: marketing liked its pop, design called it hi-vis, the owner agrees with design; Lima falls.
- Design vs scriptwriter on Papel: design still finds it elegant; scriptwriter measures it worst for the four families (10 failing heroes) and marketing finds it nearly invisible on a white UI. The incumbent's real strengths (best subtitle contrast; calm) do not outweigh two structural weaknesses.
- Marketing and scriptwriter on Mandarina: loud and warm (good for marketing) but swallows warm heroes (6 failing, the worst of the saturated set).
- Everyone on mid-lightness stages (Esmeralda, Fucsia, Frambuesa, Violeta, Cobalto): the stage is the same lightness as mid-tone heroes (the "B&W test" dL* 1-5 for red thermos and blue gears), so separation there is by hue only; every direction has this property for some hero, so it is solved by rule, not by hue (see mitigations).

### Joint verdict
Equal lens weights (the three lens scores in the table, which are my judgement on the measured inputs above), with the owner penalty (-15 on Lima and Esmeralda):
| rank | direction | marketing | design | scriptwriter | joint | without owner penalty |
|---|---|---|---|---|---|---|
| 1 | **FRAMBUESA (new)** | 74 | 90 | 67 | **77.1** | 77.1 |
| 2 | FUCSIA | 73 | 70 | 69.5 | 70.8 | 70.8 |
| 3 | MANDARINA | 72 | 80 | 55.5 | 69.2 | 69.2 |
| 4 | ROSA | 68 | 60 | 65.5 | 64.5 | 64.5 |
| 5 | ESMERALDA | 74 | 90 | 67 | 61.9 | 76.9 |
| 6 | COBALTO | 59 | 60 | 59 | 59.3 | 59.3 |
| 7 | VIOLETA | 68 | 50 | 57.5 | 58.5 | 58.5 |
| 8 | PAPEL | 48 | 70 | 53 | 57.0 | 57.0 |
| 9 | LIMA | 82 | 50 | 75 | 54.0 | 69.0 |
**Recommendation of the panel: FRAMBUESA** (deep raspberry, a refinement of Fucsia), with **FUCSIA** as the same-family alternative and **MANDARINA** as the warm alternative. Honest reading of the confidence: **low-to-medium.** FRAMBUESA wins 96% of random lens weightings and ~65% of weightings with ±6-point noise on every score, but two things inflate it: (1) it is the only direction the panel designed after seeing the others, so I scored it with knowledge of what I wanted fixed (the design and scriptwriter scores for it are the most biased numbers here); (2) without the owner penalty it ties with Esmeralda (77.1 vs 76.9). If FRAMBUESA is excluded, the panel's pick is FUCSIA, then MANDARINA.
Why the panel lands on this family: the raspberry/magenta region is the one place where a saturated, warm-leaning, non-violet, non-lime stage is robust on both UI modes (dE 36 vs black, 54 vs white), distant from yellow/orange/green/brown/skin/bone/bacteria heroes, and leaves white text and a mint accent legible.

### The new direction, validated with the same rigour (FRAMBUESA)
| item | value |
|---|---|
| stage (top / bottom) | #C21B68 / #A31256 (L* 39 mid), plinth cream #FFF3E0, accent mint #6BFFD8, white ink with #4A0A2B outline, spoken word in a white box with berry text |
| text contrast | white on stage 5.8 / 7.6; spoken box 15.3 |
| accent vs stage | mint 4.6 / 6.1 (dE tape 40, red thermos 77) |
| UI robustness | dE 36 vs black UI, 54 vs white UI; nearest platform colour dE 21 (Fucsia was 16) |
| heroes < 20 dE (36 heroes) | 4: the red thermos (19), a body red-brown (15), a number-family red die (19), a what-if red button (19): all reds; pinks are fine here (Fucsia's 2 were a pink and a red-brown) |
| B&W test | red thermos and blue gear dL* 5, tape yellow 40, white cap 56, black boot 32 |
| cost | scenes 1 / 3 / 5: 7.00 / 6.00 / 8.33 s/frame = mean 7.11 (1.8x the dark baseline of 3.94; ~2.9 s/frame at the tuned stack of `docs/render-bench.md`) |
| sheets | `docs/marketing-review/joint-1_tape_wide_midgrowth.png`, `joint-2_glowing_quantity_spring.png`, `joint-3_red_white_thermos.png` (PAPEL, FUCSIA, FRAMBUESA, MANDARINA, ESMERALDA, ROSA), `joint-grid-mock-finalists.png` (dark and light UI grids) |
Honest trade-off visible in the sheets: deepening Fucsia to a berry made it look richer and less toy-like (design's reason) but moved it closer to red heroes (marketing/scriptwriter's cost); on the thermos moment the cream plinth and rim keep the red readable.

### Known structural weaknesses of the winner, and concrete mitigations
1. **Red and berry-red heroes (and any mid-lightness hero) sit at the stage's lightness** (dL* 5). Rule: heroes in hue 330-20 with L* 33-45 are re-valued (lift to L* >= 58 or sink to <= 28) or stand on the cream plinth with a rim light (already the Papel/plinth system; the thermos sheet shows it works); never place a red hero on the bare stage.
2. **The red error X is lost on a berry stage.** Rule: errors are drawn as a white X with a near-black outline plus the failing object dimming; the doctrine's "red = error" is amended for this stage (needs the owner's approval; not applied).
3. **Body family:** organs, muscle and pinks vanish on a magenta stage. Rule: body heroes always sit inside a cream cutaway plate with the cyan/teal frame the doctrine already specifies, so local contrast is cream, not the stage; no pink hero on the bare stage.
4. **TikTok-pink proximity (dE 21)** and the "toy / cheap" read: keep the stage deep (berry, not hot pink), never add gradients stronger than the present screen-space one, keep one ground / one ink / one accent, no emoji in frame; the cream plinth + mint accent + the cut-corner mark are the repeating, ownable pieces (they are what separates us from TikTok's pink).
5. **Audience skew / "magenta = feminine" risk** is unmeasured; the first three videos should be read against the swipe-away rate by audience split in Studio.
6. **Instagram's own gradient** also contains pinks/purples: the mint accent and cream plinth are the differentiators on the grid.
**If the owner nevertheless keeps a pale stage (Papel), the grid identity must be built from other signals:** avatar in saturated vermilion with the cream cut-corner mark; every cover/first frame carries the same ink plinth block bottom-third and one vermilion element (so the grid reads as "dark block + vermilion dot" even on a white profile); a constant 6-8 px ink border on cover frames (safe-zone aware); a profile banner and name in ink on cream with a vermilion rule. These compensate for the stage disappearing on white (dE 11), they do not remove the structural weaknesses with white heroes.

### What would reverse the panel's recommendation
A swipe-away/viewed-rate difference of a few points in favour of any other stage in a like-for-like split; competitor evidence that magenta/pink stages underperform in this niche; the owner finding FRAMBUESA reads cheap or feminine (a data point of the same kind as the one just given); a hero set dominated by reds and pinks (then MANDARINA or ESMERALDA win on separation).

## Files
`factory/directions.json` (+ `frambuesa` as a PROPOSAL), `docs/marketing-review/joint-*.png`, this report. Nothing was applied to `channels/` or `CLAUDE.md`.
