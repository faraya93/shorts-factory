"""A failed render sub-step must not pass silently. Run: python tests/test_render_chain.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_chain_scripts_report_failed_scenes_as_incomplete():
    for name in ("chain_render.sh",):
        s = (ROOT / "tools" / name).read_text()
        assert "INCOMPLETE" in s and "render-failures.txt" in s, name
        assert s.index("INCOMPLETE") < s.index("factory/editor.py"), f"{name}: failures must be checked before the editor runs"
        assert "recovered on retry" in s, name


def test_code3d_render_tolerates_missing_costs_json():
    s = (ROOT / "factory" / "code3d_render.py").read_text()
    assert "costs_path.exists()" in s


def test_every_code3d_production_has_costs_json_with_all_clips():
    import json
    for d in (ROOT / "productions").glob("mecanalia-*/[0-9][0-9][0-9]-*"):
        if (d / "clips").is_dir() and any((d / "clips").glob("scene-*.mp4")) and (d / "scenes.json").exists():
            sc = json.loads((d / "scenes.json").read_text())
            if sc.get("primary_engine") == "code3d":
                assert (d / "costs.json").exists(), f"{d.name}: costs.json missing"


def test_merged_scripts_are_shims():
    assert 'exec "$(dirname "$0")/chain_render.sh"' in (ROOT / "tools" / "chain_render2.sh").read_text()
    assert "queue_chain.sh\" --watch" in (ROOT / "tools" / "render_queue.sh").read_text() or "queue_chain.sh --watch" in (ROOT / "tools" / "render_queue.sh").read_text()
    assert "pgrep" not in (ROOT / "tools" / "queue_chain.sh").read_text()


def test_chain_checks_colour_record_before_rendering_stills():
    s = (ROOT / "tools" / "chain_render.sh").read_text()
    assert "gate.py check-colour" in s and s.index("gate.py check-colour") < s.index("gate.py run")
    assert "--chain -- tools/chain_render.sh" in s


def test_no_entry_point_starts_blender_directly():
    for rel in ("factory/gate.py", "factory/code3d_render.py", "tools/draft_still.py", "tools/final_still.sh"):
        s = (ROOT / rel).read_text()
        assert '"blender", "-b"' not in s and "caffeinate -dimsu blender" not in s, rel
        assert "blender_run" in s, rel


def _stub(tmp: Path) -> Path:
    b = tmp / "blender"
    b.write_text("#!/bin/bash\necho start $$ >> " + str(tmp / "log") + "\nsleep 1\necho end $$ >> " + str(tmp / "log") + "\n")
    b.chmod(0o755)
    return b


def test_two_launchers_never_overlap():
    import os, subprocess, sys, tempfile, importlib
    sys.path.insert(0, str(ROOT / "tools"))
    with tempfile.TemporaryDirectory() as t:
        t = Path(t)
        code = ("import sys;sys.path.insert(0,'tools');from pathlib import Path;import blender_run as b;b.LOCK=Path(%r);b.gui_pids=lambda:[];b.headless_pids=lambda:[];print(b.blender(['x']).returncode)" % str(t / "lock"))
        env = {**os.environ, "SF_BLENDER_BIN": str(_stub(t))}
        ps = [subprocess.Popen([sys.executable, "-c", code], cwd=ROOT, env=env, stdout=subprocess.PIPE) for _ in range(2)]
        for p in ps:
            p.wait()
        words = [l.split()[0] for l in (t / "log").read_text().splitlines()]
        assert words == ["start", "end", "start", "end"], words


def test_lock_is_released_when_the_holder_dies():
    import fcntl, os, subprocess, sys, tempfile, time
    with tempfile.TemporaryDirectory() as t:
        lock = Path(t) / "l"
        p = subprocess.Popen([sys.executable, "-c", f"import fcntl,os,time;f=os.open({str(lock)!r},os.O_RDWR|os.O_CREAT);fcntl.flock(f,fcntl.LOCK_EX);print(1,flush=True);time.sleep(60)"], stdout=subprocess.PIPE)
        p.stdout.readline(); p.kill(); p.wait()
        fd = os.open(lock, os.O_RDWR)
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)        # would raise if the lock survived the crash
        os.close(fd)


def test_gui_blender_refuses_a_headless_job():
    import subprocess, sys
    code = "import sys;sys.path.insert(0,'tools');import blender_run as b;b.gui_pids=lambda:[123];b.blender(['x'])"
    r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
    assert r.returncode == 3 and "REFUSED" in r.stdout, (r.returncode, r.stdout, r.stderr)


def test_hook_denies_direct_blender_only():
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from hook_blender_guard import direct_blender as d
    assert d("caffeinate -dimsu blender -b --python x.py -- a=1")
    assert d("cd x && /opt/homebrew/bin/blender -b foo.blend")
    assert not d(".venv/bin/python tools/blender_run.py -- -b --python x.py")
    assert not d('grep -n "blender -b" CLAUDE.md')
    assert not d("brew info blender")


def test_hook_routes_skill_helpers_through_the_launcher():
    """2026-11-09: asset QA ran blender-core's run_in_blender.py directly, skipping the GPU lock and the GUI rule (canary 015, five calls, the asset GUI open)."""
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    from hook_blender_guard import direct_blender as d
    h = "/Users/x/.claude/skills/blender-core/scripts/run_in_blender.py"
    for cmd in (f"python3 {h} --blend a.blend q.py -- --objects A", f".venv/bin/python {h} --blend a.blend q.py", f"python3 -I {h} --expr 'x'", f"{h} --blend a.blend q.py", f"cd x && python3 {h} q.py"):
        assert d(cmd), cmd
    for cmd in (f".venv/bin/python tools/blender_run.py --skill -- {h} --blend a.blend q.py -- --objects A", f"SF_ALLOW_GUI=1 .venv/bin/python tools/blender_run.py --skill -- {h} q.py",
                f"python3 {h} --which", "grep -n run_in_blender.py docs/current/specs/asset-system.md", f"cat {h}"):
        assert not d(cmd), cmd


def test_skill_mode_takes_the_lock_pins_blender_and_refuses_beside_a_gui():
    import subprocess, sys, tempfile
    with tempfile.TemporaryDirectory() as t:
        helper = Path(t) / "helper.py"
        helper.write_text("import os, sys, fcntl\nfd = os.open(sys.argv[1], os.O_RDWR)\ntry:\n    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB); print('LOCK FREE')\nexcept BlockingIOError:\n    print('LOCK HELD')\nprint('EXE', os.environ.get('BLENDER_EXE'))\n")
        code = f"import sys;sys.path.insert(0,'tools');import blender_run as b;from pathlib import Path;b.LOCK=Path({t!r})/'l';b.gui_pids=lambda:[];b.headless_pids=lambda:[];sys.exit(b.skill([{str(helper)!r}, str(b.LOCK)]))"
        r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True)
        assert r.returncode == 0 and "LOCK HELD" in r.stdout and "EXE " in r.stdout and "EXE None" not in r.stdout, (r.stdout, r.stderr)
        code = code.replace("b.gui_pids=lambda:[]", "b.gui_pids=lambda:[123]")
        r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"})
        assert r.returncode == 3 and "REFUSED" in r.stdout, (r.stdout, r.stderr)


if __name__ == "__main__":
    n = 0
    for k, v in sorted(globals().items()):
        if k.startswith("test_") and callable(v):
            v(); n += 1; print("ok ", k)
    print(n, "tests passed")
