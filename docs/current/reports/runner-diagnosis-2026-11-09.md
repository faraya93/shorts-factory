# Runner diagnosis, 2026-11-09: why the headless sessions could not execute

Scope: analysis only. The only file written is this report. The only execution was one permissions probe. Nothing in the recommendation is approved or applied; it is a proposal for the owner's decision. Times are EST.

## Summary

- **The denial is a standing configuration gap, not a transient failure.** The probe reproduced it at 08:45, 8.5 hours after the batch. It comes from `--permission-mode dontAsk` plus an allowlist in `tools/runner-settings.json` that does not cover the shell forms the sessions use, chiefly the form the `produce` skill itself prints (`tools/blender_run.py --status`).
- **Bash was never blocked as a whole.** In the batch, 26 Bash calls ran and 17 were denied, and each denial is a specific command form. The sessions wrongly concluded "Bash is denied" and stopped.
- **A real transient failure did happen, but somewhere else.** The launching interactive session hit "auto mode classifier gave no verdict" 5 times. None of the runner's streams contain that message.
- **The batch burned out because no layer treated a denial as an infrastructure failure.** The result event reported `is_error: false`, the runner ignored `permission_denials`, three fix rounds were spent with no progress check, the driver ignored the runner's exit code, and the launching session left 15 seconds after launch.
- **All three accounting defects are confirmed,** and `batch.sh` still exists, in a temporary directory only.
- **No production has a clip or a queued final.** The step that queues the final has never run from a runner session, so it is untested.

## 1. What denied Bash

### Evidence

The launch command (`tools/run_productions.py:29`) is `claude -p ... --permission-mode dontAsk --settings tools/runner-settings.json`, with stdin closed. The `apiKeySource` is `none`, so the sessions use the subscription login. Project settings (`.claude/settings.json`) add only the Blender guard hook, which never fired here, and user settings hold no permission rules. There is no `.claude/settings.local.json` at either level. `runner-settings.json` is therefore the whole permission surface: anything it does not match is refused, because nobody can be asked.

The denial text in the streams is: "Permission to use Bash has been denied because Claude Code is running in don't ask mode... If you believe this capability is essential... STOP and explain to the user". That is a permission-mode refusal, not a network or server error.

Census of all 236 Bash calls in `output/runner/*.jsonl`:

| Set | Allowed | Denied |
|---|---|---|
| 2026-11-08 sessions (012, Opus) | 186 | 3 |
| 2026-11-09 stray `--help` unit (section 2) | 2 | 2 |
| 2026-11-09 batch (012-016, Sonnet) | 26 | 17 |

Every one of the 22 denials contains at least one form the allowlist does not cover. Sorted by primary form:

| Form | Denied | Allowed | Example |
|---|---|---|---|
| A segment starting with bare `tools/...` | 10 | 0 | `tools/blender_run.py --status 2>&1 \| tail -5` |
| `cd <path>` combined with `git` in one command | 4 (6 counting those that also had `tools/`) | 0 | `cd .../014-... && ls -la && tail -80 notes.md && git diff --stat .` |
| Redirection into a file, including heredocs | 3 | 0 | `cat >> .../notes.md <<'EOF'` |
| Shell loop | 1 | 0 | `for d in ...; do ...; done` |
| `.venv/bin/python -` with a heredoc | 1 | 0 | inline script on stdin |
| 2026-11-08 only: env prefix, `$P` expansion, `grep` outside the project | 3 | not measured as a class | `SF_ALLOW_GUI=1 .venv/bin/python ...` |

The strongest natural experiment is two near-identical commands:

- `tools/blender_run.py --status 2>&1 | tail -5` was **denied** on three consecutive sessions (012-6, 012-7, 012-8).
- `... && .venv/bin/python tools/blender_run.py --status 2>&1 | tail -3` was **allowed** (016).

The only difference is the executable's prefix.

### Why the commonest form is denied

- `runner-settings.json` allows `Bash(tools/:*)`. The `:*` form means a prefix followed by a word boundary, so it matches a command word `tools/` and not `tools/blender_run.py`. The boundary semantics are from memory; the behaviour is measured (10 denied, 0 allowed, plus the probe).
- The `produce` skill prints that exact unmatched form (`~/.claude/skills/produce/SKILL.md` step 9: "check `tools/blender_run.py --status`", "`tools/asset_blender.py close`").
- A second defect sits behind the first: `tools/blender_run.py` and `tools/asset_blender.py` are mode 644, as are 26 of the 35 scripts in `tools/`. Even with a correct allow rule, running them bare would fail at the shell.

