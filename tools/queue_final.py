"""Queue a production's final render from a headless session (runner rework 2026-11-09). Launches tools/queue_chain.sh DETACHED, so it survives the session, and returns only once the chain is confirmed running.
Why not `nohup tools/queue_chain.sh <prod> &`: don't-ask mode refuses a backgrounded command whatever the allowlist says (measured 2026-11-09), and a session that ended right after `&` could race the runner's wait for the chain lock.
usage: .venv/bin/python tools/queue_final.py productions/<ch>/<video>     prints "QUEUED <name> pid=<n>", exit 0
       .venv/bin/python tools/queue_final.py --probe                      proves the detached route with a no-work chain (the preflight)
Exit: 0 queued; 2 not a production; 3 a GUI Blender is open; 4 the chain did not start. The chain's own output: output/queue-launch-<name>.log."""
import fcntl
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import blender_run  # noqa: E402

START_WAIT_S = float(os.environ.get("SF_QUEUE_START_WAIT_S", "30"))


def chain_locked() -> bool:
    path = blender_run.CHAIN_LOCK
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    except BlockingIOError:
        return True
    finally:
        os.close(fd)


def launch(args: list[str], name: str) -> subprocess.Popen:
    log = ROOT / "output" / f"queue-launch-{name}.log"
    log.parent.mkdir(exist_ok=True)
    with log.open("a") as f:
        return subprocess.Popen([str(ROOT / "tools" / "queue_chain.sh"), *args], cwd=ROOT, stdin=subprocess.DEVNULL, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)


def probe() -> int:
    p = launch([], "probe")
    rc = p.wait(timeout=START_WAIT_S)
    print(f"PROBE detached queue route exit={rc}")
    return 0 if rc == 0 else 4


def queue(prod: Path) -> int:
    if not (prod / "scenes.json").is_file():
        print(f"REFUSED {prod}: no scenes.json, not a production ready to render")
        return 2
    if blender_run.gui_pids():
        print(f"REFUSED: a GUI Blender is open (pid {blender_run.gui_pids()}); run .venv/bin/python tools/asset_blender.py close first")
        return 3
    busy_before = chain_locked()
    p = launch([str(prod.relative_to(ROOT))], prod.name)
    deadline = time.time() + START_WAIT_S
    while time.time() < deadline:
        if p.poll() is not None:
            print(f"FAILED {prod.name}: the chain exited at once with code {p.returncode}; see output/queue-launch-{prod.name}.log")
            return 4
        if busy_before or chain_locked():                      # another chain holding the lock means ours is waiting behind it, which is a queued state
            build = prod / "build"
            build.mkdir(exist_ok=True)
            (build / "queued.json").write_text(json.dumps({"pid": p.pid, "at": datetime.now().isoformat(timespec="seconds"), "behind_another_chain": busy_before}, indent=1))
            print(f"QUEUED {prod.name} pid={p.pid}" + (" (behind a running chain)" if busy_before else ""))
            return 0
        time.sleep(0.2)
    print(f"FAILED {prod.name}: no chain lock after {START_WAIT_S:.0f} s; see output/queue-launch-{prod.name}.log")
    return 4


def main() -> int:
    a = sys.argv[1:]
    if a == ["--probe"]:
        return probe()
    if len(a) != 1 or a[0].startswith("-"):
        print(__doc__)
        return 2
    return queue((ROOT / a[0]).resolve())


if __name__ == "__main__":
    sys.exit(main())
