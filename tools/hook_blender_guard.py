"""PreToolUse backstop (2026-11-08; extended 2026-11-11, block B3 of docs/current/reports/architecture-second-opinion-2026-11-11.md).
1. Bash: denies a command that starts Blender directly instead of through tools/blender_run.py. It enforces the ROUTE; the lock in the launcher enforces the rule.
2. Bash: denies INLINE Python (a heredoc, `python -`, `python -c`) that could spawn a process, reach the network or reflect around the checks. The first-word check of (1) and the
   `.venv/bin/python:*` allowlist cannot see inside a heredoc, so a heredoc could start Blender, curl, producer.py or write provenance.json past both. The scan is an AST pass:
   code that does not parse, or that names a forbidden module, call or attribute, is denied. It is best-effort by nature; the provenance stamp does not rest on it alone
   (the runner re-hashes the stamp around every session, tools/run_productions.py).
3. Any tool, runner sessions only (SF_CTX_CAP set by the runner): once the main session's context passes the cap (the runner publishes the context it reads from the session's own stream
   into the file SF_CTX_FILE; the transcript is NOT usable, claude 2.1.308 flushes a call's usage to it only after the tools of that call have run: measured, every PreToolUse read 0), everything is denied except writing the production's
   build/checkpoint.md, so the runner can hand the work to a fresh session. Interactive sessions never set SF_CTX_CAP and are unaffected."""
import ast
import json
import os
import re
import shlex
import sys

FORBIDDEN_MODULES = {"subprocess", "socket", "ssl", "ctypes", "pty", "urllib", "http", "requests", "httpx", "aiohttp", "importlib", "runpy", "multiprocessing", "asyncio", "shlex_exec",
                     "provenance", "producer", "fal_client", "fal", "webbrowser", "smtplib", "ftplib", "telnetlib", "pexpect", "sh", "plumbum", "code", "codeop", "pdb", "builtins", "marshal", "pickle", "signal", "threading", "sched", "fcntl"}
FORBIDDEN_NAMES = {"eval", "exec", "compile", "__import__", "getattr", "setattr", "delattr", "globals", "locals", "vars", "__builtins__", "__loader__", "__spec__", "breakpoint", "input", "open_code", "system", "popen",
                   "execv", "execve", "execvp", "execvpe", "execl", "execle", "execlp", "execlpe", "spawnv", "spawnve", "spawnvp", "spawnvpe", "spawnl", "spawnle", "spawnlp", "spawnlpe",
                   "posix_spawn", "posix_spawnp", "fork", "forkpty", "startfile", "Popen", "check_output", "check_call", "call", "run", "create_subprocess_exec", "create_subprocess_shell",
                   "dlopen", "CDLL", "cdll", "load_module", "import_module", "__dict__", "__class__", "__subclasses__", "__bases__", "__globals__", "__code__", "__getattribute__", "func_globals"}
FORBIDDEN_STRINGS = ("provenance", "producer.py", "blender", "FAL_KEY", "fal_key")        # a literal naming the stamp, the spend tool, the key or Blender: no inline code needs them
ALLOWED_RUN_ATTRS: set[str] = set()


def direct_blender(command: str) -> bool:
    for seg in re.split(r"\n|;|&&|\|\||\||&", command):
        try:
            words = shlex.split(seg)
        except ValueError:
            words = seg.split()
        while words and (re.fullmatch(r"\w+=\S*", words[0]) or words[0] in ("caffeinate", "-dimsu", "nohup", "exec", "time", "env", "sudo")):
            words.pop(0)
        if words and re.fullmatch(r"(.*/)?blender", words[0], re.I):
            if any(w in ("-b", "--background", "--python", "--python-expr") for w in words[1:]):
                return True
        # a skill helper that starts Blender itself (blender-core run_in_blender.py) is allowed only as the --skill payload of the launcher (2026-11-09)
        names = [w.rsplit("/", 1)[-1] for w in words]
        if names and re.fullmatch(r"python[\d.]*", names[0]):                # the script python runs: the first word after its flags
            names = [w for w in names[1:] if not w.startswith("-")][:1]
        if names[:1] == ["run_in_blender.py"] and "--which" not in words:
            return True
    return False


# ---- inline Python ----------------------------------------------------------------------------------------------
PY = r"(?:[\w./~-]*/)?python[\d.]*"
HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n(.*?)\n[ \t]*\2[ \t]*(?:\n|$)", re.S)


