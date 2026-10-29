# Channel design system — PROPOSAL for owner approval (2026-10-27)

Status: **nothing here is applied.** `channels/umbrella-es.yaml` and `CLAUDE.md` are unchanged; the proposed edits are in
`docs/design-system-proposed.diff` (full proposed files in `docs/design-system-proposal/`). The full video was not re-rendered.
$0 spent. Everything below is either **measured** (tools/palette_metrics.py, real renders, reference frames) or **marked as argument/unknown**.

## 0. Method and honest limits
- Craft layer: Step 0 asked for `npx skills add ...`; **node/npx is not installed on this machine**, so I did not install it (system install, not authorised). I
  cloned both MIT repos (codeswithroh/tastemaker, Leonxlnx/taste-skill) and installed them the same way the CLI would, as project skills in
  `.claude/skills/tastemaker` and `.claude/skills/design-taste-frontend` (both now appear in the session's skill list = loaded). I read no script
  that touches the network; I used Tastemaker's process (reference study -> contrast-checked palette lock -> style lock + decisions log:
  `.tastemaker/style-lock.md`, `.tastemaker/decisions.log`). Both skills are web-UI oriented (sections, CSS, browser inspector); the channel's measured
  system wins wherever they conflict, as instructed.
- **What I could not measure: feed performance.** There is no controlled evidence in the sources I found that a light backdrop beats a dark one for
  Shorts views (the caption-legibility sources are vendor blogs; one says plainly there is no retention study). "Stopping power" below is therefore
  an argument from distinctiveness and legibility, labelled as such.
- Safe-zone figures are third-party estimates that disagree (no official YouTube spec found); I use the conservative union and recommend an in-app preview check.
- Brand handles: checked as "no YouTube channel at /@handle" (HTTP 404, with a negative control) on 2026-10-27. That is not a reservation and says nothing
  about TikTok/Instagram or trademarks.

## 1. Evidence base
- Reference study (docs/reference-style-spec.md): all three reference channels are dark-stage (>70% near-black). Caption band top 15-28%; subtitle
  glyph height measured on the reference frames again here at ~1.7-2.0% of frame height (about 33-38 px at 1920) -> Montserrat ~50-57 px, i.e. our 57 px.
