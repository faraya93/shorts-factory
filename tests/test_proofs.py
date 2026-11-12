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


def _png(path: Path, w: int, h: int) -> None:
    import struct
    import zlib
    raw = b"".join(b"\x00" + b"\x00\x00\x00" * w for _ in range(h))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)   # noqa: E731
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def test_a_proof_still_is_read_only_under_the_reader_policy_with_a_clean_conformance_note():
    """Redesign session 2026-11-11: B5 read EEVEE drafts and simplified builds; a non-conforming still is refused BEFORE the readers run, so no reading is spent."""
    d = _unit(_el())
    still = d / "still-0010.png"
    _png(still, 540, 960)
    def refused():
        try:
            proofs.require_conforming(d, "P1", [str(still)])
        except SystemExit:
            return True
        return False
    assert refused(), "no conformance note and no sidecar"
    spec = json.loads((d / "proofs.json").read_text())
    spec["proofs"][0]["conformance"] = {"matches_staging": True, "deviations": []}
    (d / "proofs.json").write_text(json.dumps(spec))
    assert refused(), "no reader-still sidecar"
    still.with_suffix(".render.json").write_text(json.dumps({"engine": "BLENDER_EEVEE_NEXT", "res": 50}))
    assert refused(), "an EEVEE still"
    still.with_suffix(".render.json").write_text(json.dumps({"engine": "CYCLES", "res": 50, "samples": 48}))
    assert not refused()
    _png(still, 1080, 1920)
    assert refused(), "full-size still"
    _png(still, 540, 960)
    spec["proofs"][0]["conformance"] = {"matches_staging": False, "deviations": ["no night stage"]}
    (d / "proofs.json").write_text(json.dumps(spec))
    assert refused(), "a recorded deviation defers the reading"


def test_a_reading_records_its_prompt_and_design_round():
    d = _unit({**_el(), "round": 2})
    proofs.record_reading(d, "P1", ["a ship"] * 3, [90] * 3, prompt="single", prompt_sha256="abc")
    r = json.loads((d / "proofs.json").read_text())["proofs"][0]["readings"][0]
    assert (r["prompt"], r["prompt_sha256"], r["round"]) == ("single", "abc", 2)


def test_one_alias_set_per_physical_element_is_linted_across_proofs_and_script():
    d = _unit()
    spec = {"alias_sets": {"bird": ["bird", "pigeon"]}, "proofs": [
        {"id": "P1", "element_id": "bird-on-wire", "alias_sets": ["bird"], "aliases": ["bird", "pigeon"], "status": "passed"},
        {"id": "P3", "element_id": "bird-detour", "alias_sets": ["bird"], "event_aliases": ["detour"], "aliases": ["bird", "pigeon", "detour"], "status": "passed"}]}
    (d / "proofs.json").write_text(json.dumps(spec))
    (d / "script.json").write_text(json.dumps({"scenes": [{"elements": [{"id": "bird-on-wire", "aliases": ["bird", "pigeon"]}]}]}))
    assert proofs.errors(d) == []
    spec["proofs"][1]["aliases"] = ["bird", "detour"]                                                  # P3 dropped "pigeon": the set and the proof disagree
    (d / "proofs.json").write_text(json.dumps(spec))
    assert any("P3 aliases differ" in e for e in proofs.errors(d))
    spec["proofs"][1]["aliases"] = ["bird", "pigeon", "detour"]
    (d / "proofs.json").write_text(json.dumps(spec))
    (d / "script.json").write_text(json.dumps({"scenes": [{"elements": [{"id": "bird-on-wire", "aliases": ["bird", "goose"]}]}]}))
    assert any("script element 'bird-on-wire'" in e for e in proofs.errors(d))


def test_the_multi_calibration_replays_and_rejected_the_supplement():
    """docs/current/reports/multi-calibration-2026-11-11.json: under the live matcher the multi prompt passed owner-rejected 007 and failed both accepted controls, so it is not a proof instrument."""
    sys.path.insert(0, str(ROOT / "factory"))
    import asset_library as al
    data = json.loads((ROOT / "docs" / "current" / "reports" / "multi-calibration-2026-11-11.json").read_text(encoding="utf-8"))
    judged = {r["production"]: al.judge_guesses(r["aliases"], [x["guess"] for x in r["readings"]], [x["confidence"] for x in r["readings"]]) for r in data["rows"]}
    assert all(judged[r["production"]] == r["gate_pass"] for r in data["rows"])
    assert [p for p in judged if judged[p] and p in {"006", "007", "008", "009", "010", "011"}] == ["007"]
    assert not judged["004"] and not judged["005"]


def test_the_stop_loss_allows_two_design_rounds():
    d = _unit({"id": "P1", "element_id": "x", "status": "passed", "round": 3})
    assert any("stop-loss" in e for e in proofs.errors(d))


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_") and callable(f)]
    for name, fn in tests:
        fn()
        print(f"ok  {name}")
    print(f"{len(tests)} tests passed")
