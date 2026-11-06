# Every-element rule, dynamism rule, remake of 006, 008, 009 and 010: report (2026-11-05/06)

Nothing published, $0 spent, no accounts, orchestrator, queue and excluded list untouched. All renders ran under caffeinate (the driver wraps Blender). I have not watched or heard any video: everything below is mechanical (stills, blind readers, frames, durations).

**Closing count: 1 finished publish package (010); 3 productions committed as skipped with the reason (006, 008, 009); 4 productions archived as the "before"; 2 doctrine rules recorded; 1 gate extended (hero -> every scene element).**

## Part 1: rules recorded
- **Every element at hero standard**: `CLAUDE.md` "Every element at hero standard", `docs/current/specs/asset-system.md` "Every element", lens-decisions row 2026-11-05. Routing (asset > proper material or build > primitive only if genuinely geometric and instantly readable) applies to every represented element in every scene; materials count as modelling; heat and signal graphics must match the scene's realism.
- **Extended likeness gate**: `scenes.json` `scene_elements`; `gate.py stills` (unmasked stills), `asset_library.py element` (blind naming per element), `gate.check(prod, scene)` called per scene by `code3d_render.py --mode final`. `blind-pack --multi` lets readers name up to three things so secondary elements are judged from the same stills. Tests added (27 pass in test_asset_library); the pre-existing `test_identity` failure (rig libs with hard-coded hexes) is unchanged.
- **Dynamism is a hard bar** (added mid-run): `CLAUDE.md` "Dynamism is a hard bar", lens-decisions row. Escalation is staged as growth and camera travel; at least three framings; first/middle/last-frame contact sheet before a final render.
- **`transparent` render profile** (transmission 8, volume 2, max bounces 14): `channels/mecanalia/brand.yaml`, per scene via `render.scene_types`. Measured: stills 7-25 s at 24-48 samples; final frames 6.9-7.6 s/frame at 64 samples (010, incl. a 960-bottle tower).
- **Lens decision, recorded in the code docstring and here:** clear materials (glass, water, ice) are named `clear_*` so they fall in the composition gate's unmeasured `other` class; they inherit the stage colour by refraction, so the stage-hero colour rule cannot apply; the blind-naming gate guards them instead.

## Part 2: archive and remakes
Archived (records and local media intact) to `productions/_archive/retired-006-008-009-remade-2026-11-05/` (006, 008, 009, and 010 as the before; `BEFORE.md`). Numbers reused by the remakes.

| # | Result | Structure | Package |
|---|---|---|---|
| 006 dedos-arrugados-agua | **SKIPPED** (scenes 2 and 5 blocked) | chain / 6 | none |
| 008 hielo-que-pasaria-si-se-hundiera | **SKIPPED** (scene 2 blocked) | fork / 6 | none |
| 009 termo-por-que-mantiene-el-calor | **SKIPPED** (scene 2, coffee element, blocked) | journey / 7 | none |
| 010 corazon-botellas-al-dia | **DONE**, 45.0 s, 1080x1920 with audio | scale / 6 | `productions/mecanalia-es/010-corazon-botellas-al-dia/` (final.mp4, cover.jpg, publish.json; `publish_package.py check` OK; render log has no FAILED/INCOMPLETE/Traceback/WARNING after its START) |

### 010 (finished)
Routes: heart = library asset `human-heart` (Sketchfab "Human Heart 3D Model" by Mesh-Magnet, CC-BY, credit carried in `publish.json`; licence version assumed 4.0 as before); bottles = `bottle_real.parts` (PET shell lathe with wall thickness, refracting water, cap; build route, genuinely a revolved profile); cup = `real_kit.tumbler`; pumping tube = clear glass tube with red slugs along it; wall and tower = clones of the same real bottle (150 and 960 bottles drawn; 3,600 is spoken and shown as a counter).
Extended gate, blind readers (two per scene, confidence): s1 85/88 (heart, bottle, tube); s2 88/75 (heart, glass); s3 80/80 (bottles); s4 85/90 (bottle wall); s5 70/80 (bottle tower); s6 95/96 (heart). Hero likeness record for the heart: 95/96. Colour gate: PASS.
Dynamism check (first/middle/last frame of each real clip): all six scenes change; framings differ (orbit from heart to bottle, push to heart then pan to cup, pull-back and rise, travelling along a growing wall, climbing a tower, push-in orbit on the heart alone).
Render: chain 01:11 to 02:56 (1 h 45 min), 6.85-7.56 s/frame at SF_SAMPLES=64.
Caveats: the bottle liquid reads as clear water (the red slugs are the only red), so "blood volume" is stated by the narration, not by colour; white blocky patches in the wall and tower are softbox reflections on the bottles (a reader called them rendering glitches); heart and bottle sizes are not to scale; the tower draws 960 bottles. I did not watch it.

