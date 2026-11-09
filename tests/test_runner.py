"""The external runner resumes after a usage limit, refuses --bare, halts on infrastructure failures, counts returned topics as completed, and validates its arguments. Run: python tests/test_runner.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
SRC = (ROOT / "tools" / "run_productions.py").read_text()


def test_no_bare_or_skip_permissions():
    cmd_line = next(l for l in SRC.splitlines() if l.strip().startswith("cmd = [CLAUDE"))
    assert '"--model"' in cmd_line and "dontAsk" in cmd_line
    assert "--bare" not in cmd_line and "dangerously" not in cmd_line
    assert "--max-turns" not in cmd_line and "HOURS" in SRC


def test_settings_deny_spend():
    s = json.loads((ROOT / "tools" / "runner-settings.json").read_text())
    assert any("producer.py" in d for d in s["permissions"]["deny"])


def _harness(t: Path, stub: str, verify_ok, extra: str = ""):
    bin_ = t / "claude"; bin_.write_text("#!/bin/bash\n" + stub); bin_.chmod(0o755)
    code = f"""
import sys, json
sys.path.insert(0, 'tools')
import run_productions as r
from pathlib import Path
r.OUT = Path({str(t)!r}) / 'out'; r.POLL_LIMIT_S = 0; r.wait_for_render = lambda: None
r.verify = lambda prod: ({verify_ok!r}, 'FAIL x')
r.ROOT = Path({str(t)!r})
prod = Path({str(t)!r}) / 'p'; prod.mkdir()
st = {{}}
{extra}
print(json.dumps([r.run_unit(prod, st), st]))
"""
    r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, env={**os.environ, "SF_CLAUDE_BIN": str(bin_), "SF_FIX_ROUNDS": "1"})
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout.strip().splitlines()[-1])


OK = 'echo \'{"type":"result","is_error":false,"result":"done","session_id":"S","num_turns":3}\'\n'


def test_limit_then_resume_same_session():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        stub = f"""echo "$@" >> {t}/args
if [ ! -f {t}/once ]; then touch {t}/once; echo '{{"type":"system","session_id":"S1"}}'; echo '{{"type":"result","is_error":true,"result":"Claude usage limit reached, resets 7pm","session_id":"S1"}}'; exit 1; fi
echo '{{"type":"result","is_error":false,"result":"ok","session_id":"S1","num_turns":3}}'
"""
        out, st = _harness(t, stub, True)
        assert out == "verified", st
        args = (t / "args").read_text().splitlines()
        assert "--resume S1" not in args[0] and "--resume S1" in args[1], args


def test_production_talk_about_limits_is_not_a_limit():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        out, st = _harness(t, 'echo \'{"type":"result","is_error":false,"result":"hit the 60 min limit, resets at 2","session_id":"S","num_turns":3}\'\n', True)
        assert out == "verified" and st["p"]["sessions"] == 1, st


def test_no_progress_stops_after_one_fix_round():
    with tempfile.TemporaryDirectory() as t:
        out, st = _harness(Path(t), OK, False)
        assert out == "stopped" and "no progress" in st["p"]["status"] and st["p"]["sessions"] == 2, st


def test_progress_runs_out_of_fix_rounds():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        stub = f'date +%N > {t}/p/a; echo $RANDOM > {t}/p/b\n' + OK
        out, st = _harness(t, stub, False)
        assert out == "stopped" and "after fix rounds" in st["p"]["status"] and st["p"]["sessions"] == 2, st


def _denied(turns):
    return 'echo \'{"type":"result","is_error":false,"result":"blocked","session_id":"S","num_turns":%d,"permission_denials":[{"tool_name":"Bash","tool_input":{"command":"tools/x"}}]}\'\n' % turns


def test_denial_in_short_idle_session_is_infrastructure_no_fix_round():
    with tempfile.TemporaryDirectory() as t:
        out, st = _harness(Path(t), _denied(5), False)
        assert out == "infra" and st["p"]["sessions"] == 1 and st["p"]["fix_rounds"] == 0, st


def test_denial_in_a_long_session_is_not_infrastructure():
    with tempfile.TemporaryDirectory() as t:
        out, st = _harness(Path(t), _denied(40), True)
        assert out == "verified", st


def test_policy_denial_is_not_infrastructure():
    sys.path.insert(0, str(ROOT / "tools"))
    import run_productions as r
    d = {"saw_result": True, "turns": 2, "denials": [{"tool_name": "Bash", "tool_input": {"command": "curl x"}}]}
    assert r.infra_signature(d, False) is None
    d["denials"].append({"tool_name": "Bash", "tool_input": {"command": "tools/y"}})
    assert r.infra_signature(d, False)


def test_error_and_api_failure_are_infrastructure():
    import run_productions as r
    assert r.infra_signature({"saw_result": True, "is_error": True, "result": "boom"}, True)
    assert r.infra_signature({"saw_result": True, "result": "auto mode classifier gave no verdict"}, True)
    assert r.infra_signature({"saw_result": False, "rc": 1}, True)


def test_verifier_crash_is_infrastructure():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        extra = "def bad(p): raise r.InfraFailure('verifier crashed')\nr.verify = bad"
        out, st = _harness(t, OK, True, extra)
        assert out == "infra" and "verifier crashed" in st["p"]["status"], st


def test_returned_sidecar_is_a_completed_unit_before_the_verifier():
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        extra = "(prod/'returned.json').write_text(json.dumps({'reason':'r','replacement':'productions/x/099-y','refill_due':True}))\nr.verify = lambda p: 1/0"
        out, st = _harness(t, OK, True, extra)
        assert out == "returned" and st["p"]["replacement"] == "productions/x/099-y" and st["p"]["fix_rounds"] == 0, st


def _queue(outcomes: dict, queue: list):
    import run_productions as r
    calls = []
    def fake(prod, state):
        calls.append(prod.name)
        o = outcomes[prod.name]
        state[prod.name] = {"status": o, "outcome": o, **({"replacement": "productions/c/900-new"} if o == "returned" else {})}
        return o
    with tempfile.TemporaryDirectory() as t:
        old = r.OUT, r.run_unit
        r.OUT, r.run_unit = Path(t), fake
        try:
            rc = r.run_queue(queue, {})
            halted = (Path(t) / "HALT.json").exists()
        finally:
            r.OUT, r.run_unit = old
    return rc, calls, halted


def test_replacement_joins_the_queue_in_the_same_run():
    rc, calls, _ = _queue({"010-a": "returned", "011-b": "verified", "900-new": "verified"}, ["productions/c/010-a", "productions/c/011-b"])
    assert rc == 0 and calls == ["010-a", "011-b", "900-new"], calls


def test_infra_halts_the_batch_and_a_stop_does_not():
    rc, calls, halted = _queue({"010-a": "stopped", "011-b": "infra", "012-c": "verified"}, ["productions/c/010-a", "productions/c/011-b", "productions/c/012-c"])
    assert rc == 3 and calls == ["010-a", "011-b"] and halted, calls


def test_arguments_cannot_become_productions():
    for args in (["--help2"], ["/tmp"], ["productions"]):
        r = subprocess.run([sys.executable, "tools/run_productions.py", *args], cwd=ROOT, capture_output=True, text=True, env={**os.environ, "SF_CLAUDE_BIN": "/nonexistent"})
        assert r.returncode == 2, (args, r.stdout, r.stderr)
    r = subprocess.run([sys.executable, "tools/run_productions.py", "--help"], cwd=ROOT, capture_output=True, text=True, env={**os.environ, "SF_CLAUDE_BIN": "/nonexistent"})
    assert r.returncode == 0 and "--batch" in r.stdout


def test_committed_batches_are_valid():
    import run_productions as r
    for f in (ROOT / "tools" / "batches").glob("*.json"):
        name, units = r.load_batch(f)
        assert all(r.is_production((ROOT / u).resolve()) for u in units), f


def test_probes_cover_the_queue_route_and_a_negative_control():
    import run_productions as r
    p = r.probes("productions/x/001-y")
    assert any("queue_final.py --probe" in c for c in p) and "curl --version" in p
    assert not r.skill_gaps(".venv/bin/python tools/x.py, `.venv/bin/python tools/queue_final.py <prod>`")
    assert r.skill_gaps("`tools/blender_run.py --status` and `nohup tools/queue_chain.sh <prod> &`")


def test_replay_of_last_nights_batch_halts_within_seconds():
    import run_productions as r
    out = ROOT / "output" / "runner"
    if not (out / "batch.log").exists():
        return                                     # the records are local
    res = r.replay(out)
    assert res["halt"] and res["halt"]["session"].startswith("012") and res["halt"]["after_s"] < 60, res["halt"]
    assert res["units"]["014-que-pasa-si-tragas-un-chicle"].startswith("no progress"), res["units"]
    for f, unit, turns in (("012-cepillo-de-dientes-junto-al-inodoro-1.jsonl", "012-cepillo-de-dientes-junto-al-inodoro", 142), ("013-por-que-suenan-los-dedos-2.jsonl", "013-por-que-suenan-los-dedos", None)):
        s = r.read_stream(out / f, unit)
        assert r.infra_signature(s, s["changed"]) is None, f
        assert turns is None or s["turns"] == turns


BANK = """Rolling-window tags: 012 toilet / gross; 014 digestion / bodily; 016 toilet / gross. End.

