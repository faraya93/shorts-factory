# puntos-de-sutura-v7-fal: fal estimate (NO SPEND MADE; waiting for the owner's OK, cap US$1.50)

Model minimax/h3-max-turbo/text-to-video, 480P, 9:16, prompt_expansion_mode disabled, fixed seed 1469841090 (this production's own).
Price verified live on fal.ai/models/minimax/h3-max-turbo/text-to-video on 2026-10-26: 480p US$0.025/s normal; US$0.01625/s promotional (35% off) until October 31. Model accepts 0.92-15 s; output can run up to ~0.7 s longer than requested.

| scene | clip requested | narration slot | normal rate | promo rate |
|---|---|---|---|---|
| 1 hook-contrast | 9 s | 8.93 s | $0.2250 | $0.1462 |
| 2 curved-needle | 10 s | 12.23 s (slowed x1.22) | $0.2500 | $0.1625 |
| 3 knots | 5 s | 4.43 s | $0.1250 | $0.0813 |
| 4 absorbable | 6 s | 5.47 s | $0.1500 | $0.0975 |
| 5 risk | 7 s | 6.17 s | $0.1750 | $0.1138 |
| 6 ants | 8 s | 7.57 s | $0.2000 | $0.1300 |
| 7 reframe-cta | 9 s | 11.07 s (slowed x1.23) | $0.2250 | $0.1462 |
| TOTAL | 54 s | 55.9 s + 4 s end card | $1.3500 | $0.8775 |

Gate rate (what the producer logs and the cap uses) = normal rate. Worst case with every clip running +0.7 s long: 54 + 4.9 s = $1.4725 at the normal rate, under the $1.50 cap. Headroom for a retry at the normal rate: about $0.15 (one 5-6 s scene); at the promo rate the real bill is roughly $0.88-$1.00.
Retry policy: max 2 attempts per scene; a failed or semantically wrong clip is reported, never worked around; the cap blocks any retry that would exceed it.
Local, no fal: narration (edge-tts) is already synthesized; all 25 word-locked overlays resolve; Editor assembly and overlay position tuning cost nothing.
Known limits (from the earlier spikes): t2v cannot keep one rig identical across scenes, text-to-video renders nouns better than actions, and overlay positions (labels, brackets, marks) are PROVISIONAL guesses until the clips exist; they get tuned in a free Editor pass.
