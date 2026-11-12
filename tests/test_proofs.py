"""Block B5: the recording path of blind proofs (factory/proofs.py). Run: .venv/bin/python tests/test_proofs.py"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "factory"))
import proofs  # noqa: E402


def _unit(*proof_list):
    d = Path(tempfile.mkdtemp())
    (d / "proofs.json").write_text(json.dumps({"proofs": list(proof_list)}), encoding="utf-8")
    return d


def _el(pid="P1", aliases=("ship", "ocean liner")):
    return {"id": pid, "element_id": "x", "aliases": list(aliases), "status": "pending", "readings": []}


def test_a_passing_reading_settles_the_proof_and_is_recorded():
    d = _unit(_el())
    assert proofs.record_reading(d, "P1", ["an ocean liner", "toy ship", "a ship model"], [80, 70, 90], reader_cost=0.01)
    p = json.loads((d / "proofs.json").read_text())["proofs"][0]
    assert p["status"] == "passed" and p["readings"][0]["pass"] is True and p["readings"][0]["reader_cost_usd"] == 0.01
    assert not proofs.errors(d)


def test_the_bar_is_the_gates_bar_a_reader_under_45_or_a_missing_alias_fails():
    d = _unit(_el("P1"), _el("P2"))
    assert not proofs.record_reading(d, "P1", ["a ship", "a ship", "a ship"], [90, 90, 40])               # one reader under 45
    assert not proofs.record_reading(d, "P2", ["a ship", "a boat", "a ship"], [90, 90, 90])               # one reader without an alias
    assert [p["status"] for p in json.loads((d / "proofs.json").read_text())["proofs"]] == ["failed", "failed"]
    assert len(proofs.errors(d)) == 2


def test_a_settled_proof_is_never_read_again():
    d = _unit(_el())
    proofs.record_reading(d, "P1", ["a boat", "a boat", "a boat"], [90, 90, 90])
    for fn in (proofs.require_pending, lambda dd, i: proofs.record_reading(dd, i, ["a ship"] * 3, [90] * 3)):
        try:
            fn(d, "P1")
        except SystemExit:
            continue
        raise AssertionError("a failed proof accepted another reading")


def test_a_render_cost_proof_passes_at_or_under_15_seconds_and_fails_above():
    d = _unit({"id": "W1", "status": "pending"}, {"id": "W2", "status": "pending"})
    assert proofs.record_cost(d, "W1", 6.8, "glass_water_sss") and not proofs.record_cost(d, "W2", 15.5, "nested_transmission_volumes")


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
