"""External runner (process optimization 2026-11-08; reworked 2026-11-09 after the failed batch, docs/current/reports/runner-diagnosis-2026-11-09.md). A fresh headless session per production, a non-model verifier between units, resume when the Claude Pro limit is hit.
usage: .venv/bin/python tools/run_productions.py --batch tools/batches/<name>.json     the versioned queue (--dry-run prints it); run under nohup
       .venv/bin/python tools/run_productions.py productions/<ch>/<video> [...]       an ad-hoc queue, same machinery
       .venv/bin/python tools/run_productions.py --preflight [--production P]         the permission probes alone
       .venv/bin/python tools/run_productions.py --replay                             apply the stop rules to the records of the 2026-11-09 batch
       .venv/bin/python tools/run_productions.py --reset UNIT [--state FILE]          forget one unit's state
Never --bare (it drops CLAUDE.md, hooks and the subscription login). Wall-clock limit per session in place of --max-turns (SF_RUN_HOURS, default 6). Permissions come from tools/runner-settings.json, never --dangerously-skip-permissions.
A PREFLIGHT runs before any unit: any denied command class halts the batch. State and streams: output/runner/<batch>/. Outcomes: verified or returned (next unit), stopped (next unit, the production's own merits), infra (HALT.json, the batch stops, no fix round spent)."""
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
FIX_ROUNDS = int(os.environ.get("SF_FIX_ROUNDS", "3"))
SHORT_TURNS = 10                                                    # a denial in a session this short that changed nothing is the infrastructure signature (from the 2026-11-08/09 records; judgement)
OUT = ROOT / "output" / "runner"
LIMIT = re.compile(r"(usage|session|weekly|hourly|rate)[ -]?limit|hit your .*limit|limit (reached|will reset)|resets? (at )?\d|\b429\b", re.I)
API_FAILURE = re.compile(r"classifier gave no verdict|API Error|overloaded_error|Internal server error", re.I)
MODEL = os.environ.get("SF_RUN_MODEL", "sonnet")                    # pinned so a settings change cannot silently alter a batch; "Drawing" doctrine: production sessions are Sonnet
STANDING = ("Headless session, don't-ask mode. One purpose per Bash call. The working directory is the repo root: never cd. Run Python tools as .venv/bin/python tools/x.py. Change files with Write or Edit, never with shell redirection. "
            "Repeat a command by making one call per item or with a .venv/bin/python heredoc, never a for loop. Never background with &. A denial applies to that command form only: rewrite it in an allowed form and continue; never conclude that Bash is unavailable.")
PROMPT = ("Use the produce skill to run production {prod} from its current state, under CLAUDE.md. Do not publish, spend money or create accounts. Queue the final with .venv/bin/python tools/queue_final.py <prod> and stop when it prints QUEUED; "
          "this runner waits for the render and calls you back to finish the package. When you are blocked on a standing bar, follow the Reshape ladder; if it is exhausted, return the topic with .venv/bin/python tools/return_topic.py <prod> --reason \"...\" and stop. "
          "That command replaces any older note asking for hand-written RETURNED or REPLACEMENT lines and bank marks.")
FIX_PROMPT = ("The non-model verifier says this production is not complete. Continue the build from its current state under CLAUDE.md (produce skill), or finish the package if a render has completed. If the ladder is exhausted, return the topic with .venv/bin/python tools/return_topic.py <prod> --reason \"...\" and stop.\n")
SKILL = Path.home() / ".claude" / "skills" / "produce" / "SKILL.md"


class InfraFailure(Exception):
    """The route is broken, not the production: halt the batch, spend no fix round."""


def session_cmd(prompt: str, resume: str | None) -> list[str]:
    cmd = [CLAUDE, "-p", prompt, "--output-format", "stream-json", "--verbose", "--permission-mode", "dontAsk", "--settings", str(ROOT / "tools" / "runner-settings.json"), "--model", MODEL, "--append-system-prompt", STANDING]
    return cmd + ["--resume", resume] if resume else cmd


def run_session(prod: Path | None, name: str, n: int, prompt: str, resume: str | None) -> dict:
    """One headless session, to its end or the wall-clock limit."""
    OUT.mkdir(parents=True, exist_ok=True)
    log = OUT / f"{name}-{n}.jsonl"
    cmd = session_cmd(prompt, resume)
    p = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, text=True, env={k: v for k, v in os.environ.items() if not k.startswith("CLAUDECODE")})
    out = {"session_id": resume, "limited": False, "timed_out": False, "result": "", "is_error": False, "denials": [], "turns": 0, "saw_result": False}
    deadline = time.time() + HOURS * 3600

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
            if ev.get("type") == "result":
                out.update(saw_result=True, result=str(ev.get("result", "")), is_error=bool(ev.get("is_error")), denials=ev.get("permission_denials") or [], turns=ev.get("num_turns") or 0)
                if ev.get("is_error") and LIMIT.search(out["result"]):
                    out["limited"] = True
    p.wait()
    out["rc"] = p.returncode
    if p.returncode and not out["result"] and LIMIT.search(tail):             # the CLI can print the limit and exit without a result event
        out["limited"] = True
    out["tail"] = tail
    return out


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


