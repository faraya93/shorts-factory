# Spike — three cartoon-native concepts for scene 2 (concept first), 2026-10-25

Beat to convey: a needle passes through BOTH edges of an open wound and the thread pulls the edges together.
Rules held: few bold elements, ONE hero action, readable without narration, no anatomy, visual metaphor. One draft frame each
at 1080x1920 through the toon pass (`frames/1-lace-up.png`, `2-zipper.png`, `3-mend-the-rip.png`, `sheet.png`). $0 spend.
Code: code3d/scenes/spike_concepts_02.py, code3d/lib/shapes.py (new shared cartoon primitives).

| # | Concept | One line | Why it reads instantly |
|---|---|---|---|
| 1 | LACE-UP | Two boot flaps with eyelets, laced criss-cross up from the bottom, while a chunky needle skewers the eyelet rings of BOTH flaps on the next row. | Everyone knows that pulling laces closes the gap; the V-shaped gap that is narrow where it is already laced shows "pulled together", and the needle through two rings shows "through both edges". |
| 2 | ZIPPER | A half-zipped seam: teeth interlocked below, open (red inside) above, and the needle sits exactly where the zipper slider would be, its thread hanging like a pull tab. | A half-closed zipper is the universal picture of "closing a gap from one end", and the needle replaces the slider, so the hero action is the needle moving up the seam. |
| 3 | MEND-THE-RIP | A round cushion with a jagged tear, whip-stitched shut from the bottom, with a giant needle sewing the next stitch across the open part. | Sewing up a ripped cushion is the most familiar picture of "needle and thread closing a gap"; the stitched part against the open part tells the story without words. |

## Honest observations (frames, not a verdict)
- All three read as their metaphor on the first render; round 2 only added an EYE ring to the needle (without it the needle read as a
  pointer).
- Lace-up is the most literal match to the beat (the needle really goes through an element of each edge); the lace end near the
  needle's tip ends in mid-air (unresolved).
- Zipper: the "pull tab" thread is an awkward bent cord; the needle lies across the seam rather than piercing it, so "through both
  edges" is implied.
- Mend-the-rip: the cushion reads as a flat disc, and its needle and thread loop are heavy and angular; it is the least polished.
- My ranking for instant reading: 1 (lace-up), 2 (zipper), 3 (rip). The choice is the owner's.
- Time: ~4 min wall clock (22:41:51 -> ~22:45), 2 render rounds. Nothing existing was touched.
