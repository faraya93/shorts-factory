"""The ONE way to start a headless Blender (process optimization 2026-11-08, phase 1). It owns two standing rules: one Blender job at a time and caffeinate -dimsu.
Library:  blender_run.blender(["-b", "--python", script, "--", ...], capture_output=True, text=True)   -> CompletedProcess
CLI:      .venv/bin/python tools/blender_run.py -- -b --python script.py -- args...     (exit code = Blender's; 3 = refused)
          .venv/bin/python tools/blender_run.py --chain -- tools/chain_render.sh prod   (holds the chain lock for the whole command; how queues are kept from interleaving)
          .venv/bin/python tools/blender_run.py --status
The locks are fcntl.flock on output/.blender.lock and output/.chain.lock: the kernel releases them when the holders die, so a crash leaves nothing to clean up. Blender inherits the lock
descriptor, so a Blender that outlives its launcher still holds the lock. A second job WAITS. A live GUI Blender (MCP asset job) cannot take the lock and holds GPU memory: a headless job
REFUSES (exit 3) while one is open, unless SF_ALLOW_GUI=1 (explicit override, for small asset-job stills only, never a final). tools/asset_blender.py refuses to open the GUI during a render."""
import fcntl
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCK = ROOT / "output" / ".blender.lock"
CHAIN_LOCK = ROOT / "output" / ".chain.lock"
EXIT_REFUSED = 3
_PROC = re.compile(r"(^|/)blender( |$)|Blender\.app/Contents/MacOS/Blender( |$)", re.I)


def _bin() -> str:
    return os.environ.get("SF_BLENDER_BIN", "blender")


def _procs() -> list[tuple[int, str]]:
    out = subprocess.run(["ps", "-axo", "pid=,command="], capture_output=True, text=True).stdout
    found = []
    for line in out.splitlines():
        pid, _, cmd = line.strip().partition(" ")
        if _PROC.search(cmd.split(" --python", 1)[0]) and "mcp-for-blender" not in cmd and "blender_run" not in cmd:
            found.append((int(pid), cmd))
    return found


def gui_pids() -> list[int]:
    return [p for p, c in _procs() if not re.search(r"\s(-b|--background)(\s|$)", c)]


def headless_pids() -> list[int]:
    return [p for p, c in _procs() if re.search(r"\s(-b|--background)(\s|$)", c)]


def _acquire(path: Path, label: str) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print(f"[blender_run] {label} busy, waiting for the running job to finish", flush=True)
        fcntl.flock(fd, fcntl.LOCK_EX)
    return fd


def busy() -> bool:
    """True while a headless job holds the GPU lock (what the GUI launcher asks before opening)."""
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(LOCK, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fd, fcntl.LOCK_UN)
        return bool(headless_pids())
    except BlockingIOError:
        return True
    finally:
        os.close(fd)


def blender(args: list[str], **kw) -> subprocess.CompletedProcess:
    if gui_pids() and os.environ.get("SF_ALLOW_GUI") != "1":
        print(f"[blender_run] REFUSED: a GUI Blender is open (pid {gui_pids()}) and holds GPU memory. Close it, or set SF_ALLOW_GUI=1 for a small asset-job still.", flush=True)
        sys.exit(EXIT_REFUSED)
    fd = _acquire(LOCK, "GPU lock")
    try:
        while headless_pids():                 # a Blender started outside this launcher (old script, manual run) still counts
            print(f"[blender_run] waiting for headless Blender {headless_pids()} started outside the launcher", flush=True)
            time.sleep(10)
        caff = ["caffeinate", "-dimsu"] if shutil.which("caffeinate") else []
        return subprocess.run([*caff, _bin(), *args], pass_fds=(fd,), **kw)
    finally:
        os.close(fd)


def main() -> int:
    a = sys.argv[1:]
    if a[:1] == ["--status"]:
        print(f"gpu_lock_busy={busy()} gui={gui_pids()} headless={headless_pids()}")
        return 0
    if a[:1] == ["--chain"]:
        fd = _acquire(CHAIN_LOCK, "chain lock")
        cmd = a[2:] if a[1:2] == ["--"] else a[1:]
        return subprocess.run(cmd, pass_fds=(fd,), env={**os.environ, "SF_CHAIN_HELD": "1"}).returncode
    if a[:1] == ["--"]:
        a = a[1:]
    return blender(a).returncode


if __name__ == "__main__":
    sys.exit(main())