The other forms are inferred from the correlation above, because the harness does not state a per-command reason.

### The probe

One headless session, launched from a scratch script with the runner's exact argument list, working directory, closed stdin and `CLAUDECODE*` environment stripped. Its stream went to this session's scratchpad, so `output/runner/` was not touched. It was instructed to run one command once, `tools/blender_run.py --status` (read-only: it prints lock and process state). That is the command that was refused three times running.

| Field | Result |
|---|---|
| Time | 2026-11-09 08:45:50-08:45:54 |
| Mode, model, version | `dontAsk`, `claude-opus-5-5`, 2.1.308 |
| Outcome | **DENIED**, same don't-ask message, recorded in `permission_denials` |
| Turns, wall time | 2 turns; 1.9 s reported by the session |

**The denial still happens now.** It also happens on Opus, so the model is not the cause. One probe does not re-test the forms that were allowed, but the census already shows those.

### Transient versus standing

| | Transient classifier error | Standing permission denial |
|---|---|---|
| Where | Launching interactive session only (auto mode), 5 occurrences, 00:06-00:07 | Headless runner sessions (`dontAsk`) |
| Message | "server-side auto mode classifier gave no verdict (error)... transient" | "denied because Claude Code is running in don't ask mode" |
| Occurrences in runner streams | 0 of 28 files | 22 calls |
| Clears on retry | Yes, it did within seconds | No: same refusal on identical commands, and again 8.5 hours later |

The two look alike in chat and are unrelated. The launcher's "Bash is failing at the classifier" has no bearing on the runner.

### Why the sessions believed all of Bash was gone

- Every session of the batch's first round opened with one long compound reconnaissance command, and each of those contained an uncovered form. A single denial therefore landed on the first Bash call (012-5, 013-1, 014-1, 015-1, 016-1).
- The denial text tells the model to STOP and explain. Sonnet complied, in 5 turns.
- The sessions then resumed with that belief in context ("Bash was denied again"). Notes in 014 and 015 record mistaken generalisations, such as "only the verifier command is permitted".
- On 2026-11-08 Opus took 3 denials in 012-1 and carried on for 142 turns, using `.venv/bin/python tools/...`. The runner route works when the commands match, as the 186 allowed calls show.
- The runner passes no `--model`, so it inherits whatever is configured. The streams show Opus on 11-08 and Sonnet on 11-09. User settings now say `opus`, last edited at 08:43 today, after the batch. Model behaviour widened the damage but did not cause the gap, and with only these runs the two factors (model, command style) are confounded.

## 2. Why it consumed the batch in twelve minutes

The batch ran 00:07:55-00:19:10: 012 took 64 s, 013 6 min 17 s, 014 52 s, 015 61 s, 016 2 min 2 s. Sixteen of the 20 batch sessions recorded at least one denial, and none reported an error.

| # | Mechanism | Evidence |
|---|---|---|
| 1 | A denied session is a "success". The result event carries `is_error: false`, and the runner only acts on `is_error` plus a usage-limit regex. | `run_productions.py:56-59`; `permission_denials` is populated in the streams and read nowhere |
| 2 | Fix rounds have no progress test. Any verifier failure spends a round and starts another session, regardless of whether anything changed. | `run_productions.py:119-127`; 014-4 and 016-4 ran 1 turn and no tools |
| 3 | The verifier cannot distinguish "not built yet" from "broken". A script-stage production prints `scenes.json missing` and stops there. The docstring advertises `--stage` but the code never reads it. | `tools/verify_production.py:1,20-23` |
| 4 | The fix-round prompt says "The render chain has finished (or none is running)... Finish what remains". With nothing built and no shell, the session can only write a status note. `wait_for_render` returns immediately because no chain exists. | `run_productions.py:127,68-73` |
| 5 | The runner's "stop at the first failure" guard was bypassed. The driver launches the runner once per production and ignores its exit code, so `rc=1` means nothing. | `batch.sh`; `batch.log` shows each "runner stopped" followed by the next START |
| 6 | No preflight. Nothing tested the permission route before spending the first unit. | Launcher transcript; no probe step |
| 7 | The launcher left almost at once: its last message is 00:08:10, 15 s after START, after reading the log once at +8 s. The brief said to leave it unattended, so nobody was watching, and no alert path exists. | Transcript `c25b883f...`, "I'm not waiting on it" |
| 8 | A warning was available and missed. At 00:04 the launcher ran `run_productions.py --help`. The runner has no argument parsing, so `--help` became a production and started four real sessions, two of which were denied. | `output/runner/--help-{1..4}.jsonl`; `--help` unit in `state.json` |

