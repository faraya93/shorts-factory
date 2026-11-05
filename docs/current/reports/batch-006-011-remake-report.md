# Batch 006-011 remake: report (2026-11-05)

Six finished publish packages (final.mp4 + cover.jpg + publish.json, `publish_package.py check` OK for all). Nothing published, $0 spent, no accounts, queue untouched.
Render chains: all six logged DONE with no FAILED/INCOMPLETE/Traceback/WARNING after the latest START. All renders ran under caffeinate. All files 1080x1920 with video+audio.
Mechanically verified only (format, duration, frames, gate records). I have not watched or heard them: the owner's eye is the last gate.

| # | Topic | Origin | Variant / scenes | Hero route | Sources / licence | Gate (colour / likeness) | Duration |
|---|---|---|---|---|---|---|---|
| 006 | dedos-arrugados-agua | REMAKE of pieles-arrugadas-agua (hands first, as asked) | chain / 6 | asset: human-hand | Sketchfab "hand" by kevinruiz, CC-BY (credit in description) | PASS / PASS (75, 85) | 46.7 s |
| 007 | candado-solo-abre-su-llave | NEW topic, replaces nube-cuantos-autos-pesa (cloud: no obtainable hero by the asset route) | chain / 7 | code-primitive (geometric: padlock, key, pin tumbler) | own work, no licence | PASS / PASS | 49.4 s |
| 008 | hielo-que-pasaria-si-se-hundiera | REMAKE (hero rebuilt as glass of water with ice) | fork / 6 | code-primitive: ice-cube | own work | PASS / PASS | 45.4 s |
| 009 | termo-por-que-mantiene-el-calor | NEW topic, replaces jabon-agua-sola-no-quita-grasa (soap/grease: fluids and molecules without a passing asset) | journey / 7 | code-primitive: thermos (redesigned after failing likeness twice; passed 70/70 on round 3) | own work | PASS / PASS | 46.6 s |
| 010 | corazon-botellas-al-dia | REMAKE | scale / 6 | asset: human-heart | Sketchfab "Human Heart 3D Model" by Mesh-Magnet, CC-BY (credit in description; version assumed 4.0) | PASS / PASS (90, 92) | 45.0 s |
| 011 | palomitas-por-que-explota-el-maiz | REMAKE (second one first, as asked) | journey / 6 | asset: popcorn | Sketchfab "Popcorn" by varun_malhotra1, CC-BY (credit in description) | PASS / PASS | 45.4 s |

Counts: 4 remakes (006, 008, 010, 011), 2 substitutes (007, 009). Six packages delivered.
Each production's notes.md and `docs/current/reports/lens-decisions.md` hold the lens decisions with reasons (per-production identity presets, support colours, hero redesigns, gate retry, sampling ceiling).

## Open flags for the owner
- Identity: each production uses its own preset (esmeralda, violeta, fucsia, lima, celeste, cobalto) as a lens decision, a departure from Coral; revert by editing `identity_preset`.
- Numbers use secondary, rounded sources: popcorn ~180 °C, "treinta veces"; heart ~70 mL per beat, 5 L/min, ~7,200 L/day, ~3,600 two-litre bottles. Flagged, not primary-sourced.
- 010 narration is 45 s, slightly under the 50-60 s numbers band.
- Likeness readers were two fresh haiku subagents per hero; the hand reads as a hand with pale skin on the 006 stage (skin colour #C98963): design reservation stands, owner to judge.
- CC-BY licence version for the three Sketchfab models is assumed 4.0.
- `tests/test_identity.py` fails: `code3d/lib/corn_rig.py` (ink #1D1B2E, #FFF3E0) and `ice_glass.py` (#1D1B2E) hard-code an identity hex. Not fixed, because editing rig libs stales the composition-gate records of 011 and 008; fix together with the next re-render. All other tests pass (test_asset_library updated to read the archived notes).
