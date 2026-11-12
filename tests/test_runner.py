"""The external runner resumes after a usage limit, refuses --bare, halts on infrastructure failures, counts returned topics as completed, and validates its arguments. Run: python tests/test_runner.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "factory"))
SRC = (ROOT / "tools" / "run_productions.py").read_text()


def test_no_bare_or_skip_permissions():
    cmd_line = next(l for l in SRC.splitlines() if l.strip().startswith("cmd = [CLAUDE"))
    assert '"--model"' in cmd_line and "dontAsk" in cmd_line
    assert "--bare" not in cmd_line and "dangerously" not in cmd_line
    assert "--max-turns" not in cmd_line and "HOURS" in SRC


def test_settings_deny_spend():
    s = json.loads((ROOT / "tools" / "runner-settings.json").read_text())
    assert any("producer.py" in d for d in s["permissions"]["deny"])


def _harness(t: Path, stub: str, verify_ok, extra: str = "", env: dict | None = None):
    bin_ = t / "claude"; bin_.write_text("#!/bin/bash\n" + stub); bin_.chmod(0o755)
    code = f"""
import sys, json
sys.path.insert(0, 'tools')
import run_productions as r
from pathlib import Path
r.OUT = Path({str(t)!r}) / 'out'; r.POLL_LIMIT_S = 0; r.wait_for_render = lambda *a: None
r.verify = lambda prod: ({verify_ok!r}, 'FAIL x')
r.ROOT = Path({str(t)!r})
prod = Path({str(t)!r}) / 'p'; prod.mkdir()
st = {{}}
{extra}
print(json.dumps([r.run_unit(prod, st), st]))
"""
    r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, env={**os.environ, "SF_CLAUDE_BIN": str(bin_), "SF_FIX_ROUNDS": "1", **(env or {})})
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


def test_progress_is_never_charged_and_the_budget_stops_it_loud():
    """Hardening 2026-11-09: a session that changed the production costs no fix round; a unit that keeps 'progressing' forever is stopped by its session budget."""
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        stub = f'date +%N > {t}/p/a; echo $RANDOM > {t}/p/b\n' + OK
        out, st = _harness(t, stub, False, env={"SF_UNIT_MAX_SESSIONS": "3"})
        assert out == "budget" and "session budget" in st["p"]["status"] and st["p"]["sessions"] == 3 and st["p"]["fix_rounds"] == 0, st


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
        old = r.OUT, r.run_unit, r.alert, r.commit_unit
        r.OUT, r.run_unit, r.commit_unit = Path(t), fake, lambda *a: "stubbed"          # never let a queue test commit to the real repo
        r.alert = lambda *a: calls.append("ALERT") and None
        try:
            rc = r.run_queue(queue, {})
            halted = (Path(t) / "HALT.json").exists() and "ALERT" in calls
            calls[:] = [c for c in calls if c != "ALERT"]
        finally:
            r.OUT, r.run_unit, r.alert, r.commit_unit = old
    return rc, calls, halted


def test_replacement_joins_the_queue_in_the_same_run():
    rc, calls, _ = _queue({"010-a": "returned", "011-b": "verified", "900-new": "verified"}, ["productions/c/010-a", "productions/c/011-b"])
    assert rc == 0 and calls == ["010-a", "011-b", "900-new"], calls


def test_budget_halts_the_batch_like_infra():
    rc, calls, halted = _queue({"010-a": "budget", "011-b": "verified"}, ["productions/c/010-a", "productions/c/011-b"])
    assert rc == 3 and calls == ["010-a"] and halted, calls


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


# ---- regression replays (hardening 2026-11-09) -------------------------------------------------------------------
# Each recorded session is reduced to the facts the runner sees: turns, permission denials, whether the production changed, whether it queued a final.
# The fixtures are cross-checked against output/runner/ when those local records exist; the replay itself runs everywhere.
NIGHT = [  # 2026-11-09 night batch, first unit (012) sessions 5-8: denied commands reported as success (is_error false)
    {"rec": "012-cepillo-de-dientes-junto-al-inodoro-5.jsonl", "turns": 5, "denials": ["cd /Users/fernandoaraya/projects/shorts-factory/productions/"], "changed": False},
    {"rec": "012-cepillo-de-dientes-junto-al-inodoro-6.jsonl", "turns": 3, "denials": ["tools/blender_run.py --status 2>&1 | tail -5"], "changed": False},
    {"rec": "012-cepillo-de-dientes-junto-al-inodoro-7.jsonl", "turns": 2, "denials": ["tools/blender_run.py --status 2>&1 | tail -5"], "changed": False},
    {"rec": "012-cepillo-de-dientes-junto-al-inodoro-8.jsonl", "turns": 2, "denials": ["tools/blender_run.py --status 2>&1 | tail -5"], "changed": False},
]
CANARY = [  # 2026-11-09 canary 015: four voluntary early stops, each with a commit inside its window (9aef555, 4632631, 3c0a250, 20b85b3..2018747); session 4 queued the final
    {"rec": "015-por-que-las-moscas-se-frotan-las-patas-1.jsonl", "turns": 44, "denials": ["python3 /Users/fernandoaraya/.claude/skills/blender-core/scr"], "changed": True},
    {"rec": "015-por-que-las-moscas-se-frotan-las-patas-2.jsonl", "turns": 31, "denials": [], "changed": True},
    {"rec": "015-por-que-las-moscas-se-frotan-las-patas-3.jsonl", "turns": 60, "denials": [".venv/bin/python - <<'EOF'"], "changed": True},
    {"rec": "015-por-que-las-moscas-se-frotan-las-patas-4.jsonl", "turns": 268, "denials": [], "changed": True, "queue": True},
]
STUB = r"""#!{py}
import json, os, sys
from pathlib import Path
plan = json.loads(Path(os.environ["SF_STUB_PLAN"]).read_text())
args = Path(os.environ["SF_STUB_ARGS"]); n = len(args.read_text().splitlines()) if args.exists() else 0
with args.open("a") as f: f.write(json.dumps(sys.argv[1:]) + "\n")
s = plan[n] if n < len(plan) else plan[-1]
prod = Path(os.environ["SF_STUB_PROD"])
if s.get("changed"): (prod / f"work-{n}").write_text(str(n))
if s.get("queue"): (prod / "build").mkdir(exist_ok=True); (prod / "build" / "queued.json").write_text(json.dumps({"pid": 0, "at": f"q{n}"}))
if s.get("publish"): (prod / "publish.json").write_text("{}")
print(json.dumps({"type": "result", "is_error": False, "result": "stopped early", "session_id": "S", "num_turns": s["turns"],
                  "permission_denials": [{"tool_name": "Bash", "tool_use_id": f"d{i}", "tool_input": {"command": c}} for i, c in enumerate(s["denials"])]}))
