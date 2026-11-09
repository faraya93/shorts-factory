"""Return a production's topic under the Reshape ladder and draw its replacement, as CODE (runner rework 2026-11-09). One command, one sequence, one sidecar the runner reads; no free-text marker.
usage: .venv/bin/python tools/return_topic.py productions/<ch>/<video> --reason "<rungs tried and the failing measurement>"
Writes: RETURNED in notes.md; the mark in docs/current/idea-bank.md; the INDEX.md row; a row in docs/current/reports/lens-decisions.md; the replacement folder (tools/new_production.py) with a stub notes.md and its draw mark;
<prod>/returned.json {reason, at, replacement (repo path or null), refill_due, undrawn}. Draws the highest-ranked undrawn BANKED entry that keeps the rolling five-production window inside TOPIC BALANCE (CLAUDE.md): at most two share a theme, at least three of the five tensions. Never the reserve, never an unbanked topic."""
import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import new_production  # noqa: E402

BANK = ROOT / "docs" / "current" / "idea-bank.md"
DECISIONS = ROOT / "docs" / "current" / "reports" / "lens-decisions.md"
ROLLING = re.compile(r"(\d{3}) ([a-z][a-z ]*?) / ([a-z]+)( \(returned)?")
WORKING_DEPTH = 10


@dataclass
class Entry:
    rank: int
    status: str
    hook: str
    family: str
    structure: str
    theme: str
    tension: str
    line: str


def cell(text: str) -> str:
    return " ".join(text.replace("|", "/").split())


def bank_rows(text: str) -> list[Entry]:
    rows = []
    for line in text.splitlines():
        c = [x.strip() for x in line.split("|")]
        if len(c) == 12 and c[1].isdigit():
            rows.append(Entry(int(c[1]), c[2], c[3], c[4], c[5], c[9], c[10], line))
    return sorted(rows, key=lambda e: e.rank)


def undrawn(rows: list[Entry]) -> list[Entry]:
    return [e for e in rows if e.status.startswith(("banked", "promoted"))]


def window(text: str, rows: list[Entry], returning: int) -> list[tuple[int, str, str]]:
    """Productions that count, oldest first: (number, theme, tension). Returned ones and the production being returned are out."""
    seen: dict[int, tuple[str, str]] = {}
    line = next((l for l in text.splitlines() if "Rolling-window tags" in l), "")
    for num, theme, tension, ret in ROLLING.findall(line[line.find("Rolling-window tags"):]):
        if not ret:
            seen[int(num)] = (theme.strip(), tension)
    for e in rows:
        m = re.match(r"(?:drawn|produced) (\d{3})", e.status)
        if m:
            seen[int(m.group(1))] = (e.theme, e.tension)
    seen.pop(returning, None)
    return [(n, *seen[n]) for n in sorted(seen)]


def balanced(prev: list[tuple[int, str, str]], e: Entry) -> bool:
    last = [(t, x) for _, t, x in prev[-4:]] + [(e.theme, e.tension)]
    themes = [t for t, _ in last]
    if themes.count(e.theme) > 2:
        return False
    return len(last) < 5 or len({x for _, x in last}) >= 3


def slugify(hook: str) -> str:
    q = re.search(r"¿(.+?)\?", hook).group(1)
    ascii_ = unicodedata.normalize("NFKD", q).encode("ascii", "ignore").decode().lower()
    words = re.findall(r"[a-z0-9]+", ascii_)
    out = []
    for w in words:
        if len("-".join(out + [w])) > 60:
            break
        out.append(w)
    return "-".join(out)


def draw(text: str, returning: int) -> Entry | None:
    rows = bank_rows(text)
    prev = window(text, rows, returning)
    return next((e for e in undrawn(rows) if balanced(prev, e)), None)


def return_topic(prod: Path, reason: str) -> dict:
    reason = cell(reason)
    today = date.today().isoformat()
    if not re.match(r"\d{3}-", prod.name) or not (prod / "notes.md").exists() and not (prod / "script.json").exists():
        raise SystemExit(f"not a production folder: {prod}")
    side = prod / "returned.json"
    if side.exists():
        raise SystemExit(f"already returned: {side}")
    num = int(prod.name[:3])
    text = BANK.read_text(encoding="utf-8")
    pick = draw(text, num)
    replacement = None
    if pick:
        new = new_production.create(prod.parent.name, slugify(pick.hook), family=pick.family)
        replacement = str(new.relative_to(ROOT))
        (new / "notes.md").write_text(f"# {new.name}: production notes\n\nStatus: DRAWN from the banked tier (rank {pick.rank}, replacement for returned {num:03d}, {today}). No script yet: written at production time under the standing flatness check. Topic: {pick.family}, {pick.structure}, theme {pick.theme}, main tension {pick.tension}. Hook and hero route: docs/current/idea-bank.md rank {pick.rank}.\n", encoding="utf-8")
        text = text.replace(pick.line, pick.line.replace(f"| {pick.status} |", f"| drawn {new.name[:3]} {today} (replacement for returned {num:03d}) |", 1), 1)
    mine = next((e for e in bank_rows(text) if re.match(rf"drawn {num:03d}\b", e.status)), None)
    if mine:
        text = text.replace(mine.line, mine.line.replace(f"| {mine.status} |", f"| returned {today}: {reason} |", 1), 1)
    else:                                                       # a slate production: it lives in the rolling-window line, not the table
        text = re.sub(rf"({num:03d} [a-z][a-z ]*? / [a-z]+)(?! \(returned)", rf"\1 (returned {today}: {reason})", text, count=1)
    BANK.write_text(text, encoding="utf-8")
    rest = len(undrawn(bank_rows(text)))
    refill = rest < WORKING_DEPTH
    with (prod / "notes.md").open("a", encoding="utf-8") as f:
        f.write(f"\n## RETURNED {today}\n{reason}\nReplacement: {replacement or 'none, no eligible banked entry (refill due)'}.\n")
    index = prod.parent / "INDEX.md"
    lines = index.read_text(encoding="utf-8").splitlines(keepends=True)
    for i, l in enumerate(lines):
        c = l.split("|")
        if l.startswith(f"| {num:03d} |") and len(c) >= 6:
            c[-4] = f" RETURNED {today}: {reason}; replaced by {replacement.split('/')[-1][:3] if replacement else 'none (refill due)'} "
            lines[i] = "|".join(c)
    index.write_text("".join(lines), encoding="utf-8")
    with DECISIONS.open("a", encoding="utf-8") as f:
        drew = f"Replacement drawn from the BANKED tier: rank {pick.rank} ({pick.family}, {pick.structure}, {pick.theme} / {pick.tension}), folder created by tools/new_production.py." if pick else "No eligible banked entry: no replacement."
        f.write(f"| {today} | **{num:03d} RETURNED (Reshape ladder, tools/return_topic.py):** {reason}. {drew} {rest} undrawn banked entries remain{'; REFILL DUE' if refill else ''} | scriptwriter (lead), design, marketing (one session) | The reason states the failing measurement | `{prod.relative_to(ROOT)}/notes.md`; `docs/current/idea-bank.md`; `{replacement or 'no replacement'}` | Remove the RETURNED marks and the draw mark |\n")
    record = {"reason": reason, "at": today, "replacement": replacement, "refill_due": refill, "undrawn": rest}
    side.write_text(json.dumps(record, indent=1), encoding="utf-8")
    return record


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("production")
    ap.add_argument("--reason", required=True)
    a = ap.parse_args()
    print(json.dumps(return_topic((ROOT / a.production).resolve(), a.reason)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
