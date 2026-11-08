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
    return False


if __name__ == "__main__":
    data = json.load(sys.stdin)
    if direct_blender((data.get("tool_input") or {}).get("command", "")):
        print("Blocked: start headless Blender through tools/blender_run.py (one-at-a-time lock + caffeinate): .venv/bin/python tools/blender_run.py -- -b --python ...", file=sys.stderr)
        sys.exit(2)