def segments(command: str) -> list[str]:
    """The simple commands of a shell line, split on newline ; & | outside quotes, heredoc bodies removed (they are inline text, not commands)."""
    command = HEREDOC.sub(lambda m: command[m.start():m.start(3)], command)
    out, cur, q = [], "", ""
    for ch in command:
        if q:
            cur += ch
            q = "" if ch == q else q
        elif ch in "'\"":
            cur += ch
            q = ch
        elif ch in "\n;&|":
            out.append(cur)
            cur = ""
        else:
            cur += ch
    return out + [cur]


def inline_python(command: str) -> list[str]:
    """The source text of every piece of inline Python in a shell command: heredoc bodies fed to a python reading stdin, and `python -c` arguments."""
    out = []
    for m in HEREDOC.finditer(command):
        head = command[:m.start()].split("\n")[-1] + command[m.start():m.start(3)].split("\n")[0]
        if re.search(rf"(?:^|[\s;&|(]){PY}(?:\s+-[A-Za-z]+)*\s+-(?:\s|<|$)", head) or re.search(rf"(?:^|[\s;&|(]){PY}\s*<<", head):
            out.append(m.group(3))
    for seg in segments(command):
        try:
            words = shlex.split(seg)
        except ValueError:
            continue
        for i, w in enumerate(words):
            if re.fullmatch(PY, w):
                for j in range(i + 1, len(words) - 1):
                    if re.fullmatch(r"-[A-Za-z]*c", words[j]):
                        out.append(words[j + 1])
                        break
    return out


def inline_python_hazards(src: str) -> list[str]:
    """Why this inline Python may not run; empty means the AST pass found nothing."""
    try:
        tree = ast.parse(src)
    except (SyntaxError, ValueError) as e:
        return [f"does not parse ({e.__class__.__name__}): cannot be checked"]
    bad: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            bad += [f"import {a.name}" for a in node.names if set(a.name.split(".")) & FORBIDDEN_MODULES]
        elif isinstance(node, ast.ImportFrom):
            if set((node.module or "").split(".")) & FORBIDDEN_MODULES:
                bad.append(f"from {node.module} import ...")
            bad += [f"from {node.module or ''} import {a.name}" for a in node.names if a.name in FORBIDDEN_NAMES or a.name in FORBIDDEN_MODULES]
        elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_NAMES:
            bad.append(f".{node.attr}")
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN_NAMES:
            bad.append(node.id)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and any(s.lower() in node.value.lower() for s in FORBIDDEN_STRINGS):
            bad.append(f"string naming {next(s for s in FORBIDDEN_STRINGS if s.lower() in node.value.lower())!r}")
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and re.search(r"(^|[/\s])\.env($|[^\w])", node.value):
            bad.append("string naming '.env'")
        elif isinstance(node, ast.Constant) and isinstance(node.value, bytes):
            bad.append("bytes literal")
    return sorted(set(bad))


def inline_python_denial(command: str) -> str | None:
    for src in inline_python(command):
        bad = inline_python_hazards(src)
        if bad:
            return ("Blocked: inline Python (heredoc / python -c) may not spawn processes, reach the network, reflect, or name provenance, producer, .env or Blender "
                    f"[{', '.join(bad[:6])}]. Put the logic in a tool under tools/ or factory/ and call it as .venv/bin/python tools/x.py, or use Read/Grep/Edit.")
    return None


# ---- scripts a runner session may run -------------------------------------------------------------------------
# The heredoc scan above is one door. The other: Write a .py (or .sh) file, then run it through the allowlisted `.venv/bin/python:*` or `tools/*`. In a runner session (SF_TOOLS_REV = the
# commit the runner started from) a script under tools/, factory/ or tests/ may run only if it exists in that commit and the working tree still matches it; anything else must be inline
# (scanned) or a tool of the repo. Interactive sessions never set SF_TOOLS_REV.
RUNNABLE_DIRS = ("tools", "factory", "tests")


def _git(*args: str, root: str) -> int:
    import subprocess
    return subprocess.run(["git", "-C", root, *args], capture_output=True).returncode


