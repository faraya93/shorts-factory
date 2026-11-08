# Blind-reader isolation audit (2026-11-08)

Written for the owner. Evidence: the 201 subagent transcripts of past sessions in the Claude Code project log, and `reread.json` here.

## Finding
Past "blind" readers were not fully blind.
- 174 of those transcripts are blind-reader runs. **158 were `general-purpose` agents, and every one had the full CLAUDE.md in its context** (attachment type `instructions`, before the reader answered). CLAUDE.md names the catalogue's subjects: hands, thermos, ice, coffee, heart, bottles. **16 were `Explore` agents, without it.**
- The readers saw neutrally named stills and no subject in the prompt, and their tool use was image reading (920 Read calls, 1 Bash). The priming was the ambient doctrine, not anybody telling them the answer.
- I could not separate which historic scores came from primed readers per record, so the effect on any one past score is not measurable from the log.

## Re-read with isolated readers
The passed elements of 006, 008, 009 and 010 were re-read from their stored stills by three isolated readers each (`tools/reader_audit.py`, `tools/blind_read.py`; a headless session in an empty neutral folder, Read tool only, no settings, no project memory, no MCP). No record was changed.

| Production | Elements re-read | Still pass | Do not pass |
|---|---|---|---|
| 008 ice | 12 | 12 | none |
| 009 thermos | 8 | 6 | scene 2 coffee (confidence 85/85/85, a first guess did not name it); scene 4 thermos (55/55/40, one reader under 45) |
| 010 heart/bottles | 8 | 5 | scenes 3 and 4 bottle (confidence 70-90, a first guess named the heart instead); scene 5 bottle tower (40/55/55) |
| 006 fingers | 11 | 7 | scene 3 finger (35/35/90); scene 4 finger and water (60/60/45); scene 6 finger (60/55/85) |
| **Total** | **39** | **30** | **9** |

Of the 9, some are multi-element scenes where the pass rule asks every first guess to name every element, so a correct reading that listed a different element first fails; those are 009 s2 and 010 s3-4. The weak ones on likeness itself are **006 s3, 006 s6, 010 s5 and 009 s4**. 006's secondary elements carry the owner's one-off floor exception, which this re-read did not apply.

These productions stay as they are; none is published, and the owner has the last verdict. The re-read is information for that verdict.

## What changed
Productions from 012 on (`gate_version: 2`) refuse any likeness or element record that did not come from `tools/blind_read.py`.
