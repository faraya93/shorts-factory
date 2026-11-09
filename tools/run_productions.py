"""External runner (process optimization 2026-11-08, phase 5). A fresh headless session per production, a non-model verifier between units, resume when the Claude Pro limit is hit.
usage: nohup .venv/bin/python tools/run_productions.py productions/<ch>/<video> [...] &
Never --bare (it drops CLAUDE.md, hooks and the subscription login). Wall-clock limit per session in place of --max-turns (SF_RUN_HOURS, default 6). Permissions come from tools/runner-settings.json, never --dangerously-skip-permissions.
State: output/runner/state.json; session streams: output/runner/<name>-<n>.jsonl. A unit stops at the first failure that fix rounds cannot clear, so nothing is built on top of it."""
import fcntl
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE = os.environ.get("SF_CLAUDE_BIN", "claude")
HOURS = float(os.environ.get("SF_RUN_HOURS", "6"))
POLL_LIMIT_S = float(os.environ.get("SF_LIMIT_POLL_S", "1200"))     # usage window: try again every 20 min
MAX_LIMIT_WAIT_S = float(os.environ.get("SF_LIMIT_MAX_WAIT_S", str(36 * 3600)))
FIX_ROUNDS = int(os.environ.get("SF_FIX_ROUNDS", "3"))
OUT = ROOT / "output" / "runner"
LIMIT = re.compile(r"(usage|session|weekly|hourly|rate)[ -]?limit|hit your .*limit|limit (reached|will reset)|resets? (at )?\d|\b429\b", re.I)
MODEL = os.environ.get("SF_RUN_MODEL", "sonnet")                    # pinned so a settings change cannot silently alter a batch; "Drawing" doctrine: production sessions are Sonnet
STANDING = ("Headless session, don't-ask mode. One purpose per Bash call. The working directory is the repo root: never cd. Run Python tools as .venv/bin/python tools/x.py. Change files with Write or Edit, never with shell redirection. "
            "Repeat a command by making one call per item or with a .venv/bin/python heredoc, never a for loop. Never background with &. A denial applies to that command form only: rewrite it in an allowed form and continue; never conclude that Bash is unavailable.")
PROMPT = ("Use the produce skill to run production {prod} from its current state, under CLAUDE.md. Do not publish, spend money or create accounts. Queue the final with .venv/bin/python tools/queue_final.py <prod> and stop when it prints QUEUED; "
          "this runner waits for the render and calls you back to finish the package. When you are blocked on a standing bar, follow the Reshape ladder; if it is exhausted, return the topic with .venv/bin/python tools/return_topic.py <prod> --reason \"...\" and stop.")


def run_session(prod: Path, name: str, n: int, prompt: str, resume: str | None) -> dict:
    """One headless session, to its end or the wall-clock limit. Returns {"session_id", "limited", "timed_out", "rc", "result"}."""
    OUT.mkdir(parents=True, exist_ok=True)
    cmd = [CLAUDE, "-p", prompt, "--output-format", "stream-json", "--verbose", "--permission-mode", "dontAsk", "--settings", str(ROOT / "tools" / "runner-settings.json"), "--model", MODEL, "--append-system-prompt", STANDING]
    if resume:
        cmd += ["--resume", resume]
    log = OUT / f"{name}-{n}.jsonl"
    p = subprocess.Popen(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, text=True, env={k: v for k, v in os.environ.items() if not k.startswith("CLAUDECODE")})
    out = {"session_id": resume, "limited": False, "timed_out": False, "result": ""}
    deadline = time.time() + HOURS * 3600
    import threading
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
            tail = (tail + line)[-3000:]
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("session_id"):
                out["session_id"] = ev["session_id"]
            if ev.get("type") == "result":
                out["result"] = str(ev.get("result", ""))
                if ev.get("is_error") and LIMIT.search(out["result"]):
                    out["limited"] = True
    p.wait()
    out["rc"] = p.returncode
    if p.returncode and not out["result"] and LIMIT.search(tail):             # the CLI can print the limit and exit without a result event
        out["limited"] = True
    return out


def wait_for_render() -> None:
    """The chain lock is held for a chain's whole life. Pick it up and drop it: that returns when no chain is running."""
    path = ROOT / "output" / ".chain.lock"
    path.parent.mkdir(exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
    fcntl.flock(fd, fcntl.LOCK_EX)
    os.close(fd)


def verify(prod: Path) -> tuple[bool, str]:
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "verify_production.py"), str(prod)], capture_output=True, text=True)
    return r.returncode == 0, r.stdout


def save(state: dict) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "state.json").write_text(json.dumps(state, indent=1))


def run_unit(prod: Path, state: dict) -> bool:
    name = prod.name
    st = state.setdefault(name, {"session": None, "sessions": 0, "fix_rounds": 0, "status": "running"})
    prompt, n = PROMPT.format(prod=prod.relative_to(ROOT)), st["sessions"]
    waited = 0.0
    while True:
        n += 1
        st["sessions"] = n
        save(state)
        r = run_session(prod, name, n, prompt, st["session"])
        st["session"] = r["session_id"]
        if r["limited"]:                                                     # resume the SAME session after the reset: no paying twice
            if waited >= MAX_LIMIT_WAIT_S:
                st["status"] = "stopped: usage limit did not reset"
                save(state)
                return False
            st["status"] = "waiting for usage limit reset"
            save(state)
            time.sleep(POLL_LIMIT_S)
            waited += POLL_LIMIT_S
            prompt = "The usage limit has reset. Continue where you stopped."
            continue
        waited = 0.0
        if r["timed_out"]:
            st["status"] = f"stopped: wall-clock limit of {HOURS} h reached"
            save(state)
            return False
        wait_for_render()
        ok, text = verify(prod)
        if ok:
            st["status"] = "verified"
            save(state)
            return True
        if st["fix_rounds"] >= FIX_ROUNDS:
            st["status"] = "stopped: verifier still failing after fix rounds"
            st["last_verifier"] = text[-1500:]
            save(state)
            return False
        st["fix_rounds"] += 1
        st["last_verifier"] = text[-1500:]
        st["status"] = f"fix round {st['fix_rounds']}"
        prompt = ("The render chain has finished (or none is running). The non-model verifier says this production is not complete yet. Finish what remains, under CLAUDE.md, then stop. If a standing bar cannot be met, write why in notes.md and stop.\n" + text)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    state = json.loads((OUT / "state.json").read_text()) if (OUT / "state.json").exists() else {}
    for arg in sys.argv[1:]:
        prod = Path(arg).resolve()
        if state.get(prod.name, {}).get("status") == "verified":
            continue
        if not run_unit(prod, state):
            print(f"{prod.name}: {state[prod.name]['status']}; runner stopped")
            return 1
        print(f"{prod.name}: verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
