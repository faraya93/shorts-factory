"""PreToolUse backstop on Bash (2026-11-08): denies a command that starts Blender directly instead of through tools/blender_run.py. It enforces the ROUTE; the lock in the launcher enforces the rule."""
import json
import re
import shlex
import sys


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


if __name__ == "__main__":
    data = json.load(sys.stdin)
    if direct_blender((data.get("tool_input") or {}).get("command", "")):
        print("Blocked: start headless Blender through tools/blender_run.py (one-at-a-time lock + caffeinate): .venv/bin/python tools/blender_run.py -- -b --python ...; "
              "a skill helper such as run_in_blender.py runs as .venv/bin/python tools/blender_run.py --skill -- <helper.py> <args> (prefix SF_ALLOW_GUI=1 only while an asset-job GUI is open)", file=sys.stderr)
        sys.exit(2)
