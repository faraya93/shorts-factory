# v7: fal version vs drawn (code3d) version, against the approved beat sheet (2026-10-26)

Both use the same narration (55.87 s + 4 s end card = 59.87 s), the same 7 scene slots, the same 25 word-locked overlays (Editor v2), music placeholder and end card. Finals (local, gitignored): productions/pilot/puntos-de-sutura-v7-fal/final.mp4 and productions/pilot/puntos-de-sutura-v7-drawn/final.mp4. Frames: build/frames/*-sheet.png in each. I cannot watch video: judgments are from still frames only; motion feel and timing are NOT assessed.

## Actuals
| | fal (t2v) | drawn (code3d) |
|---|---|---|
| fal spend | US$1.4024 at the normal rate (cap 1.50; 7 clips, 56.1 s, 0 retries); ~US$0.91 at the promo rate | US$0.00 |
| generation / render time | 7 clips returned in ~3 s each (about 1 min) | full-quality renders 36 min (1.15-1.40 s/frame, 1,676 frames; no stalls) |
| authoring (session) | production config + estimate ~25 min; overlay tuning 1 round | rig library + 7 scene scripts + 3 draft rounds (scene 1: 3 fixes; scene 6 and 2: 1 fix round) ~70 min |
| clip audio (gate -35 dB) | 7/7 MUTED (-21.8 to -28.2 dB, model music) | no clip audio (none to gate) |
| background QA vs #120F10 | n/a | dE 0.4-14.4, all ok (scene 7 14.4: the gold fibre glow, a signal not a defect) |
Editor v2 build (shared): ~tests 47/47 passing; $0.

## Beat-sheet fidelity (per scene)
| scene / events | fal | drawn |
|---|---|---|
| 1 hook CONTRAST (events 1-3) | STRONG: two blocks, straight needle ends below the left one, curved needle crosses the wound with a gold thread, push-in. Blocks differ in colour (navy vs grey). | GOOD: two identical blocks (as specified), straight needle plunges with a red trace, curved needle arcs under the wound with a gold thread, push-in. Blocks are plain grey boxes. |
| 2 curved needle (4-11) | PARTIAL: organic pointed-oval wound, no needle holder, arc through both lips not clearly shown, ends on a closed seam. | GOOD on the mechanics: holder-clamped curved needle, arc under the gap, gold thread pulled taut, lips close to a hairline; very geometric. |
| 3 knots (16-18) | GOOD macro of a knot and a gold stitch row; the unknotted stitch beat is unclear. | GOOD and explicit: stitches lay down and knot one by one; one dark unknotted stitch slides out. Flat/simple look. |
| 4 absorbable (19-21) | GOOD: thread with yellow-green cells dissolves, tweezers withdraw. | PARTIAL: beads dissolve, cells gather into a ring blob, tweezers barely enter. |
| 5 risk (22-25) | GOOD: gold tissue grows, red flash when pulled. | PARTIAL: gold growth is two plain lumps that cover the thread; tweezers and red flash present. |
| 6 ants (26-30) | PARTIAL: ants are near-photoreal and glossy (not stylized as the beat sheet asks) but the clamp reads. | PARTIAL: stylized chunky ants as asked, three separate ants across the narrowing wound; they stand on the lips more than bite both. |
| 7 reframe (31) + CTA/end card | GOOD: grey braided thread with a gold braid growing. | GOOD: grey thread arc with gold fibres stacking from the bottom (the specified bridge). |
Overlays (labels, bracket, ring, marks, DÍA 0-70 counter, 50% bar, Ethicon / Sushruta Samhita / Guías clínicas citations, 3 removal chips, CTA phone, end card) work identically on both and landed after one tuning round on the fal version and none on the drawn one.

## Look against the reference specs
- Both: dark stage (#120F10, bg dE 0.4-5 on drawn), warm halo, grey passive + gold accent, teal annotations, red errors.
- fal: richer, softer, more cinematic and closer to the reference "feel"; subjects are organic ovals, not the flat cross-section block; one rig is NOT kept across scenes (each clip invents its own wound), which breaks "one hero rig revisited".
- drawn: ONE rig truly reused in all 7 scenes (rule R14), precise control of every beat, but models are plain boxes: below the reference bar for polish (no fine detail where the fact is, flat shading). Closest failures: scenes 4, 5, 6.

## Verdict (mine, for you to overrule)
- Fidelity to the beat sheet's logic and the one-rig rule: drawn wins. Visual polish and mood: fal wins.
- Cost: fal US$1.40 once; drawn US$0 but ~70 min of authoring and 36 min of rendering. Scenes of this kind are reusable on the next production because the rig exists; fal gives no continuity.
- Reasonable next step if you pick drawn: a polish round on scenes 4-6 (cells, new skin, ant-bite), a layered-tissue texture/bevel pass, and the Editor-side tracking of overlays to moving objects (anchors are exported by the rig but not consumed yet). If you pick fal: re-run scenes 2, 3 and 6 with sharper prompts (about US$0.55 at the normal rate) and accept no rig continuity.
- Mixing the two in one video is forbidden by the engine rules (code3d is never mixed with diffusion footage).

## Open items
Inline emoji in subtitles not built. Anchor tracking not consumed by the Editor. Real Vicryl/Ethicon and removal-time figures are owner-sourced and not independently verified. Channel handle stays @[CANAL].