The usage cost was small: about US$3.61 notional across the batch and the `--help` unit (last cumulative figure of each session chain). The sessions use the subscription login, so this is not a charge. The real loss is the night.

The `--help` unit also explains the puzzle in 012's notes. Sessions `--help-2` and `--help-3` inferred from the repo that they were on 012, and wrote "Runner callback" entries into 012's `notes.md`. The verifier they were quoting was checking a folder literally named `--help`, hence "scenes.json missing" against a production that has one.

## 3. Accounting defects: all confirmed

**A returned topic scored as "stopped: verifier still failing".** `state.json` shows that status for 013, whose `notes.md` says RETURNED, as do the bank, the lens-decisions row and `INDEX.md`. The runner has no concept of "returned".

**The replacement was created but never queued.** The folder for 017 exists and the bank marks it drawn, but `batch.log` has 0 `QUEUED` lines. The precise cause:

1. `batch.sh` greps `^REPLACEMENT: `.
2. The session's `echo "...REPLACEMENT: ..." >> notes.md` was denied (a file-redirection denial, session 013-4).
3. It wrote the line with Edit instead, as a bullet: `- REPLACEMENT: productions/...` (`notes.md:84`), followed by another bullet, so it was neither anchored nor last.
4. The anchored grep matched nothing.

So a permission denial caused this as well, and the protocol was a free-text marker with no validation.

**The batch driver lived in a session scratchpad.** It **still exists**, 1,016 bytes, 00:07, at `/private/tmp/claude-501/-Users-fernandoaraya-projects-shorts-factory/c25b883f-f08a-4564-a27d-4d347219b872/scratchpad/batch.sh`. It is unversioned and in a temporary directory, so it should be assumed to be lost on cleanup. Its logic is reproduced in this report only in outline; the rewrite in section (b) replaces it.

## 4. What is uncommitted

The tree is even with `origin/main`. Nine entries, none staged:

| Path | Change | Matches the records? |
|---|---|---|
| `docs/current/idea-bank.md` | +2/-2: rank 1 marked `drawn 017 2026-11-09`; 013's returned note in the rolling-window line | Yes. Stale: the header still says 10 undrawn; the table now has 9 |
| `docs/current/reports/lens-decisions.md` | +1 row: 013 returned, 017 drawn, refill due | Yes. One error: it says the window has "no repeated theme", but 012 and 016 are both toilet. That is within the cap of two, so the draw stands |
| `.../012-.../notes.md` | +9 | Directive present. Also contains two callbacks written by the `--help` unit (section 2) and one tooling-block callback |
| `.../013-.../notes.md` | +16 | Directive, run logs, RETURNED and the replacement, as described |
| `.../014-.../notes.md` | +8 | Directive present. The BLOCKED section mis-states the cause (says only the verifier was permitted) and contradicts itself on whether the verifier ran |
| `.../015-.../notes.md` | +7 | Directive present; correctly says not returned |
| `.../016-.../notes.md` | +9 | Directive and two status entries |
| `productions/mecanalia-es/INDEX.md` | +2/-1 | 013 returned, 017 row added. The 017 row has five columns where 012-016 have six (the format `new_production.py` writes) |
| `.../016-.../scenes.json` | new, untracked | Not part of the directive. A skeleton from the third callback: it passes the schema, but `hero_rig`, `rig_libs` and `scene_script_prefix` name code that does not exist |

The directive blocks are present in all five slate productions, and the 013 return records agree with each other. The empty 017 folder has nothing for git to track; only its `INDEX.md` row shows up.

## 5. What exists now, per production

