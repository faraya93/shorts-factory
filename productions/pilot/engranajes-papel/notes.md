# engranajes-papel: Coral support colours (design lens, 2026-10-28)
Rule: stage colour is background only; supports are chosen per production (CLAUDE.md "Support colours and composition gate").
- Backing board: **#D2EAE6** (pale teal tint), stored in scenes.json `support_colours.board`.
  - Separation: CIEDE2000 from stage ends >= 20 (static, `identity.support_errors`); in frame 31.5-31.9 vs stage.
  - Harmony: derived from the Coral accent teal #0A5C6B (lightened), cool against the warm stage, and 40.1-40.8 from the cobalt gears.
  - Rejected: previous-derived #D1795C (dE 3.4-4.5 from stage, BLOCK); sand #F6D7B7 (17.5 from stage); deep teal-ink #1E4B57 (6.3 from accent); cream #FFF3E0 and periwinkle #E4E9F7 pass (27-29) but are less separated and not accent-derived.
- Hero pinions: DEEP changed #1F3FA0 -> **#4A2BC4** (gear_rig.py); the old deep blue lit to a grey-blue 17.8-19.7 from the ink plinth (BLOCK).
- Accent: coral `emission_gain` 0.111; rendered accent #0A5C6B, dE 0.0 from swatch, 3.44:1 vs stage.
- Gate (scenes 3, 5, 6, 48 spp): PASS. Stills: docs/design-system-assets/support-gate/.
