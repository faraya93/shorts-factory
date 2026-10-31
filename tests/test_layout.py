"""Keeps the repository organized (docs/architecture.md, CLAUDE.md "Repository organization"). Run: .venv/bin/python tests/test_layout.py"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
sys.path.insert(0, str(ROOT / "tools"))
import channel  # noqa: E402
import new_production  # noqa: E402
import publish_package  # noqa: E402

PROD = ROOT / "productions"
NUMBERED = re.compile(r"^(\d{3})-[a-z0-9]+(-[a-z0-9]+)*$")


def test_productions_top_level_is_channels_lab_and_archive_only():
    allowed = set(channel.variants()) | {"_lab", "_archive", "README.md"}
    names = {p.name for p in PROD.iterdir() if not p.name.startswith(".")}
    assert names <= allowed, names - allowed
    assert set(channel.variants()) <= names, "every channel has a production tree"


def test_channel_trees_hold_numbered_productions_with_an_index():
    for cid in channel.variants():
        tree = PROD / cid
        dirs = sorted(p.name for p in tree.iterdir() if p.is_dir())
        assert all(NUMBERED.match(d) for d in dirs), [d for d in dirs if not NUMBERED.match(d)]
        nums = [int(d[:3]) for d in dirs]
        assert len(nums) == len(set(nums)), "numbers are never reused"
        index = (tree / "INDEX.md").read_text(encoding="utf-8")
        for d in dirs:
            assert f"| {d[:3]} |" in index and d[4:] in index, f"{cid}/{d} missing from INDEX.md"
        for d in dirs:
            cfg = tree / d / "scenes.json"
            if cfg.exists():
                assert json.loads(cfg.read_text(encoding="utf-8")).get("channel") == cid, f"{d}: scenes.json channel must be {cid}"


def test_no_pilot_folder_and_no_skills_in_the_repo():
    assert not (PROD / "pilot").exists()
    assert not list(ROOT.glob(".claude/skills")) and not list(ROOT.glob("skills")), "craft skills live at user level (~/.claude/skills), not in the repo"


def test_docs_top_level_is_the_three_classes():
    names = {p.name for p in (ROOT / "docs").iterdir() if not p.name.startswith(".")}
    assert names == {"README.md", "architecture.md", "current", "experiments", "archive"}, names


def test_publish_packages_are_valid_where_present():
    for f in PROD.glob("*/*/publish.json"):
        assert publish_package.check(f.parent) == [], f.parent.name


def test_new_production_takes_the_next_number_and_never_reuses_one():
    nums = new_production.used_numbers("mecanalia-es")
    assert nums and max(nums) == max(int(p.name[:3]) for p in (PROD / "mecanalia-es").iterdir() if p.is_dir())
    try:
        new_production.create("no-such-channel", "x")
    except KeyError:
        pass
    else:
        raise AssertionError("an unknown channel must be rejected")


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