### 006 (skipped)
Built: real water and glass tray (refraction), hand asset kept, a real wrinkling fingertip mesh with subsurface skin, a nerve-and-vessel x-ray, wet glass pane with droplets, wet-grip beat. Gate: scenes 1, 3, 4, 6 pass (60-85); scene 2 (vessels inside a fingertip) failed four staging rounds (35/40, 35/35, 30/35, 60/25) because readers call it a glass tube; scene 5 (grip) failed a stone (40/65, 75/40, 40/35) and then a bar of soap with suds (65, 55/60). Fix not tried: x-ray on the hand asset itself, articulated fingers. Reasons and resume steps are in its `notes.md`.

### 008 (skipped)
Built: real glass tumbler, refracting water, ice cubes with frosted surface and cloudy core, a freezing front (water material hands over to ice material), sinking cubes, lake tanks. Gate: scenes 1 (92/80), 3 (85/85), 4 (85/70), 5 (90/85), 6 (85/85) pass; scene 2 (water freezes, 9 %) failed five reader rounds across four stagings (the frozen glass reads as "frosted glass", ice named at 25-55). Lesson recorded: a smooth ice slab reads as mist (15/25); piles of real cubes read as ice (70-90).

### 009 (skipped)
Built: hollow double-walled flask from real lathes, sweeping cut plane revealing walls, gap and coffee, coffee as refracting liquid, glowing inner steel, tracer air spheres, light rays, steam volumes; first-version blue boxes and dots are gone. Gate: scenes 1 (85/85), 3 (65/60), 4 (70/70), 5 (60/72), 6 (65/65), 7 (85/80) pass; scene 2 passed as a thermos (80/72) but its **coffee** element was never named coffee ("dark amber liquid"), and a steaming cup beside it scored 55/60. The handle was what made readers say "thermos" (without it: "blue cylinder", 55/50). Likely fix: pour the coffee or add crema and steam over the open neck.

### Lens decisions with reasons
Recorded in `docs/current/reports/lens-decisions.md` (the two rules). Staging decisions are in each production's `script.json` lens block and `notes.md`: 006 drops the tyre analogy (reframe "canales de agarre"); 008 acts freezing by a front and the lake by sinking cubes; 009 keeps the journey structure with a cut plane that moves; 010 shows the pump with a tube and staged growth. Stage presets kept from the first remakes (esmeralda, fucsia, lima, celeste).

## 010 audit of the OLD production (no rework asked): violations of the new rules
1. Bottles (s1, s3, s4): flat-colour opaque blue lathe bottles, no water, no transparency: stand-in for a real object. 
2. "Glass of blood" (s2): an alpha-blended glass cylinder with a flat red cylinder inside: flat-colour stand-in for a liquid and for glass.
3. Bottle wall (s4) and tower (s5): flat blue low-poly slivers (scale 0.3), hundreds of them; the "3,600 bottles" were not readable as bottles.
4. The pumping mechanism was never shown: the heart only scaled.
5. No scene declared key elements; the extended gate never ran.
6. Dynamism: one fixed framing for most of the video with a counter climbing (7196 L, 3600), which is exactly what the new rule forbids. Only the heart (library asset, 90/92) met the standard.

## Open flags for the owner
- **Floor of 60 on secondary elements is uncalibrated.** It was fitted on hero stills only. On stylised cutaways readers often name the object correctly but stop at 55 (009 s2, s4, s5, s6 all went 55 then passed on small changes), so near-misses may be reader noise. Reader confidence also varied 25-88 on near-identical stills. I did not loosen it or widen aliases. Your call: recalibrate on secondary elements, or keep it.
- Three productions are skipped for 1-2 scenes each; each `notes.md` lists the concrete next step. Resuming any of them is a few hours, mostly reader rounds.
- Editing `real_kit.py` or `finger_rig.py` stales the element records of every scene that lists them in `rig_libs`; re-name or carry over (I carried over unchanged scenes after comparing re-rendered stills, mean pixel difference < 0.07 of 255, and said so in 006's notes).
- Likeness readers are haiku subagents reading two stills; they are not people on a phone. Your eye is still the last gate.
