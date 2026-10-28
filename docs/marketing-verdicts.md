# Two verdicts: the closing CTA graphic, and the identity colour (marketing lens + design lens)
Written 2026-10-28. NOTHING is applied: no CLAUDE.md change, no channel-config change, no re-assembly of any production. $0. Craft layer used: the globally installed marketing/social skills (youtube-shorts, tiktok-growth, instagram-growth, facebook-strategy, short-form-video-script, thumbnail-design, design-and-templates, hook-writer) and, for the design lens, Tastemaker + design-taste-frontend (also now global).

## Step 0 — skills installed globally (done)
158 skills copied into `~/.claude/skills/` (52 from `coreyhaines31/marketingskills`, 106 from `social-media-skills/skills`; MIT, licences in `~/.claude/skills/_licenses/`), plus the existing `tastemaker` and `design-taste-frontend` packs moved there from this project's `.claude/skills/` (the project copy is gone, nothing is listed twice). All 160 SKILL.md files have valid frontmatter with names matching their folders and all four packs appear in the session's skill list. Note: the global skill list is now ~160 entries long in every project (context cost), and I did not run any script from these repos. One frontmatter in the scheduling skill names a "WoopSocial MCP" in `allowed-tools`: inert text unless that MCP is installed.
The two repos hold individual skill folders, so they were copied folder by folder (cloning the repos whole would have left every SKILL.md nested and undiscoverable).

---
# QUESTION 1 — the closing CTA graphic

## Verdict (confidence: medium on "remove the end card", low-medium on "redesign vs nothing")
1. **REMOVE the 4.0 s appended end card for good.** It adds non-content length after the last word, which can only lower average-percentage-viewed and rewatch; it duplicates the native follow button; and the owner's own behaviour is the best data point we have (he swipes when he sees one).
2. **REMOVE the 4.7 s acted-out phone.** Same reasoning, plus it re-draws UI the platform already shows (SEGUIR/share), covers the hero, and was never evidenced as converting: no source I found measures it.
3. **KEEP the spoken share ask** (it is inside the content, ~5 s, and ends on the twist "that friend who swears...": that is the "value-tied share CTA" the frameworks ask for) and **optionally REDESIGN the visual closing** into something that adds no seconds and covers nothing: the word-locked "ENVÍASELO" tag (C2) and/or a seamless loop (C1), clips below. If you want one default: **C2 now, test C1/C3 on one video.**
Removed time: 8.7 s per video (4.7 + 4.0), now gone from both Papel videos (64.00 s and 56.73 s).

