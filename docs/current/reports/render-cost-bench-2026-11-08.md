# Render-cost bench (2026-11-08)

Written for the owner and later sessions. Everything here is measured on this machine, Cycles on Metal, final settings (64-sample ceiling, as the chain uses), raw data in `render-cost-bench/`. RMSE is against a high-sample reference at 540x960 (512 spp for 008, 256 for the others). Single-frame walls include scene start-up; the 12- and 30-frame runs are the fair per-frame numbers.

**Headline, 008 scene 4 (the heaviest scene in the catalogue), frames 100-111:**

| Variant | s/frame | vs baseline |
|---|---|---|
| Baseline (`transparent` as of 2026-11-07) | 72.5 | |
| Biased volumes, step 2, adaptive 0.08 | 24.2 | -67% |
| Same + 75% resolution | 13.7 | **-81%** |

**The report's main inference was right in direction and short in reason:** Blender 5's default is unbiased volumes, where `volume_step_rate` does nothing. `volume_biased` on is the lever (82.7 → 38.0 s on frame 215 with RMSE unchanged); the step rate adds little on top.

**75% final resolution, general policy (the owner's item d):** opaque scene 007 s2, 30 frames: 3.20 → 1.87 s/frame (**-42%**). Transmission scene 008 s4: frame 215, -40% alone. Readers, isolated, three per still, upscaled to 1080x1920 as the editor does: padlock 96/96/97 (full-size control 95/95/95), and 008 s4 ice and tank both pass at 90/90/88 on the full fast stack. It passes and the saving is real, so it is the default final.

**Other variants on 008 s4 frame 215 (82.7 s, RMSE 3.2 baseline):** volume bounces 1: 80.6 s, RMSE 5.6; 0: 70.5, 24.9. Transmission 6: 66.9, 19.5; 4: 42.9, 52.5. Adaptive 0.06: 77.0, 3.3; 0.08: 67.7, 3.4. Thin Wall: 69.9, 20.9. Fake indirect glass: 79.9, 28.8. Water without absorption: 63.9, 5.2. Milky ice: 16.7, 30.0. Near-row volumes: 48.8, 17.5. **010 s5:** Thin Wall 11.2 s against 11.1, RMSE 35: no gain. **009 s3 steam:** biased volumes no change at 7.3 s.

**Not measured:** a full 008 re-render. If its other scenes scale like scene 4, 8.5 h becomes roughly 2 h; that is inference.

Limits: frame-level likeness says nothing about shimmer on thin structures in motion.