| Rank | Status | Hook | Family | Structure | Curiosity | Hero | Reshape | Theme | Main tension |
|---|---|---|---|---|---|---|---|---|---|
| 1 | drawn 017 2026-11-09 | "¿Qué pasaría si?" | whatif | fork | 10 | h | none | elevators | dangerous |
| 2 | banked (fill 1) | "¿Por qué el inodoro hace ruido?" | objects | chain | 9 | h | none | toilet | gross |
| 3 | banked (fill 1) | "¿Por qué un tenedor saca chispas en el microondas?" | objects | chain | 9 | h | none | microwave | dangerous |
"""


def test_return_topic_records_everything_and_draws_inside_balance():
    sys.path.insert(0, str(ROOT / "tools"))
    import new_production as np
    import return_topic as rt
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        rt.BANK, rt.DECISIONS, np_create = t / "b.md", t / "l.md", np.create
        rt.BANK.write_text(BANK, encoding="utf-8"); rt.DECISIONS.write_text("", encoding="utf-8")
        ch = t / "productions" / "c"; ch.mkdir(parents=True)
        prod = ch / "014-gum"; prod.mkdir(); (prod / "notes.md").write_text("x", encoding="utf-8")
        (ch / "INDEX.md").write_text("| 014 | gum | body | script | d | n |\n", encoding="utf-8")
        rt.ROOT = t
        def fake(channel, slug, family=""):
            p = ch / f"018-{slug}"; p.mkdir(); return p
        np.create = fake
        try:
            rec = rt.return_topic(prod, "rungs 1-2 failed, 0 of 3 named it")
            assert rec["replacement"] == "productions/c/018-por-que-un-tenedor-saca-chispas-en-el-microondas", rec     # toilet skipped: 012 and 016-style cap
            assert rec["refill_due"] and rec["undrawn"] == 1
            b = rt.BANK.read_text(encoding="utf-8")
            assert "drawn 018" in b and "014 digestion / bodily (returned" in b
            assert "RETURNED" in (prod / "notes.md").read_text(encoding="utf-8") and "RETURNED" in (ch / "INDEX.md").read_text(encoding="utf-8")
            assert "014 RETURNED" in rt.DECISIONS.read_text(encoding="utf-8") and json.loads((prod / "returned.json").read_text())["replacement"]
            try:
                rt.return_topic(prod, "again")
                raise AssertionError("second return accepted")
            except SystemExit:
                pass
        finally:
            np.create = np_create


def test_return_with_no_eligible_entry_records_refill():
    import return_topic as rt
    t = "Rolling-window tags: 012 toilet / gross; 013 toilet / gross.\n"
    rows = [rt.Entry(1, "banked", "¿Por qué?", "objects", "chain", "toilet", "gross", "")]
    assert not rt.balanced(rt.window(t, rows, 99), rows[0])


if __name__ == "__main__":
    n = 0
    for k, v in sorted(globals().items()):
        if k.startswith("test_") and callable(v):
            v(); n += 1; print("ok ", k)
    print(n, "tests passed")
