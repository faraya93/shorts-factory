"""The PreToolUse hook (tools/hook_blender_guard.py, block B3 of docs/current/reports/architecture-second-opinion-2026-11-11.md): inline Python cannot spawn, reach out or touch the stamp;
a runner session runs only the repo's own scripts of the commit it started from; past the context cap only the checkpoint can be written. Run: python tests/test_hook.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import hook_blender_guard as h  # noqa: E402

PY = ".venv/bin/python"


def heredoc(body: str, head: str = f"{PY} -") -> str:
    return f"{head} <<'EOF'\n{body}\nEOF"


def test_the_heredoc_hole_is_closed():
    """Before: a heredoc could start Blender, curl, producer.py or write the stamp past the first-word check and the .venv/bin/python:* allowlist."""
    holes = {
        "subprocess": "import subprocess\nsubprocess.run(['curl', 'https://x'])",
        "os.system": "import os\nos.system('blender -b')",
        "popen": "import os\nos.popen('ls')",
        "from-import": "from subprocess import run\nrun(['ls'])",
        "stamp by path": "from pathlib import Path\nPath('productions/c/025-x/provenance.json').write_text('{}')",
        "stamp by module": "from factory import provenance\nprovenance.stamp(None, 'opus', 'r')",
        "spend by module": "import producer\nproducer.main()",
        "network": "import urllib.request\nurllib.request.urlopen('https://x')",
        "reflection": "getattr(__import__('os'), 'sys' + 'tem')('x')",
        "eval": "eval('1+1')",
        "importlib": "import importlib\nimportlib.import_module('os')",
        "dunder": "().__class__.__bases__[0].__subclasses__()",
        "does not parse": "def (",
        "env file": "print(open('.env').read())",
        "blender literal": "print('blender -b --python x.py')",
    }
    for name, body in holes.items():
        assert h.inline_python_denial(heredoc(body)), name
        assert h.decide({"tool_name": "Bash", "tool_input": {"command": heredoc(body)}}, env={})[0] == 2, name
    assert h.inline_python_denial(f"{PY} -c 'import subprocess'")
    assert h.inline_python_denial("python3 -I -c \"import os; os.system('x')\"")
    assert h.inline_python_denial(heredoc("import subprocess", head="python3 -I -"))
    assert h.inline_python_denial(f"{PY} - <<EOF\nimport subprocess\nEOF")           # unquoted delimiter
    assert h.inline_python_denial(f"cd x && {PY} - <<'EOF'\nimport subprocess\nEOF")


def test_inline_python_that_only_reads_and_computes_still_runs():
    ok = [
        "import json\nfrom pathlib import Path\nd = json.loads(Path('productions/c/023-x/scenes.json').read_text())\nprint(len(d['scenes']))",
        "import re, sys, collections, math, statistics\nprint(sorted(collections.Counter('abca').items()))",
        "print('iteration route')",
    ]
    for body in ok:
        assert h.inline_python_denial(heredoc(body)) is None, body
    assert h.inline_python_denial(f"{PY} -c 'print(1)'") is None
    assert h.inline_python_denial(heredoc("print('iteration route')").replace(PY, "python3")) is None
    assert h.inline_python_denial(f"{PY} tools/status.py productions/c/023-x") is None
    assert h.inline_python_denial("ls -la && git status --short") is None
    assert h.inline_python_denial("cat <<'EOF' > notes.txt\nimport subprocess\nEOF") is None          # a heredoc to something that is not python is not inline python


def test_the_runner_preflight_heredoc_probe_passes_the_hook():
    sys.path.insert(0, str(ROOT / "tools"))
    import run_productions as r
    for c in r.probes("productions/c/015-x"):
        if c != "curl --version":
            assert h.decide({"tool_name": "Bash", "tool_input": {"command": c}}, env={})[0] == 0, c


def test_the_existing_blender_route_is_unchanged():
    assert h.decide({"tool_name": "Bash", "tool_input": {"command": "blender -b --python x.py"}}, env={})[0] == 2
    assert h.decide({"tool_name": "Bash", "tool_input": {"command": f"{PY} tools/blender_run.py -- -b --python x.py"}}, env={})[0] == 0
    assert h.decide({"tool_name": "Read", "tool_input": {"file_path": "x"}}, env={})[0] == 0


def _repo(t: Path) -> str:
    def g(*a):
        return subprocess.run(["git", "-C", str(t), *a], capture_output=True, text=True, check=True).stdout.strip()
    g("init", "-q"); g("config", "user.email", "t@t"); g("config", "user.name", "t")
    (t / "tools").mkdir(); (t / "tools" / "ok.py").write_text("print(1)\n"); (t / "tools" / "run.sh").write_text("echo\n")
    g("add", "-A"); g("commit", "-qm", "base")
    return g("rev-parse", "HEAD")


def test_a_runner_session_runs_only_repo_scripts_of_its_starting_commit():
    """The other door: Write a script, then run it through the allowlisted python or tools/*."""
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        rev = _repo(t)
        d = lambda cmd: h.script_denial(cmd, rev, str(t))
        assert d(f"{PY} tools/ok.py x") is None and d("tools/run.sh") is None and d(f"caffeinate -dimsu {PY} tools/ok.py") is None
        (t / "tools" / "evil.py").write_text("import os\n")
        assert d(f"{PY} tools/evil.py") and d(f"{PY} /tmp/x.py") and d(f"{PY} out.py")                    # new file, outside the repo, not a tool dir
        (t / "tools" / "ok.py").write_text("print(2)\n")
        assert d(f"{PY} tools/ok.py"), "a tracked tool the session changed must not run"
        subprocess.run(["git", "-C", str(t), "add", "-A"]); subprocess.run(["git", "-C", str(t), "commit", "-qm", "session commit"])
        assert d(f"{PY} tools/evil.py") and d(f"{PY} tools/ok.py"), "committing a script does not make it the starting commit's"
        assert d(f"{PY} -m http.server") and d(f"{PY} -m json.tool x.json") is None
        assert d(f"{PY} -") is None and d("ls tools") is None
        (t / "tools" / "evil.sh").write_text("x\n")
        assert d("tools/evil.sh")


def _transcript(t: Path, ctx: int) -> str:
    f = t / f"tr-{ctx}.jsonl"
    side = {"type": "assistant", "isSidechain": True, "message": {"usage": {"input_tokens": 1, "cache_read_input_tokens": 900000}}}
    main = {"type": "assistant", "message": {"usage": {"input_tokens": 2, "cache_creation_input_tokens": 1000, "cache_read_input_tokens": ctx - 1002}}}
    f.write_text("\n".join(json.dumps(x) for x in (main, side)) + "\n")
    return str(f)


def test_past_the_context_cap_only_the_checkpoint_can_be_written():
    cp = "/r/productions/mecanalia-es/025-x/build/checkpoint.md"
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        big, small = _transcript(t, 210_000), None
        env = {"SF_CTX_CAP": "200000"}

        def call(tool, inp, tr=big, e=env):
            return h.decide({"tool_name": tool, "tool_input": inp, "transcript_path": tr}, env=e)[0]
        assert h.transcript_context(big) == 210_000, "sidechain (subagent) calls are not the main context"
        assert call("Bash", {"command": "ls"}) == 2 and call("Read", {"file_path": "x"}) == 2 and call("Edit", {"file_path": "x"}) == 2
        assert call("Write", {"file_path": cp, "content": "c"}) == 0 and call("Edit", {"file_path": cp}) == 0
        assert call("Write", {"file_path": "/r/productions/mecanalia-es/025-x/build/../script.json"}) == 2
        assert call("Write", {"file_path": "/r/productions/mecanalia-es/025-x/notes.md"}) == 2
        assert h.decide({"tool_name": "Bash", "tool_input": {"command": "ls"}, "transcript_path": big}, env={})[0] == 0, "no SF_CTX_CAP, no cap (interactive sessions)"
        assert call("Bash", {"command": "ls"}, tr=_transcript(t, 150_000)) == 0
        assert call("Bash", {"command": "ls"}, tr=str(t / "missing.jsonl")) == 0, "an unreadable transcript never locks a session out"
        assert call("Bash", {"command": "ls"}, e={"SF_CTX_CAP": "0"}) == 0 and call("Bash", {"command": "ls"}, e={"SF_CTX_CAP": "x"}) == 0
        msg = h.decide({"tool_name": "Bash", "tool_input": {"command": "ls"}, "transcript_path": big}, env=env)[1]
        assert "build/checkpoint.md" in msg and "210k" in msg


def test_the_cap_reads_the_context_the_runner_publishes_not_the_transcript():
    """Measured live on claude 2.1.308: the transcript has no usage line for a call until the tools of that call have run, so every PreToolUse read 0. The runner publishes the context it reads
    from the session's stream into SF_CTX_FILE."""
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        f = t / "s.ctx"
        env = {"SF_CTX_CAP": "200000", "SF_CTX_FILE": str(f)}
        data = {"tool_name": "Bash", "tool_input": {"command": "ls"}, "transcript_path": str(t / "empty.jsonl")}
        assert h.decide(data, env=env)[0] == 0                     # no file yet
        f.write_text("199999")
        assert h.decide(data, env=env)[0] == 0
        f.write_text("200000")
        code, msg = h.decide(data, env=env)
        assert code == 2 and "200k of 200k" in msg
        assert h.decide({**data, "tool_name": "Write", "tool_input": {"file_path": "/r/productions/c/025-x/build/checkpoint.md"}}, env=env)[0] == 0
        f.write_text("garbage")
        assert h.decide(data, env=env)[0] == 0                     # an unreadable figure never locks a session out
    sys.path.insert(0, str(ROOT / "tools"))
    import run_productions as r
    with tempfile.TemporaryDirectory() as t:
        p = Path(t) / "x.ctx"
        r.publish_ctx(p, 123456)
        assert h.published_context(str(p)) == 123456 and r.session_env(p)["SF_CTX_FILE"] == str(p) and "SF_CTX_FILE" not in r.session_env()


def test_the_runner_publishes_each_calls_context_while_the_session_runs():
    src = (ROOT / "tools" / "run_productions.py").read_text()
    assert "publish_ctx(ctx_file, ctx)" in src and "session_env(ctx_file)" in src


def test_project_settings_run_the_hook_for_every_tool():
    s = json.loads((ROOT / ".claude" / "settings.json").read_text())
    entry = s["hooks"]["PreToolUse"][0]
    assert entry["matcher"] in ("*", "") and "hook_blender_guard.py" in entry["hooks"][0]["command"]


def test_status_and_iterate_tools_exist_and_work_on_a_real_production():
    sys.path.insert(0, str(ROOT / "tools"))
    import iterate
    import status
    prods = sorted((ROOT / "productions" / "mecanalia-es").glob("0*"))
    prod = next(p for p in prods if (p / "scenes.json").exists())
    text = status.report(prod, run_verifier=False)
    for needle in ("provenance:", "-- scenes", "gate:", "queued final:", "git:"):
        assert needle in text, needle
    # the identical-still memory of iterate
    with tempfile.TemporaryDirectory() as t:
        out = Path(t) / "s01"
        out.mkdir()
        (out / "still-0001.png").write_bytes(b"a")
        p1 = out / "still-0001.png"
        before = {"still-0001.png": iterate.sha(p1)}
        orig_root = iterate.ROOT
        iterate.ROOT = Path(t)
        try:
            msg, hashes = iterate.summarize(Path(t), 1, [p1], None, 1.0, before)
            assert "IDENTICAL" in msg and "NOTHING CHANGED" in msg and hashes == before
            p1.write_bytes(b"b")
            msg, _ = iterate.summarize(Path(t), 1, [p1], None, 1.0, before)
            assert "changed" in msg and "NOTHING CHANGED" not in msg
        finally:
            iterate.ROOT = orig_root


if __name__ == "__main__":
    n = 0
    for k, v in sorted(globals().items()):
        if k.startswith("test_") and callable(v):
            v(); n += 1; print("ok ", k)
    print(n, "tests passed")
