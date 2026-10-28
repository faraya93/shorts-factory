# huincha-de-medir (cinta métrica) — drawn route, full production report

Deliverable: `final.mp4` (68.00 s = 64.00 s timeline + 4 s end card, 1080x1920, 30 fps, 17.0 MB; gitignored).
Side-by-side vs reference: `build/frames/sidebyside.png`; 16-frame contact sheet: `build/frames/sheet.png` (both gitignored, regenerate with the scripts noted below).
Spend: US$0 (no fal calls).

## Rubric verdict (docs/style-rubric.md, scored on real Cycles frames — stills only, I cannot watch motion)
**Does it read as the pages' look? PARTIALLY — closer than v1–v6, but a clear step short. Verdict: NO for "indistinguishable", YES for "same family".**
1 Dark stage (#120F10, measured on draft; scene 4 review mark dE 19.2 from bright blocks) — pass (scene 4 flagged).
2 Passive grey — pass. 3 One gold accent on the active quantity with bloom (curved blade stress, counter, spring, weight) — pass, but the spring/hub glow in scene 5 is blown out to flat yellow (reads as paint, not energy).
4 Chunky simplified hard surface — pass; the housing is plain boxes + PBR, visibly less detailed than the references' hero objects.
5 Soft key + warm rim + halo + vignette — pass (the orange halo is stronger/more saturated than the references').
6 Real PBR, no outlines — pass.
7 Camera always moving — pass by scene gates (not verifiable from stills).
8 Top 25% clear — pass. 9 Hero centred lower 70% with negative space — pass in 1,4,5; scene 3 wide shot has a very thin blade that reads as a line, and scene 2's cross-section (6 s, 9 s) is the weakest frame: the "arc profile" is a thin plate seen at a shallow angle, the curve is not legible as a section.
10 Drawability law — pass (no people/hands/cloth).
Score ≈ 9/10 on the letter of the rubric, but honestly I rate the cross-section reveal and the thin blade as failing the *intent* (the references' cross-sections are large flat clean cuts with a layer stack). Biggest gaps vs the references: material richness (they have bevels, glass, tiny parts), the push-through into the section, and the cross-section legibility.

## Flags for the owner
- "3.4 m" and the chip "FICHA TÉCNICA DEL FABRICANTE" come from your brief; I could not verify them and no manufacturer is named. Treat as unverified until you give a source.
- Spoken "juego = grosor" kept qualitative (no digits).
- The specified Resulta tape-measure reel (314K) is not in docs/reference; the side-by-side uses ejemplo-1/2/3 frames.
- End card handle is the placeholder @[CANAL]. Music is the placeholder track (gitignored); credit in audio.music_credit must go to the description at publish.
- The title uses neutral "cinta métrica" (not Chilean "huincha").
- Clock disclosure: the machine clock shows ~9 h between the draft batch (10-26 23:20) and the Cycles start (10-27 08:50); no work happened in that gap.

## Assets (all logged in code3d/assets/LICENSES.md)
Source-first: Poly Haven "Measuring Tape 01" (CC0) downloaded and rejected as hero (single baked mesh, cannot extend/cut away/explode; proportion reference only). BlenderKit "Tape measure" and "25ft DeWALT" listed (royalty free) but not downloaded (same single-mesh limitation presumed). Hero therefore MODELLED hard-surface (tape_rig.py, primitives). ambientCG CC0: Metal012, Plastic010, Rubber004, Metal038. HDRI studio_small_08 reused. Nothing bought.

## Art direction rounds
Hero still: 5 rounds (framing, black-box housing, mirror-like gold from amber rim, open housing front, tick contrast, halo). Scene draft gates: S1 2 rounds, S2 2, S3 2, S4 2, S5 1, S6 1, S7 0 (fixes: stacked layouts, camera az, cursor cylinder scale axis, weight position, spring emission cap). 8-round cap not reached.

## Render actuals
EEVEE drafts: 0.20–0.27 s/frame, ~8 min for all 1,920 frames.
Cycles finals (Metal GPU, 256 samples, OIDN, adaptive 0.02), 1,920 frames:
| scene | frames | render s | s/frame |
|---|---|---|---|
| 1 | 180 | 783.3 | 4.35 |
| 2 | 294 | 1267.6 | 4.31 |
| 3 | 299 | 1140.3 | 3.81 |
| 4 | 373 | 2141.1 | 5.74 |
| 5 | 432 | 2403.3 | 5.56 |
| 6 | 196 | 755.2 | 3.85 |
| 7 | 146 | 599.3 | 4.10 |
Total Cycles 9,090 s (2.53 h) vs ~7 h budget: no samples or fps cut needed. Editor assembly ~2 min.

## Known defects to decide on
1. Scene 2 cross-section legibility (above). 2. Scene 3 blade too thin in the wide shot. 3. Scene 5 spring glow clipping. 4. Scene 4 bright wall blocks (QA mark). 5. Scene 6 weight is a plain cube. Each is a targeted re-render (scene-level, ~10–40 min), not a rebuild.

Regenerate sheets: `.venv/bin/python <sidebyside.py> final.mp4 out.png` (scripts live in the session scratchpad, not committed).

---
# Revision 2 (owner fixes, 2026-10-27) — $0
**Brightness: GRADE path taken, no re-render.** Unify pass now has a `lift` curve (`0/0.03 0.1/0.21 0.5/0.7 0.85/0.92 1/0.98`) and vignette removed (angle 0). Measured mean luma on 8 probe frames before -> after: 16/19/8/24/30/25/11/23 -> 54/73/38/85/88/79/45/50 (about 2-4x); stage now a dark charcoal (~#1C1C1C), no longer a void; highlight roll-off keeps the gold spring from clipping further. Sheet: `build/frames/brightness-before-after.png` (top before, bottom after). Not done: the scene-5 spring emission cap (no re-render was needed; the glow is still bright yellow but no longer clipped harder by the lift). Honest note: the lift also brightens the halo to a strong orange, which is more saturated than the references.
**Typography:** Montserrat ExtraBold (variable font, SIL OFL, `factory/assets/fonts/`, licence logged in `LICENSES.md`) for subtitles, counters, labels, chips; non-spoken words SemiBold. Widest subtitle 776 px (fits). Sheet: `build/frames/subtitle-before-after.png`. Counters are no longer monospace (Montserrat has proportional digits) — a counting number may shimmer slightly in width; I could not see motion to check.
**Citations:** chip "FICHA TÉCNICA DEL FABRICANTE" deleted (31 -> 30 overlays). `citation` overlay type now rejected by validation; CLAUDE.md, format spec (R8 + rule 8) and channel config amended; tests updated (all pass).
**Times:** font fetch + code/doctrine edits + grade tests ~10 min; re-assembly 24 s; no Cycles time spent. Output 68.00 s, 26.4 MB (previous 17.0 MB; the lifted frames compress heavier). Prior version kept at `build/final-v1-before.mp4` (gitignored).
