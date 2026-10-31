"""Create the next numbered production folder of a channel: productions/<channel>/<NNN>-<slug>/ (and a row in the channel's INDEX.md).
Numbers are per channel, three digits, never reused (archived productions keep theirs). The orchestrator names a production by channel + slug.
    .venv/bin/python tools/new_production.py <channel-id> <slug>"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import channel  # noqa: E402

PRODUCTIONS = ROOT / "productions"
NUM = re.compile(r"^(\d{3})-")


def used_numbers(channel_id: str) -> list[int]:
    nums = [int(m.group(1)) for d in (PRODUCTIONS / channel_id).glob("*") if (m := NUM.match(d.name))]
    for d in (PRODUCTIONS / "_archive").glob("*/*"):          # archived productions keep their number
        f = d / "scenes.json"
        if NUM.match(d.name) and f.exists() and json.loads(f.read_text(encoding="utf-8")).get("channel") == channel_id:
            nums.append(int(d.name[:3]))
    return nums


def create(channel_id: str, slug: str) -> Path:
    channel.path_of(channel_id)                                   # raises KeyError for an unknown channel
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug):
        raise SystemExit("slug: lowercase ascii words joined by '-' (Spanish accents dropped), e.g. por-que-el-cielo-es-azul")
    folder = PRODUCTIONS / channel_id
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{max(used_numbers(channel_id), default=0) + 1:03d}-{slug}"
    path.mkdir()
    index = folder / "INDEX.md"
    row = f"| {path.name[:3]} | {slug} | draft | {date.today().isoformat()} | |\n"
    index.write_text((index.read_text(encoding="utf-8") if index.exists() else "| # | slug | status | created | notes |\n|---|---|---|---|---|\n") + row, encoding="utf-8")
    return path


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(create(sys.argv[1], sys.argv[2]))