| # | State | Blockers |
|---|---|---|
| **012** toothbrush | Assets sealed in `assets/library`; `scenes.json`, `script.json`, narration audio, 7 scene scripts, `cepillo_rig.py`, gate folder with records. No clips, chain log, final, cover or package | 18 verifier failures: scenes 3 and 4 failed blind naming (plume read as "blue paint splatter"); scene 5 record stale; scenes 1, 2, 6 and 7 lack `visibility` entries (a rule newer than the build). **The liquid-drop re-stage the batch ordered was never attempted**: every session that could have done it was denied |
| **013** finger joints | `notes.md` and `script.json` only. **RETURNED.** Real pre-check work happened on rungs 1 and 2 | None; closed. Its working `.blend` and stills are in a scratchpad, and its two CC-BY assets are not in the library or `LICENSES` |
| **014** gum | `notes.md`, `script.json`. Script stage | Never started: no bar tested |
| **015** flies | `notes.md`, `script.json`. Script stage | Never started: no bar tested |
| **016** poop | `notes.md`, `script.json`, untracked skeleton `scenes.json`. No rig, assets or gate | Never started: no bar tested |
| **017** elevator | **Empty folder**; `INDEX.md` row (`draft`); bank mark `drawn 017`. No script, notes or directive | Not queued |

No Blender or runner process is live now. No render ran, nothing was published, and no chain log exists for 012-017.

## RECOMMENDATION (proposal for the owner's decision; nothing is pre-approved)

### (a) Fix the headless execution route

Keep `dontAsk` and the allowlist, and make three small changes:

1. **Fix the rules in `tools/runner-settings.json`.** Replace `Bash(tools/:*)` with a rule that actually matches shell scripts in `tools/`, and allow the exact queue form.
2. **Make the skill's commands match.** In the `produce` skill, write every Python tool as `.venv/bin/python tools/x.py ...`, a form that already passes and needs no executable bit.
3. **Add a short standing instruction to each headless session (`--append-system-prompt`):** one purpose per Bash call; no `cd` (the working directory is the repo root); use Edit, never redirection, to change a file; a denial applies to that command form only, so retry with the allowed form and never conclude that Bash is unavailable.

Also pin the model explicitly (`--model`, read from an environment variable) so a settings change cannot silently alter a batch. I would default it to Sonnet, as the "Drawing" doctrine says, and let the canary show whether that holds.

Reasons: it is the smallest change that addresses the measured causes, and it keeps the deny rules. Cost: about 30-45 minutes of session time, no render and no spend.

Caveats: the replacement wildcard syntax is not yet tested (only one probe was authorised), and the preflight in (c) must prove it.

Alternatives:

- **`bypassPermissions` / `--dangerously-skip-permissions`: reject.** The runner's own docstring forbids it, and it removes the guard rails for unattended sessions that can push to `main`.
- **A PreToolUse hook that approves project-approved patterns: keep as the fallback** if the allowlist cannot express compound commands. It is our own testable code, but I have not verified how it interacts with `dontAsk`.

### (b) Runner accounting

Move the driver into the runner as a durable, versioned queue, for example `tools/run_batch.py` with its state in `output/runner/`. Specifically:

