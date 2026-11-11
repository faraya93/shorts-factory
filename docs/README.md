# docs/

```
docs/
  architecture.md      the architecture model and the repository organization convention (read first)
  current/             in force
    idea-bank.md       the standing ranked pool of production-ready topics (CLAUDE.md "Idea bank"); filled by an Opus session, drawn by production sessions
    specs/             binding specs and rubrics: design-system.md (+ design-system-assets/), reference-format-spec.md, reference-style-spec.md, style-rubric.md, asset-system.md (hero routing, skill role map, sources, how to run an asset job), format-policy.md (one signature, five structures, three staging modes, reversal evidence)
    reports/           evidence behind adopted decisions: lens-decisions.md (audit log of decisions under standing authority), likeness-calibration.md (+ .json), marketing-verdicts.md (+ cta-redesign/), cta-endcard-audit.md, render-bench.md (+ render-bench/), render-profile-rider.md, format-widening-2026-11-10.md
    research/          reference-channels.md, names-general.md, reference/ (reference videos, gitignored media)
  experiments/         proposals, rounds and tests that informed decisions but are not themselves the spec: design-round2, colour-panel, hard-constraints, marketing-review, motion-finalists, runs/
  archive/             superseded documents, kept verbatim: design-system-round1-superseded.md, design-system-proposal/, design-system-proposed.diff
```

Rules: a new spec goes in `current/specs/`, a bench/audit/verdict in `current/reports/`, external research in `current/research/`; a round of options or a
test that nothing adopted yet goes in `experiments/`; when a document is replaced, `git mv` it to `archive/` and say what superseded it in its first lines.
File names are lowercase-with-hyphens; dated run logs carry the date in the name. Path citations inside moved documents were rewritten mechanically on 2026-10-31.