## Evidence (honest: thin; no controlled study found for end cards or CTA graphics on short-form)
- **What high performers do in the last seconds** (marketing skills + practitioner sources, NOT audited top exponents): the frameworks agree on "engineer the ending to flow back to frame 1 (replays compound reach); one fitting ~2 s CTA tied to value, never a rote like-and-subscribe" (short-form-video-script, "H — Hold the loop, land the CTA"; youtube-shorts: "write every Short backwards from the swipe"). Blitzcut argues visible wrap-up language makes viewers leave just before the end and recommends cutting the outro ([blitzcut](https://blitzcutai.com/blog/increase-tiktok-watch-time-editing): a tool vendor, not a measurement).
- **Platform mechanics (the stronger evidence, but secondary sources):** YouTube Shorts counts replays and, since 31 March 2025, any started play as a view; average percentage viewed can exceed 100% when viewers loop, and analysts steer to engaged views and % viewed ([shortimize](https://www.shortimize.com/blog/how-does-youtube-shorts-algorithm-work), [creatoressentials](https://www.creatoressentials.com/glossary/shorts-engaged-views/), [bytecap](https://www.bytecap.io/research/youtube-shorts-retention-benchmarks)). TikTok: completion and rewatch are the top signals, and completion is computed against all views, so it cannot show whether an outro helps follows ([fanpagekarma/mediavortex via search](https://www.fanpagekarma.com/insights/?p=15609); no controlled study of outro vs follow rate found). Instagram: watch time, likes per reach and sends per reach are reported as the top Reels signals (Mosseri, January 2025, via [blitzcut](https://blitzcutai.com/blog/instagram-reels-algorithm-2026), [fanpagekarma](https://www.fanpagekarma.com/insights/instagram-reels-algorithm/)): this supports a SHARE ask over a follow ask there; watermarks from other apps are reported as downranked (our own mark is not that, but a persistent bug is not recommended). Facebook Reels: no usable data found; the facebook-strategy skill treats it as a follower-trust surface with Reels for reach: low confidence.
- **CTA data in general:** a journalism-industry piece cites no study, only two expert opinions that CTAs are less common on short-form ([journalism.co.uk](https://www.journalism.co.uk/are-call-to-actions-on-social-videos-worth-it/)); a video-platform blog cites old long-form drop-off (a Visible Measures study of 40M videos: 33% lost within 30 s, 44% by 60 s) and recommends showing end CTAs only to viewers who reached the end ([uStudio](https://ustudio.com/?p=1025)): not Shorts, not recent. Loop claims are anecdotal (one agency case: 85% to 115% retention, unreplicated: [joyspace](https://joyspace.ai/looping-hack-trick-algorithm-double-views), [subscribr](https://subscribr.ai/youtube-strategy/youtube-shorts-low-watch-time-boost)).
- **Per-platform differences that do matter:** Shorts feed is full-screen with no thumbnail, so the swipe is the only vote and the last seconds only count toward % viewed and loop; Instagram favours shares (so tag the SEND, not the follow); TikTok rewards completion/rewatch (so never add length); Facebook unknown.
- **Reference reels (audited earlier, `docs/cta-endcard-audit.md`):** all three end with a dimmed 4 s card; two use an acted-out phone; one keeps the hero. They are examples, not proof of optimality (no retention data on them).
- **Bottom line:** there is no evidence that the end card or phone helps and plausible mechanics that they hurt % viewed and break loops; the evidence that a redesign HELPS is equally thin. Hence remove first, then test a no-cost redesign.

## Redesigned closings (design lens: Papel system, never over the hero, no added card)
Clips (6.0-6.8 s each: the last 6 s of each Papel video + the tail) in `docs/cta-redesign/`; compare with C0 (the current no-graphic ending):
| clip | what it is | added time | covers the hero? |
|---|---|---|---|
| `*-C0-current-nographic.mp4` | the current ending (reference) | 0 | no |
| `*-C1-loop-dissolve.mp4` | after the last word the final frame dissolves (0.64 s, blend) into frame 0, so a replay is seamless (last frame vs frame 0: mean 1.4 levels, compression noise) | +0.8 s of silent tail | no |
| `*-C2-send-tag.mp4` | one tiny ink "ENVÍASELO" tag with a hairline leader, word-locked to the spoken "envíaselo", 2.6 s, in cream space beside the hero | 0 | no |
| `*-C3-tag-plus-loop.mp4` | C2 + C1 | +0.8 s | no |
(`*` = `huincha` and `engranajes`.) Total vs the removed 8.7 s: 0 to 0.8 s. Limits: the dissolve is a ghosted double-exposure for ~0.6 s and the first frame is the hook setup (two tapes / two gear pairs), so it is a compromise, not a true match-cut; the tag is 34 px small by design; neither is evidenced to move follows or shares, test on one video and compare average % viewed and sends against the previous two.

---
# QUESTION 2 — the identity colour, marketing lens
Settled constraints respected: no celeste, no near-black stages. **Round 2 already established that no source proves a hue wins views; this is an evidence-weighted judgement, confidence LOW-MEDIUM.**

## Evidence used (and its quality)
- **Warm, saturated colours draw more attention:** KAIST eye-tracking found warm hues more eye-catching than cool or neutral and high saturation giving the greatest visual magnetism against a black background (with a blue exception) ([KAIST](https://koasas.kaist.ac.kr/handle/10203/200596)); a Nottingham study links warm hues to attention/arousal and cool to concentration ([Nottingham](https://research.nottingham.edu.cn/en/publications/impact-of-color-hues-on-arousal-concentration-and-visual-attentio/)). Lab-style studies, not feeds. Vendor numbers ("+40% CTR for warm thumbnails", "+31%") have no traceable source: ignored.
- **Brand colour recognition:** the oft-quoted "colour increases recognition by 80%" traces to a loose media headline over a 2006 paper and a Reboot survey (67% recognised IKEA from its colours alone); not a controlled effect ([jewelleryfocus](https://www.jewelleryfocus.co.uk/21345-colour-increases-brand-recognition-80-claims-new-research)). What the thumbnail-design skill adds is craft, not evidence: complementary pairs, avoid platform-brand colours (YouTube red/white), pass the desaturation test, consistent palette across the grid (it cites +15-20% CTR for consistent style: unsourced here).
- **Dark mode:** no reliable platform-level share found (aggregator blogs only, [mean.ceo](https://blog.mean.ceo/?p=11516)); so I score robustness on BOTH UI modes instead of guessing the split.
- **Pan-Hispanic fit:** no data; judgement only (warm colours read festive/energetic across LatAm and Spain; no colour here has a known negative connotation I could verify).

## Criteria and measured inputs (all in `factory/directions.json`, `tools/palette_metrics.py`)
Weights are mine (stopping power 30, UI-mode robustness 15, distinctiveness from platform colours 15, legibility + accent clarity 20, hero separation 20); scores 0-5. Cost is not scored: all palettes cost 6.9-7.5 s/frame at the round-2 settings (see table).
| direction | stage (top / bottom) | stopping power (warm/saturated/luminous) | UI robustness (dE vs black / white UI) | distinct from platform colours (nearest, dE) | text + accent (unspoken text; accent vs stage) | hero separation (n heroes <20 dE) | B&W test (heroes with dL* >= 25 of 5) |
|---|---|---|---|---|---|---|---|
| LIMA (new) | #D9F34F / #C4E233 | 4 | 3 (87 / 29) | 3 (WhatsApp green, 21) | 5 (13.4 / 11.3; accent 5.9-6.9:1) | 5 (0) | 3/5 |
| ESMERALDA | #1F8570 / #1A6E5C | 2 | 5 (38 / 46) | 5 (WhatsApp green, 31) | 3 (4.5 / 6.1; accent 4.0-5.4) | 5 (1) | 3/5 |
| FUCSIA (new) | #D22C84 / #BA1E70 | 4 | 5 (41 / 49) | 2 (TikTok pink, 16) | 4 (4.7 / 6.0; accent 3.6-4.7) | 3 (1; pink hero 13) | 3/5 |
| MANDARINA | #FF9A4A / #F26A1D | 5 | 4 (60 / 35) | 2 (Instagram orange, 15) | 3 (8.6 / 5.9; accent 2.6-3.8) | 3 (2) | 2/5 |
| VIOLETA | #7A4DE8 / #5B30C2 | 3 | 5 (39 / 55) | 1 (Instagram purple, 7) | 5 (5.2 / 7.9; accent 4.0-6.1) | 3 (2) | 3/5 |
| ROSA | #FFB6C0 / #F48FA0 | 3 | 3 (67 / 28) | 3 (TikTok pink, 22) | 4 (9.9 / 7.2; accent 3.5-4.8) | 4 (1) | 3/5 |
| COBALTO (new) | #3F63F2 / #2C47D4 | 3 | 5 (40 / 53) | 2 (Facebook blue, 14) | 3 (4.9 / 7.1; accent 2.5-3.6) | 2 (2; blue pen 7) | 3/5 |
| PAPEL (incumbent) | #FDF3DC / #EFE2C4 | 2 | **1 (90 / 11)** | 3 (Instagram orange, 22) | 4 (15.2 / 13.1; accent 3.0-3.5) | 2 (2; white appliance 8) | 3/5 |
UI robustness = CIEDE2000 between the stage's mid colour and a black UI (#0C0C0E) and a white UI (#FFFFFF), taking the lower; Papel is the only one that nearly disappears in a light-mode profile grid (dE 11 vs white; it has the highest luminance contrast on dark, 17.6:1). B&W test: every direction fails for the mid-tone heroes that share its lightness (Esmeralda/Fucsia/Cobalto/Violeta: the red thermos and blue gears have dL* 1-4 from the stage; Lima: yellow tape and white cap dL* 7-9; Papel: white cap 2, tape 14): the plinth and shading carry it, as the stills show.

## The three marketing-proposed directions, worked by the design lens (round-2 rigour)
Rationale for each idea: **LIMA** = the loudest luminous colour in a dark-UI feed, a hue no platform owns (nearest WhatsApp green, dE 21), ink text 11-13:1. **FUCSIA** = warm, saturated, robust on both UI modes, white text. **COBALTO** = the "knowledge" colour with the classic complementary accent (it leans on the blue family, closest to Facebook blue and, in spirit, to the celeste you rejected: included for completeness, ranked low).
Validated on the standard three moments with the real Editor (subtitle theme per direction): `docs/marketing-review/sheet-1_tape_wide_midgrowth.png`, `sheet-2_glowing_quantity_spring.png`, `sheet-3_red_white_thermos.png` (all eight directions side by side; columns PAPEL, ESMERALDA, VIOLETA, MANDARINA, ROSA, LIMA, FUCSIA, COBALTO), plus `grid-recognition-mock.png` (each direction's three moments as profile-grid tiles on a dark UI and a light UI).
| new direction | stage | plinth | accent | subtitle | accent vs yellow tape / red thermos (dE) | s/frame (scenes 1 / 3 / 5; 128 spp, adaptive 0.03, 4 bounces) | mean | vs dark A (3.94) |
|---|---|---|---|---|---|---|---|---|
| LIMA | lime gradient | ink #1E2412 | ultramarine #3A2BD0 | ink words + white outline; spoken word in an ink box | 83 / 43 | 7.83 / 7.00 / 7.83 | 7.55 | 1.92x |
| FUCSIA | magenta gradient | cream #FFF3E0 | mint #6BFFD8 | white words + deep-magenta outline; spoken word in a white box | 40 / 77 | 7.50 / 6.50 / 8.33 | 7.44 | 1.89x |
| COBALTO | cobalt gradient | cream #F4EFE0 | orange #FFA45C | white words + navy outline; white spoken box | 19 / 34 | 7.33 / 6.66 / 8.66 | 7.55 | 1.92x |
Same cost as the other bright directions; at the tuned render stack of `docs/render-bench.md` (x0.41) each is about 3.1 s/frame, i.e. ~1.7-2.0 h per video. What the sheets show (stills only): the glowing spring reads clearly on all three; Lima is the most luminous and makes the blue gears and red thermos pop but softens the yellow tape and the white cap; Fucsia is loud and warm with a high-contrast mint glow; Cobalto's orange accent is the weakest accent and the whole frame leans toward the celeste/blue look.

## Ranking (base weights; sensitivity from 20,000 random weightings of the same scores)
| rank | direction | score | P(rank 1) | P(top 2) | note |
|---|---|---|---|---|---|
| 1 | **LIMA** | 82 | 48% | 92% | highest pop in dark UI, unclaimed hue, best text/accent and hero separation; risks below |
| 2 | ESMERALDA | 74 | 49% | 83% | safest and most robust; weakest stopping power (cool, mid-value) |
| 3 | FUCSIA | 73 | 3% | 17% | warm, robust, but near TikTok's pink and weaker hero separation |
| 4 | MANDARINA | 72 | 0% | 4% | loudest warm colour; weakest accent and B&W test; near Instagram orange |
| 5= | VIOLETA | 68 | 1% | 4% | best accent clarity, but IS Instagram's purple (dE 7) |
| 5= | ROSA | 68 | 0% | 0% | pretty, low stopping power, audience-skew risk |
| 7 | COBALTO | 59 | 0% | 0% | blue-family overlap, weakest accent |
| 8 | PAPEL | 48 | 0% | 0% | incumbent; last in 94% of weightings |
Honest reading: Lima and Esmeralda are co-leaders (each wins about half the weightings); the scores are my 0-5 judgements on measured inputs, not data on views. Papel ranks last for one measurable reason (it disappears on a white UI, dE 11, and has little chroma) and a judged one (neutral = least attention-drawing in the KAIST evidence); its genuine strengths are the best subtitle contrast and a calm, credible look. The incumbent's advantage for the owner is that it is already built into two finished videos.

## Per-platform differences
- **YouTube Shorts:** full-screen feed, black player, thumbnails only in shelves and the channel grid; avoid red; Lima/Esmeralda are distinct, Violeta/Mandarina are fine; Papel is weakest on a white channel page.
- **Instagram (Reels + grid):** brand colours purple/orange/pink dominate the interface: Violeta, Mandarina, Fucsia and Rosa would look native (camouflage or familiarity; I cannot tell which helps); the profile grid is white by default: Papel vanishes, saturated colours hold.
- **TikTok:** dark UI with cyan and pink accents: Lima and Esmeralda are distinct, Fucsia/Rosa near the platform pink; Lima gives the strongest dark-feed pop.
- **Facebook:** blue chrome, white feed: Cobalto/celeste blend in, Papel disappears, Lima and Fucsia stand out. (Low confidence: no Facebook-specific evidence found.)

## RECOMMENDATION: LIMA, with ESMERALDA as the fallback — confidence low-medium
Why: it is the highest-pop colour in the dark-UI feeds where most Shorts/Reels/TikTok viewing happens, no major platform owns the hue, it separates the blue gears and red thermos best, and it carries the strongest text and accent contrast (ink 11-13:1; ultramarine accent 5.9-6.9:1). The cost is the same as every bright direction (about 1.9x the dark baseline; ~1.8 h per video at the tuned stack).
Risks and what I could not establish: it is a large, very bright field (eye-strain/loudness concern from the saturation literature, no feed data); yellow and white heroes (the tape, white caps) merge with it in luminance, so hero rules would need a darker plinth and rim light and yellow heroes are a known weak spot; a flat lime may read as cheap or hi-vis for some audiences (untested); light-mode UI robustness is middling. Nothing here proves it wins views: the cheap way to find out is to publish the first three videos in the chosen stage and compare % viewed, swipe-away and sends/follows per view against any non-Papel baseline.
If you prefer certainty over upside: ESMERALDA (best hero separation, most UI-robust, most distinct, cheapest) is the defensible default.

## Files added (nothing applied)
`factory/directions.json` (+ lima, fucsia, cobalto as PROPOSALS), `docs/marketing-review/*` (sheets, grid mock), `docs/cta-redesign/*` (8 clips), this report. Test productions for the tag clips live in `productions/pilot/closing-test/` (scenes only; ignored by git).