- **A returned topic is a completed unit.** Add a status `returned` with `replacement`, checked **before** the verifier, so it costs no fix round.
- **Deterministic return.** A small tool, say `tools/return_topic.py <prod> <reason>`, does the whole sequence in code: writes notes, bank mark, `INDEX.md`, calls `new_production.py`, and writes a structured sidecar such as `returned.json`. The runner reads the file and appends the replacement to the queue in the same run. No free-text marker to grep.
- **Distinct unit outcomes,** driving the batch: verified or returned (next unit), topic-level stop (next unit; the owner's stance is that production flows on), infrastructure stop (halt the batch).
- **Argument handling.** Use `argparse`, and refuse any path that is not a production folder containing `script.json` or `notes.md`. `--help` must never start a session.
- **State commands instead of hand-editing,** for example `--reset <unit>`. The launcher edited `state.json` directly last night. Clear the stray `--help` entry at the same time.

Cost: about 1-2 hours of session time plus tests (`tests/test_render_chain.py` is the model). No render, no spend.

### (c) Relaunch shape

**Preconditions, in order:** (1) apply (a) and (b); (2) commit the pending records as one commit, adding a one-line correction in 012's notes that the two `--help` callbacks came from a stray unit; (3) add a `BATCH DIRECTIVE` to 017's folder, which needs a notes file created first; (4) pass the preflight.

**Order:**

| Step | Production | Route | Why |
|---|---|---|---|
| 1 | **015, alone, as canary** | Runner, watched until it passes the hero gate | Script ready and hero asset named (CC0 fly). Its failures would be attributable to the route, not to a known likeness problem |
| 2 | **014, 016, 017** | Runner, unattended, after a clean canary | 016's skeleton `scenes.json` becomes the starting point. 017 needs its script written and the `produce` skill's script step covers it. Variants stay inside the rule: 014 journey, 015 journey, 016 scale, 017 fork |
| 3 | **012** | Interactive Opus session, while no batch is running | Departs from the owner's stated order (012 first), and the reason is attributability: 012 is blocked by a genuine likeness problem needing judgement on staging against unchanged aliases, plus a visibility pass, and is a poor test of the route. If the re-stage fails it is returned and replaced, under the standing rule |

Interactive sessions and the batch must not overlap, since the GPU lock would interleave them.

**How a future failure gets caught before it costs a batch.** Three layers, all in code:

1. **Preflight gate, before unit 1.** One headless session launched through the same function as production, running a fixed list of harmless commands that covers every route the skill needs: `.venv/bin/python tools/blender_run.py --status`, `git status --short`, a `tools/*.sh` script form, and `nohup tools/queue_chain.sh &` with no arguments (which exits at once). The runner inspects `permission_denials` in the result event: **any denial aborts the batch before any unit starts.** It takes seconds. The queue form must be in the list because **no runner session has ever executed that step**, so it is unproven.
2. **Infrastructure signature, after every session.** Halt the batch, charge no fix round and write an alert file when any of these appear: a denial in a short session (under about 10 turns) that changed no artifact; `is_error` not explained by a usage limit; a classifier or API failure message; the verifier crashing (a traceback rather than FAIL lines). The turn condition is needed because a pre-check like 013-2 (a denial, 27 turns of real Blender work, nothing saved) must not halt a batch. Replaying this rule against the records: it halts at 012-5, 18 s into the batch, and it does **not** fire on 012-1 on 11-08 (3 denials, 142 productive turns) or on 013-2. The 10-turn threshold is a judgement from these few runs.
3. **No-progress rule.** Fingerprint the production folder, excluding `notes.md`, together with the verifier's output. If neither changed after a fix round, stop that unit now. Replaying this: 014 stops after its first fix round.

The launching session should confirm the canary is past preflight and its first productive tool calls before it reports the batch as running. A push notification on halt would give the owner an early signal without any other involvement.

### (d) Other findings

- **The allowlist is not a spend boundary.** `Bash(.venv/bin/python:*)` permits arbitrary Python, so the deny rule on `factory/producer.py` can be walked around by a different spelling (`./factory/producer.py`, `-c`, `-m`). The real protection has to be the producer's own gates, which I did not audit here. Worth one explicit check, since spending is owner-only.
- **`verify_production.py` needs real stages,** as its docstring already promises, so that the runner can report phase progress rather than a uniform failure.
- **`wait_for_render` has no timeout** (`run_productions.py:68-73`). A stuck chain holding the lock hangs the batch indefinitely, and it is not caught by the session wall clock.
- **013's return is procedurally thin, and I recommend the lenses let it stand.** The readings were not recorded through `--record` (there was no `scenes.json`); one staging was tried per rung; rung 1 was partly judged by literal alias match; and rung 3 was reasoned away. But the capsule, the fact the topic depends on, read as a "clip", and the failure is plausible. Reverting is cheap if the lenses disagree, and under Governance it is theirs to reopen.
- **Refill due.** The bank holds 9 undrawn banked entries, under the working depth of ten. Only the lens-decisions row says so, because `batch.sh` only logged the "no eligible entry" case. The relaunch draws nothing more, so this does not block it.
- **`INDEX.md` is stale for 012** ("nothing modelled or rendered"), and the bank header needs its count updated. Both can go with the records commit.
- **Move 013's reusable findings out of the scratchpad** if they are wanted: the bones-inside-skin alignment file and the licence notes for the two CC-BY assets.

## Decisions for the owner

1. Approve or amend the execution-route fix in (a), including the model pin.
2. Approve the runner rework in (b).
3. Approve the relaunch in (c), noting that it moves 012 from first to last and into an interactive session.
