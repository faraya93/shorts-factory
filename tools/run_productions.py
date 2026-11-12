"""External runner (process optimization 2026-11-08; reworked 2026-11-09 after the failed batch, docs/current/reports/runner-diagnosis-2026-11-09.md). A fresh headless session per production, a non-model verifier between units, resume when the Claude Pro limit is hit.
usage: .venv/bin/python tools/run_productions.py --batch tools/batches/<name>.json     the versioned queue (--dry-run prints it); run under nohup
       .venv/bin/python tools/run_productions.py productions/<ch>/<video> [...]       an ad-hoc queue, same machinery
       .venv/bin/python tools/run_productions.py --preflight [--production P]         the permission probes alone
       .venv/bin/python tools/run_productions.py --replay                             apply the stop rules to the records of the 2026-11-09 batch
       .venv/bin/python tools/run_productions.py --reset UNIT [--state FILE]          forget one unit's state
Never --bare (it drops CLAUDE.md, hooks and the subscription login). Wall-clock limit per session in place of --max-turns (SF_RUN_HOURS, default 6). Permissions come from tools/runner-settings.json, never --dangerously-skip-permissions.
A PREFLIGHT runs before any unit: any denied command class halts the batch. State and streams: output/runner/<batch>/. Outcomes: verified or returned (next unit), stopped (next unit, the production's own merits), infra or budget (HALT.json + a desktop alert, the batch stops).
Stability hardening 2026-11-09 (docs/current/reports/lens-decisions.md): a fix round is charged only to a session that made NO progress (production files and verifier output both unchanged); a queued final (build/queued.json) always gets exactly
one callback session after its render ends, exempt from the session cap; every unit has a budget (SF_UNIT_MAX_SESSIONS, SF_UNIT_MAX_HOURS of active time, usage-limit waits excluded) whose exhaustion halts the batch loudly.
Accounting, brake and liveness 2026-11-11 (docs/current/reports/architecture-second-opinion-2026-11-11.md, block B1): every session's cost is recorded as a DELTA of the cumulative total_cost_usd per session id (never summed raw), with deduplicated API calls, first and peak context and cache reads;
usage-limit polls are counted apart and are never sessions; reader (blind_read) runs and cost are summed from build/reader-ledger.jsonl; an emergency brake (SF_UNIT_MAX_USD, SF_UNIT_MAX_CALLS) ends a unit as "stopped", never as a halt;
state.json carries the runner's pid, heartbeat and next-retry time under "_runner"; a returned or stopped unit has its own artefacts committed.
Script provenance 2026-11-11 (block B2): a unit whose folder has no Opus creative-session stamp (factory/provenance.py) is REFUSED before any session and recorded under "_refused"; the batch moves on."""
import argparse
import fcntl
import json
import os
import re
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE = os.environ.get("SF_CLAUDE_BIN", "claude")
HOURS = float(os.environ.get("SF_RUN_HOURS", "6"))
POLL_LIMIT_S = float(os.environ.get("SF_LIMIT_POLL_S", "1200"))     # usage window: try again every 20 min
MAX_LIMIT_WAIT_S = float(os.environ.get("SF_LIMIT_MAX_WAIT_S", str(36 * 3600)))
RENDER_MAX_S = float(os.environ.get("SF_RENDER_MAX_HOURS", "24")) * 3600
RENDER_POLL_S = 15.0
FIX_ROUNDS = int(os.environ.get("SF_FIX_ROUNDS", "2"))              # sessions launched after a session that made no progress; one more no-progress session stops the unit
UNIT_MAX_SESSIONS = int(os.environ.get("SF_UNIT_MAX_SESSIONS", "12"))  # per unit, real sessions only (usage-limit polls never count); the post-render callback is exempt
UNIT_MAX_HOURS = float(os.environ.get("SF_UNIT_MAX_HOURS", "14"))     # per unit, active time: sessions + render waits, usage-limit waits excluded
UNIT_MAX_USD = float(os.environ.get("SF_UNIT_MAX_USD", "22.00"))      # emergency brake: summed delta notional per unit (about 2x the largest measured unit, 019 at US$11.43)
UNIT_MAX_CALLS = int(os.environ.get("SF_UNIT_MAX_CALLS", "500"))      # emergency brake: cumulative deduplicated main-session API calls per unit (019 made about 244)
HEARTBEAT_S = float(os.environ.get("SF_HEARTBEAT_S", "30"))
CALLBACK_MIN_HOURS = 1.0                                            # the post-render callback always gets at least this much session time
SHORT_TURNS = 10                                                    # a denial in a session this short that changed nothing is the infrastructure signature (from the 2026-11-08/09 records; judgement)
OUT = ROOT / "output" / "runner"
LIMIT = re.compile(r"(usage|session|weekly|hourly|rate)[ -]?limit|hit your .*limit|limit (reached|will reset)|resets? (at )?\d|\b429\b", re.I)
API_FAILURE = re.compile(r"classifier gave no verdict|API Error|overloaded_error|Internal server error", re.I)
MODEL = os.environ.get("SF_RUN_MODEL", "sonnet")                    # pinned so a settings change cannot silently alter a batch; "Drawing" doctrine: production sessions are Sonnet
STANDING = ("Headless session, don't-ask mode. One purpose per Bash call. The working directory is the repo root: never cd. Run Python tools as .venv/bin/python tools/x.py. Change files with Write or Edit, never with shell redirection. "
            "Repeat a command by making one call per item or with a .venv/bin/python heredoc, never a for loop. Never background with &. A denial applies to that command form only: rewrite it in an allowed form and continue; never conclude that Bash is unavailable. "
            "Keep working until one of these is true: queue_final.py printed QUEUED, the production verifies, the topic is returned, or a blocker remains that you cannot clear under CLAUDE.md. Multi-hour builds are expected and there is no time pressure: "
            "never end the session to report partial progress or because the remaining work is long. Skill helper scripts that start Blender (blender-core run_in_blender.py) run only as .venv/bin/python tools/blender_run.py --skill -- <script> <args>.")
