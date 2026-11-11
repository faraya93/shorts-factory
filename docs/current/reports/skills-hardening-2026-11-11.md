# Skills hardening: project allowlist, produce skill audit, standing fossil scan

Date: 2026-11-11. Owner instruction, applied under CLAUDE.md "Amending doctrine". One session reasoned through the design, scriptwriter and marketing lenses; no disagreement. Doctrine and records only: nothing under factory/ or tools/ changed, no skill folder moved, renamed or deleted.

## Census (where skills are named)
- **Runner and produce skill:** `tools/run_productions.py` prompts name the `produce` skill and blender-core's `run_in_blender.py`. The produce skill names blender-core (helper) and asset QA.
- **Doctrine:** `docs/current/specs/asset-system.md` "Skill role map" names 14 asset-job skills (`blender-kiln` plus 13 `blender-*`, including `blender-asset-qa`). `docs/architecture.md` "Multi-lens protocol" names the lens kits: "marketingskills + social-media-skills" (two packs, not skills), "yt-* kit" (a wildcard), `short-form-video-script`, `hook-writer`, Tastemaker, `design-taste-frontend`. CLAUDE.md names `tastemaker` (style lock). Records name `yt-seo`, `youtube-shorts`, `social-seo` (lens-decisions, 2026-11-08) and `thumbnail-design` (marketing verdicts).
- **Closure:** `blender-asset-qa` names `blender-retopology-uv`, `blender-character-rigging`, `blender-scene-setup` (all already listed by the role map). The remaining `blender-*` names in blender-core and asset-qa are the uninstalled game/pipeline skills the manual already says to ignore.
- **Lens kits are resolved to names.** An allowlist cannot hold a wildcard or a pack name, so "yt-* kit" became `yt-script` and the marketing packs became the five named skills above. Other yt-* skills (`yt-audit`, `yt-chapters`, `yt-comment`, `yt-edit`, `yt-package`, `yt-plan`, `yt-retention`, `yt-viral`) have no evidence in live doctrine and are NOT listed; `yt-script` and `yt-viral` appear only in an experiments record.
- **Cross-references not adopted (decision):** `short-form-video-script`, `hook-writer`, `youtube-shorts`, `social-seo`, `thumbnail-design`, `yt-seo` and `tastemaker` point to other installed skills (`brand-profile`, `voice-builder`, `caption-writer`, `reels-script`, `tiktok-script`, `veo-3`, `nano-banana`, `ai-video`, `scheduling-and-queue`, `hashtag-strategy`, and others). These are "see also" routes to other platforms and tools, not dependencies; closing over them would pull in most of the bulk bundle. Same treatment the asset manual gives blender-core's routes to uninstalled skills. The repo's `channels/mecanalia/brand.yaml` serves as the brand profile.
- **Not listed, no evidence:** `systematic-debugging`, `verification-before-completion`, `architecture-designer` (wrote architecture.md; history), and every other installed skill.

The sanctioned list and each skill's role and evidence are in CLAUDE.md "Project skills" (25 skills).

## Changes
1. CLAUDE.md: new section "Project skills" with the list and the rule; Governance no longer authorises skill installs on its own and points to the section; "Skill roles" bullet reworded to point to it.
2. Live restatements aligned: `docs/architecture.md` (lens table names, plus a pointer line), `docs/current/specs/asset-system.md` (two sentences that said installing skills was within lens authority).
3. Amending doctrine: new step 6 "Fossil scan"; the old step 6 "Record it" is now step 7. No document cites a step number of the procedure (grepped).
4. Produce skill (outside the repo, `~/.claude/skills/produce/SKILL.md`): three fossil fixes.

## Three fossil fixes in the produce skill
- Step 1: "Productions 012-016 proceed from their slate" is now "A topic with a developed script on file proceeds from that script"; the pointers after it are unchanged.
- Step 5: "From production 019 the design lens chooses..." is now "The design lens chooses..."; the from-019 fact stays in format-policy.md and lens-decisions.
- Step 8: "(CLAUDE.md, owner 2026-11-10)" after CONTEXT STAGING is now `(CLAUDE.md "Reshape ladder")`.
After the edits the skill contains no calendar date and no production number (grepped).

## Pointer audit of the produce skill
Every target exists. "Heading" = a `##`/`###` heading; "lead-in" = a bold lead-in bullet inside a headed section (resolves, but is not a heading).
| Pointer | Result |
|---|---|
| CLAUDE.md "Governance" | heading |
| CLAUDE.md "One launcher for Blender" | lead-in under "House rules" |
| CLAUDE.md "Idea bank" | heading |
| CLAUDE.md "Drawing" | lead-in under "Idea bank" |
| CLAUDE.md "TOPIC BALANCE" | lead-in under "Topic selection" |
| CLAUDE.md "Format policy" | heading |
| CLAUDE.md "Script flatness" | heading ("Script flatness, floor handling and modellability", prefix) |
| CLAUDE.md "Reference doctrine" | heading |
| CLAUDE.md "Asset library and hero routing" | heading |
| CLAUDE.md "Every element at hero standard" | heading |
| CLAUDE.md "Dynamism is a hard bar" | heading |
| CLAUDE.md "Reshape ladder" | heading |
| CLAUDE.md "Where the ladder stops" | lead-in under "Reshape ladder" |
| CLAUDE.md "House rules" | heading |
| docs/current/idea-bank.md | file exists |
| docs/current/specs/format-policy.md "Historia" | heading ("Historia (`story`, from production 019)") |
| docs/current/specs/format-policy.md "Staging mode" | heading |
| docs/current/specs/render-cost-playbook.md | file exists |
| assets/patterns.md | file exists |
| docs/architecture.md "Multi-lens protocol" | heading |
| docs/current/reports/lens-decisions.md | file exists |
| docs/current/specs/asset-system.md | file exists |
| docs/current/specs/asset-system.md "Advance assets" | heading |
No pointer needed retargeting and none names vanished doctrine. The four lead-in pointers resolve but would break silently if someone reworded the bullet; left as is, noted.

## Fossil scan (first run, on the surfaces this amendment touched)
Touched: the new CLAUDE.md section, the Governance bullet, the Amending doctrine list, the two asset-system sentences, the architecture lens table, the produce skill. Found and fixed: the three above. Left, as standing provenance not transition facts: dated headings (the repo's convention, e.g. this section's own). Candidates NOT touched because this amendment did not edit those passages (for the next amendment that does): CLAUDE.md "Topic selection" (the line that says productions 012-016 come from the first slate), "Channel strategy"/"Format policy" 2026-dated "earliest review" text, and the asset-system "Installed ... commit" paragraph (an install record).

## What did not change
Owner-only boundaries (spending, publishing, accounts, final verdict); no skill folder moved or deleted; the asset manual's role map and its ignore-list; the rule that CLAUDE.md wins over a skill; all production and gate doctrine.

## Precedence
Where older live text (Governance's former "installing additional free skills", the asset manual's "within lens authority", the architecture lens kits) disagrees, "Project skills" governs.

## Checks against standing doctrine
Governance's lens-decision condition (recorded below); owner-only list untouched; one canonical home (list lives only in CLAUDE.md, others point to it); historical records unedited (lens-decisions gets a new row only); skill writing standard (mechanisms, not instances) applied to produce.

## Open doctrine question (for the next bank refill)
Produce step 8's return flow says "do not write the replacement's script". It was written when production sessions wrote scripts. Once the refill settles the script model it needs two cases: a topic drawn from a developed set already has its script on file; a topic drawn from the raw bank has none. Not rewritten here, by instruction.
