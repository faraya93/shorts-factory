"""The external runner resumes after a usage limit, refuses --bare, and stops rather than build on a failed unit. Run: python tests/test_runner.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = (ROOT / "tools" / "run_productions.py").read_text()


def test_no_bare_or_skip_permissions():
    cmd_line = next(l for l in SRC.splitlines() if l.strip().startswith("cmd = [CLAUDE"))
    assert "--bare" not in cmd_line and "dangerously" not in cmd_line
    assert "--max-turns" not in cmd_line and "HOURS" in SRC


def test_settings_deny_spend():
    s = json.loads((ROOT / "tools" / "runner-settings.json").read_text())
    assert any("producer.py" in d for d in s["permissions"]["deny"])


def _harness(t: Path, stub: str, verify_ok: bool):
    bin_ = t / "claude"; bin_.write_text("#!/bin/bash\n" + stub); bin_.chmod(0o755)
    code = f"""
import sys, json, runpy
sys.path.insert(0, 'tools')
import run_productions as r
from pathlib import Path
r.OUT = Path({str(t)!r}) / 'out'; r.POLL_LIMIT_S = 0; r.wait_for_render = lambda: None
calls = []
r.verify = lambda prod: ({verify_ok!r}, 'FAIL x')
r.ROOT = Path({str(t)!r})
prod = Path({str(t)!r}) / 'p'; prod.mkdir()
st = {{}}
print(json.dumps([r.run_unit(prod, st), st]))
"""
    r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, env={**os.environ, "SF_CLAUDE_BIN": str(bin_), "SF_FIX_ROUNDS": "1"})
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_limit_then_resume_same_session():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        stub = f"""echo "$@" >> {t}/args
if [ ! -f {t}/once ]; then touch {t}/once; echo '{{"type":"system","session_id":"S1"}}'; echo '{{"type":"result","is_error":true,"result":"Claude usage limit reached, resets 7pm","session_id":"S1"}}'; exit 1; fi
echo '{{"type":"result","is_error":false,"result":"ok","session_id":"S1"}}'
"""
        ok, st = _harness(t, stub, True)
        assert ok, st
        args = (t / "args").read_text().splitlines()
        assert "--resume S1" not in args[0] and "--resume S1" in args[1], args


def test_production_talk_about_limits_is_not_a_limit():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        ok, st = _harness(t, 'echo \'{"type":"result","is_error":false,"result":"hit the 60 min limit, resets at 2","session_id":"S"}\'\n', True)
        assert ok and st["p"]["sessions"] == 1, st


def test_verifier_failure_stops_after_fix_rounds():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        ok, st = _harness(t, 'echo \'{"type":"result","is_error":false,"result":"done","session_id":"S"}\'\n', False)
        assert not ok and "verifier" in st["p"]["status"] and st["p"]["sessions"] == 2, st


if __name__ == "__main__":
    n = 0
    for k, v in sorted(globals().items()):
        if k.startswith("test_") and callable(v):
            v(); n += 1; print("ok ", k)
    print(n, "tests passed")