- Identity rounds 1-2 (productions/pilot/identity2-sheets/README.md): contrast ratios and s/frame.
- Platform zones (web research, 2026): Shorts ad-safe 288 top / 672 bottom / 48 left / 192 right; TikTok 220-240 top, 480-660 bottom, 60-120 left, 120-140
  right; Reels 270 top, 670 bottom, 65-120 sides; Shorts organic bottom ~380 (20%). Sources: [clipspeed](https://www.clipspeed.ai/blog/youtube-shorts-size.html),
  [reap](https://reap.video/blog/short-form-video-safe-zones), [blitzcut](https://blitzcutai.com/blog/safe-zones-youtube-shorts-reels-tiktok),
  [adaptlypost](https://adaptlypost.com/en/blog/social-media-safe-zones-2026-complete-guide).
- Caption legibility (vendor guidance, unverified as retention evidence): heavy sans-serif; 3-4 px stroke or a semi-opaque plate beats shadow; shadows fail on
  light backgrounds; 2-5 words per block ([blitzcut](https://blitzcutai.com/blog/caption-background-vs-outline-vs-shadow),
  [opus](https://www.opus.pro/blog/youtube-shorts-caption-subtitle-best-practices)). Zack D Films' "light blue" could not be confirmed by any source I found
  (listings describe the style only as cinematic 3D); treat it as the owner's observation.

## 2. Palette (deliverable 1)
### 2.1 Verdict on the owner's celeste lean — confirmed, tone changed
Pale celeste D0 (#B9DCF0, round 2) has the weakest hero separation of the family. Searching the celeste hue family on 12 everyday hero colours
(CIEDE2000 minimum separation):

| stage | white appliance | steel/silver | mid-grey tool | black | worst |
|---|---|---|---|---|---|
| A near-black #120F10 | 90.6 | 70.9 | 43.5 | **2.1** | 2.1 (black hero) |
| E dark teal #0B2A2F | 76.6 | 66.7 | 38.6 | **12.9** | 12.9 |
| D0 pale celeste #B9DCF0 | **14.9** | **11.0** | 22.2 | 77.4 | 11.0 |
| **CELESTE top #8FD6F2 / bottom #62B4DC** | 20.9 / 26.9 | 16.7 / 19.8 | 23.5 / 18.9 | 73.0 / 57.7 | 16.7 |

No flat stage keeps every hero >= 25 (neutral greys/silver are always the weakest because only chroma separates them); the saturated mid-light celeste is
the best compromise (silver 11.0 -> 16.7-19.8, white 14.9 -> 20.9-26.9). Dark stages fail on black heroes instead (phones, remotes), which are as common as white ones.
**Mitigations built into the system (not optional):** a navy plinth under every hero (#2B4C70, 39.7 dE2000 and 3.8:1 vs the stage), cool rim light,
and a hero rule: neutral/near-white parts get a darker value or sit against the plinth.

### 2.2 The proposed palette
| role | hex | notes |
|---|---|---|
| Stage (screen-space gradient) | top **#8FD6F2** -> bottom **#62B4DC** | lighter behind the caption band, deeper low; no halo, no vignette |
| Plinth | **#2B4C70** | one navy platform for every hero, soft contact shadow |
| Hero | REAL colours (yellow tape #F2BD12 / black rubber #161618 / steel #E9E9EC; red thermos #CC2229 / white #F2F1EE) | PBR, slightly worn |
| Ink (text, leaders, brackets, chips) | **#0B2540** navy | replaces white + teal |
| Accent = the active quantity | **#E8590C** ember | replaces gold #F5C04A |
| Error | **#C92A2A** | replaces #BE4A4A |
| Outline / on-navy text | #FFFFFF | |
| Passive | #51555A | unchanged |

### 2.3 Honest cost of going light: the accent
Doctrine says gold = the active quantity. Gold has **1.08-1.16:1** against the celeste (it vanishes); on the dark stage it is 9.0:1. I therefore changed the accent to
ember **#E8590C**: 2.23:1 (top) / 1.55:1 (bottom) luminance contrast but dE2000 55 / 53 (strong hue contrast). It is usable for graphics and emissive parts but
never for text, and it reads weaker than gold-on-dark: in the real scene renders the stress glow on the blade looks salmon/pink rather than glowing (scene 1 still).
The light stage also has no bloom headroom. This is the real price of the celeste; the dark teal E keeps gold at 9:1.

### 2.4 Light-stage subtitle problem — solved, measured
White or grey text fails on the celeste (white 1.8:1, grey 1.6:1). Solution: **navy words + the spoken word reversed in a solid navy box with white text**, 4 px white
outline on the unspoken words (keeps them readable if a hero part passes behind).

| element | colours | ratio | target | pass |
|---|---|---|---|---|
| spoken (key) word | white on navy box #0B2540 | **15.52** | >= 7 | yes |
| unspoken words | navy on stage top / bottom | **9.66 / 6.71** | >= 4.5 | yes |
| selection box (key words) | ember outline on navy box | graphics, dE 55 | n/a | yes |
| counters, labels, leaders | navy on stage + 4/3 px white outline | 6.7-9.7 | >= 4.5 | yes |
| (dark option E: white / grey on #0B2A2F) | 15.2 / 5.1 | | | yes |
Implemented as `overlays.THEMES["light"]` + `editor.SUB_THEMES` (`visual_identity.text_theme: light`); default stays the dark reference style. Tests pass (7+12+...).

### 2.5 Which palette for views? (argument, not measurement)
- For celeste: owner preference; brightness and chroma are distinctive against reference competitors that are all dark; better silver/white hero separation; "inviting".
- Against: breaks the binding dark-stage doctrine (all reference evidence is dark); accent legibility drops (2.3); needs the new text theme; costs more to render.
- My professional recommendation: **celeste (this tone) if you accept the accent compromise**, with E dark teal as the lower-risk fallback (same cost as today, gold 9:1, signature
  hue). I could not measure which wins in the feed; the first three videos should be treated as the test.

## 3. Typography (deliverable 2) — Montserrat ExtraBold (+ SemiBold for unspoken), SIL OFL, `factory/assets/fonts/`
Scale at 1080x1920 (W = 1080), proportional rules in brackets. Phone check: 1080 px ~ 390 pt, so 1 pt ~ 2.8 px; minimum legible 11 pt ~ 30 px.
| element | size | stroke / treatment | note |
|---|---|---|---|
| subtitle (spoken word ExtraBold, others SemiBold) | **57 px** (5.3% W; cap height ~40 px = 2.1% H, reference 1.7-2.0%) | 4 px outline; light theme: spoken word in navy box (pad 12x6, radius 12) | max 4 words, max line 940 px; centre y = 0.24 H |
| key-word box | box 3 px + 7 px corner handles (dark) / 4 px ember outline (light) | | only on `subtitle_emphasis` words |
| counter (mono style) | **80 -> 96 px** proposed (8.9% W) | 4 px outline | currently 80; raise for phone legibility |
| tag label | **34 px** ALL-CAPS, tracking 4 (3.1% W; 12.3 pt) | 2 px outline | do not go below 30 px |
| chip | 44 px, pad 34x20, outline 5 px | navy fill (light) | figures/units only, never sources |
| leader | 3 px line, 12 px end dot | navy / white | |
| mark X / ok ring | 120 px (11% W), 18 px / 14 px | | |
| ring | dotted, 7 px | | |
| slim bar | 520x30 px | ember fill | |
Shadows are not used (they fail on light backgrounds in the sources and in my read of the stills); stroke/plate only.

## 4. Overlay and effect sizing (deliverable 3) — proportional rules
- Anchors in frame fractions (x, y = centre). Counters and chips sit **y <= 0.72**; **no existing overlay may stay at y 0.80-0.88** (the current huincha video puts its counter at y=0.80 and chip at 0.88:
  inside the platform-UI zone; the CTA phone, y 0.55 +/- 0.30, also reaches it — flagged, to fix at reassembly).
- Labels sit within 12% W of their target; leader length 8-25% H; one label per object; label count <= 3 on screen.
- Counter height 8-9% W, never over the hero; place beside/above it. Marks 11% W on the object's edge, not its centre.
- Bracket tick = 2.8% W, line 6 px; ring radius 6-12% W.
- Timing unchanged (word-locked +-0.3 s).

## 5. First frame and framing (deliverable 4) — stopping power rules
1. Frame 0 shows the hero in real colours on the plinth, no text-only or black frame; the false-belief contrast visible by t=2 s.
2. Safe rectangle for the HERO and graphics: **x 0.10-0.90, y 0.28-0.75** (thermos validation obeys it); caption band 0.15-0.30; nothing essential below y=0.75 or in the right 18% below y=0.45.
3. Subject share: the hero (housing + blade) should span **50-70% of frame width and >= 30% of frame height** in hero shots; wide shots exempt but keep the object >= 12% H.
4. Contrast placement: the hue/value contrast pair (yellow vs celeste, plinth vs hero base) must be at the hero's centre of mass; keep the accent ember out of the caption band.
5. Camera never rests (existing rule); the first move starts within 0.3 s.
6. Never place the hero's lightest part (white cap) behind the caption band (seen and fixed in the thermos test).

## 6. Brand identity (deliverable 5)
Positioning: curiosity + mechanism ("we open everyday things"), pan-Hispanic neutral, no slang, no "¿Cómo...?" (flopped).
Checked on 2026-10-27: handles that returned 404 (no channel) vs taken (200) — rejected names listed too.
| # | name | handle | check | rationale |
|---|---|---|---|---|
| **1 (recommended)** | **Abre las Cosas** | @abrelascosas | free | imperative, 3 short words, the whole format in a verb (open it); rhythm works spoken; mark = a cut-open object |
| 2 | Cosas por Dentro | @cosasporadentro | free | literal, searchable, family-friendly; weaker brand edge |
| 3 | Lo Que Hay Dentro | @loquehayadentro | free | curiosity gap as a name; long for a handle |
| 4 | Así Funciona | @asifunciona | free | strong, but very generic (many channels share the phrase) |
| 5 | Corte Abierto | @corteabierto | free | cross-section pun; "corte" also reads as court/haircut in places |
| 6 | Mecanismo Abierto | @mecanismoabierto | free | precise; dry, less warm |
| 7 | Ojo por Dentro | @ojoporadentro | free | playful; slightly awkward |
| rejected | Por Dentro, Desmontado, Qué Hay Dentro, La Pieza Oculta, Así Es Por Dentro | taken | taken | channels already exist at those handles |
Trademarks, TikTok/Instagram availability and domains NOT checked.
**Logo/avatar/end-card direction** (code-rendered, `tools/brand_mark.py`, assets in `docs/design-system-assets/brand/`): a rounded-square "object" with its top-right quadrant cut away,
revealing a white inner layer and one ember dot (the active part) — three flat shapes, scales to a 48 px avatar. Avatar = mark on a celeste circle. End card = the last frame
under a ~78% navy veil (the reference's dimmed card, ~25% brightness), white mark + handle in Montserrat ExtraBold 64 px, centred at y 0.40-0.62 (inside the safe zone), 4 s.
Not wired into the Editor yet.

## 7. Cost table (deliverable 6) — real scenes, s/frame (1080x1920, Cycles Metal, 6-frame benchmark minus ~4 s startup)
| config | scene 1 | scene 2 | scene 3 | scene 5 | mean | vs dark A | est. 1,920 frames |
|---|---|---|---|---|---|---|---|
| current grey rig, 256 spp | 4.16 | 3.33 | 3.50 | 5.33 | 4.08 | 0.93x | ~2.2 h (actual full run 2.53 h) |
| A near-black, real colours, 256 | 4.16 | 3.66 | 3.33 | 6.50 | **4.41** | 1.00x | ~2.4 h |
| E dark teal, 256 | 4.33 | 3.66 | 3.33 | 6.66 | 4.50 | 1.02x | ~2.4 h |
| CELESTE 256 spp (adaptive 0.02) | 11.33 | 10.00 | 9.83 | 12.16 | 10.83 | 2.45x | ~5.8 h |
| CELESTE 128 spp, adaptive 0.03, 4 bounces | 8.00 | 7.00 | 7.16 | 8.66 | **7.71** | 1.75x | ~4.1 h |
| CELESTE 96 spp, adaptive 0.05, 4 bounces | 6.33 | 6.16 | 6.00 | 7.00 | **6.37** | 1.44x | ~3.4 h |
Quality: 96, 128 and 256 spp crops of the same celeste frame are visually indistinguishable on stills (`docs/design-system-assets/noise-96-128-256.png`, OIDN denoise);
temporal flicker at low samples is **not tested** (stills only). Recommendation: 128 spp (1.75x A, ~4.1 h per 64 s video); fall back to 96 if flicker is absent.
Benefit side (honest): no measured view benefit exists; the quantifiable benefits are hero separation (silver 11 -> 17-20 dE) and text contrast; the cost is +1.7-2.0 h per video.

## 8. Validation stills (deliverable 8)
`docs/design-system-assets/validation-before-after.png` — columns: BEFORE (current video, grey rig, dark), E dark teal (dark theme), AFTER Celeste; rows: tape wide/counter, subtitle-heavy frame
with label + leader + key-word box, thermos (versatility). Observations (stills only): yellow and red pop on the celeste; white cap reads against the stage thanks to shading but is the
softest edge; subtitle hierarchy survives (navy box = spoken word); label/leader readable; ember is the weak point. The test counter overlaps the thermos because that
test reused the tape's overlay (not a design fault). Thermos first position was rejected (cap under the captions) and re-framed.

## 9. What changes if approved (deliverable 7)
`docs/design-system-proposed.diff`: umbrella-es.yaml visual_identity block (celeste, navy ink, ember, text_theme light) and a new CLAUDE.md "Channel design system" section superseding
the dark identity and look rules 1 and 3. Applying also requires: updating `DEFAULT_UNIFY` and `tests/test_channel.py` to the new unify, adding the safe-zone constants, moving the
counter/CTA positions, re-benchmarking one full scene, and choosing the handle. Code already in place (backwards compatible, default = current dark look): `code3d/lib/looks.py`
(`look=CEL|E|A`), `overlays.set_theme`, `editor.SUB_THEMES`, `tools/palette_metrics.py`, `tools/brand_mark.py`.

## 10. Decisions needed
1. Stage family: celeste (recommended tone above), E dark teal, or other. 2. Accept ember accent on light? 3. Name/handle (recommended: Abre las Cosas / @abrelascosas).
4. Render settings (128 spp recommended). 5. Authorise installing Node if you want the exact `npx skills add` route.