"""


def _replay(plan: list, env: dict | None = None, stub_wait: bool = False):
    """Runs run_unit for real (fingerprint, verifier stub, the real callback wait when stub_wait is False) against a scripted claude."""
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        prod = t / "productions" / "c" / "015-x"; prod.mkdir(parents=True)
        (t / "plan.json").write_text(json.dumps(plan))
        bin_ = t / "claude"; bin_.write_text(STUB.replace("{py}", sys.executable)); bin_.chmod(0o755)
        code = f"""
import sys, json
sys.path.insert(0, 'tools')
import run_productions as r
from pathlib import Path
r.OUT = Path({str(t)!r}) / 'out'; r.POLL_LIMIT_S = 0; r.RENDER_POLL_S = 0.05; r.ROOT = Path({str(t)!r})
{"r.wait_for_render = lambda *a: None" if stub_wait else ""}
prod = Path({str(prod)!r})
r.verify = lambda p: ((p / 'publish.json').exists(), 'FAIL publish.json missing' if (p / 'build' / 'queued.json').exists() else 'FAIL scenes.json missing')
st = {{}}
print(json.dumps([r.run_unit(prod, st), st]))
"""
        e = {**os.environ, "SF_CLAUDE_BIN": str(bin_), "SF_STUB_PLAN": str(t / "plan.json"), "SF_STUB_ARGS": str(t / "args"), "SF_STUB_PROD": str(prod), **(env or {})}
        r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, env=e, timeout=120)
        assert r.returncode == 0, r.stderr
        out, st = json.loads(r.stdout.strip().splitlines()[-1])
        prompts = [a[a.index("-p") + 1] for a in map(json.loads, (t / "args").read_text().splitlines())]
        return out, st["015-x"], prompts


def test_fixtures_match_the_records():
    import run_productions as r
    for root, plan in ((ROOT / "output" / "runner", NIGHT), (ROOT / "output" / "runner" / "2026-11-09-canary-015", CANARY)):
        for s in plan:
            f = root / s["rec"]
            if not f.exists():
                continue                                   # the records are local
            got = r.read_stream(f, s["rec"].rsplit("-", 1)[0])
            assert got["turns"] == s["turns"] and not got["is_error"], (f, got["turns"])
            assert [str(d["tool_input"]["command"]).startswith(c) for d, c in zip(got["denials"], s["denials"])] == [True] * len(s["denials"]) and len(got["denials"]) == len(s["denials"]), f


def test_replay_night_pattern_halts_on_the_first_session():
    """Denied commands misreported as success: the old runner spent three fix rounds per unit and moved on; now the first session halts the batch, no round charged."""
    out, st, prompts = _replay(NIGHT)
    assert out == "infra" and st["sessions"] == 1 and st["fix_rounds"] == 0 and "permission denial" in st["status"], st


def test_replay_canary_pattern_gets_its_callback_and_verifies():
    """Four progress-making early stops then a queued final: the old runner had spent all its fix rounds before the render ended (stopped, publish.json missing).
    Now no round is charged, the runner waits for the queued chain, and the callback session finishes the package."""
    plan = CANARY + [{"turns": 20, "denials": [], "changed": True, "publish": True}]
    out, st, prompts = _replay(plan)
    assert out == "verified" and st["sessions"] == 5 and st["fix_rounds"] == 0 and st["callbacks"] == ["q3"], st
    assert "has ended" in prompts[4] and "Do not re-render" in prompts[4] and "publish_package.py build" in prompts[4], prompts[4][:200]
    assert all("ended before the production was complete" in p for p in prompts[1:4]), prompts[1:4]


def test_replay_canary_with_a_dead_callback_halts_early():
    """The same pattern when the callback session does nothing: charged rounds, then a loud stop; never an endless loop."""
    plan = CANARY + [{"turns": 2, "denials": [], "changed": False}]
    out, st, prompts = _replay(plan, env={"SF_FIX_ROUNDS": "1"})
    assert out == "stopped" and "no progress" in st["status"] and st["sessions"] == 6 and st["fix_rounds"] == 1, st
    assert "WITHOUT CHANGING ANYTHING" in prompts[5]


def test_replay_canary_that_never_finishes_hits_the_budget():
    """Early stops that each change something but never queue: bounded by the unit's session budget, outcome budget (halts the batch)."""
    plan = CANARY[:3] * 5
    out, st, prompts = _replay(plan, env={"SF_UNIT_MAX_SESSIONS": "6"})
    assert out == "budget" and st["sessions"] == 6 and len(prompts) == 6, st