PROMPT = ("Use the produce skill to run production {prod} from its current state, under CLAUDE.md. Do not publish, spend money or create accounts. Queue the final with .venv/bin/python tools/queue_final.py <prod> and stop when it prints QUEUED; "
          "this runner waits for the render and calls you back to finish the package. When you are blocked on a standing bar, follow the Reshape ladder; if it is exhausted, return the topic with .venv/bin/python tools/return_topic.py <prod> --reason \"...\" and stop. "
          "That command replaces any older note asking for hand-written RETURNED or REPLACEMENT lines and bank marks.")
CONTINUE_PROMPT = ("Your previous session ended before the production was complete. Continue the build of {prod} from its current state under CLAUDE.md (produce skill) and do not stop until the final is QUEUED, the topic is returned, or a blocker remains. "
                   "If the ladder is exhausted, return the topic with .venv/bin/python tools/return_topic.py <prod> --reason \"...\" and stop. The verifier currently says:\n")
FIX_PROMPT = ("Your previous session ended WITHOUT CHANGING ANYTHING in {prod} (fix round {k} of {n}; one more session with no progress stops this production). Find what blocks the build, clear it under CLAUDE.md (produce skill), and continue. "
              "If it cannot be cleared, return the topic with .venv/bin/python tools/return_topic.py <prod> --reason \"...\" and stop. The verifier currently says:\n")
CALLBACK_PROMPT = ("The final render of {prod} that you queued has ended (chain log output/chain-{name}.log). Do not re-render. Finish the production from produce skill step 11: read the chain log, run .venv/bin/python tools/verify_production.py {prod}, "
                   "build the package with .venv/bin/python tools/publish_package.py build {prod} and check it with .venv/bin/python tools/publish_package.py check {prod}, then step 12 (report in notes.md, INDEX.md, commit). "
                   "If the render failed, say so plainly in notes.md and fix what the chain log shows. The verifier currently says:\n")
SKILL = Path.home() / ".claude" / "skills" / "produce" / "SKILL.md"


class InfraFailure(Exception):
    """The route is broken, not the production: halt the batch, spend no fix round."""


def session_cmd(prompt: str, resume: str | None) -> list[str]:
    cmd = [CLAUDE, "-p", prompt, "--output-format", "stream-json", "--verbose", "--permission-mode", "dontAsk", "--settings", str(ROOT / "tools" / "runner-settings.json"), "--model", MODEL, "--append-system-prompt", STANDING]
    return cmd + ["--resume", resume] if resume else cmd


def run_session(prod: Path | None, name: str, n: int, prompt: str, resume: str | None, hours: float | None = None) -> dict:
    """One headless session, to its end or the wall-clock limit."""
    OUT.mkdir(parents=True, exist_ok=True)
    log = OUT / f"{name}-{n}.jsonl"
    cmd = session_cmd(prompt, resume)
    p = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, text=True, env={k: v for k, v in os.environ.items() if not k.startswith("CLAUDECODE")})
    out = {"session_id": resume, "limited": False, "timed_out": False, "result": "", "is_error": False, "denials": [], "turns": 0, "saw_result": False, "total_cost": None}
    calls: dict[str, tuple[int, int]] = {}                                    # message id -> (context, cache read) of that API call (an assistant message is streamed once per content block)
    deadline = time.time() + (HOURS if hours is None else hours) * 3600

    def watchdog():
        while p.poll() is None:
            if time.time() > deadline:
                out["timed_out"] = True
                p.kill()
                return
            time.sleep(5)
    threading.Thread(target=watchdog, daemon=True).start()
    tail = ""
    with log.open("a") as f:
        for line in p.stdout:
            f.write(line)
            f.flush()
            tail = (tail + line)[-3000:]
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("session_id"):
                out["session_id"] = ev["session_id"]
            if ev.get("type") == "assistant" and not ev.get("parent_tool_use_id"):
                msg = ev.get("message") or {}
                ctx = context_tokens(msg.get("usage"))
                if msg.get("id") and ctx:                                    # a limit poll streams one all-zero message: not an API call
                    calls[msg["id"]] = (ctx, int((msg.get("usage") or {}).get("cache_read_input_tokens") or 0))
            if ev.get("type") == "result":
                out.update(saw_result=True, result=str(ev.get("result", "")), is_error=bool(ev.get("is_error")), denials=ev.get("permission_denials") or [], turns=ev.get("num_turns") or 0)
                if isinstance(ev.get("total_cost_usd"), (int, float)):
                    out["total_cost"] = float(ev["total_cost_usd"])
                if ev.get("is_error") and LIMIT.search(out["result"]):
                    out["limited"] = True
    p.wait()
    out["rc"] = p.returncode
    if p.returncode and not out["result"] and LIMIT.search(tail):             # the CLI can print the limit and exit without a result event
        out["limited"] = True
    out["tail"] = tail
    ctxs = [c for c, _ in calls.values()]
    out["usage"] = {"api_calls": len(calls), "first_ctx": ctxs[0] if ctxs else 0, "peak_ctx": max(ctxs, default=0), "cache_read": sum(cr for _, cr in calls.values())}
    return out


