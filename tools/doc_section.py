"""Print ONE section of a doctrine or spec file instead of reading the whole file (CLAUDE.md "How to read doctrine", block B2 2026-11-11).
Every whole-file read stays in the session's context for every later call, so a pointer is followed with this tool, not with Read.

usage: .venv/bin/python tools/doc_section.py <file> "<section>"     a markdown heading (any level) that starts with <section>, case-insensitive,
                                                                       through the next heading of the same or a higher level; or, failing that,
                                                                       a bold-labelled bullet or paragraph ("- **<section>" / "**<section>") through the next one
       .venv/bin/python tools/doc_section.py <file> --list            the file's headings and bold labels, with their sizes in bytes
Exit 1 when nothing matches (the headings are listed so the pointer can be corrected)."""
import re
import sys
from pathlib import Path

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
LABEL = re.compile(r"^(\s*)(?:[-*]\s+|\d+\.\s+)?\*\*([^*]+)")


def _fold(s: str) -> str:
    return " ".join(s.replace("*", "").replace("`", "").lower().split())


def outline(lines: list[str]) -> list[tuple[int, int, str, str]]:
    """(line index, heading level or 0 for a bold label, label text, kind)."""
    out = []
    for i, l in enumerate(lines):
        m = HEADING.match(l)
        if m:
            out.append((i, len(m.group(1)), m.group(2).strip(), "heading"))
            continue
        m = LABEL.match(l)
        if m:
            out.append((i, 0, m.group(2).strip().rstrip(":").strip(), "label"))
    return out


def section(text: str, name: str) -> str | None:
    lines = text.splitlines()
    want = _fold(name)
    marks = outline(lines)
    for kind in ("heading", "label"):
        for i, level, label, k in marks:
            if k != kind or not _fold(label).startswith(want):
                continue
            end = len(lines)
            if kind == "heading":
                end = next((j for j, lv, _, kk in marks if kk == "heading" and j > i and lv <= level), end)
            else:
                indent = len(lines[i]) - len(lines[i].lstrip())
                for j in range(i + 1, len(lines)):
                    l = lines[j]
                    if HEADING.match(l) or (l.strip() and len(l) - len(l.lstrip()) <= indent and (LABEL.match(l) or re.match(r"\s*([-*]|\d+\.)\s", l))):
                        end = j
                        break
            return "\n".join(lines[i:end]).rstrip() + "\n"
    return None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    path, name = Path(argv[0]), argv[1]
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if name == "--list":
        marks = outline(lines)
        for n, (i, level, label, kind) in enumerate(marks):
            nxt = marks[n + 1][0] if n + 1 < len(marks) else len(lines)
            size = sum(len(l) + 1 for l in lines[i:nxt])
            print(f"{'#' * level if level else '  **'} {label[:90]}  ({size} B)")
        return 0
    out = section(text, name)
    if out is None:
        print(f"no section starting with {name!r} in {path}; headings:")
        for _, level, label, kind in outline(lines):
            if kind == "heading":
                print(f"  {'#' * level} {label[:90]}")
        return 1
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
