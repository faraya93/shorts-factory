# productions/

```
productions/
  mecanalia-es/        CURRENT videos of the Spanish channel:  NNN-slug/   (INDEX.md lists them)
  mecanalia-en/        CURRENT videos of the English channel:  NNN-slug/   (none yet)
  _lab/                experiments and tests (look tests, identity validation, spikes, closing tests); never published
  _archive/            superseded or frozen productions, grouped by series; moved here, never deleted
```

Rules (also in CLAUDE.md, "Repository organization"):
- A new video is created ONLY with `.venv/bin/python tools/new_production.py <channel-id> <slug>`: it takes the next three-digit number of that channel
  (numbers are per channel, never reused, the highest is the newest) and adds a row to the channel's `INDEX.md`. Slugs are lowercase ascii words joined by `-`.
- Folder names under `productions/` are channel ids (`mecanalia-es`) or `_lab` / `_archive`. Nothing else lives at this level.
- A production is complete when it has `scenes.json`, `notes.md` (publish package, script, scene plan, fact-check, colour plan, gate result, render and QA),
  `costs.json`, and, once rendered, the publish package: `final.mp4`, `cover.jpg`, `publish.json` (`tools/publish_package.py build`).
- Experiments (look tests, benches, spikes, validations) go in `_lab/<kind>/<name>`; when a video is superseded (new identity, new version) move it to
  `_archive/<series>/` with `git mv`. Never delete, never reuse a number.
- Generated media (`clips/`, `audio/`, `build/`, `final.mp4`, `cover.jpg`) is local and gitignored.
