"""The visibility check measures rendered pixels and is a hard block. Run: python tests/test_visibility.py"""
import json
import sys
import tempfile
from pathlib import Path
from unittest import mock

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "factory")]
import gate  # noqa: E402
import palette_metrics  # noqa: E402
import visibility_check as v  # noqa: E402

LIME = (200, 230, 60)


def pair(d: Path, colour, name):
    a, b = Image.new("RGB", (1080, 1920), LIME), Image.new("RGB", (1080, 1920), LIME)
    ImageDraw.Draw(a).rectangle((400, 200, 700, 1000), fill=colour)
    a.save(d / f"{name}-a.png"), b.save(d / f"{name}-b.png")
    return v.measure(d / f"{name}-a.png", d / f"{name}-b.png")


def test_de00_matches_repo_metric():
    for x, y in (("#FF7A2A", "#A8D84A"), ("#102030", "#FFFFFF"), ("#808080", "#858585")):
        h = lambda s: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))  # noqa: E731
        assert abs(v.de00(v._lab(h(x)), v._lab(h(y))) - palette_metrics.de2000(x, y)) < 0.01


def test_blended_faint_fails_and_strong_passes():
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        assert not v.verdict(pair(d, (208, 234, 90), "faint"))              # a thin white veil over lime: what 009 shipped
        assert v.verdict(pair(d, (70, 30, 130), "strong"))
        assert not v.verdict(pair(d, LIME, "none"))                         # identical frames: nothing there


def prod(tmp: Path, **kw) -> Path:
    p = tmp / "p"
    (p / "build" / "gate").mkdir(parents=True)
    (p / "scenes.json").write_text(json.dumps({"scenes": [{"id": 1}], "scene_elements": {"1": [{"id": "x"}]}, **kw}))
    return p


def test_block_rules():
    with tempfile.TemporaryDirectory() as t, mock.patch.object(gate, "visibility_fingerprint", return_value="fp"):
        tmp = Path(t)
        assert gate.check_visibility(prod(tmp))[0]                          # v1 without the block: exempt
        (tmp / "p").rename(tmp / "old")
        p = prod(tmp, gate_version=2)
        assert not gate.check_visibility(p)[0]                              # v2 must declare every element
        sc = json.loads((p / "scenes.json").read_text())
        sc["visibility"] = {"1": {"x": {"objects": ["x"], "frames": [1]}}}
        (p / "scenes.json").write_text(json.dumps(sc))
        rec = p / "build" / "gate" / "visibility.json"
        assert not gate.check_visibility(p)[0]                              # no record
        rec.write_text(json.dumps({"1:x": {"pass": True, "fingerprint": "fp"}}))
        assert not gate.check_visibility(p)[0]                              # not made by the isolated route
        rec.write_text(json.dumps({"1:x": {"pass": False, "fingerprint": "fp", "isolation": "headless"}}))
        assert not gate.check_visibility(p)[0]                              # failed
        rec.write_text(json.dumps({"1:x": {"pass": True, "fingerprint": "stale", "isolation": "headless"}}))
        assert not gate.check_visibility(p)[0]                              # stale
        rec.write_text(json.dumps({"1:x": {"pass": True, "fingerprint": "fp", "isolation": "headless"}}))
        assert gate.check_visibility(p)[0]


if __name__ == "__main__":
    for k, f in list(globals().items()):
        if k.startswith("test_"):
            f()
            print("ok", k)
