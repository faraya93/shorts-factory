"""Seat the moving parts of the toilet on what carries them, at absolute positions (safe to re-run): mesh QA reads the 3-4 mm gaps of the source as floating parts.
    .venv/bin/python tools/blender_run.py -- -b assets/library/toilet/toilet.blend --python assets/library/toilet/build.py
Source: BlenderKit 6a342733; parts toilet_body, toilet_seat, toilet_lid, toilet_chrome; the lid hinge is its origin, rotation_euler.x = +90 deg closes it."""
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "factory"))
import asset_library as al  # noqa: E402

HINGE = (0.0, 0.125, 0.462)
bpy.data.objects["toilet_seat"].location = (HINGE[0], HINGE[1], HINGE[2] - 0.0035)
bpy.data.objects["toilet_lid"].location = (HINGE[0], HINGE[1] - 0.0042, HINGE[2] + 0.001)
print(al.save_collection("toilet", "asset"))