def test_callback_is_exempt_from_the_session_budget():
    """The guaranteed callback: a final queued by the last budgeted session still gets its package session."""
    plan = CANARY[2:] + [{"turns": 20, "denials": [], "changed": True, "publish": True}]
    out, st, prompts = _replay(plan, env={"SF_UNIT_MAX_SESSIONS": "2"})
    assert out == "verified" and st["sessions"] == 3, st


def test_callback_waits_for_the_queued_chain_process():
    """A chain queued behind another is not done when the lock is free: the wait follows the queued pid."""
    import run_productions as r
    p = subprocess.Popen(["bash", "-c", "exec -a queue_chain sleep 1.5"])
    try:
        assert r.chain_alive(p.pid) and not r.chain_alive(0) and not r.chain_alive(os.getpid())
        old = r.RENDER_POLL_S
        r.RENDER_POLL_S = 0.1
        import time as _t
        t0 = _t.time()
        r.wait_for_render({"pid": p.pid, "at": "x"})
        assert _t.time() - t0 > 0.8
    finally:
        r.RENDER_POLL_S = old
        p.kill()


def test_callback_survives_a_runner_restart():
    """A queued final with no callback on record is called back on the next start; once recorded it is not repeated."""
    import run_productions as r
    with tempfile.TemporaryDirectory() as t:
        prod = Path(t)
        (prod / "build").mkdir()
        (prod / "build" / "queued.json").write_text(json.dumps({"pid": 1, "at": "2026-11-09T09:58:12"}))
        assert r.pending_callback(prod, {})["at"] == "2026-11-09T09:58:12"
        assert r.pending_callback(prod, {"callbacks": ["2026-11-09T09:58:12"]}) is None


