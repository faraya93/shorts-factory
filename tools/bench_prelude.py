"""Blender-side prelude of tools/cost_bench.py: runs BEFORE a scene script (--python prelude --python scene) and applies one variant from SF_BENCH, leaving every production file untouched.
SF_BENCH = {"cy": {cycles property: value}, "res": percent, "mat": ["ice_milky", "ice_front", "water_novol", "thin_glass", "fake_glass"]}"""
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code3d" / "lib"))
import real_kit as rk      # noqa: E402
import tape_rig            # noqa: E402
import cheap_kit           # noqa: E402
import pipeline_config     # noqa: E402

V = json.loads(os.environ.get("SF_BENCH", "{}"))
pipeline_config.script_stem = lambda: os.environ["SF_BENCH_SCENE"]      # the launching script is this prelude; profiles and scene numbers key on the scene script
mats = set(V.get("mat", []))
_orig = tape_rig.Stage._apply_render_profile


def _patched(sc):
    _orig(sc)
    for k, v in V.get("cy", {}).items():
        setattr(sc.cycles, k, v)
    if "res" in V:
        sc.render.resolution_percentage = int(V["res"])
    print("[bench] applied", V)


tape_rig.Stage._apply_render_profile = staticmethod(_patched)
_ice, _water, _glass, _cube = rk.ice, rk.water, rk.glass, rk.ice_cube
if "ice_milky" in mats:
    rk.ice = cheap_kit.ice_milky
if "ice_front" in mats:                # volumetric core only on the row nearest the camera (y < 0); the rest are milky
    _m = {}

    def _front(S, name, mat, *a, **k):
        loc = k.get("loc") or (a[1] if len(a) > 1 else (0, 0, 0))
        if "m" not in _m:                  # the scene resets Blender data at start: build it on first use
            _m["m"] = cheap_kit.ice_milky("clear_ice_back", core=0.9)
        return _cube(S, name, mat if loc[1] < 0 else _m["m"], *a, **k)
    rk.ice_cube = _front
if "water_novol" in mats:
    rk.water = lambda *a, **k: cheap_kit.no_volume(_water(*a, **k))
if "thin_glass" in mats or "fake_glass" in mats:
    def _g(*a, **k):
        m = _glass(*a, **k)
        if "thin_glass" in mats:
            cheap_kit.thin_wall(m)
        if "fake_glass" in mats:
            cheap_kit.fake_indirect(m)
        return m
    rk.glass = _g
