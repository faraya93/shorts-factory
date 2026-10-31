# shorts-factory

A factory of faceless YouTube Shorts (channel brand: Mecanalia; channels `mecanalia-es`, `mecanalia-en`). Start with `CLAUDE.md` (rules and doctrine) and
`docs/architecture.md` (architecture model and repository organization).

```
channels/     brand package (channels/mecanalia/brand.yaml) + channel variants (es.yaml, en.yaml) + brand assets
factory/      the core: schema, identity/channel loader, editor, render driver, composition gate
code3d/       3D scene library and scene scripts (Blender)
tools/        narration, drafts, gate, glitch scan, new_production.py, publish_package.py
productions/  <channel-id>/NNN-slug (current), _lab (experiments), _archive (superseded)
docs/         current/ (specs, reports, research), experiments/, archive/
tests/        plain scripts: .venv/bin/python tests/test_X.py
```