# ---- block B1 (2026-11-11): accounting, brake, liveness, return-path commit, reader cost ---------------------------------
ACCT_STUB = r"""#!{py}
import json, os, sys
from pathlib import Path
plan = json.loads(Path(os.environ["SF_STUB_PLAN"]).read_text())
args = Path(os.environ["SF_STUB_ARGS"]); n = len(args.read_text().splitlines()) if args.exists() else 0
with args.open("a") as f: f.write(json.dumps(sys.argv[1:]) + "\n")
s = plan[min(n, len(plan) - 1)]
root = Path(os.environ["SF_STUB_ROOT"])
for rel, text in (s.get("write") or {}).items():
    q = root / rel; q.parent.mkdir(parents=True, exist_ok=True); q.write_text(text)
for e in s["events"]:
    print(json.dumps(e), flush=True)
sys.exit(1 if s.get("exit1") else 0)
"""


def _asst(mid, ctx, cr=0, dup=False):
    ev = {"type": "assistant", "session_id": "S", "message": {"id": mid, "usage": {"input_tokens": 2, "cache_creation_input_tokens": ctx - cr - 2, "cache_read_input_tokens": cr}}}
    return [ev, ev] if dup else [ev]


def _res(cost, limited=False, turns=5):
    return {"type": "result", "session_id": "S", "is_error": limited, "total_cost_usd": cost, "num_turns": turns,
            "result": "Claude usage limit reached, resets 7pm" if limited else "done"}


