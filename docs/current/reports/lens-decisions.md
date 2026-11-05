# Lens decision log

The audit trail required by the owner's governance directive (CLAUDE.md "Governance", 2026-11-04). Every creative or technical decision taken under standing authority gets a row: all involved lenses approved it, disagreements were settled against measured criteria and written doctrine, and the row says how to undo it. Add new rows at the bottom.

Owner decisions are listed separately because they are not lens decisions. Owner-only matters (spending, publishing, creating accounts, the final publish/reject verdict on a finished video) never appear in the lens table.

**How the lenses ran** matters for the audit, so each row states it. "One session" means a single session reasoned through each lens under `docs/architecture.md` "Multi-lens protocol"; "panel" means separate agents.

## Lens decisions
| Date | Decision | Lenses (how run) | Reason and criterion | Where | How to revert |
|---|---|---|---|---|---|
| 2026-11-04 | Likeness gate requires confidence >= 60 from every reader, on top of naming | design, marketing, scriptwriter (one session; the data came from a 16-reader panel) | Names alone wrongly passed 008. Rejected videos scored 15-45, accepted controls 70-95. Manual rule: tighten when the gate passes something the owner rejects. Fitted on these 8 videos | `factory/asset_library.py` `MIN_BLIND_CONFIDENCE`; `docs/current/reports/likeness-calibration.md` | Set the constant to 0 and update the calibration test |
| 2026-11-04 | Blind-naming matches whole words, not substrings | design (one session; technical fix, no other lens involved) | "ice" would have matched "device" | `judge_guesses` | Revert the regex |
| 2026-11-04 | Add 004 and 005 to the calibration as positive controls | design, marketing (one session) | A gate that fails everything would also catch all six; it needs accepted videos to prove it can pass | `likeness-calibration.json` | Remove the two rows |
| 2026-11-04 | AGPL use needs a recorded lens decision instead of the owner's dated OK | design, marketing, scriptwriter (one session) | Licence choice is a technical matter under the directive; the licence rule itself is unchanged, and unclear still means not used | `licence.decision` in `asset_library.py`; registry | Restore `owner_ok` |
| 2026-11-04 | Skill role map, and kiln installed without Studio | design lead, scriptwriter, marketing (one session) | Details and reasons in the manual. Studio auto-registered an MCP server whose worker can bill an API key | `docs/current/specs/asset-system.md` | Reinstall from the pinned commits |

## Owner decisions (2026-11-04)
| Decision | Applied in |
|---|---|
| BlenderKit anonymous search and download allowed; no account | `assets/registry.yaml`, manual, `tools/asset_blender.py` |
| MCP telemetry off (`DISABLE_TELEMETRY=true`) | local Claude Code MCP config, `code3d/TOOLING.md` |
| Sketchfab approved, connection pending the owner's account | `assets/registry.yaml`, manual "Connecting Sketchfab" |
| Likeness gate, declared hero route from 012, organic heroes in code3d: all stand | CLAUDE.md, manual |
| Library `.blend` backup deferred | manual "Open decisions" |
| Governance directive | CLAUDE.md "Governance" |