def wait_for_render() -> None:
    """The chain lock is held for a chain's whole life. Returns when no chain is running; a chain stuck past SF_RENDER_MAX_HOURS is an infrastructure failure."""
    path = ROOT / "output" / ".chain.lock"
    path.parent.mkdir(exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
    deadline = time.time() + RENDER_MAX_S
    try:
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return
            except BlockingIOError:
                if time.time() > deadline:
                    raise InfraFailure(f"render chain still holds the lock after {RENDER_MAX_S / 3600:.0f} h")
                time.sleep(15)
    finally:
        os.close(fd)


def verify(prod: Path) -> tuple[bool, str]:
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "verify_production.py"), str(prod)], capture_output=True, text=True)
    if "Traceback" in r.stderr or r.returncode not in (0, 1):
        raise InfraFailure(f"verifier crashed on {prod.name}: {r.stderr[-400:]}")
    return r.returncode == 0, r.stdout


def save(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "state.json").write_text(json.dumps(state, indent=1))


def log(msg: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    with (OUT / "batch.log").open("a") as f:
        f.write(line + "\n")


def finish(st: dict, state: dict, outcome: str, status: str) -> str:
    st["outcome"], st["status"] = outcome, status
    save(state)
    return outcome


def run_unit(prod: Path, state: dict) -> str:
    """Runs one unit to an outcome: verified | returned | stopped | infra."""
    name = prod.name
    st = state.setdefault(name, {"session": None, "sessions": 0, "fix_rounds": 0, "status": "running"})
    prompt, n = PROMPT.format(prod=prod.relative_to(ROOT)), st["sessions"]
    waited = 0.0
    in_fix_round = False
    while True:
        n += 1
        st["sessions"] = n
        save(state)
        before = fingerprint(prod)
        r = run_session(prod, name, n, prompt, st["session"])
        st["session"] = r["session_id"]
        st["last_denials"] = len(r.get("denials", []))
        if r["limited"]:                                                     # resume the SAME session after the reset: no paying twice
            if waited >= MAX_LIMIT_WAIT_S:
                return finish(st, state, "infra", "stopped: usage limit did not reset")
            st["status"] = "waiting for usage limit reset"
            save(state)
            time.sleep(POLL_LIMIT_S)
            waited += POLL_LIMIT_S
            prompt = "The usage limit has reset. Continue where you stopped."
            continue
        waited = 0.0
        why = infra_signature(r, fingerprint(prod) != before)
        if why:
            return finish(st, state, "infra", f"infrastructure failure: {why}")
        if r["timed_out"]:
            return finish(st, state, "stopped", f"stopped: wall-clock limit of {HOURS} h reached")
        try:
            wait_for_render()
            side = prod / "returned.json"
            if side.exists():                                                # a returned topic is a completed unit, before the verifier, costing no fix round
                rec = json.loads(side.read_text(encoding="utf-8"))
                st["replacement"], st["refill_due"] = rec.get("replacement"), rec.get("refill_due")
                return finish(st, state, "returned", f"returned: {rec.get('reason', '')[:200]}")
            ok, text = verify(prod)
        except InfraFailure as e:
            return finish(st, state, "infra", f"infrastructure failure: {e}")
        if ok:
            return finish(st, state, "verified", "verified")
        if in_fix_round and fingerprint(prod) == before and text == st.get("last_verifier"):
            return finish(st, state, "stopped", "stopped: fix round made no progress on the verifier")
        if st["fix_rounds"] >= FIX_ROUNDS:
            st["last_verifier"] = text
            return finish(st, state, "stopped", "stopped: verifier still failing after fix rounds")
        st["fix_rounds"] += 1
        st["last_verifier"] = text
        st["status"] = f"fix round {st['fix_rounds']}"
        in_fix_round = True
        prompt = FIX_PROMPT + text


def run_queue(queue: list[str], state: dict) -> int:
    """Walks the queue in order; a replacement drawn by a returned unit joins it in the same run. Exit 0, or 3 when the batch halted."""
    state["_queue"] = list(dict.fromkeys(state.get("_queue", []) + queue))
    units = state
    i = 0
    while i < len(state["_queue"]):
        rel = state["_queue"][i]
        i += 1
        prod = ROOT / rel
        if units.get(prod.name, {}).get("outcome") in ("verified", "returned", "stopped"):
            continue
        log(f"START {rel}")
        outcome = run_unit(prod, state)
        st = units[prod.name]
        log(f"END {rel}: {outcome}: {st['status']}")
        if outcome == "infra":
            (OUT / "HALT.json").write_text(json.dumps({"at": datetime.now().isoformat(timespec="seconds"), "unit": rel, "status": st["status"]}, indent=1))
            log("BATCH HALTED (infrastructure); see HALT.json")
            return 3
        if outcome == "returned":
            if st.get("replacement"):
                state["_queue"].append(st["replacement"])
                log(f"QUEUED replacement {st['replacement']}")
                save(state)
            else:
                log(f"NO REPLACEMENT for {rel}: no eligible banked entry; refill due")
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
    """Forms the produce skill prints that do not pass (a bare .py tool, nohup, a backgrounded command)."""
    text = SKILL.read_text(encoding="utf-8") if text is None else text
    return [c for c in re.findall(r"`([^`\n]+)`", text) if re.match(r"(tools|factory)/\S+\.py", c) or c.startswith("nohup") or c.rstrip().endswith(" &")]


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
    for unit, fs in per.items():
        out["units"][unit] = next((f"no progress: stops after fix round {i}" for i, f in enumerate(fs[1:], 1) if not f["changed"]), f"ran {len(fs)} sessions")
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
        return 3
    state = json.loads((OUT / "state.json").read_text()) if (OUT / "state.json").exists() else {}
    return run_queue(resolved, state)


if __name__ == "__main__":
    sys.exit(main())