def _poll(cost=4.5):
    return {"events": [{"type": "assistant", "session_id": "S", "message": {"id": "z", "usage": {"input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}}}, _res(cost, limited=True, turns=1)], "exit1": True}


class _Env:
    """In-process runner against a scripted claude, in a temp tree that is its own git repo."""
    def __init__(self, plan, verify=None, **attrs):
        self.plan, self.verify, self.attrs = plan, verify, attrs

    def __enter__(self):
        import run_productions as r
        self.r, self.t = r, Path(tempfile.mkdtemp())
        t = self.t
        subprocess.run(["git", "init", "-q"], cwd=t, check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=t); subprocess.run(["git", "config", "user.name", "t"], cwd=t)
        (t / "README").write_text("x"); subprocess.run(["git", "add", "-A"], cwd=t); subprocess.run(["git", "commit", "-qm", "init"], cwd=t, check=True)
        self.prod = t / "productions" / "c" / "015-x"; self.prod.mkdir(parents=True)
        (t / "plan.json").write_text(json.dumps(self.plan))
        bin_ = t / "claude"; bin_.write_text(ACCT_STUB.replace("{py}", sys.executable)); bin_.chmod(0o755)
        self.saved = {k: getattr(r, k) for k in ("OUT", "ROOT", "CLAUDE", "POLL_LIMIT_S", "wait_for_render", "verify", "alert", "UNIT_MAX_SESSIONS", "UNIT_MAX_USD", "UNIT_MAX_CALLS", "HEARTBEAT_S")}
        self.env = {k: os.environ.get(k) for k in ("SF_STUB_PLAN", "SF_STUB_ARGS", "SF_STUB_ROOT")}
        os.environ.update(SF_STUB_PLAN=str(t / "plan.json"), SF_STUB_ARGS=str(t / "args"), SF_STUB_ROOT=str(self.prod))
        r.OUT, r.ROOT, r.CLAUDE, r.POLL_LIMIT_S, r.alert = t / "out", t, str(bin_), 0, lambda *a: None
        r.wait_for_render = lambda *a: None
        r.verify = self.verify or (lambda p: ((p / "done").exists(), "FAIL not done"))
        for k, v in self.attrs.items():
            setattr(r, k, v)
        return self

    def __exit__(self, *a):
        for k, v in self.saved.items():
            setattr(self.r, k, v)
        for k, v in self.env.items():
            os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
        import shutil
        shutil.rmtree(self.t, ignore_errors=True)


def test_delta_accounting_never_double_counts_a_resume():
    """One session id across a limit, three polls and a resume: the raw total_cost_usd is cumulative and every poll repeats it; the unit's cost is the last cumulative figure, once."""
    plan = [{"events": _asst("m1", 70000, 0) + _asst("m2", 72000, 70000, dup=True) + [_res(4.5, limited=True, turns=9)], "write": {"a": "1"}, "exit1": True},
            _poll(), _poll(), _poll(),
            {"events": _asst("m3", 80000, 72000) + _asst("m4", 90000, 80000) + [_res(6.25)], "write": {"done": "1"}}]
    with _Env(plan) as e:
        r = e.r
        st = {}
        assert r.run_unit(e.prod, st) == "verified", st
        a = st["015-x"]["acct"]
        assert abs(a["cost_usd"] - 6.25) < 1e-9, a                          # NOT 4.5*4 + 6.25
        assert a["api_calls"] == 4 and a["limit_polls"] == 3 and a["peak_ctx"] == 90000 and a["first_ctx"] == 70000, a   # the duplicated message id counts once
        assert a["cache_read_tokens"] == 70000 + 72000 + 80000 and st["015-x"]["sessions"] == 2, (a, st["015-x"]["sessions"])
        assert [x["delta_cost_usd"] for x in a["session_log"]] == [4.5, 0, 0, 0, 1.75], a["session_log"]


def test_polls_never_count_as_sessions_in_any_budget():
    """Old runner: every poll was a session, so a long limit halted the batch for 'budget' right after a productive session. Now four polls leave a 2-session budget intact."""
    plan = [{"events": _asst("m1", 70000) + [_res(1.0, limited=True)], "write": {"a": "1"}, "exit1": True}, _poll(1.0), _poll(1.0), _poll(1.0), _poll(1.0),
            {"events": _asst("m2", 71000) + [_res(2.0)], "write": {"b": "1"}},
            {"events": _asst("m3", 72000) + [_res(3.0)], "write": {"done": "1"}}]
    with _Env(plan, UNIT_MAX_SESSIONS=3) as e:
        st = {}
        out = e.r.run_unit(e.prod, st)
        u = st["015-x"]
        assert out == "verified" and u["acct"]["limit_polls"] == 4 and u["sessions"] == 3, (out, u)   # 1 + 2 real sessions, 4 polls apart
        assert abs(u["acct"]["cost_usd"] - 3.0) < 1e-9, u["acct"]


def test_brake_stops_a_unit_on_the_cost_ceiling():
    plan = [{"events": _asst(f"m{i}", 70000) + [_res(12.0 * i)], "write": {f"w{i}": "1"}} for i in range(1, 6)]
    with _Env(plan) as e:
        st = {}
        out = e.r.run_unit(e.prod, st)
        u = st["015-x"]
        assert out == "stopped" and "emergency brake" in u["status"] and "US$24.00" in u["status"] and u["sessions"] == 2 and u["acct"]["cost_usd"] == 24.0, u


def test_brake_stops_a_unit_on_the_call_ceiling():
    plan = [{"events": sum((_asst(f"s{i}-m{j}", 70000) for j in range(3)), []) + [_res(0.1 * (i + 1))], "write": {f"w{i}": "1"}} for i in range(1, 8)]
    with _Env(plan, UNIT_MAX_CALLS=7) as e:
        st = {}
        out = e.r.run_unit(e.prod, st)
        u = st["015-x"]
        assert out == "stopped" and "9 API calls" in u["status"] and u["sessions"] == 3, u        # 3 + 3 = 6 is within 7; 9 is over: no fourth session


def test_brake_is_a_stop_not_a_halt():
    rc, calls, halted = _queue({"010-a": "stopped", "011-b": "verified"}, ["productions/c/010-a", "productions/c/011-b"])
    assert rc == 0 and calls == ["010-a", "011-b"] and not halted, calls


def test_liveness_fields_pid_heartbeat_and_next_retry():
    """state.json answers 'is a batch active, and until when': pid, heartbeat, and the next-retry time while a usage limit is being waited out."""
    import time as _t
    seen = {}
    plan = [{"events": _asst("m1", 70000) + [_res(1.0, limited=True)], "write": {"a": "1"}, "exit1": True},
            {"events": _asst("m2", 71000) + [_res(2.0)], "write": {"done": "1"}}]
    with _Env(plan, HEARTBEAT_S=0.2) as e:
        r = e.r
        real_sleep = r.time.sleep

        def spy(x):
            if x == 0:
                seen["during_wait"] = json.loads((r.OUT / "state.json").read_text())
            real_sleep(x)
        r.time.sleep = spy
        try:
            r.POLL_LIMIT_S = 0.0
            out = {}
            state = {}
            rc = r.run_queue(["productions/c/015-x"], state)
        finally:
            r.time.sleep = real_sleep
        assert rc == 0
        w = seen["during_wait"]
        assert w["_runner"]["pid"] == os.getpid() and w["_runner"]["alive"] and w["_runner"]["heartbeat"], w["_runner"]
        assert w["_runner"]["next_retry_at"] and w["015-x"]["next_retry_at"] and w["015-x"]["status"] == "waiting for usage limit reset", w
        fin = json.loads((r.OUT / "state.json").read_text())
        assert fin["_runner"]["alive"] is False and fin["_runner"]["next_retry_at"] is None and fin["_runner"]["ended"], fin["_runner"]


def test_heartbeat_thread_refreshes_state_while_a_unit_runs():
    import time as _t
    with _Env([{"events": []}], HEARTBEAT_S=0.1) as e:
        r = e.r
        state = {}
        stop = r.start_heartbeat(state)
        try:
            first = json.loads((r.OUT / "state.json").read_text()) if (r.OUT / "state.json").exists() else None
            _t.sleep(0.5)
            on_disk = json.loads((r.OUT / "state.json").read_text())
            assert on_disk["_runner"]["pid"] == os.getpid() and on_disk["_runner"]["alive"] and on_disk["_runner"]["heartbeat_every_s"] == 0.1
        finally:
            stop.set()


def _git_log(t):
    return subprocess.run(["git", "log", "--name-only", "--format=%s"], cwd=t, capture_output=True, text=True).stdout


def test_return_path_commits_the_units_own_artefacts_only():
    """A returned unit commits its production folder and the rig it created; a rig already untracked before it started, and unrelated modified work, stay as they were."""
    plan = [{"events": _asst("m1", 70000) + [_res(1.0)],
             "write": {"notes.md": "RETURNED", "returned.json": json.dumps({"reason": "ladder exhausted", "replacement": None}), "../../../code3d/lib/new_rig.py": "x=1", "../../../code3d/scenes/new_01.py": "y=1"}}]
    with _Env(plan) as e:
        r, t = e.r, e.t
        (t / "code3d" / "lib").mkdir(parents=True)
        (t / "code3d" / "lib" / "old_rig.py").write_text("old")                 # untracked BEFORE the unit: not this unit's
        (t / "README").write_text("modified by someone else")
        state = {}
        rc = r.run_queue(["productions/c/015-x"], state)
        log = _git_log(t)
        assert rc == 0 and state["015-x"]["outcome"] == "returned" and state["015-x"]["commit"].startswith("committed"), state["015-x"]
        assert "productions/c/015-x/notes.md" in log and "productions/c/015-x/returned.json" in log and "code3d/lib/new_rig.py" in log and "code3d/scenes/new_01.py" in log, log
        status = subprocess.run(["git", "status", "--porcelain"], cwd=t, capture_output=True, text=True).stdout
        assert "old_rig.py" in status and "README" in status and "new_rig.py" not in status and "015-x" not in status, status


def test_commit_without_a_start_snapshot_never_takes_other_peoples_files():
    """Regression: a unit state with no untracked_before (a fake unit, an old state file) once committed every untracked rig in the repo. Now the code trees are left alone."""
    with _Env([{"events": []}]) as e:
        (e.t / "code3d" / "lib").mkdir(parents=True)
        (e.t / "code3d" / "lib" / "someone_elses_rig.py").write_text("x")
        (e.prod / "notes.md").write_text("n")
        out = e.r.commit_unit(e.prod, {"status": "s"}, "stopped")
        files = subprocess.run(["git", "show", "--name-only", "--format=", "HEAD"], cwd=e.t, capture_output=True, text=True).stdout
        assert out.startswith("committed") and "015-x/notes.md" in files and "someone_elses_rig" not in files, (out, files)


def test_return_path_commits_a_stopped_unit_and_never_fails_the_runner():
    plan = [{"events": _asst(f"m{i}", 70000) + [_res(12.0 * i)], "write": {f"w{i}": "1"}} for i in range(1, 4)]
    with _Env(plan) as e:
        state = {}
        assert e.r.run_queue(["productions/c/015-x"], state) == 0
        assert state["015-x"]["outcome"] == "stopped" and state["015-x"]["commit"].startswith("committed"), state["015-x"]
        e.r.ROOT = e.t / "nowhere"                                              # a broken repo: the commit reports, never raises
        assert not e.r.commit_unit(e.prod, {}, "stopped").startswith("committed")


def test_blind_read_reports_cost_from_json_output():
    import blind_read as br
    assert br.unwrap(json.dumps({"type": "result", "result": '{"guess": "fork", "confidence": 90}', "total_cost_usd": 0.0123})) == ('{"guess": "fork", "confidence": 90}', 0.0123)
    assert br.unwrap(json.dumps([{"type": "system"}, {"type": "result", "result": "r", "total_cost_usd": 0.5}])) == ("r", 0.5)
    assert br.unwrap('{"guess": "x"}') == ('{"guess": "x"}', 0.0)
    assert "--output-format" in (ROOT / "tools" / "blind_read.py").read_text() and '"json"' in (ROOT / "tools" / "blind_read.py").read_text()


def test_reader_cost_is_recorded_in_the_gate_record_and_summed_per_unit():
    """blind_read writes each reading's cost into the record and an append-only ledger; the runner sums the ledger into the unit's accounting (two readings of one element both count)."""
    import blind_read as br
    import asset_library as al
    import run_productions as r
    with tempfile.TemporaryDirectory() as t:
        prod = Path(t)
        br.ledger(prod, "4:sparks", [{"cost_usd": 0.01}, {"cost_usd": 0.02}, {"cost_usd": 0.03}])
        br.ledger(prod, "4:sparks", [{"cost_usd": 0.01}, {"cost_usd": 0.01}, {"cost_usd": 0.01}])
        assert r.reader_totals(prod) == (6, 0.09)
        st = {}
        r.account(st, {"session_id": "S", "total_cost": 1.0, "usage": {"api_calls": 1}}, prod, 1, False)
        assert st["acct"]["reader_runs"] == 6 and st["acct"]["reader_cost_usd"] == 0.09
        r.account(st, {"session_id": "S", "total_cost": 1.0, "usage": {}, "limited": True}, prod, 2, True)    # a poll recomputes, never re-adds
        assert st["acct"]["reader_runs"] == 6 and st["acct"]["cost_usd"] == 1.0 and st["acct"]["limit_polls"] == 1
    src = (ROOT / "factory" / "asset_library.py").read_text()
    assert src.count("reader_cost_usd") >= 3 and "reader_cost=cost" in (ROOT / "tools" / "blind_read.py").read_text()


if __name__ == "__main__":
    n = 0
    for k, v in sorted(globals().items()):
        if k.startswith("test_") and callable(v):
            v(); n += 1; print("ok ", k)
    print(n, "tests passed")
