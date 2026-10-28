# Overnight 2026-10-27/28 — summary
- Video 1: `productions/pilot/huincha-de-medir-papel/` (report.md): Papel version of the tape measure, 256 spp, 6.37 h render, scene 4 retried after a transient Metal crash.
- Video 2: `productions/pilot/engranajes-papel/` (report.md): gear ratios, new hero rig `code3d/lib/gear_rig.py`, 128 spp, 4.41 h render.
- Chain: video 1 render (23:49-06:12) -> assembly -> video 2 render (06:12-10:38) -> assembly, driven by an overnight script; the only mechanical failure was the scene 4 start-up crash (auto-retried).
- Names (general): `docs/names-general.md`.
- Infra added: `factory/code3d_render.py` (`render_args`, `--samples`), `tools/narrate.py`, `factory/overlays.py` (Papel end card), `code3d/lib/looks.py` (papel direction), `code3d/lib/gear_rig.py`, `code3d/scenes/gear_01..07.py`.