def context_tokens(usage: dict | None) -> int:
    """Tokens the model read for one API call: fresh input + cache creation + cache read."""
    u = usage or {}
    return sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))


def infra_denials(denials: list[dict]) -> list[dict]:
    """Denials of the policy kind (deny rules: curl, generate_3d) are the allowlist working, not a broken route."""
    return [d for d in denials if d.get("tool_name") != "mcp__blender__generate_3d" and not str((d.get("tool_input") or {}).get("command", "")).lstrip().startswith("curl")]


def infra_signature(r: dict, changed: bool) -> str | None:
    """Why this session is an infrastructure failure, or None. Replayed on the records: fires at 012-5, not on 012-1 (142 productive turns) or 013-2 (27 turns of real work)."""
    if not r.get("saw_result") and not r.get("timed_out") and not r.get("limited"):
        return f"session ended with no result event (exit {r.get('rc')})"
    if r.get("is_error") and not r.get("limited"):
        return f"session reported an error: {r.get('result', '')[:200]}"
    if API_FAILURE.search(r.get("result", "")):
        return f"classifier or API failure: {r.get('result', '')[:200]}"
    denied = infra_denials(r.get("denials", []))
    if denied and r.get("turns", 0) < SHORT_TURNS and not changed:
        return f"{len(denied)} permission denial(s) in a {r.get('turns')}-turn session that changed nothing: {str(denied[0].get('tool_input'))[:160]}"
    return None


def _walk(root: Path) -> list[str]:
    out = []
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for f in files:
            if f == "notes.md":
                continue
            p = Path(d) / f
            try:
                st = p.stat()
            except OSError:
                continue
            out.append(f"{p.relative_to(ROOT) if p.is_relative_to(ROOT) else p}:{st.st_size}:{st.st_mtime_ns}")
    return out


def fingerprint(prod: Path) -> str:
    """What a session can have built: the production folder minus notes.md, plus the code and asset trees a build writes to."""
    trees = [prod] + [ROOT / x for x in ("code3d/lib", "code3d/scenes", "assets/library")]
    return "\n".join(sorted(x for t in trees if t.exists() for x in _walk(t)))


def queued_marker(prod: Path) -> dict | None:
    """build/queued.json, written by tools/queue_final.py once the chain is confirmed running; its 'at' identifies one queued final."""
    try:
        q = json.loads((prod / "build" / "queued.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return q if q.get("at") else None


def pending_callback(prod: Path, st: dict) -> dict | None:
    """A queued final that has not had its post-render callback yet (survives a runner restart: the record is in state)."""
    q = queued_marker(prod)
    return q if q and q["at"] not in st.get("callbacks", []) else None


def chain_alive(pid) -> bool:
    """The queued chain's own process (queue_final launches tools/queue_chain.sh); a reused pid running something else does not count."""
    if not isinstance(pid, int) or pid <= 0:
        return False
    out = subprocess.run(["ps", "-p", str(pid), "-o", "command="], capture_output=True, text=True).stdout
    return "queue_chain" in out or "chain_render" in out


def chain_lock_free() -> bool:
    path = ROOT / "output" / ".chain.lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fd, fcntl.LOCK_UN)
        return True
    except BlockingIOError:
        return False
    finally:
        os.close(fd)


def wait_for_render(q: dict | None = None) -> None:
    """Returns when the queued chain (q's pid) has exited and no chain holds the lock. The pid matters: a chain queued BEHIND another one is not finished when the first releases the lock.
    A chain stuck past SF_RENDER_MAX_HOURS is an infrastructure failure."""
    deadline = time.time() + RENDER_MAX_S
    while (q and chain_alive(q.get("pid"))) or not chain_lock_free():
        if time.time() > deadline:
            raise InfraFailure(f"render chain still running after {RENDER_MAX_S / 3600:.0f} h")
        time.sleep(RENDER_POLL_S)


def verify(prod: Path) -> tuple[bool, str]:
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "verify_production.py"), str(prod)], capture_output=True, text=True)
    if "Traceback" in r.stderr or r.returncode not in (0, 1):
        raise InfraFailure(f"verifier crashed on {prod.name}: {r.stderr[-400:]}")
    return r.returncode == 0, r.stdout


