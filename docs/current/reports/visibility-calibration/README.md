# Visibility check: calibration and regression (2026-11-08)

Written for the lenses and the owner. Evidence for docs/current/specs/asset-system.md "Visibility check".

- `map.json`: the scenes measured and which rendered objects each element is.
- `results.json`: frame against plate at the final profile with the narration slot. `__control__` hides nothing and renders the same frame twice.
- `regression-009-final-mp4.json`: the frames of 009's shipped final.mp4 against plates graded with the editor's own pass. Subtitle and overlay cells are excluded.
- Calibration set: scenes of docs/current/reports/reader-isolation/ whose elements all passed and whose mean confidence is at least 85 (006 s1, 008 s1-6, 009 s1 and s7, 010 s1, s2, s6), plus 009 s6 thermos (mean 74.7) as a same-frame control beside the plume.

| Group | Readings | p90 dE (min-max) | Area at dE >= 10, % (min-max) | Result |
|---|---|---|---|---|
| 009 plume s6, final.mp4 | 3 | 8.5-10.6 | 0.87-1.64 | FAIL 3/3 |
| 009 steam s1, final.mp4 | 2 | 6.1-6.2 | 0.00-0.02 | FAIL 2/2 |
| 009 plume and steam, raw frames | 5 | 6.5-11.2 | 0.00-2.46 | FAIL 5/5 |
| Strong elements | 21 | 23.2-85.9 | 1.07-49.8 | PASS 21/21 |
| Noise control (same frame twice) | 3 | 0.0 (max dE 1.5 or lower) | 0.00 | nothing measured |

Limits: only one failing subject family (two effects of one production), and the band 11.2-23.2 has no measured case; the threshold is the midpoint of that gap. The owner's verdict on the next translucent effects is what can tighten it.
