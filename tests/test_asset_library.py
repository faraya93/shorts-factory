"""The asset library's rules hold (docs/current/specs/asset-system.md). Run: .venv/bin/python tests/test_asset_library.py"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import asset_library as al  # noqa: E402
import gate  # noqa: E402
import scenes_schema  # noqa: E402

FIRST_ROUTED = 12          # productions from this number on declare a hero route; older ones are frozen records


def sandbox():
    t = tempfile.TemporaryDirectory()
    al.LIBRARY = Path(t.name)
    return t


def ready_asset(slug="human-heart", **licence):
    al.new(slug, "Human heart", ["heart", "corazon"], "body")
    m = al.read_meta(slug)
    (al.asset_dir(slug) / f"{slug}.blend").write_bytes(b"fake")
    m["status"], m["route"] = "ready", "library"
    m["brief"]["must_read_as"] = "a human heart"
    m["source"] = {"registry_id": "polyhaven", "url": "https://x", "asset_id": "y", "author": "z", "retrieved": "2026-11-04"}
    m["licence"] = {"id": "CC0-1.0", "url": None, "attribution": None, "note": None, "owner_ok": None, **licence}
    m["checks"]["qa"] = {"pass": True, "date": "2026-11-04"}
    al.write_meta(m)
    al.seal(slug)
    assert al.record_blind(slug, ["a human heart", "un corazón"])
    return slug


def errors(slug):
    return al.validate(slug, al.source_ids())[0]


def test_a_complete_asset_is_valid():
    with sandbox():
        assert errors(ready_asset()) == []


def test_the_same_object_cannot_be_started_twice():
    with sandbox():
        ready_asset()
        for slug, name, alias in [("human-heart", "x", "y"), ("heart-2", "Other", "corazón")]:
            try:
                al.new(slug, name, [alias], "body")
            except SystemExit:
                continue
            raise AssertionError(f"{slug} should have been refused")


def test_licence_rule():
    for licence, ok in [({"id": "CC-BY-NC-4.0"}, False), ({"id": "CC-BY-SA-4.0"}, False), ({"id": "unknown"}, False), ({"id": "CC-BY-4.0"}, False),
                        ({"id": "CC-BY-4.0", "attribution": "Model by Ana (CC BY)"}, True), ({"id": "Royalty-Free"}, False),
                        ({"id": "Royalty-Free", "url": "https://terms"}, True), ({"id": "AGPL-3.0"}, False), ({"id": "AGPL-3.0", "owner_ok": "2026-11-04"}, True)]:
        with sandbox():
            assert (errors(ready_asset(**licence)) == []) == ok, licence


def test_ready_needs_qa_blind_naming_and_a_sealed_unchanged_file():
    with sandbox():
        s = ready_asset()
        (al.asset_dir(s) / f"{s}.blend").write_bytes(b"changed")
        assert any("changed since" in x for x in errors(s))
    with sandbox():
        s = ready_asset()
        m = al.read_meta(s)
        m["checks"]["qa"]["pass"] = False
        al.write_meta(m)
        assert any("qa" in x for x in errors(s))
    with sandbox():
        s = ready_asset()
        assert not al.record_blind(s, ["an abstract red blob", "a heart"]), "every guess must name the object"
        assert any("blind" in x for x in errors(s))


def test_one_guess_is_not_enough():
    assert not al.judge_guesses(["heart"], ["heart"])
    assert al.judge_guesses(["corazon"], ["Un corazón humano", "corazón"])


def test_blind_pack_hides_the_name():
    with tempfile.TemporaryDirectory() as t:
        still = Path(t) / "human-heart-q1.PNG"
        still.write_bytes(b"x")
        out, prompt = al.blind_pack([str(still)])
        assert (out / "view-1.png").exists() and "heart" not in prompt


def test_readme_records_source_licence_date_and_productions_and_keeps_notes():
    with sandbox():
        s = ready_asset()
        path = al.asset_dir(s) / "README.md"
        path.write_text(path.read_text(encoding="utf-8") + "keep this note\n", encoding="utf-8")
        al.seal(s)
        text = path.read_text(encoding="utf-8")
        for needle in ("**Source:**", "**Licence:** CC0-1.0", "2026-11-04", "**Productions that used it:**", "keep this note"):
            assert needle in text, needle


def test_schema_ties_route_and_assets():
    v = scenes_schema.validate_production
    has = lambda c, w: any(w in e for e in v(c))
    assert has({"hero_route": "asset"}, "needs library_assets")
    assert has({"hero_route": "guess", "library_assets": ["a"]}, "hero_route must be")
    assert has({"library_assets": ["a"]}, "needs hero_route")
    assert not has({"hero_route": "asset", "library_assets": ["a"]}, "library_assets")
    assert not has({}, "library_assets"), "older productions declare neither"


def test_gate_requires_a_ready_asset_and_a_fresh_passing_likeness():
    with sandbox(), tempfile.TemporaryDirectory() as t:
        s = ready_asset()
        p = Path(t)
        cfg = {"gate_stills": {}, "rig_libs": ["looks"], "hero_route": "asset", "library_assets": [s]}
        (p / "scenes.json").write_text(json.dumps(cfg))
        assert not gate.check_hero(p)[0], "no likeness record"
        assert not al.record_likeness(p, s, ["a blob", "a ball"])
        assert not gate.check_hero(p)[0], "failed likeness"
        assert al.record_likeness(p, s, ["a heart", "human heart"])
        assert gate.check_hero(p)[0]
        (al.asset_dir(s) / "x").write_text("")
        m = al.read_meta(s)
        m["files"]["sha256"] = "other"
        al.write_meta(m)
        assert not gate.check_hero(p)[0], "changed asset makes the record stale"
        m["status"] = "in_progress"
        al.write_meta(m)
        assert "not ready" in gate.check_hero(p)[1]


def test_older_productions_are_not_affected():
    with tempfile.TemporaryDirectory() as t:
        p = Path(t)
        (p / "scenes.json").write_text(json.dumps({"gate_stills": {}, "rig_libs": ["looks"]}))
        assert gate.check_hero(p)[0]


def test_registry_is_ordered_and_marks_accounts():
    import yaml
    r = yaml.safe_load(al.REGISTRY.read_text(encoding="utf-8"))
    by = {s["id"]: s for s in r["sources"]}
    assert [s["priority"] for s in r["sources"]] == sorted(s["priority"] for s in r["sources"])
    assert by["polyhaven"]["priority"] == 1 and by["ambientcg"]["priority"] == 2 and by["mb-lab"]["priority"] == 4
    for s in r["sources"]:
        if s["account_required"]:
            assert s["status"] == "owner-step", s["id"]
    assert "agpl_note" in by["mb-lab"]
    doc = (ROOT / "docs" / "current" / "specs" / "asset-system.md").read_text(encoding="utf-8")
    for s in r["sources"]:
        assert s["name"].split(" (")[0] in doc, s["id"]


def test_real_library_is_valid():
    al.LIBRARY = ROOT / "assets" / "library"
    known = al.source_ids()
    for slug in al.slugs():
        assert al.validate(slug, known)[0] == [], slug


def test_new_productions_declare_a_hero_route():
    for tree in (ROOT / "productions").glob("mecanalia-*"):
        for cfg in tree.glob("*/scenes.json"):
            m = re.match(r"(\d{3})-", cfg.parent.name)
            if m and int(m.group(1)) >= FIRST_ROUTED:
                c = json.loads(cfg.read_text(encoding="utf-8"))
                assert c.get("hero_route") and c.get("library_assets"), f"{cfg.parent.name}: declare hero_route and library_assets"
                for slug in c["library_assets"]:
                    assert (ROOT / "assets" / "library" / slug / "asset.json").exists(), f"{cfg.parent.name}: {slug} is not in the library"


def test_binaries_are_ignored_and_records_are_not():
    probe = {"assets/library/x/x.blend": True, "assets/library/x/job/stills/a.png": True, "assets/library/x/textures/a.jpg": True,
             "assets/library/x/asset.json": False, "assets/library/x/README.md": False, "assets/library/x/build.py": False, "assets/library/x/job/report.md": False}
    for path, ignored in probe.items():
        r = subprocess.run(["git", "check-ignore", "-q", "--no-index", path], cwd=ROOT)
        assert (r.returncode == 0) == ignored, path


def test_docs_and_doctrine_are_wired():
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    assert "Asset library and hero routing" in claude and "asset-system.md" in claude
    doc = (ROOT / "docs" / "current" / "specs" / "asset-system.md").read_text(encoding="utf-8")
    assert "How to run an asset job" in doc and "Skill role map" in doc


if __name__ == "__main__":
    os.environ.pop("ASSET_LIBRARY", None)
    real = al.LIBRARY
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        al.LIBRARY = real
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