def save(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    runner = state.get("_runner")
    if runner and runner.get("alive"):
        runner["heartbeat"] = now()
    tmp = OUT / "state.json.tmp"
    tmp.write_text(json.dumps(state, indent=1))
    os.replace(tmp, OUT / "state.json")                                      # atomic: a reader of state.json never sees a half-written file


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def set_live(state: dict, **kw) -> None:
    """Liveness block of state.json (key "_runner"): pid, alive, heartbeat, next_retry_at, status. Answers "is a batch active, and until when" from the file alone."""
    state.setdefault("_runner", {}).update(kw)


def start_heartbeat(state: dict) -> threading.Event:
    """pid + heartbeat every HEARTBEAT_S while the runner lives, also through a session, a render wait or a usage-limit sleep. A reader treats a heartbeat older than ~3x heartbeat_every_s as a dead runner."""
    set_live(state, pid=os.getpid(), alive=True, started=now(), heartbeat_every_s=HEARTBEAT_S, next_retry_at=None)
    stop = threading.Event()

    def beat():
        while not stop.wait(HEARTBEAT_S):
            try:
                save(state)
            except (RuntimeError, OSError, ValueError):                    # the main thread was mutating the dict mid-dump: skip this tick
                pass
    threading.Thread(target=beat, daemon=True).start()
    return stop


# ---- per-unit accounting ------------------------------------------------------------------------------------------
def new_acct() -> dict:
    return {"cost_usd": 0.0, "api_calls": 0, "cache_read_tokens": 0, "peak_ctx": 0, "first_ctx": None, "limit_polls": 0, "reader_runs": 0, "reader_cost_usd": 0.0, "cum_by_session": {}, "session_log": []}


def reader_totals(prod: Path) -> tuple[int, float]:
    """(reader runs, reader cost) from the production's append-only build/reader-ledger.jsonl, written by tools/blind_read.py; recomputed whole each time, so it cannot double count."""
    runs, cost = 0, 0.0
    try:
        for line in (prod / "build" / "reader-ledger.jsonl").read_text().splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            runs += int(e.get("readers") or 0)
            cost += float(e.get("cost_usd") or 0.0)
    except OSError:
        pass
    return runs, round(cost, 6)


def is_poll(r: dict) -> bool:
    """A usage-limit poll: the session ended on the limit before it made a single API call. The session that first hit the limit after real work is a real session."""
    return bool(r.get("limited")) and not r.get("usage", {}).get("api_calls")


def account(st: dict, r: dict, prod: Path, n: int, poll: bool) -> None:
    """Records one session. total_cost_usd is CUMULATIVE per session id across resumes (a limit poll repeats the previous figure), so the cost of this session is the difference to the last figure recorded for that id; the raw field is never summed."""
    a = st.setdefault("acct", new_acct())
    u = r.get("usage") or {}
    delta = 0.0
    sid, total = r.get("session_id"), r.get("total_cost")
    if total is not None:
        delta = max(0.0, total - a["cum_by_session"].get(sid, 0.0))
        a["cum_by_session"][sid] = max(total, a["cum_by_session"].get(sid, 0.0))
    a["cost_usd"] = round(a["cost_usd"] + delta, 6)
    a["api_calls"] += u.get("api_calls", 0)
    a["cache_read_tokens"] += u.get("cache_read", 0)
    a["peak_ctx"] = max(a["peak_ctx"], u.get("peak_ctx", 0))
    if a["first_ctx"] is None and u.get("first_ctx"):
        a["first_ctx"] = u["first_ctx"]
    if poll:
        a["limit_polls"] += 1
    a["reader_runs"], a["reader_cost_usd"] = reader_totals(prod)
    a["session_log"].append({"n": n, "poll": poll, "session_id": sid, "delta_cost_usd": round(delta, 6), "cumulative_cost_usd": total, "api_calls": u.get("api_calls", 0), "first_ctx": u.get("first_ctx", 0), "peak_ctx": u.get("peak_ctx", 0), "cache_read_tokens": u.get("cache_read", 0)})


def brake(st: dict) -> str | None:
    """The emergency brake, checked before any continuation session launches: a unit that has spent more than SF_UNIT_MAX_USD of summed delta notional or more than SF_UNIT_MAX_CALLS API calls is ended as 'stopped'."""
    a = st.get("acct") or {}
    if a.get("cost_usd", 0.0) > UNIT_MAX_USD:
        return f"emergency brake: US${a['cost_usd']:.2f} notional spent, over the US${UNIT_MAX_USD:.2f} ceiling"
    if a.get("api_calls", 0) > UNIT_MAX_CALLS:
        return f"emergency brake: {a['api_calls']} API calls, over the {UNIT_MAX_CALLS}-call ceiling"
    return None


# ---- return-path commit -------------------------------------------------------------------------------------------
CODE_TREES = ("code3d/lib", "code3d/scenes", "assets/library")                 # the trees a build writes to (the same as fingerprint())


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)


def untracked(paths: list[str]) -> set[str]:
    out = git("ls-files", "--others", "--exclude-standard", "--", *paths).stdout
    return {l for l in out.splitlines() if l}