def script_denial(command: str, rev: str, root: str | None = None) -> str | None:
    root = root or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    for seg in segments(command):
        try:
            words = shlex.split(seg)
        except ValueError:
            continue
        while words and (re.fullmatch(r"\w+=\S*", words[0]) or words[0] in ("caffeinate", "-dimsu", "nohup", "exec", "time", "env")):
            words.pop(0)
        if not words:
            continue
        target = None
        if re.fullmatch(PY, words[0]):
            rest = words[1:]
            if "-m" in rest[:3]:
                mod = rest[rest.index("-m") + 1] if rest.index("-m") + 1 < len(rest) else ""
                if mod != "json.tool":
                    return f"Blocked: python -m {mod} is not a sanctioned form in a runner session; run a tool as .venv/bin/python tools/x.py"
                continue
            target = next((w for w in rest if not w.startswith("-")), None)
            if target in (None, "-") or not target.endswith(".py"):
                continue
        elif words[0].endswith((".sh", ".py")) or words[0].startswith("tools/"):
            target = words[0]
        if not target:
            continue
        path = os.path.normpath(target if os.path.isabs(target) else os.path.join(root, target))
        try:
            rel = os.path.relpath(path, root)
        except ValueError:
            continue
        if rel.startswith("..") or rel.split(os.sep)[0] not in RUNNABLE_DIRS:
            if rel.startswith("..") or target.endswith(".py"):
                return f"Blocked: {target} is not a script of this repo's tools/, factory/ or tests/. A runner session runs only repo tools; use inline Python for reading and computing."
            continue
        rp = rel.replace(os.sep, "/")
        if _git("cat-file", "-e", f"{rev}:{rp}", root=root) or _git("diff", "--quiet", rev, "--", rp, root=root):
            return f"Blocked: {rp} is not the version in the commit this batch started from ({rev[:9]}): a runner session does not run scripts it wrote or changed."
    return None


# ---- context cap (runner sessions) ------------------------------------------------------------------------------
def transcript_context(path: str) -> int:
    """Tokens the model read for the latest main-session API call in the transcript (fresh input + cache creation + cache read)."""
    last = 0
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                if '"usage"' not in line:
                    continue
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                if ev.get("type") != "assistant" or ev.get("isSidechain"):
                    continue
                u = (ev.get("message") or {}).get("usage") or {}
                ctx = sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
                if ctx:
                    last = ctx
    except OSError:
        return 0
    return last


def is_checkpoint_write(tool: str, tool_input: dict) -> bool:
    p = str((tool_input or {}).get("file_path", ""))
    return tool in ("Write", "Edit") and bool(re.search(r"(^|/)productions/[^/]+/[^/]+/build/checkpoint\.md$", p)) and ".." not in p


def published_context(path: str) -> int:
    """The context the runner last published for this session (one integer in a file); 0 when absent or unreadable."""
    try:
        with open(path, encoding="utf-8") as f:
            return int(f.read().strip() or 0)
    except (OSError, ValueError):
        return 0


def cap_denial(data: dict, cap: int, ctx_file: str = "") -> str | None:
    if cap <= 0 or is_checkpoint_write(data.get("tool_name", ""), data.get("tool_input") or {}):
        return None
    ctx = max(published_context(ctx_file) if ctx_file else 0, transcript_context(str(data.get("transcript_path") or "")))
    if ctx < cap:
        return None
    return (f"Context cap reached ({ctx // 1000}k of {cap // 1000}k). Do exactly this and nothing else: write (or update) the production's build/checkpoint.md with the Write tool "
            "(stage, what is done and verified, the exact next step, open decisions and failing measurements, files and commands that matter), then end your turn with one short line. "
            "A fresh session continues from that file. Every other tool is denied until then.")


def decide(data: dict, env: dict | None = None) -> tuple[int, str]:
    env = os.environ if env is None else env
    try:
        cap = int(env.get("SF_CTX_CAP") or 0)
    except ValueError:
        cap = 0
    why = cap_denial(data, cap, env.get("SF_CTX_FILE", ""))
    if why:
        return 2, why
    if data.get("tool_name", "Bash") == "Bash":
        command = (data.get("tool_input") or {}).get("command", "")
        if direct_blender(command):
            return 2, ("Blocked: start headless Blender through tools/blender_run.py (one-at-a-time lock + caffeinate): .venv/bin/python tools/blender_run.py -- -b --python ...; "
                       "a skill helper such as run_in_blender.py runs as .venv/bin/python tools/blender_run.py --skill -- <helper.py> <args> (prefix SF_ALLOW_GUI=1 only while an asset-job GUI is open)")
        why = inline_python_denial(command)
        if why:
            return 2, why
        rev = env.get("SF_TOOLS_REV")
        why = script_denial(command, rev, env.get("CLAUDE_PROJECT_DIR")) if rev else None
        if why:
            return 2, why
    return 0, ""


if __name__ == "__main__":
    code, msg = decide(json.load(sys.stdin))
    if code:
        print(msg, file=sys.stderr)
    sys.exit(code)
