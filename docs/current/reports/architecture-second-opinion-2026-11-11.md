Read-only. The batch counts as active under your own test. No run_productions.py process is alive and there is no HALT.json, but output/runner/2026-11-11-batch-019-024/state.json (last written 18:06) leaves unit 026 in "waiting for usage limit reset" with no outcome. The runner writes that status just before a 20-minute retry sleep, and restarting it would resume the unit. So I wrote no report file; the full report is below. Once you confirm the batch is stopped (or 026 is reset), I can save it to docs/current/reports/architecture-second-opinion-2026-11-11.md.

Architecture skill: none is on the "Project skills" list. The installed architecture-designer is not sanctioned; I used it under your one-time authorisation as a frame only: requirements, alternatives, failure modes, running cost.

1. Verified baseline, with corrections
Per unit, batch 2026-11-11 (VERIFIED: output/runner/2026-11-11-batch-019-024/*.jsonl, result events, messages deduplicated by id)

Unit	Outcome	Sessions	API calls (main)	Turns (main)	Notional, unit total	Peak context	Images read (distinct)	Bash calls
019	verified	2	235	381	$11.43	454k (callback 463k)	32 (28)	201
020	verified	2	133	215	$5.77	344k	25 (17)	103
021	returned	5 (3 were usage-limit polls)	101+27	181+44	$6.99	361k	29 (20)	104
022	returned	1	145	297	$6.48	375k	25 (10)	131
023	returned	1	112	188	$4.32	294k	18 (10)	82
024	verified	2	183	298	$9.20	480k	33 (24)	126
025	returned	1	107	180	$4.19	303k	17 (13)	89
026	paused	7 (6 were usage-limit polls)	76	142	$3.62	305k	24 (17)	60
Batch totals: $52.00 notional. Of that, $21.98 (42%) went to the four returned topics. That is $17.33 per verified video (3 verified). VERIFIED.

Where the baseline you were given was right (VERIFIED):

Every session starts at about 68k tokens (68.4k–69.5k).
CLAUDE.md is 651 lines and 78,749 bytes.
181–381 turns and 179–365 tool calls per main session.
201 Bash calls in 019.
022 read 25 images of 10 distinct stills.
020 = 215 turns / $5.47; 019 = 381 turns / $10.94.
Sessions are resumed for continuations.
Budget is 12 sessions / 14 active hours.
The runner tells sessions never to stop to report partial progress.
Corrections:

total_cost_usd is cumulative across resumes. 019's callback reports $11.43, not $0.49. Each 021 limit poll repeats $4.51. Summing it per session (as P1 proposes) double-counts. VERIFIED.
Skills exposed: 228, not ~196. The 196 is the user-level folder count; plugins add the rest. Tools exposed: 46, including 8 Claude Docs MCP tools, plus Artifact, Cron, PushNotification and similar that production never uses. VERIFIED (init event).
Ranges are wider than stated.
Peak context: 293k–480k (not 326k–455k).
Main-session notional: $4.17–$10.91.
Images per session: 17–33.
VERIFIED.
"Turns" are not API calls. 181–381 turns is 100–235 API calls, about 1.6–2.0 turns per call. Cost follows API calls × context size. VERIFIED.
Cost composition.
About 75–80% of notional is cache reads: Σ context per call, 21–74M tokens per session. ESTIMATE (standard cache multipliers fit both 019 and 020 within 5%).
Context grows about 1.6k tokens per call, so cost grows roughly with the square of session length.
Thinking: 30–73k tokens per session (VERIFIED, modelUsage.thinkingTokens), at most 11–19% of context growth. Images and tool output make up the rest.
The premise of P15 is false.
025 already ran: its Sonnet session wrote script.json and scenes.json at 15:48, and the topic was returned at 15:52.
026 has a Sonnet-written script and scenes (a Historia, written in about 10 minutes with 3 web searches) and is paused mid-build.
Returning 025 drew a further replacement, 028 (birds on wires).
027 and 028 are stubs (notes.md only).
Return rate so far: 4 of 8 units.
VERIFIED (file timestamps, batch.log).
The script rule is broken in doctrine, not only in the skill. CLAUDE.md "Who writes the script" (the canonical rule, lens decision 2026-11-11) says a raw-bank replacement is scripted by its own production session. The produce skill's step 8 only restates that. Your rule that Opus writes every script contradicts the canonical text. VERIFIED.
The session budget counts usage-limit polls. In run_productions.py lines 271–296, every limit poll increments sessions. The budget is skipped while polling, but checked after the next real session ends. 026 is at 7 of 12, and 6 of those are polls. A longer limit would halt the whole batch for "budget" right after a productive session. VERIFIED.
Interactive sessions outside the runner.
The Opus creative session that developed 019–024 also did the refill and the batch launch: 83 calls, 22.8M cache-read, peak 386k.
The asset-build session ran on Sonnet with no brake or accounting: 93 calls, 16.7M cache-read.
Reader (Haiku) sessions are not costed anywhere, because blind_read.py uses --output-format text.
VERIFIED (project transcripts).
2. Verdicts P1–P16
P1 Cost accounting in state.json: ADOPT WITH CHANGES

What to record:
Per-session deltas: the session's cumulative cost minus its previous cumulative cost for the same session id.
Deduplicated API calls, first-call context, peak context, Σ cache-read.
Images read (total and distinct), limit polls as their own count.
Reader runs and their cost; this needs blind_read.py switched to --output-format json.
Effect: no direct saving. It is the prerequisite for P3 and P16.
Risk: double-counting if built as written (correction 1).
P2 Turn cap with checkpoint handoffs: ADOPT WITH CHANGES (largest per-session lever)

Simulated on the real context curves (fresh session every ~75 API calls ≈ 120 turns, 30k brief, 8 re-orientation calls per handoff):

Unit	Saving
019	46%
024	38%
022	33%
020	30%
021 / 023 / 025	19–21%
026	0%
ESTIMATE. It assumes no rework from lost working memory.

Required changes:

--max-turns does not exist in CLI 2.1.308 (VERIFIED, claude --help). Enforce the cap with a PreToolUse hook that reads context size from the transcript. Past the cap, it denies everything except writing build/checkpoint.md.
Cap on context size (about 200k), not turns, because cost tracks context.
Sessions keep the checkpoint current at every stage boundary, so an abrupt end loses nothing.
Exclude checkpoint.md from the progress fingerprint, as notes.md already is. Otherwise a session that only rewrites the checkpoint never uses up its fix rounds.
Callback as a fresh session: adopt. The callback currently resumes at 455–480k context: 9 calls ≈ 4M cache-read, against about 1M fresh. That saves about $0.30 per video (ESTIMATE).

Limit-hit resumes: keep --resume only for small contexts. 021-5 re-wrote a 326k cache on its first call after the wait (VERIFIED).

P3 Emergency brake: ADOPT WITH CHANGES

Brake on summed delta notional (about $22, which is 2× 019) and on API calls.
Keep the active-hours limit.
Limit polls must never count.
Correctly, the brake ends the unit as "stopped" rather than halting the batch.
P4 Image discipline: ADOPT WITH CHANGES (small)

Drafts are already half-resolution EEVEE (draft_still.py docstring), so the frame cap is largely met.
Real savings: stop re-reads (022 re-read 15 images) and route staging checks through the existing tools/contact_sheet.py.
Effect: about 3–8% (ESTIMATE).
P5 Fewer calls per iteration: ADOPT WITH CHANGES

Collapse calls into a sanctioned tool (for example tools/iterate.py: build, draft stills, contact sheet, compact summary), not free heredocs.
Why not heredocs: hook_blender_guard.py checks only the first word of each line, and the allowlist permits .venv/bin/python:*. A heredoc can therefore spawn Blender, curl or producer.py past both the hook and the deny list. That hole exists today; P5 as written widens it (VERIFIED).
Also add a status tool. 019 spent 26 ls and 30 grep/sed calls just finding its bearings.
Effect: 10–20% (ESTIMATE).
P6 Opus writes every script: ADOPT WITH CHANGES (essential)

The runner cannot gate on "script.json exists": Sonnet sessions create one (025, 026). It needs a provenance stamp written by the creative session, refused by the runner and by scenes_schema.py when absent.
Keep a developed standby buffer. Returns ran at 50%, so without it automation stalls on every return. return_topic.py draws a developed standby first; with none available, it records "replacement pending creative session" and creates no folder.
Amend CLAUDE.md "Who writes the script" under the amending procedure.
Token effect: small. An Opus script is about one sixth of a creative session.
P7 Judge morphology and re-judging 022: forward-only fix ADOPT WITH CHANGES; the 022 re-judge as specified REJECT

Narrow effect today. Replaying a verb-form matcher over all 118 current element records flips exactly one verdict, 022 scene 4 (VERIFIED).
But elements.json keeps only the last reading. Replaying all 16 readings in 022's stream, the first to pass is rung 2, not rung 4: "metal fork sparking in a microwave", 85/85/92. Re-judging only rung 4 means picking which reading counts.
Symmetric stemming loosens the gate on noun/verb homographs. "A bird flying" passes for fly, "a phone ringing" for ring (VERIFIED by a synthetic probe).
Forward fix: event elements (sparks, arcs) declare verb-form aliases at script stage, before any reading, or opt in per element. Root cause for both spark returns: the reader prompt asks for "the single object", which pulls readers toward the dominant object.
022: send it back to a creative session with the corrected aliases and take a new reading of scene 4. Scenes 1–3 and 5 already passed. That costs about one reading cycle and keeps the gate's "never rescue after the guess" principle intact.
P8 Blind proofs before a topic is batch-eligible: ADOPT WITH CHANGES (largest overall lever)

Why it matters: returns are 42% of batch spend.
What the concept audit got right and wrong:
It flagged the sparks in 022 and 023 correctly.
It flagged the mountain in 021, but the column failed.
025 was never audited.
So the trigger must be broader. Prove every element that is not a sealed asset in a sealed pose and not already a passed pattern, not only the elements flagged risky.
Don't run the proofs in Opus. Blender builds there are the most expensive tokens in the system. Opus specifies the proof; a braked Sonnet proof unit builds the still and runs it through blind_read.py; Opus redesigns from the actual readings.
Commission the electric-arc asset job now. Two of the four returns failed on a spark.
Effect: if proofs catch 2–3 of 4 returns at $1–2 each, cost per verified video falls from about $17 to about $11–12 (ESTIMATE).
P9 Fallbacks written by Opus from proof readings: ADOPT

Already half-practised: 019–024's notes carry the audit's fallbacks.
Risk: more topics go back to a creative session. The standby buffer (P6) absorbs that.
P10 Reading budget: ADOPT WITH CHANGES

As written, a 5-per-element cap would have stopped 022 before its doctrine-guaranteed rung-4 attempt; that was its 7th reading (VERIFIED).
Use: at most 2 readings per rung 1–3 (doctrine already treats a second failed round as the signal to step down), exactly 1 at rung 4.
Saving: small. P8 is the real fix.
P11 Notes as a ledger: ADOPT (low impact)

Notes run 13–18 KB. Effect about 1–3%. It helps P2 checkpoints.
Each ledger line must keep what changed, the rung, and why.
P12 Reuse plan in the beat sheet: ADOPT WITH CHANGES

Five new rig files sit untracked in git: paper_rig, micro_rig, corr_rig, manz_rig, titanic_rig.
Supply a generated one-line-per-function index of code3d/lib plus patterns.md, so the Opus session plans reuse without reading the libraries.
Effect: 5–15% of build calls (ESTIMATE).
P13 Session startup isolation: ADOPT WITH CHANGES — target zero skills, not 25

Evidence: every production session invoked Skill exactly once (produce), and none used a blender-* skill (VERIFIED).
Documented mechanisms:
--disable-slash-commands, with the 31-line produce text passed through --append-system-prompt.
--strict-mcp-config with a Blender-only --mcp-config.
--disallowed-tools for Artifact, Cron and the like.
blind_read.py already uses --setting-sources "" and --strict-mcp-config.
The Blender hook is in project settings and is unaffected (VERIFIED).
Effect: about 6–11% per session if the startup context drops ~20k. ESTIMATE; prove it with one trivial headless session comparing first-call cache creation.
P14 CLAUDE.md diet: ADOPT WITH CHANGES

CLAUDE.md is about 20k tokens. Cutting it to 25 KB saves about 4–7% per call.
That saving is illusory if pointers send sessions to read whole specs. 019 already read 84k characters of .md files.
Pair the diet with section-scoped reads, and add a size test.
CLAUDE.md grew from 66 KB (the 2026-11-08 report) to 78.7 KB in three days.
P15 Pending scripts: ADOPT, with a revised scope

025: report it; it is already returned.
026: report its Sonnet-written script and stop the runner from resuming that session (reset its state). An Opus session decides openly, with a lens record, whether to re-source or rewrite the Historia.
027 and 028: an Opus session writes them, or returns them to the bank.
Also commit or archive the untracked artefacts of the returned units: the return path never commits.
P16 Canary: ADOPT WITH CHANGES

One production cannot measure the return rate, and main-session cost varies 2.6× ($4.17–$10.91).
Run at least 3 consecutive units, including one with a proven-risky element. The full metric list is in section 5.
3. Additional optimisations, ranked by saving against risk
Return-rate package: P8 plus the electric-arc asset plus event-element aliases. The largest lever; risk is a thinner bank.
Runner budget defect: limit polls count as sessions (correction 8). A stability fix at near-zero risk.
Runner liveness.
Today "is a batch active?" can't be answered reliably; this session hit exactly that.
Fix: a pid and heartbeat in state.json, plus a next-retry timestamp.
Returned units also leave uncommitted rigs and notes; the return path should commit.
Post-render callback as code. The runner runs verify_production.py and publish_package.py build and check itself; a small fresh session writes only the report and INDEX row. Saves about $0.30–0.50 per video.
Reader cost and context are unmeasured.
019 ran 32 readings, so 96 Haiku sessions.
Capture each reader's cost, and verify whether --setting-sources "" also drops the 228-skill listing.
Status tool to replace orientation calls. Part of P5.
Asset-build sessions under the runner's accounting and brake. The Sonnet build session ran 93 calls with neither.
Split Opus creative work into separate sessions (develop about 3 scripts per session; bank fill separate). The same context-growth argument applies, at a higher per-token price. ESTIMATE.
Test --effort medium on production sessions. Thinking is 11–19% of context growth. Medium risk to judgement, so do it only as a measured A/B.
Doctrine size budget: a test that fails when CLAUDE.md grows past a set limit.
Preflight results reused when nothing relevant has changed. Minor.
Savings I judge illusory or overstated:

P13's "25 skills": the right target is zero.
P14 without section-scoped reads.
P10's cap: P8 is the real fix.
P4's resolution cap: drafts are already half-resolution.
P2 on short sessions: 0–20%.
P11: tiny.
4. Strongest single objection to the package as a whole
It optimises cost per session, but the measured driver is cost per verified video.

Four of eight units were returned, and those returns consumed 42% of the batch's notional spend.
Even the best per-session package (P2 + P13 + P5 + P14, roughly 35–50%) is multiplied by that return rate.
Only P8 attacks it, and P8 as written puts Blender builds into Opus, the costliest place.
The proposed single-production canary can see neither effect.
On a subscription, the binding constraint is the usage window (021 and 026 both hit it), so the true metric is verified videos per usage window.
5. Recommended execution plan
Block	Model	What	Why this model
B0	Owner	Keep the runner stopped; decide the 026 reset	Owner-only call
B1	Sonnet	P1, P3, budget fix, liveness, return-path commit, reader cost capture, with tests	Mechanical and fully specified
B2	Opus	Doctrine amendments: P6, P7 (forward-only), P9, P10 (reworded), P11, P14, size test, under the amending procedure	Preserving meaning and lens approval
B3	Sonnet	P2 (hook and fresh continuation), P13 (proven by one trivial session), P5 tools, P4 wording, callback as code	Code
B4	Opus	P15, developed standby buffer, P12 reuse plans, P8 proof specifications	Your rule: Opus writes every script
B5	Sonnet	Braked proof units; electric-arc asset job	Building, not judging
Before production resumes:

B1–B3 merged, and the test suite green.
026's state reset.
027 and 028 carry Opus provenance, or are back in the bank.
The runner refuses any unit without a provenance stamp.
Preflight passes with the new flags.
What the canary must measure (at least 3 units, against 020, 019 and this batch's averages):

Sessions and handoffs.
Summed delta notional per unit, and per verified video.
API calls and turns.
First-call context, peak context, Σ cache-read.
Images read (total and distinct).
Reader runs and reader cost.
Limit polls.
Return rate, and whether any return was predicted by a proof.
Wall-clock time.
Quality guards: verifier PASS, gate thresholds and aliases untouched, and your verdict.
Success: cost per verified video down at least 30% with no lowering of the gate, and no stalled queue.