def commit_unit(prod: Path, st: dict, outcome: str) -> str:
    """A terminal unit (returned or stopped) leaves nothing untracked behind: commits its production folder and the files it created under code3d/lib, code3d/scenes and assets/library
    (untracked now, not at its first session). Only those paths are committed (a pathspec commit), never other staged or modified work. No push. A failure is logged, never raised."""
    try:
        rel = str(prod.relative_to(ROOT))
        before = st.get("untracked_before")                                  # no start snapshot = no way to tell this unit's files from anyone else's: then the code trees are left alone
        created = untracked(list(CODE_TREES)) - set(before) if before is not None else set()
        mine = sorted(created | untracked([rel]))
        tracked_changes = [l[3:] for l in git("status", "--porcelain", "--", rel).stdout.splitlines()]
        paths = sorted(set(mine) | set(tracked_changes))
        if not paths:
            return "nothing to commit"
        add = git("add", "--", *paths)
        if add.returncode:
            return f"git add failed: {add.stderr.strip()[:200]}"
        a = st.get("acct") or {}
        msg = (f"{prod.name}: {outcome} ({str(st.get('status', ''))[:100]}); unit artefacts committed by the runner\n\n"
               f"{len(paths)} path(s); {a.get('api_calls', 0)} API calls, US${a.get('cost_usd', 0.0):.2f} notional.")
        c = git("commit", "-m", msg, "--", *paths)
        return f"committed {len(paths)} path(s)" if c.returncode == 0 else f"git commit failed: {(c.stderr or c.stdout).strip()[:200]}"
    except Exception as e:                                                   # never fails the runner
        return f"commit error: {e}"


def log(msg: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with (OUT / "batch.log").open("a") as f:
        f.write(line + "\n")


def alert(title: str, msg: str) -> None:
    """Loud and cheap: a desktop notification on top of HALT.json and the batch log. Never fails the runner."""
    try:
        subprocess.run(["osascript", "-e", f"display notification {json.dumps(msg[:200])} with title {json.dumps(title)}"], capture_output=True, timeout=10)
    except Exception:
        pass


def over_budget(st: dict) -> str | None:
    if st["sessions"] >= UNIT_MAX_SESSIONS:
        return f"session budget spent: {st['sessions']} of {UNIT_MAX_SESSIONS} sessions without a verified, returned or stopped outcome"
    if st["active_s"] >= UNIT_MAX_HOURS * 3600:
        return f"time budget spent: {st['active_s'] / 3600:.1f} h of {UNIT_MAX_HOURS} h active"
    return None


def finish(st: dict, state: dict, outcome: str, status: str) -> str:
    st["outcome"], st["status"] = outcome, status
    st["next_retry_at"] = None
    save(state)
    return outcome


def run_unit(prod: Path, state: dict) -> str:
    """Runs one unit to an outcome: verified | returned | stopped | infra | budget.
    Progress rule: a session made progress when the production fingerprint or the verifier output changed. Only a session WITHOUT progress is charged a fix round; after FIX_ROUNDS of them the next no-progress session stops the unit.
    Callback rule: a final queued by a session (build/queued.json) gets exactly one callback session once its chain has ended, exempt from the session cap and with at least CALLBACK_MIN_HOURS."""
    name, rel = prod.name, str(prod.relative_to(ROOT))
    st = state.setdefault(name, {"session": None, "sessions": 0, "fix_rounds": 0, "status": "running"})
    st.setdefault("acct", new_acct())
    st.setdefault("launches", 0)                                             # every launched claude process, polls included: names the stream files
    if "untracked_before" not in st:                                         # what already sat untracked in the build trees: the return-path commit takes only what this unit adds
        st["untracked_before"] = sorted(untracked(list(CODE_TREES)))
    st.setdefault("active_s", 0.0)
    st.setdefault("callbacks", [])
    st.setdefault("fix_rounds", 0)
    prompt = PROMPT.format(prod=rel)
    waited = 0.0
    resumed_after_limit = False
    while True:
        callback = False
        q = None if resumed_after_limit else pending_callback(prod, st)
        if q:                                                                # the render of a queued final: wait, then call back once
            st["status"] = f"waiting for the queued final ({q['at']})"
            save(state)
            t0 = time.time()
            try:
                wait_for_render(q)
            except InfraFailure as e:
                return finish(st, state, "infra", f"infrastructure failure: {e}")
            finally:
                st["active_s"] += time.time() - t0
            st["callbacks"].append(q["at"])
            try:
                ok, text = verify(prod)
            except InfraFailure as e:
                return finish(st, state, "infra", f"infrastructure failure: {e}")
            if ok:
                return finish(st, state, "verified", "verified")
            st["last_verifier"] = text
            prompt, callback = CALLBACK_PROMPT.format(prod=rel, name=name) + text, True
            log(f"CALLBACK {rel}: render of the final queued at {q['at']} ended")
        elif not resumed_after_limit:
            why = over_budget(st)
            if why:
                return finish(st, state, "budget", f"budget: {why}")
        why = brake(st)
        if why:                                                              # a unit outcome, not an infrastructure halt: the batch moves on
            log(f"BRAKE {rel}: {why}")
            return finish(st, state, "stopped", f"stopped: {why}")
        resumed_after_limit = False
        st["launches"] += 1
        st["status"] = "post-render callback" if callback else st["status"]
        save(state)
        left_h = max(0.0, UNIT_MAX_HOURS - st["active_s"] / 3600)
        hours = max(min(HOURS, left_h), CALLBACK_MIN_HOURS if callback else 0.05)
        before = fingerprint(prod)
        t0 = time.time()
        r = run_session(prod, name, st["launches"], prompt, st["session"], hours)
        st["session"] = r["session_id"]
        st["last_denials"] = len(r.get("denials", []))
        poll = is_poll(r)
        if not poll:
            st["sessions"] += 1                                              # a usage-limit poll is never a session, in any budget or ceiling
        n = st["sessions"]
        account(st, r, prod, st["launches"], poll)
        if r["limited"]:                                                     # resume the SAME session after the reset: no paying twice; the wait is not active time
            st["active_s"] += time.time() - t0
            if waited >= MAX_LIMIT_WAIT_S:
                return finish(st, state, "infra", "stopped: usage limit did not reset")
            st["status"] = "waiting for usage limit reset"
            retry = time.time() + POLL_LIMIT_S
            st["next_retry_at"] = datetime.fromtimestamp(retry).isoformat(timespec="seconds")
            set_live(state, next_retry_at=st["next_retry_at"], waiting_unit=name)
            save(state)
            time.sleep(POLL_LIMIT_S)
            st["next_retry_at"] = None
            set_live(state, next_retry_at=None, waiting_unit=None)
            waited += POLL_LIMIT_S
            prompt, resumed_after_limit = "The usage limit has reset. Continue where you stopped.", True
            continue
        st["active_s"] += time.time() - t0
        waited = 0.0
        st["next_retry_at"] = None
        changed = fingerprint(prod) != before
        why = infra_signature(r, changed)
        if why:
            return finish(st, state, "infra", f"infrastructure failure: {why}")
        if r["timed_out"]:
            return finish(st, state, "stopped" if not over_budget(st) else "budget", f"stopped: session wall-clock limit of {hours:.1f} h reached")
        side = prod / "returned.json"
        if side.exists():                                                    # a returned topic is a completed unit, before the verifier, costing no fix round
            rec = json.loads(side.read_text(encoding="utf-8"))
            st["replacement"], st["refill_due"] = rec.get("replacement"), rec.get("refill_due")
            return finish(st, state, "returned", f"returned: {rec.get('reason', '')[:200]}")
        if pending_callback(prod, st):                                       # this session queued a final: the loop waits for it and calls back
            st["status"] = "final queued"
            continue
        try:
            if not callback:
                t1 = time.time()
                wait_for_render()                                            # a chain started some other way must end before the verifier reads its outputs
                st["active_s"] += time.time() - t1
            ok, text = verify(prod)
        except InfraFailure as e:
            return finish(st, state, "infra", f"infrastructure failure: {e}")
        if ok:
            return finish(st, state, "verified", "verified")
        progress = changed or (st.get("last_verifier") is not None and text != st["last_verifier"])
        st["last_verifier"] = text
        if progress:
            st["status"] = f"session {n} made progress; continuing"
            prompt = CONTINUE_PROMPT.format(prod=rel) + text
            continue
        if st["fix_rounds"] >= FIX_ROUNDS:
            return finish(st, state, "stopped", f"stopped: no progress in session {n} after {FIX_ROUNDS} fix round(s) without progress")
        st["fix_rounds"] += 1
        st["status"] = f"fix round {st['fix_rounds']} (session {n} made no progress)"
        prompt = FIX_PROMPT.format(prod=rel, k=st["fix_rounds"], n=FIX_ROUNDS) + text


def provenance_errors(prod: Path) -> list[str]:
    """The unit's script must carry an Opus creative-session stamp (factory/provenance.py); empty means it may start."""
    sys.path.insert(0, str(ROOT / "factory"))
    import provenance
    return provenance.errors(prod)


def run_queue(queue: list[str], state: dict) -> int:
    """Walks the queue in order; a replacement drawn by a returned unit joins it in the same run. Exit 0, or 3 when the batch halted."""
    state["_queue"] = list(dict.fromkeys(state.get("_queue", []) + queue))
    units = state
    stop_beat = start_heartbeat(state)
    try:
        return _run_queue(queue, state, units)
    finally:
        stop_beat.set()
        set_live(state, alive=False, ended=now(), next_retry_at=None, waiting_unit=None)
        save(state)


def _run_queue(queue: list[str], state: dict, units: dict) -> int:
    i = 0
    while i < len(state["_queue"]):
        rel = state["_queue"][i]
        i += 1
        prod = ROOT / rel
        if units.get(prod.name, {}).get("outcome") in ("verified", "returned", "stopped"):
            continue
        bad = provenance_errors(prod)
        if bad:                                                              # no Opus script on record: never start a session that would write one (doctrine "Who writes the script")
            state.setdefault("_refused", {})[prod.name] = {"at": now(), "why": bad}
            save(state)
            log(f"REFUSED {rel}: {'; '.join(bad)}")
            continue
        state.get("_refused", {}).pop(prod.name, None)
        log(f"START {rel}")
        outcome = run_unit(prod, state)
        st = units[prod.name]
        log(f"END {rel}: {outcome}: {st['status']}")
        if outcome in ("returned", "stopped"):                               # terminal outcome: leave no untracked rigs or notes behind
            st["commit"] = commit_unit(prod, st, outcome)
            log(f"COMMIT {rel}: {st['commit']}")
            save(state)
        if outcome in ("infra", "budget"):
            (OUT / "HALT.json").write_text(json.dumps({"at": datetime.now().isoformat(timespec="seconds"), "unit": rel, "outcome": outcome, "status": st["status"]}, indent=1))
            log(f"BATCH HALTED ({outcome}); see HALT.json")
            alert("shorts-factory runner HALTED", f"{prod.name}: {st['status']}")
            return 3
        if outcome == "returned":
            if st.get("replacement"):
                state["_queue"].append(st["replacement"])
                log(f"QUEUED replacement {st['replacement']}")
                save(state)
            else:
                log(f"NO REPLACEMENT for {rel}: no developed standby is eligible; replacement pending a creative session")
    log("BATCH DONE")
    return 0


# ---- preflight -------------------------------------------------------------------------------------------------
def probes(prod: str) -> list[str]:
    """One Bash command per class the produce skill prints, in the form it prints. Harmless: read-only, dry-run, or no-work."""
    return [
        ".venv/bin/python tools/blender_run.py --status",
        ".venv/bin/python tools/blender_run.py --status 2>&1 | tail -5",
        "SF_ALLOW_GUI=1 .venv/bin/python tools/blender_run.py --status",
        ".venv/bin/python tools/queue_final.py --probe",
        "tools/queue_chain.sh",
        f".venv/bin/python tools/verify_production.py {prod}",
        ".venv/bin/python - <<'EOF'\nprint('iteration route')\nEOF",
        "git status --short",
        "git log --oneline -1",
        f"git diff --stat {prod}",
        "git add --dry-run tools/run_productions.py",
        "git mv -n tools/run_productions.py tools/run_productions.py",
        "git commit --dry-run -m probe",
        "git push origin main --dry-run",
        "ls productions",
        "grep -c main .gitignore",
        "find tools -maxdepth 1 -name queue_final.py",
        "mkdir -p output/runner/preflight",
        "ffprobe -version | head -1",
        "curl --version",
    ]


EXPECTED_DENIED = ("curl --version",)                                # the negative control: proves the run can see a denial at all


def skill_gaps(text: str | None = None) -> list[str]:
    """Forms the produce skill prints that do not pass (a bare .py tool, nohup, a backgrounded command) or that the Blender hook denies (a direct Blender or skill-helper call)."""
    sys.path.insert(0, str(ROOT / "tools"))
    from hook_blender_guard import direct_blender
    text = SKILL.read_text(encoding="utf-8") if text is None else text
    return [c for c in re.findall(r"`([^`\n]+)`", text) if re.match(r"(tools|factory)/\S+\.py", c) or c.startswith("nohup") or c.rstrip().endswith(" &") or direct_blender(c)]


def preflight(prod: str) -> list[str]:
    """Launched the runner's own way. Returns the problems; empty means the route is proven."""
    problems = [f"skill prints a form that does not pass: {g}" for g in skill_gaps()]
    if problems:
        return problems
    tmp = f"output/runner/preflight/write-probe-{int(time.time())}.txt"
    cmds = probes(prod)
    body = "\n".join(f"{i + 1}.\n```\n{c}\n```" for i, c in enumerate(cmds))
    prompt = (f"Permissions preflight. Do these in order, one tool call each, sequentially, with no commentary. Issue every Bash command verbatim. Do not change a command, do not skip one if an earlier one was denied or failed, do not retry.\n"
              f"A. Use the Write tool to create {tmp} with the text: probe\nB. Use the Edit tool to change probe to probe2 in that file.\nThen the Bash commands:\n{body}")
    r = run_session(None, f"preflight-{int(time.time())}", 1, prompt, None)
    if not r["saw_result"] or r["is_error"]:
        return [f"preflight session failed: {r.get('result') or r.get('tail', '')[-300:]}"]
    log_file = max(OUT.glob("preflight-*-1.jsonl"), key=lambda p: p.stat().st_mtime)
    issued, tools = [], set()
    for line in log_file.read_text().splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for c in ev["message"]["content"]:
                if c.get("type") == "tool_use":
                    tools.add(c["name"])
                    if c["name"] == "Bash":
                        issued.append(c["input"]["command"].strip())
    denied = {str((d.get("tool_input") or {}).get("command", d.get("tool_name"))).strip() for d in r["denials"]}
    problems += [f"DENIED: {c}" for c in sorted(denied - set(EXPECTED_DENIED))]
    problems += [f"not issued: {c}" for c in cmds if c.strip() not in issued]
    problems += [f"negative control not denied: {c}" for c in EXPECTED_DENIED if c not in denied and c in issued]
    problems += [f"{t} tool not used" for t in ("Write", "Edit") if t not in tools]
    log(f"PREFLIGHT {len(cmds)} commands issued {len(issued)}, denials {len(denied)} (expected {len(EXPECTED_DENIED)}); {'PASS' if not problems else 'FAIL'}")
    return problems


# ---- replay ----------------------------------------------------------------------------------------------------
def read_stream(path: Path, unit: str) -> dict:
    """The facts of one recorded session, in the shape infra_signature takes. 'changed' comes from the stream: a non-denied Write/Edit of a production file other than notes.md."""
    r = {"saw_result": False, "is_error": False, "denials": [], "turns": 0, "result": "", "limited": False, "timed_out": False, "changed": False}
    writes = []
    for line in path.read_text(errors="replace").splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for c in ev["message"]["content"]:
                if c.get("type") == "tool_use" and c["name"] in ("Write", "Edit"):
                    writes.append((c["id"], str(c["input"].get("file_path", ""))))
        if ev.get("type") == "result":
            r.update(saw_result=True, is_error=bool(ev.get("is_error")), denials=ev.get("permission_denials") or [], turns=ev.get("num_turns") or 0, result=str(ev.get("result", "")))
    refused = {d.get("tool_use_id") for d in r["denials"]}
    r["changed"] = any(i not in refused and unit in f and not f.endswith("notes.md") for i, f in writes)
    return r


def replay(root: Path) -> dict:
    """Applies the stop rules to the recorded 2026-11-09 batch: where the batch would have halted, and where each unit's fix rounds would have stopped."""
    first = next(l for l in (root / "batch.log").read_text().splitlines() if " START " in l)
    start = time.mktime(time.strptime(first.split(" START ")[0].replace(" EST", ""), "%a %b %d %H:%M:%S %Y"))
    sessions = sorted((p for p in root.glob("[0-9]*-[0-9]*.jsonl") if p.stat().st_mtime >= start), key=lambda p: p.stat().st_mtime)
    out: dict = {"halt": None, "units": {}}
    per: dict[str, list] = {}
    for p in sessions:
        unit = p.name.rsplit("-", 1)[0]
        f = read_stream(p, unit)
        per.setdefault(unit, []).append(f)
        why = infra_signature(f, f["changed"])
        if why and not out["halt"]:
            out["halt"] = {"session": p.stem, "after_s": round(p.stat().st_mtime - start), "why": why}
    for unit, fs in per.items():                                           # the run_unit rule: only a session without progress is charged; the one after FIX_ROUNDS charges stops the unit
        idle = [i for i, f in enumerate(fs, 1) if not f["changed"]]
        out["units"][unit] = f"no progress: stops at session {idle[FIX_ROUNDS]}" if len(idle) > FIX_ROUNDS else f"ran {len(fs)} sessions"
    return out


# ---- entry ------------------------------------------------------------------------------------------------------
def is_production(p: Path) -> bool:
    try:
        rel = p.relative_to(ROOT / "productions")
    except ValueError:
        return False
    return len(rel.parts) == 2 and bool(re.match(r"\d{3}-", rel.parts[1])) and p.is_dir() and ((p / "script.json").exists() or (p / "notes.md").exists())


def load_batch(path: Path) -> tuple[str, list[str]]:
    b = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(b.get("name"), str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", b["name"]) or not isinstance(b.get("units"), list) or not b["units"]:
        raise SystemExit(f"{path}: a batch needs a lowercase-hyphen 'name' and a non-empty 'units' list of production paths")
    return b["name"], b["units"]


def main(argv: list[str] | None = None) -> int:
    global OUT
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("productions", nargs="*")
    ap.add_argument("--batch", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--preflight", action="store_true")
    ap.add_argument("--production")
    ap.add_argument("--replay", action="store_true")
    ap.add_argument("--reset")
    ap.add_argument("--state", type=Path)
    a = ap.parse_args(argv)
    if a.replay:
        print(json.dumps(replay(OUT), indent=1))
        return 0
    if a.reset:
        path = a.state or OUT / "state.json"
        state = json.loads(path.read_text())
        state.pop(a.reset, None)
        path.write_text(json.dumps(state, indent=1))
        print(f"reset {a.reset} in {path}")
        return 0
    if a.preflight:
        OUT = OUT / "preflight"
        bad = preflight(a.production or "productions/mecanalia-es/015-por-que-las-moscas-se-frotan-las-patas")
        print("\n".join(bad) or "PREFLIGHT PASS")
        return 3 if bad else 0
    if bool(a.batch) == bool(a.productions):
        ap.error("give either --batch FILE or production paths")
    name, units = load_batch(a.batch) if a.batch else (f"adhoc-{datetime.now():%Y%m%d-%H%M%S}", a.productions)
    resolved = []
    for u in units:
        p = (ROOT / u).resolve()
        if not is_production(p):
            ap.error(f"not a production folder (productions/<channel>/NNN-slug with script.json or notes.md): {u}")
        resolved.append(str(p.relative_to(ROOT)))
    if a.dry_run:
        print(json.dumps({"name": name, "units": resolved}, indent=1))
        return 0
    OUT = OUT / name
    OUT.mkdir(parents=True, exist_ok=True)
    bad = preflight(resolved[0])
    if bad:
        (OUT / "HALT.json").write_text(json.dumps({"at": datetime.now().isoformat(timespec="seconds"), "unit": "preflight", "status": bad}, indent=1))
        log("PREFLIGHT FAILED; nothing started:\n  " + "\n  ".join(bad))
        alert("shorts-factory runner: preflight failed", bad[0])
        return 3
    state = json.loads((OUT / "state.json").read_text()) if (OUT / "state.json").exists() else {}
    return run_queue(resolved, state)


if __name__ == "__main__":
    sys.exit(main())
